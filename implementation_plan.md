# Industrial PCB AOI System: Comprehensive Implementation Plan (2026)

This core design document outlines the technical strategy for building a state-of-the-art **Automated Optical Inspection (AOI)** system for Printed Circuit Boards (PCBs). It is optimized for smart manufacturing industries (Germany/UAE) and Academic PhD research (Computer Vision).

## 🎯 Project Core Objectives
- **Fast Detection:** Use **YOLO26-S (Small)** for low-latency defect localization via an NMS-Free (Non-Maximum Suppression) architecture.
- **Precision Segmentation:** Integrate **SAM 2 (Segment Anything Model)** to refine detection boxes into pixel-perfect metallurgical masks.
- **Benchmark Alignment:** Utilize the **PKU-Market-PCB** dataset, consistent with the **Mageshwari et al. (2026)** framework.

---

## 🛠️ Execution Strategy & Files to be Created

The following files represent the complete system architecture and SHOULD BE CREATED by the implementing agent:

### 1. Training Infrastructure (Cloud/GPU Only)
- **File:** `pcb_industrial_train_yolo26.ipynb`
- **Purpose:** A Google Colab notebook to download the PKU-Market-PCB dataset and train the YOLO26-S model on a T4/A100 GPU.
- **Target Metrics:** >0.90 mAP on 6 standard defect classes (Short, Open, Mouse Bite, etc.).

### 2. Local Inference Core (CPU Compatible)
- **File:** `inference_engine.py`
- **Logic:** Stage 1 (YOLO detection) -> Stage 2 (SAM 2 mask refinement).
- **Key Feature:** Implement **SAHI (Slicing Aided Hyper Inference)** logic to handle high-resolution boards without losing detail on tiny traces.

### 3. Industrial Operator Interface
- **File:** `app.py`
- **Framework:** Streamlit.
- **Workflow:** File Upload -> Automated Analysis -> Multi-stage Visual Validation (Original vs. Mask Overlay) -> Export PDF Quality Audit Report.

### 4. Configuration & Dependencies
- **File:** `requirements.txt`
- **Core Packages:** `ultralytics`, `sam2`, `streamlit`, `opencv-python`, `torch`.

---

## 🔬 Scientific Foundations & Drawbacks
- **NMS-Free Advantage:** YOLO26 eliminates the post-processing bottleneck, allowing for smooth local CPU testing.
- **SAM 2 Zero-Shot:** We use pre-trained SAM 2 weights directly, passing YOLO boxes as prompts. No segmentation training is required on the industrial dataset.
- **Latency Drawback:** SAM 2 is computationally heavy. On a standard CPU, mask generation will take ~1-3 seconds. The UI should reflect this "processing" state to the user.

---

## ✅ Deliverable Verification Plan
1. **Model Loading:** Confirm YOLO weights load and run on sample data.
2. **Mask Adherence:** Verify the SAM 2 mask perfectly matches the boundaries of the defect (e.g., a short circuit trace).
3. **Report Fidelity:** Ensure the exported PDF contains the Defect ID, Class, Confidence, and Severity Area (mm²).

---
> [!IMPORTANT]
> This plan is designed for an agent following a **Research-First** approach. Ensure all code adheres to the high standards required for Industrial Quality Assurance.
