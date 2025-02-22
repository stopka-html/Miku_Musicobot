#load list of music from json
import os
import json
import asyncio
import yt_dlp as youtube_dl
music_list = {}
def load_list():
    with open('auidos.json', 'r') as f:
        global music_list
        try:
            music_list = json.load(f)
        except:
            music_list = {}
        try:
            os.makedirs("music")
        except FileExistsError:
            # directory already exists
            pass
def acess_await(url):
    asyncio.create_task(check_music(url))
async def check_music(url):
    
    if url in music_list:
        return music_list[url]["filename"]
    else:
        ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'player_client':'default,-ios',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)

            output_filename = info_dict['id'] + '.mp3'
            name_of_music = info_dict['title']
            os.rename(output_filename, "music/" + output_filename)
            print(f"downloaded {output_filename}")
            music_list[url] = {"name": name_of_music, "filename": "music/" + output_filename}
            with open('auidos.json', 'w') as f:
                json.dump(music_list, f)
            return "music/"+output_filename
