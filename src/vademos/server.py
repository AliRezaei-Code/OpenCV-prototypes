from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import threading
import time
import uvicorn
from typing import Optional
from vademos.io.capture import VideoSource
from vademos.ops.filters import apply_clahe, apply_unsharp_mask, apply_denoise

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Config(BaseModel):
    clahe: bool = False
    unsharp_amount: float = 0.0
    denoise: bool = False
    source: str = "0"

# Global state
state = Config()
video_source: Optional[VideoSource] = None
lock = threading.Lock()

def get_video_source():
    global video_source
    if video_source is None:
        src_val = int(state.source) if state.source.isdigit() else state.source
        video_source = VideoSource(src_val)
    return video_source

@app.post("/config")
def update_config(config: Config):
    global state, video_source
    # If source changed, release and recreate
    if config.source != state.source:
        with lock:
            if video_source:
                video_source.release()
                video_source = None
    state = config
    return {"status": "updated", "config": state}

@app.get("/config")
def get_config():
    return state

def generate_frames():
    src = get_video_source()
    # Iterate manually to handle re-creation safely? 
    # Actually, the VideoSource iterator might be tricky if source changes.
    # Let's just read from the current global source.
    
    while True:
        with lock:
            if video_source is None:
                get_video_source()
            src = video_source
            
        # We can't use the simple loop because we might want to change params per frame
        # and src object might change.
        if src:
            ret, frame = src.cap.read()
            if not ret:
                # If file ends, loop or stop? Let's loop for demo purposes if it's a file
                src.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Apply ops
            if state.denoise:
                frame = apply_denoise(frame)
            if state.clahe:
                frame = apply_clahe(frame)
            if state.unsharp_amount > 0:
                frame = apply_unsharp_mask(frame, amount=state.unsharp_amount)
                
            # Encode
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            time.sleep(0.1)

@app.get("/video_feed")
def video_feed():
    return Response(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
