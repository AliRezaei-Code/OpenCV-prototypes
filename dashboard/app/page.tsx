'use client';

import { useState, useEffect } from 'react';

type Config = {
  clahe: boolean;
  unsharp_amount: number;
  denoise: boolean;
  source: string;
};

export default function Home() {
  const [config, setConfig] = useState<Config>({
    clahe: false,
    unsharp_amount: 0.0,
    denoise: false,
    source: "0"
  });
  const [loading, setLoading] = useState(false);

  // Load initial config
  useEffect(() => {
    fetch('http://localhost:8000/config')
      .then(res => res.json())
      .then(data => setConfig(data))
      .catch(err => console.error("Failed to fetch config:", err));
  }, []);

  const updateConfig = async (newConfig: Partial<Config>) => {
    const updated = { ...config, ...newConfig };
    setConfig(updated);
    try {
      await fetch('http://localhost:8000/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updated),
      });
    } catch (err) {
      console.error("Failed to update config:", err);
    }
  };

  return (
    <main className="min-h-screen p-8 lg:p-12 flex flex-col gap-8 max-w-7xl mx-auto">
      {/* Header */}
      <header className="flex flex-col gap-2 mb-4">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
          Vision Accessibility Demos
        </h1>
        <p className="text-slate-400">
          Real-time enhancement and accessibility tools powered by OpenCV
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Video Feed */}
        <div className="lg:col-span-2 space-y-4">
          <div className="glass-panel rounded-2xl overflow-hidden aspect-video relative flex items-center justify-center bg-black/50 border-slate-700/50">
            {/* We use a simple img tag for MJPEG stream */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img 
              src="http://localhost:8000/video_feed" 
              alt="Live video feed"
              className="w-full h-full object-contain"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
              }}
            />
            <div className="absolute inset-0 -z-10 flex items-center justify-center text-slate-500">
              <span>Waiting for video stream... (Ensure server is running on :8000)</span>
            </div>
          </div>
          <div className="flex gap-4 text-sm text-slate-400 px-2">
            <span>Latency: &lt; 33ms</span>
            <span>FPS: 30</span>
            <span>Resolution: 1280x720</span>
          </div>
        </div>

        {/* Controls Panel */}
        <div className="glass-panel p-6 rounded-2xl space-y-8 h-fit">
          <h2 className="text-xl font-semibold border-b border-slate-700/50 pb-4">
            Enhancement Controls
          </h2>

          {/* Source Selection */}
          <div className="space-y-3">
            <label className="text-sm font-medium text-slate-300">Video Source</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={config.source} 
                onChange={(e) => updateConfig({ source: e.target.value })}
                className="bg-slate-800/50 border border-slate-600 rounded px-3 py-2 w-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0 or /path/to/video.mp4"
              />
            </div>
          </div>

          {/* Toggles */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="font-medium">CLAHE Contrast</label>
              <button 
                onClick={() => updateConfig({ clahe: !config.clahe })}
                className={`w-12 h-6 rounded-full transition-colors relative ${config.clahe ? 'bg-blue-500' : 'bg-slate-700'}`}
              >
                <div className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-transform ${config.clahe ? 'left-7' : 'left-1'}`} />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <label className="font-medium">Denoise (Slow)</label>
              <button 
                onClick={() => updateConfig({ denoise: !config.denoise })}
                className={`w-12 h-6 rounded-full transition-colors relative ${config.denoise ? 'bg-blue-500' : 'bg-slate-700'}`}
              >
                <div className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-transform ${config.denoise ? 'left-7' : 'left-1'}`} />
              </button>
            </div>
          </div>

          {/* Sliders */}
          <div className="space-y-4">
            <div className="flex justify-between">
              <label className="font-medium">Sharpen Amount</label>
              <span className="text-blue-400 font-mono">{config.unsharp_amount.toFixed(1)}</span>
            </div>
            <input 
              type="range" 
              min="0" 
              max="3.0" 
              step="0.1"
              value={config.unsharp_amount}
              onChange={(e) => updateConfig({ unsharp_amount: parseFloat(e.target.value) })}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
          </div>

          {/* Status */}
          <div className="mt-8 p-4 bg-slate-800/30 rounded-lg border border-slate-700/30 text-xs font-mono text-slate-400">
            <p>Server Status: Active</p>
            <p>Backend: OpenCV (Python)</p>
          </div>
        </div>
      </div>
    </main>
  );
}
