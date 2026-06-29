"""
Top contenido por plataforma — video/post con mejor performance esta semana.
Se ejecuta en weekly_kpi antes de generar el markdown.
"""
import os
from datetime import datetime, timedelta, timezone

import requests

_YT_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
_YT_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID', 'UC9hqN2eNx1X-U-2ev9GUsCg')
_META_PAGE_TOKEN = os.getenv('META_PAGE_TOKEN', '')
_META_IG_ID = os.getenv('META_IG_ID', '17841408150037364')
_META_PAGE_ID = os.getenv('META_PAGE_ID', '112522961877445')


def fetch_all() -> dict:
    top = {}
    yt = _youtube_top()
    if yt:
        top['youtube'] = yt
    ig = _instagram_top()
    if ig:
        top['instagram'] = ig
    fb = _facebook_top()
    if fb:
        top['facebook'] = fb
    return {'top_content': top}


def _youtube_top() -> dict | None:
    if not _YT_API_KEY:
        return None
    try:
        # Uploads playlist = channel ID con UC→UU
        playlist_id = 'UU' + _YT_CHANNEL_ID[2:]
        cutoff = (datetime.now(tz=timezone.utc) - timedelta(days=30)).isoformat()

        r = requests.get(
            'https://www.googleapis.com/youtube/v3/playlistItems',
            params={
                'part': 'contentDetails,snippet',
                'playlistId': playlist_id,
                'maxResults': 10,
                'key': _YT_API_KEY,
            },
            timeout=10,
        )
        items = r.json().get('items', [])
        if not items:
            return None

        recent = [i for i in items if i.get('snippet', {}).get('publishedAt', '') >= cutoff]
        pool = recent if recent else items[:5]

        video_ids = [i['contentDetails']['videoId'] for i in pool]
        stats_r = requests.get(
            'https://www.googleapis.com/youtube/v3/videos',
            params={'part': 'statistics,snippet', 'id': ','.join(video_ids), 'key': _YT_API_KEY},
            timeout=10,
        )
        videos = stats_r.json().get('items', [])
        if not videos:
            return None

        videos.sort(key=lambda v: int(v.get('statistics', {}).get('viewCount', 0)), reverse=True)
        top = videos[0]
        stats = top.get('statistics', {})
        snippet = top.get('snippet', {})
        return {
            'title': snippet.get('title', ''),
            'url': f"https://youtu.be/{top['id']}",
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'published_at': snippet.get('publishedAt', '')[:10],
        }
    except Exception:
        return None


def _instagram_top() -> dict | None:
    if not _META_PAGE_TOKEN:
        return None
    try:
        r = requests.get(
            f'https://graph.facebook.com/v21.0/{_META_IG_ID}/media',
            params={'fields': 'id,timestamp,like_count,comments_count', 'limit': 10, 'access_token': _META_PAGE_TOKEN},
            timeout=10,
        )
        media = r.json().get('data', [])
        if not media:
            return None

        media.sort(key=lambda m: m.get('like_count', 0), reverse=True)
        top = media[0]

        reach = saved = 0
        try:
            ins_r = requests.get(
                f"https://graph.facebook.com/v21.0/{top['id']}/insights",
                params={'metric': 'reach,saved', 'access_token': _META_PAGE_TOKEN},
                timeout=10,
            )
            for item in ins_r.json().get('data', []):
                val = (item.get('values') or [{}])[-1].get('value', 0)
                if item.get('name') == 'reach':
                    reach = val
                elif item.get('name') == 'saved':
                    saved = val
        except Exception:
            pass

        return {
            'published_at': top.get('timestamp', '')[:10],
            'likes': top.get('like_count', 0),
            'comments': top.get('comments_count', 0),
            'reach': reach,
            'saved': saved,
        }
    except Exception:
        return None


def _facebook_top() -> dict | None:
    if not _META_PAGE_TOKEN:
        return None
    try:
        since = int((datetime.now(tz=timezone.utc) - timedelta(days=7)).timestamp())
        r = requests.get(
            f'https://graph.facebook.com/v21.0/{_META_PAGE_ID}/posts',
            params={'fields': 'id,message,created_time', 'since': since, 'access_token': _META_PAGE_TOKEN},
            timeout=10,
        )
        posts = r.json().get('data', [])
        if not posts:
            return None

        best = None
        best_reach = -1
        for post in posts[:5]:
            try:
                ins_r = requests.get(
                    f"https://graph.facebook.com/v21.0/{post['id']}/insights",
                    params={
                        'metric': 'post_impressions_unique,post_reactions_by_type_total',
                        'access_token': _META_PAGE_TOKEN,
                    },
                    timeout=10,
                )
                reach = reactions = 0
                for item in ins_r.json().get('data', []):
                    val = (item.get('values') or [{}])[-1].get('value', 0)
                    if item.get('name') == 'post_impressions_unique':
                        reach = val or 0
                    elif item.get('name') == 'post_reactions_by_type_total':
                        reactions = sum(val.values()) if isinstance(val, dict) else 0
                if reach > best_reach:
                    best_reach = reach
                    best = {
                        'message': (post.get('message') or '')[:80],
                        'created_at': post.get('created_time', '')[:10],
                        'reach': reach,
                        'reactions': reactions,
                    }
            except Exception:
                continue
        return best
    except Exception:
        return None
