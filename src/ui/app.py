import streamlit as st
import numpy as np
import cv2
import tempfile
import os
import httpx
import base64
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ----------------- Configuration & Styling -----------------
st.set_page_config(page_title="InspectAid - AOI System", page_icon="🔬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    :root {
        --primary-color: #00d2ff;
        --secondary-color: #3a7bd5;
        --bg-color: #0a0e17;
        --card-bg: #151b29;
        --text-color: #e2e8f0;
    }
    
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }
    
    .premium-title {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: -10px;
        margin-bottom: 30px;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 20px;
    }
    
    .metric-card {
        background: rgba(21, 27, 41, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 210, 255, 0.15);
        border: 1px solid rgba(0, 210, 255, 0.2);
    }
    
    .metric-title {
        font-size: 1rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .metric-value.danger { color: #f43f5e; }
    .metric-value.success { color: #10b981; }
    
    .image-container {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #1e293b;
        background: var(--card-bg);
        padding: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='premium-title'>InspectAid</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Next-Gen Automated Optical Inspection Phase 2</div>", unsafe_allow_html=True)

API_URL = "http://localhost:8000/analyze"

# ----------------- Sidebar Data Input -----------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2835/2835560.png", width=60)
st.sidebar.markdown("### 🎛️ Operator Traceability")
operator_id = st.sidebar.text_input("Operator ID", "OP-001")
serial_number = st.sidebar.text_input("Board Serial Number", "SN-987654321")

st.sidebar.markdown("### 🎛️ Inspection Controls")
input_mode = st.sidebar.radio("Input Source", ["Test with Sample Images", "Upload Diagnostics Scan"])

image_path_to_process = None

if input_mode == "Test with Sample Images":
    sample_images_dir = "sample_images"
    if os.path.exists(sample_images_dir) and os.listdir(sample_images_dir):
        samples = [f for f in os.listdir(sample_images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        selected_sample = st.sidebar.selectbox("Select Benchmark Scan", samples)
        image_path_to_process = os.path.join(sample_images_dir, selected_sample)
else:
    uploaded_file = st.sidebar.file_uploader("Upload Raw PCB Scan (.jpg, .png)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tfile.write(uploaded_file.read())
        image_path_to_process = tfile.name

def create_pdf_report(image, overlay, boxes, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "InspectAid: Quality Audit Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Total Defects Found: {len(boxes)}")
    c.drawString(50, height - 100, f"Operator: {operator_id} | SN: {serial_number}")
    
    temp_img = "temp_overlay.jpg"
    cv2.imwrite(temp_img, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    c.drawImage(temp_img, 50, height - 420, width=500, height=300, preserveAspectRatio=True)
    os.remove(temp_img)
    
    y = height - 450
    c.drawString(50, y, "Defect Details & Assessment:")
    y -= 25
    for idx, det in enumerate(boxes):
        if y < 50:
            c.showPage()
            y = height - 50
        details = f"#{idx+1} Type: {det.get('class_name', 'Unknown')} | Confidence: {det.get('score', 0):.2f}"
        c.drawString(70, y, details)
        y -= 20
    c.save()

if image_path_to_process:
    image = Image.open(image_path_to_process).convert("RGB")
    image_np = np.array(image)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📷 Input Optical Scan")
        st.markdown("<div class='image-container'>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.sidebar.button("🚀 Run AI Analysis", use_container_width=True):
        with st.spinner("Neural Processing Active (Communicating with FastAPI Engine)..."):
            try:
                files = {'file': open(image_path_to_process, 'rb')}
                data = {'operator_id': operator_id, 'serial_number': serial_number}
                
                response = httpx.post(API_URL, files=files, data=data, timeout=60.0)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    overlay_bytes = base64.b64decode(result['overlay_b64'])
                    heatmap_bytes = base64.b64decode(result['heatmap_b64'])
                    boxes = result['boxes']
                    status = result.get('status', 'FAIL')
                    
                    overlay_np = np.frombuffer(overlay_bytes, dtype=np.uint8)
                    overlay_img = cv2.imdecode(overlay_np, cv2.IMREAD_COLOR)
                    overlay_rgb = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB)
                    
                    heatmap_np = np.frombuffer(heatmap_bytes, dtype=np.uint8)
                    heatmap_img = cv2.imdecode(heatmap_np, cv2.IMREAD_COLOR)
                    heatmap_rgb = cv2.cvtColor(heatmap_img, cv2.COLOR_BGR2RGB)
                    
                else:
                    st.error(f"API Error: {response.text}")
                    overlay_rgb = image_np
                    heatmap_rgb = image_np
                    boxes = []
                    status = "FAIL"
            except Exception as e:
                st.error(f"Connection Error: Is the FastAPI server running on port 8000? {e}")
                overlay_rgb = image_np
                heatmap_rgb = image_np
                boxes = []
                status = "FAIL"
                
        with col2:
            st.markdown("### 🎯 Intelligent Detection Map")
            st.markdown("<div class='image-container'>", unsafe_allow_html=True)
            st.image(overlay_rgb, use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ----------------- Analytics & XAI Dashboard -----------------
        st.markdown("### 📊 Metrics & Traceability")
        critical_count = sum(1 for b in boxes if b.get('class_name') in ['Short', 'Mouse_bite'])
        status_class = "danger" if status == "FAIL" else "success"
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Total Defects</div><div class='metric-value'>{len(boxes)}</div></div>", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Critical Anomalies</div><div class='metric-value danger'>{critical_count}</div></div>", unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Production Status</div><div class='metric-value {status_class}'>{status}</div></div>", unsafe_allow_html=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("### 🧠 Explainable AI (XAI) GradCAM Heatmap")
        st.markdown("<p style='color: #64748b;'>Visualizing the neural activation map to understand the AI's internal attention areas.</p>", unsafe_allow_html=True)
        st.markdown("<div class='image-container' style='max-width: 600px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.image(heatmap_rgb, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
        # PDF Generation
        report_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        create_pdf_report(image_np, overlay_rgb, boxes, report_path)
        
        st.markdown("<br>", unsafe_allow_html=True)
        with open(report_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Official QA Audit Report",
                data=pdf_file,
                file_name=f"InspectAid_QA_{serial_number}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
else:
    st.markdown('''
    <div style='text-align: center; padding: 100px 20px; background: rgba(21, 27, 41, 0.4); border-radius: 20px; border: 1px dashed #3a7bd5; margin-top: 20px;'>
        <h2 style='color: #94a3b8;'>System Ready for Inspection</h2>
        <p style='color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;'>Select a sample benchmark image from the sidebar or upload a fresh High-Resolution PCB scan to initiate the Automated Optical Inspection pipeline.</p>
    </div>
    ''', unsafe_allow_html=True)
