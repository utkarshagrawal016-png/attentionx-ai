import streamlit as st
from moviepy.editor import VideoFileClip

st.set_page_config(page_title="AttentionX AI", layout="wide")

st.title("🎬 AttentionX AI - Video to Shorts")
st.write("Upload a video → get short clips instantly")

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded!")

    if st.button("Generate Clips"):

        st.info("Processing...")

        # 🔥 FAKE AI OUTPUT (instant)
        segments = [
            {"start": 0, "end": 5, "text": "This is a powerful idea"},
            {"start": 5, "end": 10, "text": "that can change your mindset"}
        ]

        st.subheader("🔥 Selected Moments")
        for i, seg in enumerate(segments):
            st.write(f"Clip {i+1}: {seg['start']}s → {seg['end']}s")
            st.write(seg["text"])

        video = VideoFileClip("input.mp4")

        st.subheader("🎬 Generated Clips")

        for i, seg in enumerate(segments):
            output = f"clip_{i}.mp4"
            clip = video.subclip(seg["start"], seg["end"])
            clip.write_videofile(output, codec="libx264", audio_codec="aac")

            st.video(output)
            st.caption(seg["text"])

        st.success("Done!")