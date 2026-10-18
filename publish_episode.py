#!/usr/bin/env python3
"""Add one episode to the Le Petit Matin podcast feed.

Usage:
  python3 publish_episode.py <repo_dir> <base_url> <mp3> "<title>" "<summary>" <YYYY-MM-DD>

Re-encodes the MP3 to 64 kbps mono, stores it as episodes/<date>.mp3, records it in
episodes.json, keeps the newest KEEP episodes and rebuilds feed.xml (Apple Podcasts RSS).
"""
import json, os, subprocess, sys, datetime, email.utils
from xml.sax.saxutils import escape

KEEP = 30
SHOW = {
    "title": "Petit Matin Good Vibes",
    "author": "Petit Matin Good Vibes",
    "description": ("Chaque matin, sept minutes : les quatre infos du jour (France, monde, Asie, États-Unis), un conseil de management, une idée de voyage en Asie, "
                    "les modes et anecdotes du Japon, de la Corée et de la Chine, une citation française, "
                    "un moment de l'histoire de France et un fait de culture générale. Voix de synthèse."),
    "language": "fr-fr",
    "category": "Society &amp; Culture",
    "email": os.environ.get("PODCAST_OWNER_EMAIL", "podcast@users.noreply.github.com"),
}

def main():
    repo, base, mp3, title, summary, date = sys.argv[1:7]
    base = base.rstrip("/")
    os.makedirs(os.path.join(repo, "episodes"), exist_ok=True)
    out = os.path.join(repo, "episodes", f"{date}.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-b:a", "64k", out], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", out]).decode().strip())
    idx_path = os.path.join(repo, "episodes.json")
    eps = json.load(open(idx_path)) if os.path.exists(idx_path) else []
    eps = [e for e in eps if e["date"] != date]
    eps.append({"date": date, "title": title, "summary": summary,
                "bytes": os.path.getsize(out), "duration": int(round(dur))})
    eps.sort(key=lambda e: e["date"], reverse=True)
    for old in eps[KEEP:]:
        p = os.path.join(repo, "episodes", f"{old['date']}.mp3")
        if os.path.exists(p):
            os.remove(p)
    eps = eps[:KEEP]
    json.dump(eps, open(idx_path, "w"), ensure_ascii=False, indent=1)

    items = []
    for e in eps:
        d = datetime.datetime.strptime(e["date"], "%Y-%m-%d").replace(hour=5, minute=0,
                                                                         tzinfo=datetime.timezone.utc)
        url = f"{base}/episodes/{e['date']}.mp3"
        items.append(f"""  <item>
   <title>{escape(e['title'])}</title>
   <description>{escape(e['summary'])}</description>
   <itunes:summary>{escape(e['summary'])}</itunes:summary>
   <enclosure url="{url}" length="{e['bytes']}" type="audio/mpeg"/>
   <guid isPermaLink="false">le-petit-matin-{e['date']}</guid>
   <pubDate>{email.utils.format_datetime(d)}</pubDate>
   <itunes:duration>{e['duration']}</itunes:duration>
   <itunes:explicit>false</itunes:explicit>
   <itunes:episodeType>full</itunes:episodeType>
  </item>""")
    now = email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>{SHOW['title']}</title>
  <link>{base}/</link>
  <atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>
  <language>{SHOW['language']}</language>
  <description>{escape(SHOW['description'])}</description>
  <itunes:author>{SHOW['author']}</itunes:author>
  <itunes:summary>{escape(SHOW['description'])}</itunes:summary>
  <itunes:image href="{base}/cover.jpg"/>
  <itunes:category text="{SHOW['category']}"/>
  <itunes:explicit>false</itunes:explicit>
  <itunes:type>episodic</itunes:type>
  <itunes:owner><itunes:name>{SHOW['author']}</itunes:name><itunes:email>{SHOW['email']}</itunes:email></itunes:owner>
  <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
 </channel>
</rss>
"""
    open(os.path.join(repo, "feed.xml"), "w", encoding="utf-8").write(feed)
    print(f"OK {date} {dur/60:.1f} min, {len(eps)} episodes in feed")

if __name__ == "__main__":
    main()
