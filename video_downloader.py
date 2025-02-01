#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import json
from datetime import datetime
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

HISTORY_FILE = 'download_history.json'

class VideoDownloader:
    def __init__(self, config):
        self.config = config
        self.history = self._load_history()

    def _load_history(self):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_history(self, entry):
        self.history.append(entry)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            logger.info(f"Progress: {progress} @ {speed} | ETA: {eta}")
        elif d['status'] == 'finished':
            logger.info("Download completed, post-processing...")

    def _get_ydl_options(self):
        return {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': self.config['output_template'],
            'merge_output_format': self.config['format'],
            'writethumbnail': self.config['embed_metadata'],
            'writeautomaticsub': self.config['subtitles'],
            'writesubtitles': self.config['subtitles'],
            'subtitleslangs': ['all'] if self.config['subtitles'] else [],
            'postprocessors': [
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                },
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegEmbedSubtitle'},
            ] if self.config['embed_metadata'] else [],
            'ratelimit': self.config['speed_limit'] * 1024 if self.config['speed_limit'] else None,
            'proxy': self.config['proxy'],
            'logger': logger,
            'progress_hooks': [self._progress_hook],
            'noplaylist': True,
            'restrictfilenames': True,
        }

    def download(self, url):
        entry = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'status': 'failed',
            'output': None
        }

        try:
            with YoutubeDL(self._get_ydl_options()) as ydl:
                info = ydl.extract_info(url, download=True)
                entry['status'] = 'success'
                entry['output'] = ydl.prepare_filename(info)
                entry['title'] = info.get('title', '')
                entry['duration'] = info.get('duration', 0)
                
                logger.info(f"Successfully downloaded: {entry['output']}")
                self._save_history(entry)
                return True

        except DownloadError as e:
            logger.error(f"Download failed for {url}: {str(e)}")
            self._save_history(entry)
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            self._save_history(entry)
            return False

def list_video_formats():
    return ['mp4', 'mkv', 'mp3']  # Example formats

def main():
    parser = argparse.ArgumentParser(description='Universal Media Downloader')
    parser.add_argument('urls', nargs='*', help='URL(s) to download')
    parser.add_argument('-b', '--batch', help='File containing list of URLs')
    parser.add_argument('-f', '--format', choices=['mp4', 'mkv', 'mp3'], default='mp4',
                      help='Output format (default: mp4)')
    parser.add_argument('-o', '--output-template', default='%(title)s.%(ext)s',
                      help='Output filename template')
    parser.add_argument('-s', '--subtitles', action='store_true',
                      help='Download subtitles')
    parser.add_argument('-m', '--embed-metadata', action='store_true',
                      help='Embed metadata and thumbnail')
    parser.add_argument('-p', '--proxy',
                      help='Use proxy (e.g., socks5://user:pass@host:port)')
    parser.add_argument('-l', '--speed-limit', type=int,
                      help='Speed limit in KB/s')
    parser.add_argument('-r', '--retries', type=int, default=3,
                      help='Number of retries for failed downloads')

    args = parser.parse_args()

    # Collect URLs
    urls = args.urls
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                urls += [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"Batch file {args.batch} not found")
            sys.exit(1)

    if not urls:
        logger.error("No URLs provided")
        sys.exit(1)

    # Configure downloader
    config = {
        'format': args.format,
        'output_template': args.output_template,
        'subtitles': args.subtitles,
        'embed_metadata': args.embed_metadata,
        'proxy': args.proxy,
        'speed_limit': args.speed_limit,
        'retries': args.retries
    }

    downloader = VideoDownloader(config)
    failed = []

    for url in urls:
        logger.info(f"Processing URL: {url}")
        success = False
        for attempt in range(args.retries):
            if downloader.download(url):
                success = True
                break
            logger.warning(f"Retrying ({attempt+1}/{args.retries})...")
        
        if not success:
            failed.append(url)
            logger.error(f"Failed to download {url} after {args.retries} attempts")

    if failed:
        logger.error(f"Failed downloads: {len(failed)}/{len(urls)}")
        sys.exit(1)

    logger.info("All downloads completed successfully")
    sys.exit(0)

if __name__ == '__main__':
    main()