import cv2
import time
import threading
import numpy as np
import pyttsx3
from ultralytics import YOLO
import uvicorn
import socketio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import base64
from io import BytesIO
from PIL import Image

# --- Configuration Section ---
MODEL_PATH = "./runs/detect/train5/weights/best.pt"
CAMERA_INDEX = 0
CONFIDENCE_THRESHOLD = 0.50
SPEAK_INTERVAL = 5
IOU_THRESHOLD = 0.7
IMG_SIZE = 640

# --- AAC VOCABULARY MAPPING ---
AAC_VOCABULARY = {
    "table": "I need to sit at the table now.",
    "chair": "Please push the chair closer for me.",
    "whiteboard": "I want to draw on the whiteboard.",
    "bookshelf": "I want a book from the bookshelf.",
    "clock": "What time is it on the clock?",
    "wall-magazine": "Can you show me the wall magazine?",
    "trash-can": "I need to throw this into the trash can.",
    "eraser": "I made a mistake. I need the eraser.",
    "sharpener": "My pencil is dull. I need the sharpener.",
    "pen": "I need a pen to write with.",
    "book": "Read this book to me.",
    "ruler": "I need the ruler to measure something.",
    "scissor": "I want to cut this paper with the scissor.",
    "fan": "I feel hot. Turn on the fan.",
    "laptop": "I want to watch the laptop.",
    "remote-control": "Give me the remote control.",
    "bag": "I need to put this in my bag.",
    "pants": "I need help with my pants.",
    "shoes": "I want to put my shoes on.",
    "hat": "I need my hat because it is cold."
}

# --- Shared State ---
# 1. Initialize FastAPI app FIRST
app = FastAPI()

# 2. Initialize Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

# Global variables
last_speak_time = time.time()
last_detected_object = ""


# --- Helper Functions ---

def load_model():
    """Loads the YOLO model."""
    try:
        print(f"Loading model from: {MODEL_PATH}")
        return YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def speak_text_in_thread(text):
    """Initializes a local pyttsx3 engine, speaks, and cleanly stops."""
    try:
        local_engine = pyttsx3.init()
        local_engine.stop()
        local_engine.say(text)
        local_engine.runAndWait()
        local_engine.stop()
        del local_engine
    except Exception as e:
        print(f"Error during speech thread execution: {e}")


# --- NEW STATIC IMAGE ANALYSIS ENDPOINT (FastAPI Route) ---
@app.post("/analyze-image")
async def analyze_image(request: Request):
    """
    Handles a POST request with an image data URL, runs detection, and returns the result.
    """
    try:
        data = await request.json()
        image_data_url = data.get("image")

        if not image_data_url or not image_data_url.startswith('data:image'):
            return {"error": "Invalid or missing image data URL"}, 400

        # Decode the base64 image data
        header, encoded = image_data_url.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        model = load_model()
        if not model:
            return {"error": "Model not loaded on server"}, 500

        # Perform Inference
        results = model.predict(
            source=image, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD,
            imgsz=IMG_SIZE, verbose=False, device='cpu'
        )

        current_detected_object = None
        max_conf = 0.0

        if results and results[0].boxes:
            for box in results[0].boxes:
                conf = float(box.conf[0])
                if conf > max_conf:
                    max_conf = conf
                    class_id = int(box.cls[0])
                    if class_id < len(model.names):
                        current_detected_object = model.names[class_id]

        # Generate AAC Phrase
        if current_detected_object:
            phrase = AAC_VOCABULARY.get(
                current_detected_object,
                f"I see the {current_detected_object}."
            )

            speech_thread = threading.Thread(target=speak_text_in_thread, args=(phrase,), daemon=True)
            speech_thread.start()

            return {
                "object": current_detected_object,
                "phrase": phrase,
                "confidence": round(max_conf * 100, 2)
            }
        else:
            return {
                "object": None,
                "phrase": "No recognizable object found in the captured image.",
                "confidence": 0.0
            }

    except Exception as e:
        print(f"Error processing image: {e}")
        return {"error": f"Internal server error: {e}"}, 500


# ------------------------------------------

# 4. Mount the SocketIO application LAST
# This must happen after all FastAPI routes are defined
app.mount("/", socketio.ASGIApp(sio))


# --- Core Detection Loop (MODIFIED for Camera-on-Demand) ---

def run_detection_loop(model):
    """
    Runs the real-time detection, opening and closing the camera for each cycle,
    to prevent camera conflict with the React frontend.
    """
    global last_speak_time, last_detected_object

    print("Detection loop started successfully. Waiting for connections...")

    while True:
        cap = None
        frame = None
        try:
            # 1. Open Camera
            cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
            if not cap.isOpened():
                time.sleep(SPEAK_INTERVAL)
                continue

            # 2. Grab Frame
            ret, frame = cap.read()

            # 3. Release Camera immediately after grabbing the frame
            cap.release()
            cap = None

            if not ret:
                print("Can't receive frame. Retrying...")
                time.sleep(2)
                continue

            # 4. Perform Inference on the frame
            results = model.predict(
                source=frame, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD,
                imgsz=IMG_SIZE, verbose=False, device='cpu'
            )

            current_detected_object = ""
            max_conf = 0.0

            if results and results[0].boxes:
                for box in results[0].boxes:
                    conf = float(box.conf[0])
                    if conf > max_conf:
                        max_conf = conf
                        class_id = int(box.cls[0])
                        if class_id < len(model.names):
                            current_detected_object = model.names[class_id]

            # AAC Logic: Speak and Emit
            if time.time() - last_speak_time > SPEAK_INTERVAL:
                if current_detected_object:
                    phrase = AAC_VOCABULARY.get(
                        current_detected_object,
                        f"I see the {current_detected_object}."
                    )

                    if current_detected_object != last_detected_object:
                        print(f"DETECTED & SPEAKING: {current_detected_object} -> {phrase}")

                        speech_thread = threading.Thread(target=speak_text_in_thread, args=(phrase,), daemon=True)
                        speech_thread.start()

                        sio.emit('detection_update', {
                            'object': current_detected_object,
                            'phrase': phrase,
                            'confidence': round(max_conf * 100, 2)
                        })

                        last_speak_time = time.time()
                        last_detected_object = current_detected_object
                else:
                    if time.time() - last_speak_time > SPEAK_INTERVAL * 2 and last_detected_object != "":
                        last_detected_object = ""
                        sio.emit('detection_update', {'object': None, 'phrase': None})

            time.sleep(0.1)

        except Exception as e:
            print(f"Error in detection loop: {e}")
            if cap:
                cap.release()
            time.sleep(1)


# --- Server Startup ---

@app.on_event("startup")
async def startup_event():
    model = load_model()
    if model:
        threading.Thread(target=run_detection_loop, args=(model,), daemon=True).start()
    else:
        print("Model failed to load. Server starting without detection.")


@sio.event
def connect(sid, environ):
    print('Client connected:', sid)


@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("Starting AAC Voice Board Server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)