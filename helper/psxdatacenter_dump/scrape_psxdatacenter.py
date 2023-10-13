#! /usr/bin/env python3
'''
Scrape metadata from PlayStation DataCenter dump
'''
from bs4 import BeautifulSoup
from datetime import datetime
from os import makedirs
from os.path import abspath, expanduser
from sys import argv
from zipfile import ZipFile

# clean a string
def clean(s):
    return s.replace(chr(65533),'').replace(chr(0),'').replace(u'\xa0 ',u' ').replace(u'\xa0',u' ').strip()

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
    data = dict(); html_files = [fn for fn in z.namelist() if fn.lower().endswith('.html')]
    for html_fn_num, html_fn in enumerate(html_files):
        # set up parsing current HTML file
        print("Parsing HTML file %d of %d..." % (html_fn_num+1, len(html_files)), end='\r')
        raw_data = clean(z.read(html_fn).decode('utf-8', errors='replace'))
        soup = BeautifulSoup(raw_data, 'html.parser')
        official_title = None
        region = None
        genre = None
        developer = None
        publisher = None
        release_date = None
        serials = None
        languages = None

        # parse current HTML file
        for row in soup.find_all('tr'):
            cols = [clean(col.text) for col in row.find_all('td')]
            if len(cols) == 0:
                continue
            if cols[0] == 'Official Title':
                official_title = cols[1]
            elif cols[0] == 'Region':
                region = cols[1]
            elif cols[0] == 'Genre / Style':
                genre = cols[1]
            elif cols[0] == 'Developer':
                developer = cols[1].rstrip('.')
            elif cols[0] == 'Publisher':
                publisher = cols[1].rstrip('.')
            elif cols[0] == 'Date Released':
                try:
                    if cols[1].strip() == 'None':
                        release_date = ''
                    else:
                        try:
                            release_date = datetime.strptime(cols[1], '%d %B %Y').strftime('%Y-%m-%d')
                        except:
                            release_date = int(cols[1])
                except Exception as e:
                    print("ERROR: %s" % html_fn); raise e
            elif cols[0] == 'Serial Number In Disc':
                serials = [col for col in cols[1:] if len(col) != 0]

        # parse game languages
        soup_lang = BeautifulSoup(raw_data.split('<!-- Languages Sectional -->')[1], 'html.parser')
        cols = [clean(col.text) for i, row in enumerate(soup_lang.find_all('tr')) if i < 2 for col in row.find_all('td')]
        if len(cols) > 6:
            languages = [col for col in cols if len(col) != 0]

        # handle parsed entries
        curr_data = dict()
        if official_title is None:
            print("Missing official title: %s" % html_fn); exit(1)
        else:
            curr_data['official_title'] = official_title
        if region is None:
            print("Missing region: %s" % html_fn); exit(1)
        else:
            curr_data['region'] = region
        if genre is None:
            print("Missing genre: %s" % html_fn); exit(1)
        else:
            curr_data['genre'] = genre
        if developer is None:
            print("Missing developer: %s" % html_fn); exit(1)
        else:
            curr_data['developer'] = developer
        if publisher is None:
            print("Missing publisher: %s" % html_fn); exit(1)
        else:
            curr_data['publisher'] = publisher
        if release_date is None:
            print("Missing release date: %s" % html_fn); exit(1)
        elif isinstance(release_date, int):
            curr_data['release_date'] = str(release_date)
        elif release_date != '':
            curr_data['release_date'] = release_date
        if languages is None:
            print("Missing languages: %s" % html_fn); exit(1)
        else:
            curr_data['languages'] = languages
        if serials is None or len(serials) == 0:
            print("Missing seral numbers in disc: %s" % html_fn); exit(1)
        elif len(serials) == 1:
            data[serials[0]] = curr_data
        else:
            for i, serial in enumerate(serials):
                data[serial] = curr_data.copy()
                data[serial]['official_title'] += ' (Disc %d)' % (i+1)
    print("Successfully parsed %d HTML files              " % len(html_files))

    # save game data
    for serial in data:
        game_path = '%s/%s' % (games_path, serial)
        makedirs(game_path, exist_ok=True)
        for k in data[serial]:
            f = open('%s/%s.txt' % (game_path, k), 'w')
            if isinstance(data[serial][k], str):
                f.write('%s\n' % data[serial][k])
            elif isinstance(data[serial][k], list):
                f.write('%s\n' % '\n'.join(data[serial][k]))
            else:
                raise ValueError("Unknown metadata type (%s) when writing field (%s): %s" % (type(data[serial][k]), k, data[serial]))
            f.close()
