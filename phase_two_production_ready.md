# Phase 2: Production-Ready Implementation Plan (Definitive)

This architecture plan dictates how we will upgrade the YOLO26-S + SAM 2 MVP into an asynchronous, flexible, and fully traceable Phase 2 backend. We prioritize a robust **flexible software pipeline** over complex hardware machine protocol integrations, ensuring the system is professional, scalable, and research-grade for your M.Tech standards.

---

## 🛠️ Module 1: Environment & Isolation
To ensure portability across any device (Windows/Linux/Mac), we are moving to a localized environment.

### [setup_venv.bat](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/setup_venv.bat)
- **Action:** Automates `python -m venv venv`, activation, and `pip install -r requirements.txt`.
- **Why:** Isolates heavy AI libraries (Ultralytics, SAM 2, SAM, etc.) from your system and prevents "Missing DLL" errors on new machines.

---

## 🧪 Module 2: Flexible Training Pipeline (Colab Optimization)
We will re-configure the Colab environment to be extremely robust to dataset changes.
- **[MODIFY] [pcb_industrial_train_yolo26.ipynb](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/pcb_industrial_train_yolo26.ipynb)**
    - Add a top-level `CONFIG` block defining dataset paths and boolean toggles (e.g., `USE_BLACK_BOARD_FILTER = True`, `ENABLE_AUGMENTATION = False`).
    - Ensure dataset loading logic can be seamlessly swapped by just commenting/uncommenting dataset string constants. This creates a resilient pipeline for future MobileSAM/different model tests.

---

## 🏗️ Module 3: Enterprise Backend Architecture

### 📂 Professional Folder Structure
We will migrate from a flat file list to a standard Python backend layout:
- `src/api/`: FastAPI endpoints and Pydantic schemas.
- `src/core/`: Inference logic (YOLO, SAHI, SAM 2, GradCAM).
- `src/ui/`: Streamlit frontend components.
- `src/db/`: SQLite database handlers.
- `config/`: Centralized `config.yaml` for system-wide constants.

### 🌐 Asynchronous FastAPI Backend (The "Brain")
By decoupling Streamlit from the model, we guarantee application stability.
- **[NEW] `src/api/main.py`**
    - Initialize **Asynchronous** FastAPI endpoints: `/analyze` (heavy inference) and `/config` (dynamic retrieval).
    - Prevents the UI from freezing during high-resolution segmentation.

---

## 📊 Module 4: Audit & Industrial Traceability

### 🗄️ SQLite Logging System
- **[NEW] `src/db/database.py`**
    - Introduce **Traceability** using Python's built-in `sqlite3`.
    - Create an `inspections` table that records: 
        - `operator_id` (Who?)
        - `timestamp` (When?)
        - `serial_number` (Which board?)
        - `defect_count` (How many?)
        - `severity` (How bad?)
- **Action for you**: Use **"DB Browser for SQLite"** to view and export these logs for your thesis results.

---

## 🧠 Module 5: Core Inference & Explainable AI (XAI)

### 🚀 Industrial Pipeline Enhancements
- **[MODIFY] [inference_engine.py](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/inference_engine.py) → `src/core/inference.py`**
    - Upgrade to load optimal **ONNX** models from the existing `a_model_download/` folder.
- **[NEW] `src/core/xai_gradcam.py`**
    - Integrate **Explainable AI (GradCAM)**. We will generate heatmaps on YOLO's output features to highlight *why* the model made a prediction locally, adding significant "WOW" factor.

---

## 💻 Module 6: Frontend Adjustments (Streamlit)

- **[MODIFY] [app.py](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/app.py) → `src/ui/app.py`**
    - Remove all local AI dependencies; replace them with `requests` calls to the FastAPI server.
    - **Traceability UI:** Add an "Operator Login" and "Serial Number" input field to replace physical barcode scanning.
    - **GradCAM View:** Plot the heatmap output directly inside the analytics report for the operator to verify AI logic.

---

## 💡 Roadmap Context
> [!IMPORTANT]
> **Docker Status:** Dockerization is officially moved to **Phase 3: Deployment**. 
> Phase 2 is the "Refactoring & Innovation" stage that makes the code professional and high-performance in a local environment.

## 🏁 How to Start Work (Daily)
1. Run `.\setup_venv.bat` (if first time or requirements updated).
2. Activate: `.\venv\Scripts\activate`.
3. Give me (the AI) context: *"We are working on Phase 2 refactoring. Check [task.md](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/task.md) and [phase_two_production_ready.md](file:///d:/Study material/JMI Mtech ds/sem 4/major_2/phase_two_production_ready.md)."*
