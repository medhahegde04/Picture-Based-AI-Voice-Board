# ==============================================================================
# SCRIPT NAME: detect_and_speak.py
# DESCRIPTION: Loads a trained YOLOv8 model, performs inference on an image,
#              and uses the results to generate voice output describing the detections.
# ==============================================================================

from ultralytics import YOLO
import pyttsx3
import os

# --- Configuration Section (UPDATE THESE PATHS) ---
# 1. Path to your best trained model weights (from the train5 run)
MODEL_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/runs/detect/train5/weights/best.pt"

# 2. Path to the file containing your 20 class names, one per line (create this file!)
# Ensure the classes are in the same order as in your data.yaml.
CLASS_FILE_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/classes.txt"

# 3. Path to the image file you want the system to analyze.
# Use a specific image, not a folder.
TEST_IMAGE_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/images/test/118.png"

# Detection confidence threshold (0.25 is the default, adjust if needed)
CONFIDENCE_THRESHOLD = 0.25


# --- Function to load class names ---
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
        # Run inference on the specified image
        results = model.predict(
            source=TEST_IMAGE_PATH,
            conf=CONFIDENCE_THRESHOLD,
            iou=0.7,  # Intersection over Union threshold for Non-Maximum Suppression
            imgsz=640,  # Image size (should match your training size)
            verbose=False,  # Set to True for more detailed output
            save=False  # We handle the output ourselves, no need to save image with boxes
        )
    except Exception as e:
        print(f"Error during prediction: {e}")
        engine.say("Error during image analysis.")
        engine.runAndWait()
        return

    # 5. Process Results and Prepare Speech
    detections = {}

    # Process results for the single image
    for result in results:
        # result.boxes contains the bounding box and confidence data
        for box in result.boxes:
            class_id = int(box.cls[0])  # Class ID is a tensor item
            class_name = class_names[class_id]

            # Count the detection
            detections[class_name] = detections.get(class_name, 0) + 1

    # Format the speech output
    if not detections:
        speech_text = "I don't see any objects I was trained to recognize."
    else:
        # Build the list of detected objects (e.g., "one chair, two tables")
        parts = []
        for name, count in detections.items():
            # Use count for quantity and pluralize the name if necessary
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