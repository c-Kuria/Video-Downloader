# YouTube Video Downloader and Audio Merger

A simple terminal-based Python application for downloading YouTube videos and audio. This tool uses `yt-dlp` to list available formats, download videos or audio separately, and even merge pre-downloaded video files with audio streams seamlessly using `FFmpeg`.

---

## Features:
- Lists all available video and audio formats for selection.
- Downloads videos in the highest quality with audio.
- Option to download audio separately and merge with an existing video file.
- Automatically merges video and audio into a single MP4 file.
- Lightweight and easy to use directly from the terminal.

---

## Requirements:
- Python 3.x
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Install via `pip install yt-dlp`)
- [FFmpeg](https://ffmpeg.org) (Required for merging video and audio)

---

## Usage:

### 1. Download a Video with Audio:
Run the `youtube_video_downloader.py` script to download videos in your desired quality:

```bash
python youtube_video_downloader.py <YouTube Video URL>
```

- The script will list all available formats.
- Enter the format code to download the video with the best audio merged automatically.

---

### 2. Merge Pre-Downloaded Video with Audio:
If you have already downloaded a video (without audio) and want to merge it with the audio stream:

1. Use the `audio_video_merger.py` script:

```bash
python audio_video_merger.py <Video File Path> <YouTube Video URL>
```

- Replace `<Video File Path>` with the path to your pre-downloaded video file.
- Replace `<YouTube Video URL>` with the URL of the YouTube video to extract the audio.

2. The script will:
   - Download the best available audio stream.
   - Merge the audio with the video into a single file (`merged_output.mp4`).

---

## Example Scenarios:

### Scenario 1: Download Full Video with Audio
- Use `youtube_video_downloader.py` to download a complete video file with merged audio.

### Scenario 2: Merge Existing Video and Audio
- If you already have a video file without audio, use `audio_video_merger.py` to merge it with the audio stream.

---

## Contributing:
Feel free to contribute by reporting issues, suggesting new features, or submitting pull requests to make this tool even better!

---
