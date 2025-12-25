import typer
import cv2
import time
from pathlib import Path
from typing import Optional
from vademos.io.capture import VideoSource
from vademos.ops.filters import apply_clahe, apply_unsharp_mask, apply_denoise

app = typer.Typer()

@app.command()
def text_enhance(
    source: str = typer.Option("0", help="Video source: '0' for webcam or file path"),
    clahe: bool = typer.Option(False, help="Enable CLAHE"),
    unsharp: float = typer.Option(0.0, help="Unsharp mask amount (0.0 to disable)"),
    denoise: bool = typer.Option(False, help="Enable denoising (slow)"),
    show: bool = typer.Option(False, help="Show live preview using cv2.imshow"),
    out: Optional[Path] = typer.Option(None, help="Path to save output video/image")
):
    """
    Run text enhancement pipeline on video source.
    """
    
    # Handle numeric source for webcam
    src_val = int(source) if source.isdigit() else source
    
    src = VideoSource(src_val)
    fps = src.get_fps()
    
    typer.echo(f"Starting text enhancement on {source}...")
    
    # Simple loop
    try:
        for ts, frame in src:
            processed = frame
            
            if denoise:
                processed = apply_denoise(processed)
            
            if clahe:
                processed = apply_clahe(processed)
                
            if unsharp > 0:
                processed = apply_unsharp_mask(processed, amount=unsharp)
            
            if show:
                cv2.imshow("Text Enhance Preview", processed)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            # TODO: Implement writer if 'out' is specified
            
    except KeyboardInterrupt:
        pass
    finally:
        src.release()
        if show:
            cv2.destroyAllWindows()
        typer.echo("Done.")

if __name__ == "__main__":
    app()
