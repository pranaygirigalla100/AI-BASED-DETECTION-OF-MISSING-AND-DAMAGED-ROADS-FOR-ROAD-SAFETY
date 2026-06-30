import io
import os
import shutil
import tempfile
from PIL import Image
import streamlit as st
from ultralytics import YOLO

st.set_page_config(
    page_title="Road Damage AI",
    page_icon="🛣️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0d0f14 !important;
    color: #e2e8f0;
}
.hero-wrap {
    background: linear-gradient(135deg, #0d0f14 0%, #111827 60%, #0d0f14 100%);
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 2.4rem 2rem 1.8rem 2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f97316, #ef4444, #f97316);
}
.hero-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #f97316;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    letter-spacing: 0.06em;
    line-height: 1;
    color: #f1f5f9;
    margin: 0 0 0.6rem 0;
}
.hero-title span { color: #f97316; }
.hero-sub {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 300;
    font-size: 0.9rem;
    color: #94a3b8;
    max-width: 520px;
}
.badge-row { display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }
.badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    padding: 0.22rem 0.65rem;
    border-radius: 4px;
    letter-spacing: 0.1em;
    font-weight: 600;
    text-transform: uppercase;
}
.badge-orange { background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3); }
.badge-red    { background: rgba(239,68,68,0.12);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }
.badge-blue   { background: rgba(59,130,246,0.12); color: #60a5fa; border: 1px solid rgba(59,130,246,0.25); }
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    margin-top: 1.4rem;
}
[data-testid="stFileUploader"] {
    border: 1.5px dashed #1e3a5f !important;
    border-radius: 10px !important;
    background: #0f1520 !important;
    padding: 0.6rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover { border-color: #f97316 !important; }
[data-testid="stFileUploader"] label { color: #94a3b8 !important; }
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ea580c, #dc2626) !important;
    color: #fff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.65rem 2.4rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 18px rgba(234,88,12,0.35) !important;
}
[data-testid="stButton"] > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
[data-testid="stButton"] > button:active { transform: translateY(0px) !important; }
.result-box {
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
}
.result-detected { background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.3); color: #86efac; }
.result-clean    { background: rgba(234,179,8,0.08);  border: 1px solid rgba(234,179,8,0.28); color: #fde047; }
.result-error    { background: rgba(239,68,68,0.08);  border: 1px solid rgba(239,68,68,0.28); color: #f87171; }
.detection-item {
    display: inline-block;
    margin: 0.25rem 0.3rem 0.25rem 0;
    padding: 0.2rem 0.7rem;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.det-crack   { background: rgba(249,115,22,0.2); color: #fb923c; border: 1px solid rgba(249,115,22,0.4); }
.det-pothole { background: rgba(239,68,68,0.2);  color: #f87171; border: 1px solid rgba(239,68,68,0.4); }
.divider { border: none; border-top: 1px solid #1e2a3a; margin: 1.5rem 0; }
[data-testid="stImage"] img { border-radius: 8px !important; border: 1px solid #1e2a3a !important; }
[data-testid="stExpander"] { border: 1px solid #1e2a3a !important; border-radius: 8px !important; background: #0f1520 !important; }
header[data-testid="stHeader"], footer { display: none !important; }
[data-testid="stSpinner"] p { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-wrap">
<div class="hero-tag">⚠ Computer Vision · YOLOv8 · Road Safety</div>
<h1 class="hero-title">AI-BASED DETECTION<br>OF <span>DAMAGED</span> &amp;<br>MISSING <span>ROAD</span></h1>
<p class="hero-sub">
    Upload a road photo to instantly detect potholes and cracks
    using a trained YOLOv8 model. Built for road-safety monitoring.
</p>
<div class="badge-row">
    <span class="badge badge-orange">Potholes</span>
    <span class="badge badge-red">Cracks</span>
    <span class="badge badge-blue">YOLOv8 · Real-time</span>
</div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading AI model…")
def load_model():
    MODEL_PATH = "model.pt"
    return YOLO(MODEL_PATH)

try:
    model = load_model()
    model_ok = True
except Exception as e:
    st.markdown(f'<div class="result-box result-error">⚠ Failed to load model: {e}</div>', unsafe_allow_html=True)
    model_ok = False

st.markdown('<div class="section-label">Step 1 — Upload Road Image (JPG · 200–300 KB)</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Drag & drop or browse",
    type=["jpg", "jpeg"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    if file_size_kb < 200 or file_size_kb > 300:
        st.warning(f"Note: Uploaded image size is {file_size_kb:.1f} KB. Your recommended range is 200–300 KB.")

    image = Image.open(uploaded_file).convert("RGB")
    st.markdown('<div class="section-label">Uploaded Image</div>', unsafe_allow_html=True)
    st.image(image, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Step 2 — Run Detection</div>', unsafe_allow_html=True)

    predict_btn = st.button("🔍  Predict Road Damage", disabled=not model_ok)

    if predict_btn:
        with st.spinner("Analyzing image…"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp_path = tmp.name
                image.save(tmp_path, format="JPEG")

            try:
                results = model(tmp_path, conf=0.25)
                boxes = results[0].boxes

                if boxes is not None and len(boxes) > 0:
                    detected = []
                    for box in boxes:
                        cid = int(box.cls[0])
                        name = model.names[cid]
                        conf = float(box.conf[0])
                        detected.append((name, conf))

                    # ── FIXED: use .plot() instead of .save(dir=...) ──
                    annotated = Image.fromarray(results[0].plot())

                    tags_html = ""
                    for name, conf in detected:
                        css_cls = "det-pothole" if name.lower() == "potholes" else "det-crack"
                        tags_html += f'<span class="detection-item {css_cls}">{name} {conf:.0%}</span>'

                    st.markdown(
                        f'<div class="result-box result-detected">'
                        f'✅ &nbsp;<strong>Damage Detected!</strong><br><br>{tags_html}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown('<div class="section-label" style="margin-top:1rem">Detection Result (with bounding boxes)</div>', unsafe_allow_html=True)
                    st.image(annotated, use_container_width=True)

                    buf = io.BytesIO()
                    annotated.save(buf, format="JPEG", quality=95)
                    st.download_button(
                        label="⬇ Download annotated image",
                        data=buf.getvalue(),
                        file_name=f"predicted_{uploaded_file.name}",
                        mime="image/jpeg",
                    )

                else:
                    not_predicted_dir = "Not_Predicted"
                    os.makedirs(not_predicted_dir, exist_ok=True)
                    dest = os.path.join(not_predicted_dir, uploaded_file.name)

                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy(tmp_path, dest)

                    st.markdown(
                        f'<div class="result-box result-clean">'
                        f'ℹ️ &nbsp;<strong>No road damage detected.</strong><br><br>'
                        f'<span style="color:#94a3b8">Image saved → <code style="color:#fde047">{dest}</code></span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.markdown(
                    f'<div class="result-box result-error">❌ Prediction error: {e}</div>',
                    unsafe_allow_html=True,
                )
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)