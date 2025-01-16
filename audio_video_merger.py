import os
import subprocess
import sys

def download_audio(video_url, output_filename):
    try:
        # Define output path (current working directory)
        output_path = os.getcwd()
        audio_output = os.path.join(output_path, "audio.m4a")

        print(f"Downloading audio to: {audio_output}")

        # Use yt-dlp to download the best audio
        subprocess.run([
            "yt-dlp",
            "-f", "bestaudio",  # Best available audio
            "-o", audio_output,  # Save as audio.m4a
            video_url
        ])

        print("Audio download completed successfully!")
        return audio_output
    except Exception as e:
        print(f"An error occurred while downloading audio: {e}")
        sys.exit(1)

def merge_audio_video(video_file, audio_file, output_file):
    try:
        print(f"Merging video ({video_file}) and audio ({audio_file}) into {output_file}...")

        # Use ffmpeg to merge video and audio
        subprocess.run([
            "ffmpeg",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_file,
            "-y"  # Overwrite if the file exists
        ])

        print("Merging completed successfully!")
    except Exception as e:
        print(f"An error occurred while merging: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python audio_video_merger.py <Video File Path> <YouTube Video URL>")
    else:
        video_file = sys.argv[1]
        video_url = sys.argv[2]

        # Step 1: Download the audio
        audio_file = download_audio(video_url, "audio.m4a")

        # Step 2: Merge video and audio
        output_file = "merged_output.mp4"
        merge_audio_video(video_file, audio_file, output_file)

        print(f"Final merged file: {output_file}")

