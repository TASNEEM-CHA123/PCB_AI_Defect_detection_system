# Strategic Project Roadmap: Hybrid Industrial PCB AOI

## Stage 1: Cloud-Based Training (Colab)
- Setup PKU-Market-PCB data repository.
- Train YOLO26-S (Small) for 50+ epochs.
- Export weights to `.onnx` and `.pt` for local deployment.
- **Milestone:** Achieve >90% mAP on industrial validation set.

## Stage 2: Local Core Infrastructure
- Implement `inference_engine.py` with multi-stage logic.
- Integrate SAHI (Slicing) for high-res PCB scans.
- Setup SAM 2 locally for prompt-based masking.
- **Milestone:** Successful local test run on unseen PCB image.

## Stage 3: Operator Dashboard (UI)
- Develop Streamlit `app.py`.
- Add interactive multi-file uploader.
- Build the "Trace Verification" view with mask overlays.
- **Milestone:** Functional dashboard with local model loading.

## Stage 4: Reporting & Audit
- Implement the PDF/CSV generation module.
- Add "Industrial Severity Scoring" (Area calculated via Segmentation mask).
- **Milestone:** Final end-to-end walkthrough from upload to PDF.
