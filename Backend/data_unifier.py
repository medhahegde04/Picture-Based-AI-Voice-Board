import json
import os
from pathlib import Path

# ===============================================
# CONFIGURATION: Define your desired class mapping
# ===============================================
# This dictionary maps the 'classTitle' found in your JSON files
# to their desired *new numerical class ID* (YOLO requires 0-indexed IDs).
# ===============================================
# CONFIGURATION: Define your desired class mapping
# ===============================================
CLASS_MAPPING = {
    "table": 0,
    "chair": 1,
    "whiteboard": 2,
    "bookshelf": 3,
    "clock": 4,
    "wall-magazine": 5,
    "trash-can": 6,
    "eraser": 7,
    "sharpener": 8,
    "pen": 9,
    "book": 10,
    "ruler": 11,
    "scissor": 12,
    "fan": 13,
    "laptop": 14,
    "remote-control": 15,
    "bag": 16,
    "pants": 17,
    "shoes": 18,
    "hat": 19,
}


def convert_bbox_to_yolo(img_size, points):
    """
    Converts Supervisey/JSON bounding box points to the YOLO format.
    :param img_size: A tuple of the image size (width, height)
    :param points: A list of two lists [[xmin, ymin], [xmax, ymax]]
    :return: A tuple of the YOLO bbox (x_center, y_center, width, height) in normalized form
    """
    img_width, img_height = img_size

    # Extract coordinates
    # The format is [[xmin, ymin], [xmax, ymax]]
    xmin, ymin = points[0]
    xmax, ymax = points[1]

    # Calculate center, width, and height in absolute pixels
    abs_x_center = (xmin + xmax) / 2.0
    abs_y_center = (ymin + ymax) / 2.0
    abs_width = xmax - xmin
    abs_height = ymax - ymin

    # Normalize coordinates (YOLO format: 0 to 1)
    rel_x_center = abs_x_center / img_width
    rel_y_center = abs_y_center / img_height
    rel_width = abs_width / img_width
    rel_height = abs_height / img_height

    # Ensure all values are between 0 and 1 (with minor safety clipping)
    rel_x_center = max(0, min(1, rel_x_center))
    rel_y_center = max(0, min(1, rel_y_center))
    rel_width = max(0, min(1, rel_width))
    rel_height = max(0, min(1, rel_height))

    return (rel_x_center, rel_y_center, rel_width, rel_height)


def json_to_yolo(input_json_path, output_txt_dir, class_mapping):
    """
    Parses a JSON annotation file and converts it to a YOLO TXT file.
    """
    try:
        with open(input_json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {input_json_path}: {e}")
        return

    # Extract image size
    img_width = data["size"]["width"]
    img_height = data["size"]["height"]
    img_size = (img_width, img_height)

    yolo_annotations = []

    for obj in data.get("objects", []):
        class_name = obj.get("classTitle")

        # Check if the object is a rectangle and has valid points
        points = obj.get("points", {}).get("exterior")
        if obj.get("geometryType") != "rectangle" or not points:
            continue  # Skip non-rectangle or invalid objects

        # Check if the class is in our mapping
        if class_name not in class_mapping:
            print(f"Warning: Class '{class_name}' not in CLASS_MAPPING. Skipping object in {input_json_path.name}.")
            continue

        class_id = class_mapping[class_name]

        # Convert to YOLO format
        yolo_bbox = convert_bbox_to_yolo(img_size, points)

        # Format the line: <class_id> <x_center> <y_center> <width> <height>
        line = f"{class_id} {' '.join([f'{coord:.6f}' for coord in yolo_bbox])}"
        yolo_annotations.append(line)

    # Save the YOLO annotations to a text file
    if yolo_annotations:
        json_filename = Path(input_json_path).stem
        output_txt_path = Path(output_txt_dir) / f"{json_filename}.txt"

        with open(output_txt_path, 'w') as f:
            f.write('\n'.join(yolo_annotations))
        print(f"Converted {json_filename}.json -> {json_filename}.txt")
    else:
        print(f"No objects found or mapped in {Path(input_json_path).name}. Skipping TXT creation.")


def main(input_dir, output_dir):
    """
    Main function to process all JSON files in the input directory.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Look for JSON files
    json_files = list(input_path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return

    print(f"Found {len(json_files)} JSON files. Starting conversion...")

    for json_file in json_files:
        json_to_yolo(json_file, output_path, CLASS_MAPPING)

    print("\nConversion complete!")


if __name__ == "__main__":
    # 1. Update the CLASS_MAPPING dictionary above to match your classes and new IDs.
    # 2. Set your input directory (where your JSON files are).
    # 3. Set your output directory (where the YOLO TXT files will be saved).

    input_json_directory = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Datasets/indoor-objects-detection-DatasetNinja/valid/ann"
    output_yolo_label_directory = "D:/sem 5/assignments/Picture-Based-AI-Voice-Board/Data/labels/val"

    # --- Run the main conversion process ---
    main(input_json_directory, output_yolo_label_directory)