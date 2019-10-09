import re
import urllib.request
import requests
import sys
from datetime import datetime, timezone 
import datedelta
import copy

basepath = 'downloads/'
base_clip_path = 'https://clips-media-assets2.twitch.tv/'
time_regex_str = '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\.[0-9]+)?(([Zz])|([\+|\-]([01][0-9]|2[0-3]):[0-5][0-9]))$'
broadcaster_id = ''
from_time = ''
to_time = ''
video_map = {}
game_map = {}

def retrieve_mp4_data(slug):
    cid = sys.argv[1]
    video_info = ''
    video_name = ''
    game_name = ''
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": cid}).json()
    print("1:" + str(clip_info))
    if clip_info['data'][0]['game_id']:
        if game_map.get(clip_info['data'][0]['game_id']):
            game_name = game_map.get(clip_info['data'][0]['game_id'])
        else:
            game_info = requests.get(
            "https://api.twitch.tv/helix/games?id=" + clip_info['data'][0]['game_id'],
            headers={"Client-ID": cid}).json()
            print("2:" + str(game_info))
            game_map.update({clip_info['data'][0]['game_id'] : game_info['data'][0]['name']})
            game_name = game_map.get(clip_info['data'][0]['game_id'])
    thumb_url = clip_info['data'][0]['thumbnail_url']
    if clip_info['data'][0]['video_id']:
        if video_map.get(clip_info['data'][0]['video_id']):
            video_name = video_map.get(clip_info['data'][0]['video_id'])
        else:
            video_info = requests.get(
            "https://api.twitch.tv/helix/videos?id=" + clip_info['data'][0]['video_id'],
            headers={"Client-ID": cid}).json()
            video_map.update({clip_info['data'][0]['video_id'] : video_info['data'][0]['title']})
            video_name = video_map.get(clip_info['data'][0]['video_id'])
    # No title provided, possibly too long file name
    if video_name == clip_info['data'][0]['title']:
        title = clip_info['data'][0]['created_at'] + '_' + game_name + '_' + video_name + '_' + clip_info['data'][0]['creator_name'] + '_' + slug
    else:
        title = clip_info['data'][0]['created_at'] + '_' + game_name + '_' + video_name + '_' + clip_info['data'][0]['title'] + '_' + clip_info['data'][0]['creator_name'] + '_' + slug
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
    provided_time_frame = ''
    from_time = "" if len(sys.argv) <= 3 else sys.argv[3]
    to_time = "" if len(sys.argv) <= 4 else sys.argv[4]
    if from_time and to_time and re.search(time_regex_str, from_time) and re.search(time_regex_str, to_time):
        provided_time_frame = '&started_at=' + from_time + '&ended_at=' + to_time
    clips = []
    list = []
    #Generic first args
    value_list = [{"sort0":"","sort1":"", "first0":"","first1":""},{"sort0":"","sort1":"", "first0":"","first1":"100"},{"sort0":"","sort1":"", "first0":"100","first1":""},{"sort0":"","sort1":"", "first0":"100","first1":"100"}\
#    #Time args
#    ,{"sort0":"","sort1":"time", "first0":"","first1":""},{"sort0":"","sort1":"time", "first0":"","first1":"100"},{"sort0":"","sort1 ":"time", "first0":"100","first1":""},{"sort0":"","sort1":"time", "first0":"100","first1":"100"},\
#    {"sort0":"time","sort1":"", "first0":"","first1":""},{"sort0":"time","sort1":"", "first0":"","first1":"100"},{"sort0":"time","sort1":"", "first0":"100","first1":""},{"sort0":"time","sort1":"", "first0":"100","first1":"100"},\
#    {"sort0":"time","sort1":"time", "first0":"","first1":""},{"sort0":"time","sort1":"time", "first0":"","first1":"100"},{"sort0":"time","sort1":"time", "first0":"100","first1":""},{"sort0":"time","sort1":"time", "first0":"100","first1":"100"},\
#    #Time_desc args
#    {"sort0":"","sort1":"time_desc", "first0":"","first1":""},{"sort0":"","sort1":"time_desc", "first0":"","first1":"100"},{"sort0":"","sort1":"time_desc", "first0":"100","first1":""},{"sort0":"","sort1":"time_desc", "first0":"100","first1":"100"},\
#    {"sort0":"time_desc","sort1":"", "first0":"","first1":""},{"sort0":"time_desc","sort1":"", "first0":"","first1":"100"},{"sort0":"time_desc","sort1":"", "first0":"100","first1":""},{"sort0":"time_desc","sort1":"", "first0":"100","first1":"100"},\
#    {"sort0":"time_desc","sort1":"time_desc", "first0":"","first1":""},{"sort0":"time_desc","sort1":"time_desc", "first0":"","first1":"100"},{"sort0":"time_desc","sort1":"time_desc", "first0":"100","first1":""},{"sort0":"time_desc","sort1":"time_desc", "first0":"100","first1":"100"},\
#    #Time_asc args
#    {"sort0":"","sort1":"time_asc", "first0":"","first1":""},{"sort0":"","sort1":"time_asc", "first0":"","first1":"100"},{"sort0":"","sort1":"time_asc", "first0":"100","first1":""},{"sort0":"","sort1":"time_asc", "first0":"100","first1":"100"},\
#    {"sort0":"time_asc","sort1":"", "first0":"","first1":""},{"sort0":"time_asc","sort1":"", "first0":"","first1":"100"},{"sort0":"time_asc","sort1":"", "first0":"100","first1":""},{"sort0":"time_asc","sort1":"", "first0":"100","first1":"100"},\
#    {"sort0":"time_asc","sort1":"time_asc", "first0":"","first1":""},{"sort0":"time_asc","sort1":"time_asc", "first0":"","first1":"100"},{"sort0":"time_asc","sort1":"time_asc", "first0":"100","first1":""},{"sort0":"time_asc","sort1":"time_asc", "first0":"100","first1":"100"},\
#    #Views args
#    {"sort0":"","sort1":"views", "first0":"","first1":""},{"sort0":"","sort1":"views", "first0":"","first1":"100"},{"sort0":"","sort1":"views", "first0":"100","first1":""},{"sort0":"","sort1":"views", "first0":"100","first1":"100"},\
#    {"sort0":"views","sort1":"", "first0":"","first1":""},{"sort0":"views","sort1":"", "first0":"","first1":"100"},{"sort0":"views","sort1":"", "first0":"100","first1":""},{"sort0":"views","sort1":"", "first0":"100","first1":"100"},\
#    {"sort0":"views","sort1":"views", "first0":"","first1":""},{"sort0":"views","sort1":"views", "first0":"","first1":"100"},{"sort0":"views","sort1":"views", "first0":"100","first1":""},{"sort0":"views","sort1":"views", "first0":"100","first1":"100"},\
#    #Views_desc args
#    {"sort0":"","sort1":"views_desc", "first0":"","first1":""},{"sort0":"","sort1":"views_desc", "first0":"","first1":"100"},{"sort0":"","sort1":"views_desc", "first0":"100","first1":""},{"sort0":"","sort1":"views_desc", "first0":"100","first1":"100"},\
#    {"sort0":"views_desc","sort1":"", "first0":"","first1":""},{"sort0":"views_desc","sort1":"", "first0":"","first1":"100"},{"sort0":"views_desc","sort1":"", "first0":"100","first1":""},{"sort0":"views_desc","sort1":"", "first0":"100","first1":"100"},\
#    {"sort0":"views_desc","sort1":"views_desc", "first0":"","first1":""},{"sort0":"views_desc","sort1":"views_desc", "first0":"","first1":"100"},{"sort0":"views_desc","sort1":"views_desc", "first0":"100","first1":""},{"sort0":"views_desc","sort1":"views_desc", "first0":"100","first1":"100"},\
#    #Views_asc args
#    {"sort0":"","sort1":"views_asc", "first0":"","first1":""},{"sort0":"","sort1":"views_asc", "first0":"","first1":"100"},{"sort0":"","sort1":"views_asc", "first0":"100","first1":""},{"sort0":"","sort1":"views_asc", "first0":"100","first1":"100"},\
#    {"sort0":"views_asc","sort1":"", "first0":"","first1":""},{"sort0":"views_asc","sort1":"", "first0":"","first1":"100"},{"sort0":"views_asc","sort1":"", "first0":"100","first1":""},{"sort0":"views_asc","sort1":"", "first0":"100","first1":"100"},\
#    {"sort0":"views_asc","sort1":"views_asc", "first0":"","first1":""},{"sort0":"views_asc","sort1":"views_asc", "first0":"","first1":"100"},{"sort0":"views_asc","sort1":"views_asc", "first0":"100","first1":""},{"sort0":"views_asc","sort1":"views_asc", "first0":"100","first1":"100"},\
    ]
    if from_time and not to_time:
        # Make time_range requests spanning 1 month until current day
        date_time_obj = datetime.strptime(from_time, '%Y-%m-%dT%H:%M:%SZ')
        next_month_obj = copy.deepcopy(date_time_obj) + datedelta.MONTH
        time_frame = '&started_at=' + date_time_obj.isoformat(timespec='seconds') + 'Z&ended_at=' + next_month_obj.isoformat(timespec='seconds') + 'Z'
        today = datetime.today()
        while date_time_obj < today:
            time_frame = '&started_at=' + date_time_obj.isoformat(timespec='seconds') + 'Z&ended_at=' + next_month_obj.isoformat(timespec='seconds') + 'Z'
            print("Using time_frame: " + time_frame)
            for current_dict in value_list:
                print("Preparing clip list using: " + str(current_dict) + "...")
                sort = "&sort=" + current_dict['sort0'] if current_dict['sort0'] else ""
                first = "&first=" + current_dict['first0'] if current_dict['first0'] else ""
                clip_list = requests.get("https://api.twitch.tv/helix/clips?broadcaster_id=" + streamer_id + time_frame + sort + first, headers={"Client-ID": cid}).json()
                while clip_list.get('pagination'):
                    sort = "&sort=" + current_dict.get('sort1') if current_dict.get('sort1') else ""
                    first = "&first=" + current_dict.get('first1') if current_dict.get('first1') else ""
                    clip_list = requests.get("https://api.twitch.tv/helix/clips?broadcaster_id=" + streamer_id+ "&after=" + clip_list['pagination']['cursor']  + time_frame + sort + first, headers={"Client-ID": cid}).json()
                    for entry in clip_list['data']:
                        if {'url':entry['url'], 'created_at': entry['created_at']} not in list:
                            print("New entry: " + str(entry['url']))
                            list.append({'url':entry['url'], 'created_at': entry['created_at']})
            date_time_obj = date_time_obj + datedelta.MONTH
            next_month_obj = next_month_obj + datedelta.MONTH
    # Some clips aren't listed in the time_frame requests so do this as well
    for current_dict in value_list:
        print("Preparing clip list using: " + str(current_dict) + "...")
        sort = "&sort=" + current_dict['sort0'] if current_dict['sort0'] else ""
        first = "&first=" + current_dict['first0'] if current_dict['first0'] else ""
        clip_list = requests.get("https://api.twitch.tv/helix/clips?broadcaster_id=" + streamer_id + provided_time_frame + sort + first, headers={"Client-ID": cid}).json()
        while clip_list['pagination']:
            sort = "&sort=" + current_dict.get('sort1') if current_dict.get('sort1') else ""
            first = "&first=" + current_dict.get('first1') if current_dict.get('first1') else ""
            clip_list = requests.get("https://api.twitch.tv/helix/clips?broadcaster_id=" + streamer_id+ "&after=" + clip_list['pagination']['cursor'] + provided_time_frame + sort + first, headers={"Client-ID": cid}).json()
            for entry in clip_list['data']:
                if {'url':entry['url'], 'created_at': entry['created_at']} not in list:
                    print("New entry: " + str(entry['url']))
                    list.append({'url':entry['url'], 'created_at': entry['created_at']})
    sorted_list = sorted(list, key = lambda i: i['created_at'], reverse=True)
    f4 = open("clips.txt", "w")
    for entry in sorted_list:
        f4.write(entry['url'] + "\n")
    print("Clip list created with size: " + str(len(sorted_list)))

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
else:
    download_clips()

print('Finished downloading all the videos.')
