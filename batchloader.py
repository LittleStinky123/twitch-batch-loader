import re
import urllib.request
import requests
import sys
import time

basepath = 'downloads/'
base_clip_path = 'https://clips-media-assets2.twitch.tv/'
time_regex_str = '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\.[0-9]+)?(([Zz])|([\+|\-]([01][0-9]|2[0-3]):[0-5][0-9]))$'
broadcaster_id = ''
from_time = ''
to_time = ''

def retrieve_mp4_data(slug):
    cid = sys.argv[1]
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": cid}).json()
    game_info = requests.get(
        "https://api.twitch.tv/helix/games?id=" + clip_info['data'][0]['game_id'],
        headers={"Client-ID": cid}).json()
    thumb_url = clip_info['data'][0]['thumbnail_url']
    if not game_info['data']:
        title = clip_info['data'][0]['created_at'] + '_' + clip_info['data'][0]['title'] + '_' + clip_info['data'][0]['creator_name'] + '_' + slug
    else:
         title = clip_info['data'][0]['created_at'] + '_' + game_info['data'][0]['name'] + '_' + clip_info['data'][0]['title'] + '_' + clip_info['data'][0]['creator_name'] + '_' + slug
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url, title


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

def create_clip_list():
    streamer_id = sys.argv[2]
    time_frame = ''
    if len(sys.argv) > 3:
        from_time = sys.argv[3]
        to_time = sys.argv[4]
        if from_time and to_time:
            if re.search(time_regex_str, from_time) and re.search(time_regex_str, to_time):
                time_frame = '&started_at=' + from_time + '&ended_at=' + to_time
    clips = []
    dict = []
    value_list = [{"sort0":"","sort1":"", "first0":"","first1":""},{"sort0":"","sort1":"", "first0":"100","first1":"100"}]
    for current_dict in value_list:
        print("Preparing clip list using: " + str(current_dict) + "...")
        sort = "&sort=" + current_dict['sort0'] if current_dict['sort0'] else ""
        first = "&first=" + current_dict['first0'] if current_dict['first0'] else ""
        clip_list = requests.get("https://api.twitch.tv/helix/clips?broadcaster_id=" + streamer_id + time_frame + sort + first, headers={"Client-ID": cid}).json()
        clips.append(clip_list['data'])
        while clip_list['pagination']:
            sort = "&sort=" + current_dict['sort1'] if current_dict['sort1'] else ""
            first = "&first=" + current_dict['first1'] if current_dict['first1'] else ""
            clip_list = requests.get("https://api.twitch.tv/helix/clips?broadcaster_id=" + streamer_id+ "&after=" + clip_list['pagination']['cursor'] + sort + first, headers={"Client-ID": cid}).json()
            clips.append(clip_list['data'])
            for entry in clip_list['data']:
                if entry['url'] not in dict:
                    print("New entry: " + str(entry['url']))
                    dict.append(entry['url'])
    f4 = open("dict.txt", "w")
    f4.write(str(dict))
    print("Clip list created with size: " + str(len(dict)))

def download_clips():
    for clip in open('clips.txt', 'r'):
        slug = clip.split('/')[3].replace('\n', '')
        mp4_url, clip_title = retrieve_mp4_data(slug)
        regex = re.compile('[^a-zA-Z0-9_]')
        clip_title = clip_title.replace(' ', '_')
        out_filename = regex.sub('', clip_title) + '.mp4'
        output_path = (basepath + out_filename)
        print('\nDownloading clip slug: ' + slug)
        print('"' + clip_title + '" -> ' + out_filename)
        print(mp4_url)
        urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
        print('\nDone.')

# for each clip in clips.txt
cid = sys.argv[1]
if len(sys.argv) > 2:
    broadcaster_id = sys.argv[2]

if broadcaster_id:
    create_clip_list()
    download_clips()
else:
    download_clips()

print('Finished downloading all the videos.')
