# Task List: InspectAid - Next-Gen Industrial PCB AOI

## ✅ Phase 1: MVP & Core Setup (COMPLETED)
- [x] Trained YOLO26-S model in Google Colab and downloaded weights (`best.pt`).
- [x] Set up local `sample_images` directory for zero-upload UI testing.
- [x] Created `inference_engine.py` logic combining YOLO and SAM2.
- [x] Delivered a premium Streamlit UI (`app.py`) with PDF generation.

## 🚀 Phase 2: Production-Grade Refactoring 
## 🚀 Phase 2: Production-Grade Refactoring & Innovation
- [x] **Environment:** Automated Virtual Environment setup (`setup_venv.bat`).
- [ ] **Module 2: Training Pipeline:** Robustify Colab notebook with CONFIG blocks and dataset toggles.
- [ ] **Module 3: Architecture:** Migrate to professional folder structure (`/src/api`, `/src/core`, etc.).
- [ ] **Module 3: FastAPI:** Implement Asynchronous Backend for SAM 2 / YOLO decoupling.
- [ ] **Module 4: Traceability:** Implement SQLite logging (Inspections table).
- [ ] **Module 5: XAI:** Integrate Explainable AI (GradCAM heatmaps).
- [ ] **Module 6: UI Refinement:** Add "Operator Login" and "Serial Number" simulated inputs.

## 🌍 Phase 3: Deployment & Dockerization
- [ ] **Dockerization:** Create a `Dockerfile` and `docker-compose.yml` to containerize the FastAPI backend and Streamlit frontend.
- [ ] **Cloud Deployment:** Prepare deployment scripts for AWS EC2, HuggingFace Spaces, or Google Cloud Run.
- [ ] **CI/CD Pipeline:** (Optional) Set up basic GitHub Actions for automatic code linting and testing.
