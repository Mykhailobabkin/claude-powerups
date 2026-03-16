#!/usr/bin/env python3
"""Fetch YouTube video transcripts and output as JSON.

Accepts video IDs or URLs. Uses youtube-transcript-api for transcripts
and yt-dlp for video titles. No API keys required.
"""

import argparse
import json
import re
import subprocess
import sys
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(input_str: str) -> str:
    """Extract a YouTube video ID from a URL or return the raw ID."""
    input_str = input_str.strip()

    # Already a bare video ID (11 chars, alphanumeric + - _)
    if re.fullmatch(r"[\w-]{11}", input_str):
        return input_str

    parsed = urlparse(input_str)
    host = parsed.hostname or ""

    # youtube.com/watch?v=ID
    if "youtube.com" in host:
        if parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]
        # youtube.com/shorts/ID or youtube.com/embed/ID
        match = re.match(r"/(shorts|embed|v)/([\w-]{11})", parsed.path)
        if match:
            return match.group(2)

    # youtu.be/ID
    if "youtu.be" in host:
        vid = parsed.path.lstrip("/")
        if re.fullmatch(r"[\w-]{11}", vid):
            return vid

    # Last resort: try to find an 11-char ID in the string
    match = re.search(r"([\w-]{11})", input_str)
    if match:
        return match.group(1)

    return input_str  # return as-is, let downstream error handle it


def fetch_title(video_id: str) -> str:
    """Fetch video title using yt-dlp (no download)."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--print", "title", "--no-warnings",
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=30,
        )
        title = result.stdout.strip()
        return title if title else "Unknown Title"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "Unknown Title"


def fetch_transcript(video_id: str) -> dict:
    """Fetch and clean a transcript for a single video."""
    result = {
        "video_id": video_id,
        "title": "Unknown Title",
        "transcript": "",
        "word_count": 0,
        "is_generated": False,
        "error": None,
    }

    # Fetch title
    result["title"] = fetch_title(video_id)

    # Fetch transcript
    try:
        api = YouTubeTranscriptApi()
        # Try English first, then any available language
        try:
            transcript_data = api.fetch(video_id, languages=["en"])
        except Exception:
            # Fall back to listing and picking the first available
            transcript_list = api.list(video_id)
            first = next(iter(transcript_list))
            transcript_data = first.fetch()
            result["is_generated"] = first.is_generated

        # Check is_generated from the fetched transcript if available
        if hasattr(transcript_data, "is_generated"):
            result["is_generated"] = transcript_data.is_generated

        # Build full text
        raw_text = " ".join(snippet.text for snippet in transcript_data)

        # Clean: remove [Music], [Applause], ♪ lines, etc.
        cleaned = re.sub(r"\[[\w\s♪]+\]", "", raw_text)
        cleaned = re.sub(r"♪[^♪]*♪", "", cleaned)
        cleaned = re.sub(r"[♪♫]", "", cleaned)
        # Collapse whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        result["transcript"] = cleaned
        result["word_count"] = len(cleaned.split())

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube transcripts and output as JSON."
    )
    parser.add_argument(
        "videos",
        nargs="+",
        help="YouTube video IDs or URLs",
    )
    args = parser.parse_args()

    video_ids = [extract_video_id(v) for v in args.videos]
    results = [fetch_transcript(vid) for vid in video_ids]

    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
