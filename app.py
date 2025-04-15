import streamlit as st
from PIL import Image
from gtts import gTTS
import tempfile
import os
from googletrans import Translator
from test import predict_step  # Ensure this function is correctly defined

# Streamlit UI
st.set_page_config(page_title="See & Say", layout="centered")
st.title("🖼️ See & Say : AI-Generated Image Captions + Audio")
st.write("Upload an image and let the AI describe it for you.")

# Upload image
uploaded_image = st.file_uploader("📤 Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Open image
    image = Image.open(uploaded_image)

    # Display image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate caption
    caption = predict_step(image)  # Call your caption prediction function

    # Display generated caption
    st.subheader("🗣️  Generated Caption:")
    st.text_area("Caption:", value=caption, height=100)


    # Inside your Streamlit block (after generating `caption`)
    st.subheader("🔊 Hear the Caption:")
    try:
        tts = gTTS(text=caption, lang='en')
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)  # Close the file so gTTS can write to it
        tts.save(path)  # Save audio to the path
    
        # Play audio in Streamlit
        st.audio(path, format="audio/mp3")

    except Exception as e:
        st.error(f"Error generating audio: {e}")


    
    # Step 3: Option to translate
    if st.button("🌐 Translate to Hindi"):
        try:
            translator = Translator()
            translated = translator.translate(caption, src='en', dest='hi')
            hindi_caption = translated.text

            # Show translated caption
            st.subheader("🌐 Caption (Hindi)")
            st.text_area("Translated Caption:", value=hindi_caption, height=100)

            # Replace audio with Hindi version
            tts_hi = gTTS(text=hindi_caption, lang='hi')
            fd_hi, path_hi = tempfile.mkstemp(suffix=".mp3")
            os.close(fd_hi)
            tts_hi.save(path_hi)
            st.subheader("🔊 Hear the Caption:")
            st.audio(path_hi, format="audio/mp3")

        except Exception as e:
            st.error(f"Error translating or generating Hindi audio: {e}")
else:
    st.info("Upload an image to begin.")
