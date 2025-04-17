import streamlit as st
from PIL import Image
from test import predict_step
from gtts import gTTS
from googletrans import Translator
import os
import tempfile
import time

# ---------- Custom CSS for Polished Look ----------
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to right, #f8fff6, #e6f7ff);
            font-family: 'Segoe UI', sans-serif;
        }
        .title-container {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .title-text {
            font-size: 2.2rem;
            font-weight: 700;
            color: #30475e;
        }
        .logo {
            width: 70px;
        }
        .stTextArea, .stFileUploader {
            border-radius: 12px !important;
        }
        .stAudio {
            background-color: #fff;
            border-radius: 10px;
        }
        .section-title {
            font-size: 1.5rem;
            margin-top: 2rem;
            font-weight: 600;
            color: #1a3c40;
        }
        .caption-box {
            background-color: #ffffff;
            padding: 1.2rem;
            margin-top: 1rem;
            margin-bottom: 2rem;
            border-left: 5px solid #45a049;
            border-radius: 15px;
            font-size: 1.2rem;
            font-weight: 500;
            color: #333333;
            box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        }
        .stFileUploader {
            background-color: #ffffff;
            padding: 0.75rem;
            border: 2px dashed #4CAF50;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- App Title ----------
st.markdown("""
    <div class="title-container">
        <img src="https://cdn-icons-png.flaticon.com/512/3275/3275561.png" class="logo">
        <div class="title-text">See & Say : AI-Generated Image Captions + Audio</div>
    </div>
""", unsafe_allow_html=True)

# ---------- Main Container ----------
with st.container():
    st.write("🎯 Upload an image to generate a smart AI caption. You can translate it and listen in your language too!")

    uploaded_image = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

        with st.spinner("⏳ Generating caption..."):
            time.sleep(1)
            caption = predict_step(image)

        st.markdown(f"<div class='section-title'>📝 Caption in English</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='caption-box'>{caption}</div>", unsafe_allow_html=True)

        # ---------- English TTS ----------
        if st.button("🔊 Hear Caption in English"):
            tts_en = gTTS(text=caption, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts_en.save(f.name)
                st.audio(f.name, format="audio/mp3")

        # ---------- Language Selection ----------
        indian_languages = {
            'Hindi': 'hi', 'Marathi': 'mr', 'Tamil': 'ta', 'Telugu': 'te',
            'Kannada': 'kn', 'Malayalam': 'ml', 'Gujarati': 'gu', 'Bengali': 'bn',
            'Punjabi': 'pa'
        }

        st.markdown(f"<div class='section-title'>🌐 Translate Caption</div>", unsafe_allow_html=True)
        selected_lang = st.selectbox("Choose your language", list(indian_languages.keys()))

        if st.button("🌍 Translate & Hear"):
            try:
                lang_code = indian_languages[selected_lang]
                translator = Translator()
                translated_text = translator.translate(caption, dest=lang_code).text

                st.markdown(f"<div class='caption-box'>{translated_text}</div>", unsafe_allow_html=True)

                tts_translated = gTTS(text=translated_text, lang=lang_code)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts_translated.save(f.name)
                    st.audio(f.name, format="audio/mp3")
            except Exception as e:
                st.error(f"Translation or TTS failed: {e}")

# ---------- Feedback ----------
st.markdown("""
<div class="card">
    <div class="section-title">📣 Feedback</div>
""", unsafe_allow_html=True)

feedback = st.radio("Was the caption helpful?", ("👍 Yes", "👎 No"))
if feedback:
    st.success("Thank you for your feedback!")

st.markdown("</div>", unsafe_allow_html=True)
