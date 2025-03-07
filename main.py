# modules:
# pip install pyperclip
# pip install --use-pep517 git+https://github.com/stschake/savify@feature/use-yt-dlp

import os
import pyperclip
from savify import Savify
from savify.types import Format, Quality
from savify.utils import PathHolder

# You will have to create a spotify app and add the client id and client secret
# https://developer.spotify.com/dashboard/applications
# https://developer.spotify.com/documentation/general/guides/app-settings/

# You can find more information in the savify documentation
# https://github.com/LaurenceRawlings/savify 

# Add your own paths in path.txt
# Works with linux and wsl. cannot get ffmpeg to work on windows. have not tested on mac.

PATHLIST = open("paths.txt", "r")
PATH = PATHLIST.read().split("\n")

VIDEO = ["avi", "flv", "gif", "mkv", "mov", "mp4", "webm", "aiff", "mka", "ogg"]
AUDIO = ["aac", "alac", "flac", "m4a", "mp3", "opus", "vorbis", "wav"]

def SAVE_PATH():
    global save_path
    path_count = 1
    for i in PATH:
        print(f'{path_count}: {i}')
        path_count += 1
    save_path = input('Where would you like to save the song? ')
    save_path = PATH[int(save_path) - 1]
    save_path = save_path.replace(' ', '')

def SERVICE():
    global url
    print('Copy link to the song, playlist, or album')
    while 'https://open.spotify.com/' not in pyperclip.paste() and 'youtube.com/' not in pyperclip.paste():
        pass
    url = pyperclip.paste()
    if 'https://open.spotify.com/' in url:
        FOLDER()
        SPOTIFY()
    elif 'youtube.com/' in url:
        FOLDER()
        YOUTUBE()
    
def FOLDER():
    os.system('clear')
    global global_folder, save_folder
    global_folder = input('What folder would you like to save the song to? ')
    save_folder = global_folder.replace(' ', '').lower()
    if save_folder == 'ls':
        os.system(f'ls {save_path}')
        FOLDER()
    elif save_folder == 'exit' or save_folder == 'quit':
        exit()
    elif save_folder == 'no':
        RUN()
    os.makedirs(f'{save_path}{save_folder}', exist_ok=True)

def YOUTUBE():
    os.system('clear')
    file_name = input('What would you like to name the media? ')
    file_name = file_name.replace(' ', '')
    file_type = input('''Audio: aac, alac, flac, m4a, mp3, opus, vorbis, wav
Video: avi, flv, gif, mkv, mov, mp4, webm, aiff, mka, ogg 
''')
    for i in VIDEO:
        if i == file_type:
            is_video = True
            break
        for i in AUDIO:
            if i == file_type:
                is_video = False
                break
    if is_video:
        os.system(f'yt-dlp -o {save_path}{save_folder}/{file_name} --recode-video {file_type} {url}')
    if not is_video:
        os.system(f'yt-dlp -o {save_path}{save_folder}/{file_name} -x --audio-format {file_type} --audio-quality 0 {url}')

def SPOTIFY():
    os.system('clear')
    s = Savify(quality=Quality.BEST, download_format=Format.MP3, path_holder=PathHolder(downloads_path=f"{save_path}{save_folder}"), skip_cover_art=False)
    s.download(url)
    
def RUN():
    os.system('clear')
    SAVE_PATH()
    os.system('clear')
    SERVICE()
    os.system('clear')

try:
    RUN()
except KeyboardInterrupt:
    os.system('clear')
    exit()
