import config.config as config
import soundcloud
import requests
import csv
import io


API_BASE = 'https://api.soundcloud.com'
CLIENT_ID = config.config.SOUNDCLOUD_CLIENT_ID

def get_likes(username):
    user_endpoint = '/users/{}.json'.format(username)
    user_info = get(user_endpoint)
    num_likes = user_info['public_favorites_count']

    likes_endpoint = '/users/{}/favorites'.format(username)
    page_size = 200

    payload = {
        'limit': page_size,
        'linked_partitioning': 1,
        'offset': 0
    }

    next_href = likes_endpoint
    likes = []

    while next_href:
        chunk = get(next_href, payload)
        likes += chunk['collection']
        next_href = chunk.get('next_href', None)

    return likes


def likes_to_csv(likes):
    order = ['id', 'title', 'duration', 'user', 'genre', 'tag_list', 'description', 'playback_count', 'favoritings_count', 'comment_count', 'label_name', 'release', 'release_day', 'release_month', 'release_year', 'created_at', 'last_modified', 'uri', 'stream_url', 'permalink', 'permalink_url', 'purchase_title', 'purchase_url', 'artwork_url', 'attachments_uri', 'user_id', 'label_id', 'isrc', 'track_type', 'sharing', 'state', 'streamable', 'commentable', 'downloadable', 'bpm', 'key_signature', 'original_content_size', 'waveform_url', 'embeddable_by', 'download_count', 'original_format', 'video_url', 'kind', 'license']

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(order)

    for track in likes:
        writer.writerow(track.get(item, None) for item in order)

    return output.getvalue()


def get(url, params={}):
    params['client_id'] = CLIENT_ID
    if 'http' not in url:
        url = API_BASE + url
    return requests.get(url, params=params).json()
