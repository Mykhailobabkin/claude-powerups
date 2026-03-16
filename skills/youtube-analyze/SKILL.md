---
name: youtube-analyze
description: Analyze YouTube videos by pulling transcripts and compiling insights. Use when the user says "analyze youtube", "youtube insights", "video research", "pull transcripts", "watch these videos", or provides YouTube URLs for analysis.
---

# YouTube Video Analysis

Pulls transcripts from YouTube videos and analyzes them to extract insights, compile articles, or answer questions.

## Process

1. Extract video IDs from user-provided URLs (support youtube.com/watch?v=, youtu.be/, and raw video IDs)
2. Run the transcript fetcher script: `python3 ~/.claude/skills/youtube-analyze/assets/youtube_transcripts.py <video_id1> <video_id2> ...`
3. The script outputs JSON to stdout with video titles, transcripts, word counts
4. Analyze the transcripts based on the user's goal:
   - If compiling an article: identify key themes, unique insights per video, common patterns, actionable takeaways
   - If answering questions: search transcripts for relevant sections
   - If comparing videos: note agreements, contradictions, unique contributions

## Output Formats

Based on user request:
- **Article draft**: Structured article with sections, quotes from videos (attributed), and synthesis
- **Insights summary**: Bullet points organized by theme
- **Comparison**: Side-by-side analysis of what each video covers

## Notes

- Works with any YouTube video that has captions (manual or auto-generated)
- Videos without captions will fail — the script reports which ones
- Auto-generated captions may have minor errors but are usable for analysis
- 5 videos ~ 70-100K words ~ fits easily in context window
- For large batches (20+), consider processing in groups
