# Product Requirements Document (PRD): SAM-Detect Industrial

## 1. Goal & Objectives
**Goal:** Build a robust, zero-shot defect segmentation system for professional PCB manufacturing lines.
- **Objective 1:** Detect 95%+ of specified defect types using YOLO26-S.
- **Objective 2:** Provide sub-pixel accurate masks via SAM 2.
- **Objective 3:** Generate industrial-grade audit reports (PDF).

## 2. Target Users
- **Quality Assurance Engineers:** Monitoring board integrity in German/UAE smart factories.
- **Research Scholars:** Conducting ablation studies on detect-then-segment pipelines.

## 3. Technical Requirements
- **Hardware:** Local PC/Laptop for Inference (Dashboard), Google Colab for Training (YOLO).
- **Architecture:** Hybrid Detector-Segmenter (YOLO-Prompted SAM 2).
- **Data Source:** PKU-Market-PCB (Benchmark Dataset).

## 4. Functional Requirements
- **FR-01: Detection**: Identify 6 standard classes (Mouse Bite, Short, Open, etc.).
- **FR-02: Precise Refinement**: Generate high-fidelity masks for every detected bounding box.
- **FR-03: Industrial Slicing**: Use SAHI to maintain resolution during inference.
- **FR-04: Audit Logging**: Export results in a structured PDF/CSV format.

## 5. Success Metrics
- **mAP@50**: ≥ 0.90 for the YOLO component.
- **Inference Time**: ≤ 500ms for YOLO, ≤ 3s for SAM 2 refinement on CPU.
- **Reporting**: 100% accuracy in defect location mapping.
