"""
Scraping automático de métricas RRSS.
Corre dentro del management command weekly_kpi antes de enviar el email.

Instagram: instagrapi (API mobile unofficial, sin browser)
TikTok: endpoint público JSON unofficial
"""
import json
import os
from datetime import datetime, timedelta, timezone

import requests

_IG_USERNAME = os.getenv('IG_USERNAME', '')
_IG_PASSWORD = os.getenv('IG_PASSWORD', '')
_IG_TARGET = os.getenv('IG_TARGET_USERNAME', 'endonautas')
_TT_USERNAME = os.getenv('TIKTOK_USERNAME', 'endonautas')
_SESSION_PATH = '/tmp/ig_session.json'

_EMPTY = {
    'instagram_seguidores': 0,
    'posts_publicados_semana': 0,
    'tiktok_seguidores': 0,
}


def fetch_all() -> dict:
    result = dict(_EMPTY)
    result.update(_instagram())
    result.update(_tiktok())
    return result


def _instagram() -> dict:
    if not _IG_USERNAME or not _IG_PASSWORD:
        return {}
    try:
        from instagrapi import Client

        cl = Client()
        cl.delay_range = [1, 3]

        # Reusar sesión si existe y es reciente (< 6 días)
        if os.path.exists(_SESSION_PATH):
            age = datetime.now().timestamp() - os.path.getmtime(_SESSION_PATH)
            if age < 6 * 86400:
                cl.load_settings(_SESSION_PATH)
                cl.login(_IG_USERNAME, _IG_PASSWORD)
            else:
                _do_login(cl)
        else:
            _do_login(cl)

        user = cl.user_info_by_username(_IG_TARGET)
        followers = user.follower_count

        # Posts publicados en últimos 7 días
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=7)
        medias = cl.user_medias(user.pk, amount=20)
        posts_semana = sum(1 for m in medias if m.taken_at and m.taken_at > cutoff)

        return {
            'instagram_seguidores': followers,
            'posts_publicados_semana': posts_semana,
        }
    except Exception:
        return {}


def _do_login(cl):
    cl.login(_IG_USERNAME, _IG_PASSWORD)
    cl.dump_settings(_SESSION_PATH)


def _tiktok() -> dict:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.tiktok.com/',
        }
        r = requests.get(
            'https://www.tiktok.com/api/user/detail/',
            params={'uniqueId': _TT_USERNAME, 'aid': '1988', 'app_language': 'es'},
            headers=headers,
            timeout=10,
        )
        data = r.json()
        stats = data.get('userInfo', {}).get('stats', {})
        followers = stats.get('followerCount', 0)
        return {'tiktok_seguidores': followers}
    except Exception:
        return {}
