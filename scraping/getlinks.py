from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

folder = '../sitemap/'
files = [f for f in listdir(folder) if isfile(join(folder, f))]
link_no = 1

with open('links.txt', 'w') as fp: # links.txt will contain all links that contain songs
    for f in files:
        with open(folder + f, 'r') as xml:
            soup = BeautifulSoup(xml, 'xml') #
            links = soup.find_all('loc')  # site map contains all links in tag 'loc'
            for link in links:
                link = link.get_text()
                if 'song' in link:  # extracting links that have word song in them
                    fp.writelines(link + '\n')   # writing links to file fp=links.txt
                    print('\r%d links wrote' % link_no, end='')  # printing on command line no of links wrote till now
                    link_no += 1
