# coding=utf-8

import os
import json
import base64

from bs4 import BeautifulSoup
import lxml



# Get the Emoji spec
with open('raw-emojis.json', 'r', encoding='utf-8') as f:
    emojis = json.load(f)

# Get the emoji library
with open('emojilib.json', 'r', encoding='utf-8') as f:
    library = json.load(f)

def match_emoji(char):
    if char == '*\u20e3':
        char = "*\ufe0f\u20e3"
    if emojis.get(char):
        return emojis[char]
    return emojis[char.rstrip('\ufe0f')]

for name, library_info in library.items():
    char = library_info['char']
    keywords = library_info['keywords']

    info = match_emoji(char)
    info['short_name'] = name
    info['keywords'] = keywords

    # Trust emojilib more than Unicode
    info['char'] = char


# Enrich with GitHub colon-codes
with open('codes.json') as f:
    codes = json.load(f)

for code, char in codes.items():
    info = match_emoji(char)
    if 'code' in info:
        info['code'] += " " + code
    else:
        info['code'] = code


# Write out icons
os.mkdir('icons')

def choose_filename(info):
    if 'short_name' in info:
        return info['short_name']
    if 'code' in info:
        return info['code'].strip(':')
    return info['title'].replace(' ', '_')

seen_filenames = set()
for info in emojis.values():
    filename = choose_filename(info)
    while filename in seen_filenames:
        filename = filename + '_'
    seen_filenames.add(filename)

    path = os.path.join('icons', filename + '.png')
    info['path'] = path
    with open(path, 'wb') as f:
        png_bytes = base64.b64decode(info['png_base64'])
        f.write(png_bytes)
        del info['png_base64']


# Print out matches
def match(info):
    if 'code' in info:
        yield info['code'].replace(':', '') #.replace('_', ' ')

    if 'short_name' in info:
        yield info['short_name'].replace("_", " ")
        for k in info['keywords']:
            yield k.replace("_", " ")

    else:
        # for a in info['aliases']:
        #     yield a.replace("_", " ")
        yield info['title']

    yield info['char']

def dedupe(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        yield x
        seen.add(x)

def item(info):
    return dict(
        title = info['title'],
        subtitle = info.get('code', ''),
        icon = dict(
            path = info['path'],
        ),
        arg = info['char'],
        match = " ".join(dedupe(match(info))),
    )
items = map(item, emojis.values())

json.dump(dict(
    items = list(items),
), open('alfred-emoji.json', 'w'), ensure_ascii=False, indent=2)

