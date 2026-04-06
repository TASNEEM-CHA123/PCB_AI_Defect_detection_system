# Phase 2: Production-Ready Implementation Plan

This architecture plan dictates how we will upgrade the YOLO26-S + SAM 2 MVP into an asynchronous, flexible, and fully traceable Phase 2 backend. We are prioritizing a robust **Pipeline** over hardware machine protocol integrations as per your requirements.

## Proposed Changes

### Component: The Flexible Training Pipeline
We will re-configure the Colab environment to be extremely robust to dataset changes.
#### [MODIFY] [pcb_industrial_train_yolo26.ipynb](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/pcb_industrial_train_yolo26.ipynb)
- Add a top-level `CONFIG` block defining dataset paths and boolean toggles (e.g., `USE_BLACK_BOARD_FILTER = True`, `ENABLE_AUGMENTATION = False`).
- Ensure dataset loading logic can be seamlessly swapped by just commenting/uncommenting dataset string constants. This creates a resilient pipeline for future MobileSAM/different model tests.

### Component: Backend Microservice (FastAPI & Traceability)
By decoupling Streamlit from the model, we guarantee application stability heavily required for asynchronous jobs.
#### [NEW] `src/api/main.py`
- Initialize FastAPI to serve endpoints: `/analyze` (for processing images) and `/config` (for dynamic retrieval).
#### [NEW] `src/db/database.py` (Database Logging)
- Introduce **Traceability** out-of-the-box using python's built-in `sqlite3`.
- Create an `inspections` table that records: `operator_id`, `timestamp`, `serial_number`, `defect_count`, and `severity`.
#### [NEW] `config.yaml`
- Centralize all configurations, enabling **Dynamic Thresholds**. Confidence scores, pathings, and server ports will be fetched from here.

### Component: Core Inference & Explainable AI (XAI)
#### [MODIFY] [inference_engine.py](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/inference_engine.py) → `src/core/inference.py`
- Upgrade the file to load the optimal ONNX model from your existing `a_model_download` folder, making the process explicitly pipeline-driven. 
#### [NEW] `src/core/xai_gradcam.py`
- Integrate **Explainable AI (GradCAM)**. We will generate heatmaps on YOLO's output features to highlight *why* the model made a prediction locally, adding significant "WOW" factor for your M.Tech submission.

### Component: Frontend Adjustments (Streamlit)
#### [MODIFY] [app.py](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/app.py) → `src/ui/app.py`
- Remove all local HuggingFace/YOLO dependencies from `app.py`. Replace them with `requests` blocks pointing to `http://localhost:8000/analyze`.
- Introduce user inputs to simulate Traceability: an "Operator Login ID" and a simulated "Barcode/Serial Number" field (to replace physical scanning). 
- Plot the GradCAM heatmap output cleanly inside the analytics report.

---

## User Review Required / Open Questions

> [!IMPORTANT]
> - **Database Setup (Your Actions):** You do not need to install complex software like MySQL/PostgreSQL. I will configure `database.py` to auto-generate a lightweight `.db` file directly in your project folder. **Action for you**: You can download a free desktop app called **"DB Browser for SQLite"** to view and export your logs visually. Is this acceptable?
> - **ONNX Integration:** I notice the `a_model_download/` folder exists. I want to point the pipeline there automatically to leverage your best ONNX export. Could you confirm the exact file name of the `.onnx` model inside this folder?
> - **Simulated Barcode Tracking:** Since we lack barcode data, I will build an input box where operators simulate scanning by typing a numeric `Serial_Number`. Do you approve of this workaround?
