import React, { useEffect, useRef } from 'react';

export default function CameraModal({ onClose, onCapture }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    let stream;
    async function start() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (e) {
        alert('Unable to access camera: ' + e.message);
      }
    }
    start();
    return () => {
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
  }, []);

  function snap() {
    const video = videoRef.current,
      canvas = canvasRef.current;
    if (!video || !canvas) return;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL('image/png');
    onCapture(dataUrl);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="bg-slate-800 text-white rounded-lg w-11/12 max-w-lg overflow-hidden shadow-lg">
        <div className="p-3 border-b border-slate-600 flex items-center justify-between">
          <h3 className="font-semibold text-lg">Capture Image</h3>
          <button
            onClick={onClose}
            className="text-slate-300 hover:text-white transition-colors"
          >
            Close
          </button>
        </div>
        <div className="p-3">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="w-full rounded-lg bg-black border border-slate-600"
          />
          <canvas ref={canvasRef} className="hidden" />
          <div className="mt-3 flex gap-2">
            <button
              onClick={snap}
              className="flex-1 py-2 rounded bg-sky-600 text-white hover:bg-sky-500 transition-colors"
            >
              Capture
            </button>
            <button
              onClick={onClose}
              className="flex-1 py-2 rounded border border-slate-500 text-white hover:bg-slate-700 transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
