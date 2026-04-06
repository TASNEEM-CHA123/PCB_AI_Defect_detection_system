import os
import cv2
import numpy as np
import torch
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

class PCBInferenceEngine:
    def __init__(self, yolo_weights_path="yolov8s.pt", sam_checkpoint="sam2_hiera_small.pt", config_file="sam2_hiera_s.yaml"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Initializing Inference Engine on {self.device}...")
        
        # Load YOLO model via SAHI wrapper for slicing
        # Ensure model_path handles generic YOLO architecture mapping
        try:
            self.detection_model = AutoDetectionModel.from_pretrained(
                model_type='yolov8',
                model_path=yolo_weights_path,
                confidence_threshold=0.3,
                device=self.device.type,
            )
        except Exception as e:
            print(f"Warning: Failed to load YOLO weights ({e}). Make sure {yolo_weights_path} is downloaded.")
            self.detection_model = None

        # SAM 2 initialization placeholder
        # Following Mageshwari et al. (2026) framework
        # from sam2.build_sam import build_sam2
        # from sam2.sam2_image_predictor import SAM2ImagePredictor
        # self.sam2_model = build_sam2(config_file, sam_checkpoint, device=self.device)
        # self.predictor = SAM2ImagePredictor(self.sam2_model)
        
    def detect_defects(self, image_path):
        """
        Stage 1: YOLO Detection utilizing SAHI (Slicing Aided Hyper Inference)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}")
            
        print("Running Stage 1: SAHI Detection...")
        if self.detection_model is None:
            # Fallback if no model
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
        """
        Stage 2: SAM 2 Mask Refinement using YOLO boxes as prompts.
        """
        print("Running Stage 2: SAM 2 Mask Refinement...")
        # Placeholder actual SAM2 logic:
        # self.predictor.set_image(image)
        
        masks = []
        for det in boxes:
            box = np.array(det["box"])
            
            # Dummy Mask generator until true SAM2 weights loaded
            mask = np.zeros(image.shape[:2], dtype=bool)
            x1, y1, x2, y2 = map(int, box)
            
            # Mocks the boundary of the defect
            # A real implementation would invoke:
            # masks_, _, _ = self.predictor.predict(box=box, multimask_output=False)
            # mask = masks_[0]
            mask[y1:y2, x1:x2] = True
            masks.append(mask)
            
        return masks
    
    def process_image(self, image_path):
        """
        End-to-End Hybrid Pipeline Flow
        """
        image, boxes = self.detect_defects(image_path)
        masks = self.segment_defects(image, boxes)
        
        overlay = image.copy()
        for idx, det in enumerate(boxes):
            box = det["box"]
            x1, y1, x2, y2 = map(int, box)
            
            # Bounding box
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(overlay, f"{det['class_name']} {det['score']:.2f}", 
                        (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            # Defect segmentation representation
            mask_img = masks[idx]
            overlay[mask_img] = overlay[mask_img] * 0.5 + np.array([0, 255, 0]) * 0.5 # Green tint
            
        return overlay, boxes, masks
