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
        else:
            print("\nAn error occurred during the download process.")
    except Exception as e:
        print(f"An error occurred: {e}")
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
            format_code = input("Enter the format code of the desired quality: ").strip()
            if format_code:
                break
            print("Invalid input. Please enter a valid format code.")
        
        # Step 3: Download the video in the chosen format
        download_video(video_url, format_code)
        
        print("\nThank you for using this multi-platform downloader! For supported sites, run 'yt-dlp --list-extractors'.")
