# ==============================================================================
# SCRIPT NAME: yolo_detector.py
# DESCRIPTION: Loads a trained YOLOv8 model, performs inference, and generates
#              voice output describing the detections.
# ==============================================================================

from ultralytics import YOLO
import pyttsx3
import os
from config import * # Import all configurations from the new file

# --- Utility Function ---
def load_class_names(file_path):
    """Reads class names from a text file, one name per line."""
    try:
        with open(file_path, 'r') as f:
            # Strip whitespace and ignore empty lines
            class_names = [line.strip() for line in f if line.strip()]
        return class_names
    except FileNotFoundError:
        print(f"Error: Class names file not found at {file_path}")
        return None

# --- Main Detection and Speaking Logic ---
def run_voice_detection():
    """Initializes the engine and model, runs detection, and speaks the results."""
    # 1. Initialize Text-to-Speech Engine
    try:
        engine = pyttsx3.init()
    except Exception as e:
        print(f"Error initializing text-to-speech engine: {e}")
        return

    # 2. Load Class Names
    class_names = load_class_names(CLASS_FILE_PATH)
    if class_names is None:
        engine.say("Fatal Error. Cannot find class names file.")
        engine.runAndWait()
        return

    # 3. Load YOLOv8 Model
    print(f"Loading model from: {MODEL_PATH}")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        engine.say("Fatal Error. Cannot load the detection model.")
        engine.runAndWait()
        return

    # 4. Perform Inference
    print(f"Running prediction on: {TEST_IMAGE_PATH}")
    try:
        results = model.predict(
            source=TEST_IMAGE_PATH,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,  # Use imported config
            imgsz=IMAGE_SIZE,   # Use imported config
            verbose=False,
            save=False
        )
    except Exception as e:
        print(f"Error during prediction: {e}")
        engine.say("Error during image analysis.")
        engine.runAndWait()
        return

    # 5. Process Results and Prepare Speech
    detections = {}

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = class_names[class_id]
            detections[class_name] = detections.get(class_name, 0) + 1

    # Format the speech output
    if not detections:
        speech_text = "I don't see any objects I was trained to recognize."
    else:
        parts = []
        for name, count in detections.items():
            # Handle singular/plural
            parts.append(f"{count} {name}{'s' if count > 1 and name[-1] != 's' else ''}")

        speech_text = f"I see: {', '.join(parts)}."

    # 6. Generate Voice Output
    print(f"Detections found: {detections}")
    print(f"Speech Output: {speech_text}")

    engine.say(speech_text)
    engine.runAndWait()

    print("\n--- Detection Complete ---")


if __name__ == "__main__":
    run_voice_detection()