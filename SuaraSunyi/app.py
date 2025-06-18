import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import datetime

from utils.transcribe import transcribe_audio
from utils.emotion import detect_emotion
from style import STYLE

# Setup folder
os.makedirs("diary/audio_logs", exist_ok=True)

# Page config
st.set_page_config(page_title="SuaraSunyi", page_icon="🕊️", layout="centered")
st.markdown(STYLE, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🕊️ SuaraSunyi</h1>", unsafe_allow_html=True)
st.caption("Tempat aman untuk menyuarakan isi hati. Biarkan AI mendengarkan dan memahami perasaanmu.")

# Rekaman
fs = 44100
duration = st.slider("🎙️ Pilih durasi rekaman (detik)", 5, 60, 10)

if st.button("🔴 Mulai Rekaman"):
    with st.spinner("Merekam..."):
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

    if np.abs(recording).sum() < 100:
        st.warning("⚠️ Tidak ada suara terekam. Coba ulangi rekaman.")
    else:
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        audio_path = f"diary/audio_logs/audio_{now}.wav"
        write(audio_path, fs, recording)

        # Transkripsi
        transcript = transcribe_audio(audio_path)
        st.subheader("Transkripsi:")
        st.markdown(f"<div class='transcript-box'>{transcript}</div>", unsafe_allow_html=True)

        # Deteksi emosi
        emotion = detect_emotion(transcript)

        # Kata penguat
        affirmations = {
            "marah": "❤️ Tarik napas, lepas perlahan. Emosi itu valid, tapi kamu bisa mengendalikannya.",
            "takut": "🤍 Kamu tidak sendiri. Rasa takut itu manusiawi. Kamu cukup, kamu aman.",
            "sedih": "💛 Tidak apa-apa merasa sedih. Kamu sudah kuat sampai sejauh ini.",
            "senang": "💚 Senang melihatmu bahagia! Nikmati setiap momennya 😊",
            "netral": "🩶 Hari ini mungkin biasa saja, tapi kamu tetap luar biasa.",
            "terkejut": "🧡 Hal-hal mengejutkan kadang datang tiba-tiba. Tapi kamu bisa menghadapinya.",
            "jijik": "🩷 Rasa tidak nyaman itu bisa muncul, tapi kamu tetap layak didengar.",
            "cemas": "💙 Rasa cemas itu nyata. Ingat, kamu tidak sendiri. Pelan-pelan, ya."
        }
        affirmation_text = affirmations.get(emotion.lower(), "Kamu hebat sudah berbagi hari ini 🤗")

        # Gabungan emosi + kata penguat
        st.markdown(f"""
        <div class='emotion-card'>
            <h4>🎭 Emosi Terdeteksi:</h4>
            <p style='font-size:1.2rem; font-weight:bold'>{emotion}</p>
            <h4>🗣️ Kata Penguat:</h4>
            <p>{affirmation_text}</p>
        </div>
        """, unsafe_allow_html=True)

        with open(audio_path, "rb") as f:
            st.markdown("<div style='text-align: center; margin-top: 1.5rem;'>", unsafe_allow_html=True)
            st.download_button(
                label="Unduh Rekaman",
                data=f,
                file_name=os.path.basename(audio_path),
                mime="audio/wav",
                help="Klik untuk menyimpan rekamanmu"
            )
            st.markdown("</div>", unsafe_allow_html=True)

