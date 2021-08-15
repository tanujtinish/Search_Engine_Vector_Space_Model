from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, ChunkedEncodingError
from langdetect import detect
import re
from tqdm import trange
import os

songs_folder = '../songs/'
files_skipped = 0
try:
    with open('songs_done.txt', 'r') as done_file:
        count = done_file.readline()
        count = int(count)
except FileNotFoundError:
    count = -1
with open('links.txt', 'r') as f:
    links = f.readlines()
    for i in trange(len(links)):
        if i <= count:
            continue
        link = links[i]
        try:
            html = requests.get(link).text # get text of page link is pointing to
        except ConnectionError or ChunkedEncodingError:
            continue
        soup = BeautifulSoup(html, 'html.parser')  # soup will parse html page returned by links in links.txt
        song = soup.find_all('p', {'class': 'songtext'})[0] # searching for paragraph with class=songtext and storing lyrics
        song_filtered = song.get_text()
        try:
            lang = detect(song_filtered[:50])  # checking language of song text
        except Exception:
            continue
        if lang != 'en': # if song is not in english then skip this song
            with open('songs_done.txt', 'w') as done_file:
                done_file.write(str(i))
            continue
        song_title = re.findall(r'/s.*?.html', link)[0][1:-5] # using regex code to find title of song which will act as file name to store its lyrics
        try:
            with open(songs_folder + song_title + '.txt', 'w') as sf:
                sf.write(song_filtered) # adding song lyrics in file('song_title.txt')
        except UnicodeEncodeError as err:
            print(song_title + lang)
            print('%d files skipped' % (files_skipped + 1))
            files_skipped += 1
            try:
                os.remove(songs_folder + song_title + '.txt')
            except FileNotFoundError:
                print('Skipped file is not deleted because it is not there')
        with open('songs_done.txt', 'w') as done_file:
            done_file.write(str(i))
