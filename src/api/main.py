import os
import cv2
import tempfile
import yaml
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys

# Ensure src is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.inference import PCBInferenceEngine
from src.core.xai_gradcam import GradCAMExplainer
from src.db.database import Database

app = FastAPI(title="InspectAid API", version="1.0.0")

# Enable CORS for external frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load configuration
try:
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
except Exception:
    config = {"model": {"yolo_weights": "a_model_download/best.pt"}, "database": {"db_path": "src/db/industrial_pcb.db"}}

# Initialize Engines
engine = PCBInferenceEngine(config_path="config/config.yaml")
gradcam_explainer = GradCAMExplainer(yolo_weights_path=config["model"]["yolo_weights"])
db = Database(db_path=config["database"]["db_path"])

@app.get("/")
async def root():
    return {
        "status": "Ready",
        "message": "InspectAid Phase 2 Backend is LIVE",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc_ui": "/redoc"
        },
        "active_endpoints": ["/analyze (POST)", "/history (GET)"]
    }

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    operator_id: str = Form("OP-001"),
    serial_number: str = Form("SN-DEFAULT")
):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 1. Run Inference
        overlay, boxes, masks = engine.process_image(tmp_path)
        
        # 2. Run GradCAM
        heatmap_overlay = gradcam_explainer.generate_heatmap(tmp_path)
        
        # Determine Severity and Status
        critical_count = sum(1 for b in boxes if b.get('class_name') in ['Short', 'Mouse_bite'])
        status = "FAIL" if len(boxes) > 0 else "PASS"
        severity = "HIGH" if critical_count > 0 else ("LOW" if len(boxes) > 0 else "NONE")

        # 3. Log to DB
        db.log_inspection(
            operator_id=operator_id,
            serial_number=serial_number,
            defect_count=len(boxes),
            severity=severity,
            status=status
        )

        # Encode to base64
        _, overlay_encoded = cv2.imencode('.png', overlay)
        overlay_b64 = base64.b64encode(overlay_encoded).decode('utf-8')
        
        _, heatmap_encoded = cv2.imencode('.png', heatmap_overlay)
        heatmap_b64 = base64.b64encode(heatmap_encoded).decode('utf-8')
        
        os.remove(tmp_path)
        
        return JSONResponse({
            "status": status,
            "severity": severity,
            "defect_count": len(boxes),
            "boxes": boxes,
            "overlay_b64": overlay_b64,
            "heatmap_b64": heatmap_b64
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(limit: int = 50):
    records = db.get_history(limit=limit)
    return {"history": records}
