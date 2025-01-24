import os
import subprocess
import sys
from tqdm import tqdm  # Import tqdm for progress bar

def create_output_folder(folder_name):
    """Create the output folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # Create the folder if it doesn't exist
        print(f"Created output folder: {folder_name}")
    else:
        print(f"Output folder already exists: {folder_name}")

def download_audio(video_url, output_folder):
    try:
        # Define the output path for the audio
        audio_output = os.path.join(output_folder, "audio.m4a")

        print(f"Downloading audio to: {audio_output}")

        # Use yt-dlp to download the best audio
        subprocess.run([
            "yt-dlp",
            "-f", "bestaudio",  # Best available audio
            "-o", audio_output,  # Save as specified audio file
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

        # Use ffprobe to get the total duration of the video for progress tracking
        result = subprocess.run([
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_file
        ], capture_output=True, text=True)

        total_duration = float(result.stdout.strip()) if result.returncode == 0 else 0

        # Use ffmpeg to merge video and audio with a progress bar
        process = subprocess.Popen([
            "ffmpeg",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_file,
            "-y"  # Overwrite if the file exists
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Monitor the output for progress
        with tqdm(total=total_duration, unit='s', desc='Merging Progress') as pbar:
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # Extract the time from ffmpeg output
                    if 'time=' in output:
                        time_str = output.split('time=')[1].split(' ')[0]
                        time_parts = time_str.split(':')
                        if len(time_parts) == 3:  # HH:MM:SS
                            current_time = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + float(time_parts[2])
                        elif len(time_parts) == 2:  # MM:SS
                            current_time = int(time_parts[0]) * 60 + float(time_parts[1])
                        else:
                            current_time = 0
                        pbar.update(current_time - pbar.n)

        process.wait()  # Wait for the process to finish
        print("Merging completed successfully!")
    except Exception as e:
        print(f"An error occurred while merging: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Define the output folder name
    output_folder = "output formats"
    create_output_folder(output_folder)  # Create the output folder

    if len(sys.argv) < 3:
        print("Usage: python audio_video_merger.py <Video File Path> <YouTube Video URL>")
    else:
        video_file = sys.argv[1]
        video_url = sys.argv[2]

        # Step 1: Download the audio
        audio_file = download_audio(video_url, output_folder)

        # Step 2: Merge video and audio
        output_file = os.path.join(output_folder, "merged_output.mp4")  # Save merged file in the same folder
        merge_audio_video(video_file, audio_file, output_file)

        print(f"Final merged file: {output_file}")

