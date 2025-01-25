import os
import subprocess
import sys
from tqdm import tqdm  # Import tqdm for progress bar


def list_video_formats(video_url):
    try:
        # Use yt-dlp to list available formats
        result = subprocess.run([
            "yt-dlp",
            "-F",  # List all available formats
            video_url
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        print("\nAvailable formats:\n")
        print(result.stdout)
    except Exception as e:
        print(f"An error occurred while fetching formats: {e}")
        sys.exit(1)


def download_video(video_url, format_code):
    try:
        # Define output path (current working directory)
        output_path = os.getcwd()
        print(f"\nDownloading video to: {output_path}\n")
        
        # Use yt-dlp to download and merge video and audio if needed
        command = [
            "yt-dlp",
            "-f", format_code,  # Use the chosen format code
            "--merge-output-format", "mp4",  # Ensure output is in MP4 format
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),  # Output file pattern
            video_url
        ]
        
        # Run the yt-dlp command
        result = subprocess.run(command, text=True)
        if result.returncode == 0:
            print("\nDownload completed successfully!")
            return True  # Indicate that the video was downloaded successfully
        else:
            print("\nAn error occurred during the download process.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def merge_audio_with_video(video_file, video_url):
    # Check if the user wants to download and merge audio
    while True:
        choice = input("Do you want to download and merge the audio with the downloaded video? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            # Call the audio merger function
            output_folder = "output formats"
            create_output_folder(output_folder)  # Ensure the output folder exists

            # Extract the base name of the video file (without extension)
            base_name = os.path.splitext(os.path.basename(video_file))[0]
            audio_filename = os.path.join(output_folder, f"{base_name}_audio.m4a")  # Use the base name for audio file
            audio_file = download_audio(video_url, output_folder, audio_filename)

            # Merge video and audio
            output_file = os.path.join(output_folder, f"{base_name}_merged_output.mp4")  # Use the base name for merged file
            merge_audio_video(video_file, audio_file, output_file)
            print(f"Final merged file: {output_file}")
            break
        elif choice in ['no', 'n']:
            print("Audio merging skipped.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def create_output_folder(folder_name):
    """Create the output folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # Create the folder if it doesn't exist
        print(f"Created output folder: {folder_name}")
    else:
        print(f"Output folder already exists: {folder_name}")


def download_audio(video_url, output_folder, audio_filename):
    try:
        # Define the output path for the audio
        audio_output = os.path.join(output_folder, audio_filename)

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
    if len(sys.argv) < 2:
        print("Usage: python video_downloader.py <Video URL>")
        print("Supports YouTube, Vimeo, TikTok, Facebook, Instagram, Twitter, and more!")
    else:
        video_url = sys.argv[1]
        
        # Step 1: List available formats
        print("Fetching available formats... This might take a moment.")
        list_video_formats(video_url)
        
        # Step 2: Prompt the user to select a format
        while True:
            format_code = input("Enter the format code/ID of the desired quality: ").strip()
            if format_code:
                break
            print("Invalid input. Please enter a valid format code.")
        
        # Step 3: Download the video in the chosen format
        video_downloaded = download_video(video_url, format_code)
        
        if video_downloaded:
            # Get the downloaded video file name
            video_file = os.path.join(os.getcwd(), f"{video_url.split('=')[-1]}.mp4")  # Adjust this based on your output pattern
            merge_audio_with_video(video_file, video_url)
        
        print("\nThank you for using this multi-platform downloader! For supported sites, run 'yt-dlp --list-extractors'.")
