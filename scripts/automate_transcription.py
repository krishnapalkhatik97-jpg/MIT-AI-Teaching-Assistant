import os
import subprocess

VIDEO_FOLDER = "videos"
OUTPUT_FOLDER = "transcripts"

for file in os.listdir(VIDEO_FOLDER):

    if file.endswith(".mp4"):

        video_path = os.path.join(VIDEO_FOLDER, file)

        transcript_name = os.path.splitext(file)[0] + ".txt"
        transcript_path = os.path.join(OUTPUT_FOLDER, transcript_name)

        if os.path.exists(transcript_path):
            print(f"✅ Skipping {file} (already transcribed)")
            continue

        print(f"\n🎙️ Processing: {file}")

        subprocess.run([
            "whisper",
            video_path,
            "--model", "base",
            "--language", "English",
            "--output_dir", OUTPUT_FOLDER
        ])

print("\n🎉 All lectures have been processed!")