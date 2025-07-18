# 🎨 StorySketch

**StorySketch** is an AI-powered storytelling app that transforms a child’s voice or text idea into a complete animated story — with magical visuals, voice narration, and a final video.

---

## ✨ Features

- 🎙️ Voice input using Whisper (Groq)
- ✍️ Text input with smart prompt detection
- 🤖 Story generation via LangChain + LLaMA (Groq)
- 🎬 Scene extraction for visual storytelling
- 🖼️ Image generation with Flux  (`flux-dev`)
- 🔊 Audio narration using gTTS
- 🎞️ Scene videos & final video creation using MoviePy
- 🌐 Interactive UI using Streamlit

---

## 🚀 How It Works

1. **User Input** — Speak or type a story idea.
2. **Transcription** — If using voice, it's transcribed using Whisper (Groq).
3. **Story Generation** — A child-friendly story is generated using LLaMA via LangChain.
4. **Scene Extraction** — The story is broken into vivid, image-ready sentences.
5. **Image Generation** — Each scene is turned into an image using Replicate or Hugging Face models (e.g., Flux).
6. **Audio Narration** — Each scene is narrated using Google TTS (gTTS).
7. **Video Creation** — Image + audio merged into short clips and then combined into a single video.
8. **Playback** — Streamlit displays the story and final video in-browser.

---

## 🧠 Tech Stack

| Component     | Tool/Library                        |
|---------------|-------------------------------------|
| LLM           | Groq + LangChain (LLaMA)            |
| TTS           | gTTS (Google Text-to-Speech)        |
| Image Gen     | Replicate (`flux-dev`)              |
| Audio         | `audiorecorder` + Whisper (Groq)    |
| Video         | `MoviePy`                           |
| UI            | `Streamlit`                         |
| API (optional)| `FastAPI` for Whisper transcription |

---

## 📁 Folder Structure

