#! /usr/bin/env python3
'''
Scrape metadata from PlayStation DataCenter dump
'''
from bs4 import BeautifulSoup
from os import makedirs
from os.path import abspath, expanduser
from sys import argv
from zipfile import ZipFile

# main program
if __name__ == "__main__":
    # parse user args
    if len(argv) != 2:
        print("USAGE: %s psxdatacenter_dump.zip" % argv[0]); exit(1)
    try:
        z = ZipFile(argv[1])
    except:
        print("Unable to open zip file: %s" % argv[1]); exit(1)
    games_path = '%s/games' % '/'.join(abspath(expanduser(argv[0])).split('/')[:-3])

    # load game data
    data = dict()
    for html_fn in [fn for fn in z.namelist() if fn.lower().endswith('.html')]:
        serial = html_fn.split('/')[-1].split('.html')[0]
        if serial in data:
            print("DUPLICATE: %s" % serial)
        else:
            data[serial] = dict()
        #raw_data = z.read(html_fn).decode(errors='replace')
        #soup = BeautifulSoup(raw_data, 'html.parser')
        #for row in soup.find_all('tr'):
        #    for col in row.find_all('td'):
        #        print(col.text)
        #    exit()

    # save game data
    exit() # TODO
    for serial in data:
        game_path = '%s/%s' % (games_path, serial)
        makedirs(game_path, exist_ok=True)
