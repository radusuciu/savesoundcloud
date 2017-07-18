import config.config as config
import requests
import csv
import io
import zipfile


API_BASE = 'https://api.soundcloud.com'
CLIENT_ID = config.config.SOUNDCLOUD_CLIENT_ID

ENDPOINTS = ('tracks', 'playlists', 'followings', 'followers', 'comments', 'favorites')

COLUMN_ORDERS = {
    'tracks': ['id', 'title', 'user', 'user_id', 'genre', 'tag_list', 'description', 'duration', 'playback_count', 'favoritings_count', 'commentable', 'comment_count', 'reposts_count', 'downloadable', 'download_count', 'label_id', 'label_name', 'release', 'release_day', 'release_month', 'release_year', 'created_at', 'last_modified', 'artwork_url', 'attachments_uri', 'bpm', 'embeddable_by', 'key_signature', 'kind', 'license', 'isrc', 'monetization_model', 'original_content_size', 'original_format', 'permalink', 'permalink_url', 'policy', 'purchase_title', 'purchase_url', 'sharing', 'state', 'streamable', 'stream_url', 'download_url', 'track_type', 'uri', 'video_url', 'waveform_url'],
    'favorites': ['id', 'title', 'user', 'user_id', 'genre', 'tag_list', 'description', 'duration', 'playback_count', 'favoritings_count', 'likes_count', 'commentable', 'comment_count', 'reposts_count', 'downloadable', 'download_count', 'label_id', 'label_name', 'release', 'release_day', 'release_month', 'release_year', 'created_at', 'last_modified', 'artwork_url', 'attachments_uri', 'bpm', 'embeddable_by', 'key_signature', 'kind', 'license', 'isrc', 'monetization_model', 'original_content_size', 'original_format', 'permalink', 'permalink_url', 'policy', 'purchase_title', 'purchase_url', 'sharing', 'state', 'streamable', 'stream_url', 'track_type', 'uri', 'video_url', 'waveform_url'],
    'followers': ['id', 'permalink', 'username', 'first_name', 'last_name', 'full_name', 'description', 'followings_count', 'followers_count', 'public_favorites_count', 'likes_count', 'comments_count', 'track_count', 'reposts_count', 'playlist_count', 'country', 'city', 'discogs_name', 'myspace_name', 'last_modified', 'online', 'plan', 'website', 'website_title', 'avatar_url', 'kind', 'uri', 'permalink_url'],
    'followings': ['id', 'permalink', 'username', 'first_name', 'last_name', 'full_name', 'description', 'followings_count', 'followers_count', 'public_favorites_count', 'likes_count', 'comments_count', 'track_count', 'reposts_count', 'playlist_count', 'country', 'city', 'discogs_name', 'myspace_name', 'last_modified', 'online', 'plan', 'website', 'website_title', 'avatar_url', 'kind', 'uri', 'permalink_url'],
    'comments': ['id', 'created_at', 'body', 'timestamp',  'track_id', 'user_id', 'user', 'uri'],
}

class UserNotFound(Exception):
    pass

def export_all(username):
    memory_file = io.BytesIO()
    user = get_user(username)

    if 'id' not in user:
        raise UserNotFound

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for endpoint in ENDPOINTS:
            try:
                filename, file = to_csv(username, endpoint, user_info=user)
                zf.writestr(filename, file.getvalue())
            except:
                pass

    memory_file.seek(0)
    return memory_file


def to_csv(username, endpoint, user_info=None):
    coll = consume(username, endpoint, user_info)
    order = COLUMN_ORDERS.get(endpoint, None)
    filename = '{}-{}.csv'.format(username, endpoint)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(order or coll[0].keys())

    if order:
        for line in coll:
            writer.writerow(line.get(item, None) for item in order)
    else:
        for line in coll:
            writer.writerow(line.get(item, None) for item in line)

    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)

    return filename, mem


def consume(username, endpoint, user_info=None):
    user = user_info or get_user(username)

    uri = '/users/{}/{}'.format(user['id'], endpoint)
    page_size = 200

    payload = {
        'limit': page_size,
        'linked_partitioning': 1,
        'offset': 0
    }

    next_href = uri
    coll = []

    while next_href:
        chunk = get(next_href, payload)
        coll += chunk['collection']
        next_href = chunk.get('next_href', None)

    return coll


def get_user(username):
    return get('/users/{}'.format(username))


def find_users(term):
    return get('/users', { 'q': term, 'limit': 5 })


def get(url, params={}):
    params['client_id'] = CLIENT_ID
    if 'http' not in url:
        url = API_BASE + url
    return requests.get(url, params=params).json()
