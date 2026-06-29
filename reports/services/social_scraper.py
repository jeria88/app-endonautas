"""
Scraping automático de métricas RRSS.
Corre dentro del management command weekly_kpi antes de enviar el email.

Instagram: Meta Graph API (Page Access Token permanente)
TikTok: endpoint público JSON unofficial
YouTube: ytInitialData HTML scraping (o API key si YOUTUBE_API_KEY está seteada)
"""
import os
import re
from datetime import datetime, timedelta, timezone

import requests

# Meta Graph API — Page Access Token (no expira)
_META_PAGE_TOKEN = os.getenv('META_PAGE_TOKEN', '')
_META_IG_ID = os.getenv('META_IG_ID', '17841408150037364')

# Fallback instagrapi (solo si no hay META_PAGE_TOKEN)
_IG_USERNAME = os.getenv('IG_USERNAME', '')
_IG_PASSWORD = os.getenv('IG_PASSWORD', '')
_IG_TARGET = os.getenv('IG_TARGET_USERNAME', 'endonautas')
_SESSION_PATH = '/tmp/ig_session.json'

_TT_USERNAME = os.getenv('TIKTOK_USERNAME', 'endonautas')
_YT_USERNAME = os.getenv('YOUTUBE_USERNAME', 'endonautas')
_YT_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

_META_PAGE_ID = os.getenv('META_PAGE_ID', '112522961877445')
_LI_COMPANY = os.getenv('LINKEDIN_COMPANY', 'endonautas')

_PW_ARGS = ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
_DESKTOP_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

_EMPTY = {
    'instagram_seguidores': 0,
    'posts_publicados_semana': 0,
    'tiktok_seguidores': 0,
    'youtube_seguidores': 0,
    'facebook_seguidores': 0,
    'linkedin_seguidores': 0,
}


def fetch_all() -> dict:
    result = dict(_EMPTY)
    result.update(_instagram())
    result.update(_tiktok())
    result.update(_youtube())
    result.update(_facebook())
    result.update(_linkedin())
    return result


def _instagram() -> dict:
    if _META_PAGE_TOKEN:
        return _instagram_meta_api()
    return _instagram_instagrapi()


def _instagram_meta_api() -> dict:
    try:
        r = requests.get(
            f'https://graph.facebook.com/v21.0/{_META_IG_ID}',
            params={'fields': 'followers_count,media_count', 'access_token': _META_PAGE_TOKEN},
            timeout=10,
        )
        data = r.json()
        if 'error' in data:
            return {}
        followers = data.get('followers_count', 0)

        # Posts últimos 7 días via /media endpoint
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=7)
        media_r = requests.get(
            f'https://graph.facebook.com/v21.0/{_META_IG_ID}/media',
            params={'fields': 'timestamp', 'limit': 30, 'access_token': _META_PAGE_TOKEN},
            timeout=10,
        )
        media_data = media_r.json().get('data', [])
        posts_semana = sum(
            1 for m in media_data
            if m.get('timestamp') and datetime.fromisoformat(m['timestamp'].replace('Z', '+00:00')) > cutoff
        )
        return {'instagram_seguidores': followers, 'posts_publicados_semana': posts_semana}
    except Exception:
        return {}


def _instagram_instagrapi() -> dict:
    if not _IG_USERNAME or not _IG_PASSWORD:
        return {}
    try:
        from instagrapi import Client
        cl = Client()
        cl.delay_range = [1, 3]
        if os.path.exists(_SESSION_PATH):
            age = datetime.now().timestamp() - os.path.getmtime(_SESSION_PATH)
            if age < 6 * 86400:
                cl.load_settings(_SESSION_PATH)
                cl.login(_IG_USERNAME, _IG_PASSWORD)
            else:
                cl.login(_IG_USERNAME, _IG_PASSWORD)
                cl.dump_settings(_SESSION_PATH)
        else:
            cl.login(_IG_USERNAME, _IG_PASSWORD)
            cl.dump_settings(_SESSION_PATH)
        user = cl.user_info_by_username(_IG_TARGET)
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=7)
        medias = cl.user_medias(user.pk, amount=20)
        posts_semana = sum(1 for m in medias if m.taken_at and m.taken_at > cutoff)
        return {'instagram_seguidores': user.follower_count, 'posts_publicados_semana': posts_semana}
    except Exception:
        return {}


def _tiktok() -> dict:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=_PW_ARGS)
            page = browser.new_page(user_agent=_DESKTOP_UA)
            page.goto(f'https://www.tiktok.com/@{_TT_USERNAME}', timeout=30000, wait_until='networkidle')
            content = page.content()
            browser.close()
        m = re.search(r'"followerCount":(\d+)', content)
        if m:
            return {'tiktok_seguidores': int(m.group(1))}
        return {}
    except Exception:
        return {}


def _linkedin() -> dict:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=_PW_ARGS)
            page = browser.new_page(user_agent=_DESKTOP_UA)
            page.goto(f'https://www.linkedin.com/company/{_LI_COMPANY}/', timeout=20000, wait_until='domcontentloaded')
            content = page.content()
            browser.close()
        m = re.search(r'([\d,\.]+)\s*(?:followers|seguidores)', content, re.IGNORECASE)
        if m:
            count = int(m.group(1).replace(',', '').replace('.', ''))
            return {'linkedin_seguidores': count}
        return {}
    except Exception:
        return {}


def _youtube() -> dict:
    try:
        if _YT_API_KEY:
            r = requests.get(
                'https://www.googleapis.com/youtube/v3/channels',
                params={'part': 'statistics', 'forHandle': _YT_USERNAME, 'key': _YT_API_KEY},
                timeout=10,
            )
            items = r.json().get('items', [])
            if items:
                count = int(items[0].get('statistics', {}).get('subscriberCount', 0))
                return {'youtube_seguidores': count}

        # Fallback: parse ytInitialData from channel page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
        }
        r = requests.get(f'https://www.youtube.com/@{_YT_USERNAME}', headers=headers, timeout=15)
        for pattern in (
            r'"subscriberCountText":\{"simpleText":"([^"]+)"',
            r'"shortSubscriberCountText":\{"simpleText":"([^"]+)"',
        ):
            m = re.search(pattern, r.text)
            if m:
                return {'youtube_seguidores': _parse_yt_count(m.group(1))}
        return {}
    except Exception:
        return {}


def _facebook() -> dict:
    if not _META_PAGE_TOKEN:
        return {}
    try:
        r = requests.get(
            f'https://graph.facebook.com/v21.0/{_META_PAGE_ID}',
            params={'fields': 'fan_count', 'access_token': _META_PAGE_TOKEN},
            timeout=10,
        )
        data = r.json()
        if 'error' in data:
            return {}
        return {'facebook_seguidores': data.get('fan_count', 0)}
    except Exception:
        return {}


def _parse_yt_count(text: str) -> int:
    t = text.lower().strip()
    m = re.search(r'([\d][\d,.]*)\s*([kmb]|mil|mill)?', t)
    if not m:
        return 0
    try:
        num = float(m.group(1).replace(',', '.'))
    except ValueError:
        return 0
    suffix = (m.group(2) or '').strip()
    if suffix in ('k', 'mil'):
        return int(num * 1_000)
    if suffix in ('m', 'mill'):
        return int(num * 1_000_000)
    return int(num)
