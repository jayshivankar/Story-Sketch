import streamlit as st
import sys
import os
import io
import tempfile
from pydub import AudioSegment

# 📦 Internal Imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from llm.llm_prompts import generate_story, extract_scenes
from audio_translation import transcribe_audio, save_text
from image_audio_generator import generate_all_assets
from merge_videos import merge_all_scenes

# ✅ Streamlit WebRTC for recording audio
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np

# App Header
st.set_page_config(page_title="🎨 StorySketch", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎨 StorySketch</h1>", unsafe_allow_html=True)
st.caption("🚀 Speak or type your story — Let AI bring it to life!")
st.markdown("---")

# Step 1: Input
st.subheader("🎤 Voice or ✍️ Text Prompt")
col1, col2 = st.columns(2)

with col1:
    user_text = st.text_input("📝 Type your story idea", placeholder="A panda flies to space...")

# ---- WebRTC Audio Recorder ----
with col2:
    st.markdown("🎙️ Record your prompt below:")
    audio_frames = []

    class AudioProcessor:
        def __init__(self) -> None:
            self.frames = []

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            self.frames.append(frame)
            return frame

    ctx = webrtc_streamer(
        key="audio",
        mode=WebRtcMode.SENDRECV,
        in_audio=True,
        video_processor_factory=None,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"video": False, "audio": True},
        async_processing=True,
    )

    wav_bytes = None
    if ctx.audio_processor:
        if st.button("✅ Done Recording"):
            with st.spinner("🔄 Processing audio..."):
                # Combine and convert to WAV
                audio = b"".join([f.to_ndarray().tobytes() for f in ctx.audio_processor.frames])
                sample_rate = ctx.audio_processor.frames[0].sample_rate
                channels = ctx.audio_processor.frames[0].layout.channels
                sample_width = 2  # 16-bit audio

                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                audio_segment = AudioSegment(
                    data=audio, sample_width=sample_width, frame_rate=sample_rate, channels=channels
                )
                audio_segment.export(temp_file.name, format="wav")
                wav_bytes = open(temp_file.name, "rb").read()
                st.success("🎧 Audio saved!")

# -------------- Transcribe --------------
final_prompt = None
transcript = None

if wav_bytes:
    st.audio(wav_bytes, format="audio/wav")
    with st.spinner("🧠 Transcribing..."):
        transcript = transcribe_audio(wav_bytes)
        st.success("📝 Transcription complete!")
        st.markdown(f"**Transcript:** `{transcript}`")
        final_prompt = transcript
        save_text("data/transcripts", transcript, "transcript")

elif user_text.strip():
    final_prompt = user_text.strip()

# -------------- Generate ----------------
st.markdown("---")

if final_prompt:
    if st.button("✨ Generate Story & Video"):
        with st.spinner("🧠 Generating story..."):
            story = generate_story(final_prompt)
            st.success("📖 Story generated!")
            st.markdown("### 📚 Story:")
            st.markdown(story)

        with st.spinner("🎨 Extracting scene prompts..."):
            scenes = extract_scenes(story)
            st.success(f"📸 Extracted {len(scenes)} scenes!")

        with st.spinner("🎨 Generating images and audio..."):
            generate_all_assets(scenes)

        with st.spinner("🎬 Merging scene videos..."):
            output_path = "final_story_video.mp4"
            merge_all_scenes(output_path)

        st.success("✅ Final video is ready!")
        st.video(output_path)
else:
    st.info("💡 Please enter text or record audio to start.")

