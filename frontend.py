import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="🛡️",
    layout="wide",
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 25%,
        #1e293b 50%,
        #111827 75%,
        #020617 100%
    );
    color: white;
}

/* Main Title */
.main-title {
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-bottom: 40px;
}

/* Glassmorphism Card */
.glass-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(14px);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Text Area */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    padding: 18px !important;
    font-size: 16px !important;
}

/* Button */
div.stButton > button {
    width: 100%;
    height: 60px;
    border: none;
    border-radius: 18px;
    background: linear-gradient(90deg, #06b6d4, #6366f1, #8b5cf6);
    color: white;
    font-size: 20px;
    font-weight: 600;
    transition: 0.3s ease-in-out;
    box-shadow: 0 4px 20px rgba(99,102,241,0.5);
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 30px rgba(139,92,246,0.7);
}

/* Result Cards */
.result-real {
    background: linear-gradient(135deg, #10b981, #059669);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 24px;
    font-weight: 600;
    margin-top: 25px;
    box-shadow: 0 8px 25px rgba(16,185,129,0.4);
}

.result-fake {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 24px;
    font-weight: 600;
    margin-top: 25px;
    box-shadow: 0 8px 25px rgba(239,68,68,0.4);
}

/* Confidence Box */
.conf-box {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    margin-top: 20px;
    text-align: center;
    color: #f8fafc;
    font-size: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    color: #94a3b8;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================

st.markdown(
    """
    <div class="main-title">
        🛡️ AI Fake News Detector
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Detect misinformation instantly using Artificial Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# MAIN CARD
# =========================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.subheader("📰 Paste News Article")

news_text = st.text_area(
    "",
    height=250,
    placeholder="Paste your news article here..."
)

# =========================
# BUTTON
# =========================

predict = st.button("🚀 Analyze News")

# =========================
# PREDICTION
# =========================

if predict:

    if news_text.strip() == "":
        st.warning("⚠️ Please enter some text.")

    else:

        with st.spinner("Analyzing article with AI..."):

            try:
                url = "http://127.0.0.1:5000/predict"

                payload = {
                    "text": news_text
                }

                response = requests.post(url, json=payload)

                result = response.json()

                if "error" in result:
                    st.error(result["error"])

                else:

                    prediction = result["result"]
                    confidence = result["confidence"]

                    # REAL NEWS
                    if prediction == "Real":

                        st.markdown(
                            f"""
                            <div class="result-real">
                                ✅ REAL NEWS
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # FAKE NEWS
                    else:

                        st.markdown(
                            f"""
                            <div class="result-fake">
                                ❌ FAKE NEWS
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # Confidence
                    st.markdown(
                        f"""
                        <div class="conf-box">
                            🎯 Confidence Score: <b>{confidence}%</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Progress Bar
                    st.progress(float(confidence) / 100)

            except Exception as e:
                st.error(f"Server Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">
        Built with ❤️ using Streamlit + Flask + Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)