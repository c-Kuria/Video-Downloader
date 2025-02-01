# Video Downloader and Audio Merger

A simple terminal-based Python application for downloading YouTube videos and audio. This tool uses `yt-dlp` to list available formats, download videos or audio separately, and even merge pre-downloaded video files with audio streams seamlessly using `FFmpeg`.

---

## Features:
✅ **Multi-platform Support** - Download from 1000+ sites (YouTube, Vimeo, Dailymotion, TikTok, Facebook, etc.)  
✅ **Smart Quality Selection** - Automatically downloads highest quality video with audio  
✅ **Auto Merge Capability** - Combines video+audio streams when needed (MP4/MKV)  
✅ **Batch Processing** - Download multiple URLs simultaneously from file input  
✅ **Advanced Features**:
   - Progress tracking with real-time statistics  
   - Automatic subtitle downloads (.srt/.vtt)  
   - Metadata embedding (title, artist, thumbnail)  
   - Download history tracking (JSON format)  
   - Proxy/VPN support for restricted content  
   - Bandwidth throttling controls  
   - Custom filename templates (e.g. `{title}-{uploader}.mp4`)  
   - Multiple output formats (MP4, MKV, MP3)  
   - Comprehensive error handling with retries  

---

## Supported Platforms
This downloader supports **1000+ websites** through yt-dlp's extraction network including:

- YouTube (videos/shorts/playlists)  
- Vimeo  
- TikTok  
- Facebook  
- Instagram  
- Twitter/X  
- Dailymotion  
- SoundCloud  
- Twitch  
- Bilibili  
- Niconico  

For complete list of supported sites, run:
```bash
yt-dlp --list-extractors
```

## Requirements & Installation:

- Python 3.8+

## Dependencies

```
pip install -r requirements.txt
```

## Basic Usage

### Single URL download
```
python downloader.py "URL" -f mp4 --metadata
```

### Batch download from file
```
python downloader.py -b urls.txt -o "%(title)s - %(uploader)s.%(ext)s"
```

### Download as MP3 with metadata
```
python downloader.py "URL" -f mp3
```

### Download with subtitles and proxy
```
python downloader.py "URL" -s -p socks5://localhost:1080
```

### Download with subtitles and metadata
```
python downloader.py "URL" -s -m
```

### Throttle download speed (1MB/s)
```
python downloader.py "URL" -l 1024
```

### Use proxy and speed limiting
```
python downloader.py "URL" -p socks5://proxy:port -l 1024
```

---

## Merge Pre-Downloaded Video with Audio:
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
