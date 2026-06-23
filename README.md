# Picture-Based AI Voice Board

A picture-based AAC (Augmentative and Alternative Communication) voice board that uses a YOLOv8 object detection model to identify classroom objects in real time and speak contextual phrases aloud. Built as a mini project for the AI/ML course in Semester 5.

---

## What It Does

Point your camera at any of the 20 supported classroom objects and the system will:
- Detect the object using a custom-trained YOLOv8 model.
- Display the detected object and confidence score.
- Speak a relevant AAC phrase aloud (e.g. *"I need to put this in my bag."*).

### Supported Objects
`table` `chair` `whiteboard` `bookshelf` `clock` `wall-magazine` `trash-can` `eraser` `sharpener` `pen` `book` `ruler` `scissor` `fan` `laptop` `remote-control` `bag` `pants` `shoes` `hat`

---

## Project Structure

```
Picture-Based-AI-Voice-Board/
├── Backend/
│   ├── voice board server.py   # Main FastAPI + Socket.IO server
│   ├── config.py               # Model and inference configuration
│   ├── yolo detector.py        # YOLO detection logic
│   ├── detect and speak.py     # Speech output
│   ├── webcam detect.py        # Webcam capture
│   ├── data_unifier.py         # Dataset preprocessing utility
│   └── voice board.py          # Standalone voice board script
├── Frontend/
│   ├── src/
│   │   ├── App.jsx             # Main app with routing and socket connection
│   │   └── components/         # Login, Signup, Home, Camera, Favourites, Profile
│   └── ...
├── Data/
│   ├── classes.txt             # 20 class names
│   └── data.yaml               # YOLO dataset config
└── runs/detect/train5/weights/ # Trained model weights
    ├── best.pt
    ├── best.onnx
    └── last.pt
```

---

## Setup & Running

### Prerequisites
- Python 3.13+
- Node.js 18+

### 1. Clone the repository
```bash
git clone https://github.com/medhahegde04/Picture-Based-AI-Voice-Board.git
cd Picture-Based-AI-Voice-Board
```

### 2. Install Python dependencies
```bash
pip install ultralytics fastapi uvicorn python-socketio pyttsx3 opencv-python pillow
```

### 3. Run the backend server
```bash
cd Backend
python "voice board server.py"
```
Server starts at `http://localhost:8000`

### 4. Run the frontend (in a separate terminal)
```bash
cd Frontend
npm install
npm run dev
```
Frontend starts at `http://localhost:5173`

### 5. Use the app
- Log in or sign up.
- Click the **camera button** in the top right to open the camera and capture the image.
- The system detects the object and speaks the AAC phrase aloud.

---

## Model

The detection model is a YOLOv8n fine-tuned with two datasets for 20 classroom object classes over 5 training runs.

- **Architecture:** YOLOv8n (nano)
- **Confidence threshold:** 0.50
- **Image size:** 640×640
- **Weights:** included in `runs/detect/train5/weights/`

---

## Dataset

Two datasets were used for training:

- **Indoor Objects Detection** — [DatasetNinja](https://datasetninja.com/indoor-object-detection) *(also available on [Kaggle, by thepbordin](https://www.kaggle.com/datasets/thepbordin/indoor-object-detection))*
- **Objects in the Classroom** — [Kaggle, by Arya Krisna Putra](https://www.kaggle.com/datasets/aryakrisnaputra/objects-in-the-classroom)

Download and place them under `Datasets/` if you wish to retrain. Training was done locally using `data_unifier.py` to preprocess and split into train/val/test sets.

---

## Notes for Developers

Several scripts in `Backend/` (`detect and speak.py`, `voice board.py`, `webcam detect.py`, `yolo.py`, `data_unifier.py`) contain hardcoded local paths and were used as standalone utilities during development and training. If you wish to run them, update the file paths at the top of each script to match your local directory.

The main app only requires `voice board server.py` and `config.py` for the backend, which use relative paths and work out of the box after cloning.

---

## Team

| Role | Name | GitHub |
|------|------|--------|
| Backend & Model Training | Medha Hegde | [medhahegde04](https://github.com/medhahegde04) |
| Frontend | Meghana M | [meghana2024](https://github.com/meghana2024) |

---

## Course

AI/ML Mini Project — Semester 5
