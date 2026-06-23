# ==============================================================================
# SCRIPT NAME: config.py
# DESCRIPTION: Centralized configuration settings for the YOLOv8 voice board project.
# ==============================================================================

# --- File Paths ---
# Path to your best trained model weights (from the train5 run)
MODEL_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/runs/detect/train5/weights/best.pt"

# Path to the file containing your 20 class names, one per line.
CLASS_FILE_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/classes.txt"

# Path to the image file you want the system to analyze.
TEST_IMAGE_PATH = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/images/test/118.png"

# --- Model & Inference Parameters ---
# Detection confidence threshold (0.25 is the default, adjust if needed)
CONFIDENCE_THRESHOLD = 0.25

# Intersection over Union threshold for Non-Maximum Suppression
IOU_THRESHOLD = 0.7

# Image size (should match your training size)
IMAGE_SIZE = 640