# ==============================================================================
# SCRIPT NAME: aac_voice_board.py (FINAL STABLE VERSION - Threading/Cleanup Fix)
# DESCRIPTION: Fixed script to ensure non-blocking, periodic speech and clean shutdown.
# ==============================================================================

from ultralytics import YOLO
import pyttsx3
import cv2
import time
import os
import threading

# --- Configuration Section (CHECK THESE VALUES) ---
MODEL_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/runs/detect/train5/weights/best.pt"
CLASS_FILE_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/classes.txt"
CAMERA_INDEX = 0  # If webcam fails, change to 1.

# --- DETECTION PARAMETERS (Tune these if detection is noisy) ---
CONFIDENCE_THRESHOLD = 0.50
SPEAK_INTERVAL = 5
IOU_THRESHOLD = 0.7
IMG_SIZE = 640

# --- 🧠 AAC VOCABULARY MAPPING (Your 20 objects) ---
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

# Global Engine and Lock
global_engine = None
speech_lock = threading.Lock()


# --- Threaded Voice Function (FIX 1: Added small sleep) ---
def speak_text(text):
    """Function to be run in a separate thread to handle pyttsx3 speech."""
    if global_engine is not None:
        # Give the thread a moment to stabilize before speaking
        time.sleep(0.05)
        with speech_lock:
            # Clear previous speech and queue new text
            global_engine.stop()
            global_engine.say(text)
            # Blocks THIS thread until speech is complete (non-blocking for the main loop)
            try:
                global_engine.runAndWait()
            except RuntimeError as e:
                # Catching potential errors if the engine is already closing
                print(f"Speech error: {e}")
                pass


# --- Function to load class names ---
def load_class_names(file_path):
    try:
        with open(file_path, 'r') as f:
            class_names = [line.strip() for line in f if line.strip()]
        return class_names
    except FileNotFoundError:
        print(f"Error: Class names file not found at {file_path}")
        return None


# ==============================================================================
# --- Main Webcam Loop ---
# ==============================================================================

def run_realtime_detection():
    global global_engine

    # 1. Setup
    class_names = load_class_names(CLASS_FILE_PATH)
    if class_names is None:
        print("FATAL: Cannot start without class names.")
        return

    # Initialize Global TTS Engine
    try:
        global_engine = pyttsx3.init()
    except Exception as e:
        print(f"Error initializing pyttsx3: {e}")
        return

    # Load YOLOv8 Model
    print(f"Loading model from: {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Open Webcam Capture
    print(f"Attempting to open camera at index {CAMERA_INDEX}...")
    # NOTE: Using cv2.CAP_DSHOW for better Windows compatibility
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"FATAL: Cannot open camera at index {CAMERA_INDEX}. Try changing CAMERA_INDEX to 1 in the script.")
        return

    last_speak_time = time.time()
    last_detected_object = ""

    # 2. Real-Time Processing Loop
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Perform Inference (Omitted for brevity, but runs here...)
            results = model.predict(
                source=frame,
                conf=CONFIDENCE_THRESHOLD,
                iou=IOU_THRESHOLD,
                imgsz=IMG_SIZE,
                verbose=False,
                device='cpu'
            )

            # Process Results - Focus on the Single Highest Confidence Detection
            current_detected_object = ""
            max_conf = 0.0

            if results and results[0].boxes:
                for box in results[0].boxes:
                    conf = float(box.conf[0])
                    if conf > max_conf:
                        max_conf = conf
                        class_id = int(box.cls[0])
                        if class_id < len(class_names):
                            current_detected_object = class_names[class_id]

            # Annotate Frame
            annotated_frame = frame.copy()
            if results:
                annotated_frame = results[0].plot()

            # 3. AAC Logic (Conditional Speaking)
            if time.time() - last_speak_time > SPEAK_INTERVAL:

                if current_detected_object:
                    phrase = AAC_VOCABULARY.get(
                        current_detected_object,
                        f"I see the {current_detected_object}, but I don't have a specific phrase for it."
                    )

                    # Speak only if the object has changed
                    if current_detected_object != last_detected_object:
                        print(f"Starting Speech Thread: {current_detected_object} -> {phrase}")

                        thread = threading.Thread(target=speak_text, args=(phrase,), daemon=True)
                        thread.start()

                        last_speak_time = time.time()
                        last_detected_object = current_detected_object

                else:
                    # Reset last_detected_object if nothing is seen for a prolonged time
                    if time.time() - last_speak_time > SPEAK_INTERVAL * 2 and last_detected_object != "":
                        last_detected_object = ""

            # Display the annotated frame
            cv2.imshow('AAC Voice Board - Detection', annotated_frame)

            # Press 'q' to exit
            if cv2.waitKey(1) == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred during the loop: {e}")
    finally:
        # 4. Cleanup (FIX 2: Ensure threads are waited for, or handle engine stop gracefully)
        cap.release()
        cv2.destroyAllWindows()

        # This explicit cleanup helps avoid the AttributeError during Python's garbage collection
        if global_engine:
            global_engine.stop()

        print("Camera stream closed.")


if __name__ == "__main__":
    run_realtime_detection()