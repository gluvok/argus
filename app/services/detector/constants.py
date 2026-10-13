"""Object detection and vehicle category constants for YOLO inference."""

VEHICLE_CLASS_NAMES: dict[int, str] = {
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

MAX_DETECTIONS = 100
MIN_CROP_EDGE_PX = 8
