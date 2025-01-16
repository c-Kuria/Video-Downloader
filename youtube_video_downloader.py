import os
import subprocess
import sys

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
        
        print("Available formats:")
        print(result.stdout)
    except Exception as e:
        print(f"An error occurred while fetching formats: {e}")
        sys.exit(1)

def download_video(video_url, format_code):
    try:
        # Define output path (current working directory)
        output_path = os.getcwd()
        print(f"Downloading video to: {output_path}")
        
        # Use yt-dlp to download and merge video and audio if needed
        subprocess.run([
            "yt-dlp",
            "-f", f"{format_code}+bestaudio/best",  # Merge video and best audio
            "--merge-output-format", "mp4",  # Ensure output is in MP4 format
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),  # Output file pattern
            video_url
        ])
        
        print("\nDownload completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_video_downloader.py <YouTube Video URL>")
    else:
        video_url = sys.argv[1]
        
        # Step 1: List available formats
        list_video_formats(video_url)
        
        # Step 2: Prompt the user to select a format
        format_code = input("Enter the format code of the desired quality: ")
        
        # Step 3: Download the video in the chosen format
        download_video(video_url, format_code)

