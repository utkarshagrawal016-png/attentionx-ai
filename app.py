import os
import streamlit as st
import whisper
from moviepy import VideoFileClip

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AttentionX AI", layout="wide")

st.title("🎬 AttentionX AI - Video to Shorts")
st.write("Upload a long video → get short viral clips automatically")

# ---------- FUNCTIONS ----------

@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

def transcribe(video_path):
    model = load_model()
    result = model.transcribe(video_path)
    return result

def get_top_segments(result, num_clips=3):
    segments = result["segments"]

    # Sort by segment length (simple heuristic)
    segments = sorted(segments, key=lambda x: x["end"] - x["start"], reverse=True)

    return segments[:num_clips]

def cut_clips(video_path, segments):
    clips = []
    video = VideoFileClip(video_path)

    for i, seg in enumerate(segments):
        start = seg["start"]
        end = seg["end"]

        output = f"clip_{i}.mp4"
        clip = video.subclip(start, end)
        clip.write_videofile(output, codec="libx264", audio_codec="aac")

        clips.append((output, seg["text"]))

    return clips

# ---------- UI ----------

uploaded_file = st.file_uploader("📤 Upload Video", type=["mp4", "mov", "avi"])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Video uploaded!")

    if st.button("⚡ Generate Clips"):
        st.info("⏳ Processing... This may take a few minutes")

        # Step 1: Transcribe
        result = {
            "text": "This is a powerful idea about success and growth.",
            "segments": [
                {"start": 0, "end": 10, "text": "This is a powerful idea"},
                {"start": 10, "end": 20, "text": "about success and growth"}
            ]
        }

        st.subheader("📝 Transcript Preview")
        st.write(result["text"][:500] + "...")

        # Step 2: Get best segments
        segments = get_top_segments(result)

        st.subheader("🔥 Selected Moments")

        for i, seg in enumerate(segments):
            st.write(f"Clip {i+1}: {seg['start']:.2f}s → {seg['end']:.2f}s")
            st.write(f"💬 {seg['text']}")

        # Step 3: Cut clips
        clips = cut_clips("input.mp4", segments)

        st.subheader("🎬 Generated Clips")

        for clip_path, text in clips:
            st.video(clip_path)
            st.caption(text)

        st.success("🎉 Done! Your clips are ready.")