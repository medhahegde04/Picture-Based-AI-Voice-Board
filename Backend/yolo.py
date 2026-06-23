from ultralytics import YOLO

# Load a pretrained model (e.g., YOLOv8n)
model = YOLO('yolov8n.pt')

# Define the training parameters
data_yaml_path = 'D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/data.yaml'

# Start training
results = model.train(
    data=data_yaml_path,
    epochs=50,
    imgsz=640,
    batch=16,
    # Add other parameters like project, name, etc., if needed
)