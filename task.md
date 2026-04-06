# Task List: InspectAid - Next-Gen Industrial PCB AOI

## ✅ Phase 1: MVP & Core Setup (COMPLETED)
- [x] Trained YOLO26-S model in Google Colab and downloaded weights (`best.pt`).
- [x] Set up local `sample_images` directory for zero-upload UI testing.
- [x] Created `inference_engine.py` logic combining YOLO and SAM2.
- [x] Delivered a premium Streamlit UI (`app.py`) with PDF generation.

## 🚀 Phase 2: Production-Grade Refactoring 
- [ ] **Folder Structure:** Restructure flat files into a standard Python backend architecture (e.g., `/src`, `/api`, `/ui`, `/config`, `/models`).
- [ ] **Decoupling:** Separate Streamlit (Frontend) from Inference (Backend) using **FastAPI**.
- [ ] **Logging & Config:** Implement a centralized `.yaml` config file and proper `logging` instead of python `print()` statements.
- [ ] **Error Handling:** Add robust try-except blocks and Pydantic validation for the pipeline.

## 🌍 Phase 3: Deployment & Dockerization
- [ ] **Dockerization:** Create a `Dockerfile` and `docker-compose.yml` to containerize the FastAPI backend and Streamlit frontend.
- [ ] **Cloud Deployment:** Prepare deployment scripts for AWS EC2, HuggingFace Spaces, or Google Cloud Run.
- [ ] **CI/CD Pipeline:** (Optional) Set up basic GitHub Actions for automatic code linting and testing.
