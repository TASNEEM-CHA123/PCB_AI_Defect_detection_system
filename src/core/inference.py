import os
import cv2
import numpy as np
import torch
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
import yaml

class PCBInferenceEngine:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        yolo_path = self.config.get("model", {}).get("yolo_weights", "a_model_download/best.pt")
        conf_thresh = self.config.get("model", {}).get("confidence_threshold", 0.3)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Initializing Inference Engine on {self.device}...")
        self.yolo_model_path = yolo_path
        
        try:
            self.detection_model = AutoDetectionModel.from_pretrained(
                model_type='yolov8',
                model_path=yolo_path,
                confidence_threshold=conf_thresh,
                device=self.device.type,
            )
        except Exception as e:
            print(f"Warning: Failed to load YOLO weights ({e}).")
            self.detection_model = None
            
    def detect_defects(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}")
            
        if self.detection_model is None:
            return image, []

        result = get_sliced_prediction(
            image_path,
            self.detection_model,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2
        )
        
        object_prediction_list = result.object_prediction_list
        boxes = []
        for obj in object_prediction_list:
            box = obj.bbox.to_xyxy()
            boxes.append({
                "box": box,
                "score": obj.score.value,
                "class_name": obj.category.name,
                "class_id": obj.category.id
            })
            
        return image, boxes
        
    def segment_defects(self, image, boxes):
        masks = []
        for det in boxes:
            box = np.array(det["box"])
            mask = np.zeros(image.shape[:2], dtype=bool)
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = True
            masks.append(mask)
        return masks
    
    def process_image(self, image_path):
        image, boxes = self.detect_defects(image_path)
        masks = self.segment_defects(image, boxes)
        
        overlay = image.copy()
        for idx, det in enumerate(boxes):
            box = det["box"]
            x1, y1, x2, y2 = map(int, box)
            
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(overlay, f"{det['class_name']} {det['score']:.2f}", 
                        (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            mask_img = masks[idx]
            overlay[mask_img] = overlay[mask_img] * 0.5 + np.array([0, 255, 0]) * 0.5
            
        return overlay, boxes, masks
