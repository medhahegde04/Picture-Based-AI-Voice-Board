# ==============================================================================
# SCRIPT NAME: webcam_detect_and_speak.py (Option 2 - Periodic Speak)
# DESCRIPTION: Performs real-time YOLOv8 object detection on a webcam stream
#              and uses pyttsx3 for voice feedback every SPEAK_INTERVAL seconds.
# ==============================================================================

from ultralytics import YOLO
import pyttsx3
import cv2
import time
import os

# --- Configuration Section (UPDATE THESE PATHS) ---
# 1. Path to your best trained model weights
MODEL_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/runs/detect/train5/weights/best.pt"

# 2. Path to the clean class names file (e.g., 'table', 'chair', etc.)
# IMPORTANT: Ensure this file ONLY contains the names (e.g., 'bookshelf', NOT '3: bookshelf')
CLASS_FILE_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/classes.txt"

# CAMERA_INDEX: 0 is usually the built-in webcam. Change to 1 or 2 if using an external one.
CAMERA_INDEX = 0

# --- Detection Parameters ---
CONFIDENCE_THRESHOLD = 0.40  # Adjust this value (0.25 is default, 0.40 is stricter)
SPEAK_INTERVAL = 5  # Time in seconds between speaking updates (Repeat frequency)
IOU_THRESHOLD = 0.7
IMG_SIZE = 640


# --- Function to load class names (Crucial for correct speech output) ---
def load_class_names(file_path):
    """Reads class names from a text file, one name per line."""
    try:
        with open(file_path, 'r') as f:
            # Cleanly load names, stripping whitespace
            class_names = [line.strip() for line in f if line.strip()]
        return class_names
    except FileNotFoundError:
        print(f"Error: Class names file not found at {file_path}")
        return None


# --- Main Webcam Loop ---
def run_realtime_detection():
    # 1. Setup
    class_names = load_class_names(CLASS_FILE_PATH)
    if class_names is None:
        print("FATAL: Cannot start without class names.")
        return

    # Initialize TTS Engine
    engine = pyttsx3.init()

    # Load YOLOv8 Model
    print(f"Loading model from: {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        engine.say("Fatal Error. Cannot load the detection model.")
        engine.runAndWait()
        return

    # Open Webcam Capture
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"FATAL: Cannot open camera at index {CAMERA_INDEX}")
        engine.say("Error. Cannot access the camera.")
        engine.runAndWait()
        return

    last_speak_time = time.time()

    # 2. Real-Time Processing Loop
    try:
        while True:
            # Read frame from the camera
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Perform Inference on the frame
            results = model.predict(
                source=frame,
                conf=CONFIDENCE_THRESHOLD,
                iou=IOU_THRESHOLD,
                imgsz=IMG_SIZE,
                verbose=False,
                device='cpu'
            )

            # Process Results
            detections = {}
            annotated_frame = frame.copy()

            for result in results:
                # Get the frame with bounding boxes drawn by YOLO
                annotated_frame = result.plot()

                # Process detections for speech
                for box in result.boxes:
                    class_id = int(box.cls[0])

                    # Ensure the class ID is within the bounds of our class_names list
                    if class_id < len(class_names):
                        class_name = class_names[class_id]
                        detections[class_name] = detections.get(class_name, 0) + 1
                    # Note: We now assume class_name is clean (no ID prefix)

            # Prepare speech text
            if detections:
                # Build the speech string, pluralizing where needed
                parts = []
                for name, count in detections.items():
                    # Simple pluralization check: add 's' unless the name ends in 's'
                    plural_name = f"{name}s" if count > 1 and not name.endswith('s') else name
                    parts.append(f"{count} {plural_name}")

                current_speech_text = f"I see: {', '.join(parts)}."
            else:
                current_speech_text = "I don't see any recognized objects."

            # 3. Speech Logic (Modified for Periodic Repeat)
            # Speak if enough time has passed, regardless of detection change
            if time.time() - last_speak_time > SPEAK_INTERVAL:
                print(f"Speaking: {current_speech_text}")
                engine.say(current_speech_text)
                engine.runAndWait()

                # Reset timer
                last_speak_time = time.time()

            # Display the annotated frame
            cv2.imshow('YOLOv8 Real-Time Detection', annotated_frame)

            # Press 'q' to exit
            if cv2.waitKey(1) == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred during the loop: {e}")
    finally:
        # 4. Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("Camera stream closed.")


if __name__ == "__main__":
    run_realtime_detection()