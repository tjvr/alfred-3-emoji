# coding=utf-8

import json

from bs4 import BeautifulSoup
import lxml


# Get the Emoji spec
html_content = open('full-emoji-list.html')
soup = BeautifulSoup(html_content, 'lxml')

rows = soup.find_all('tr')

emojis = {}
for row in rows:
    if not row.find(class_='chars'):
        continue
    char = row.find(class_='chars').text
    # apple is first image
    img = row.find('img')
    title = row.find(class_='name').text
    
    _, _, encoded = img.attrs['src'].partition('data:image/png;base64,')
    
    recently_added = title.startswith('⊛')
    if recently_added:
        title = title.lstrip('⊛ ')

    emojis[char] = dict(
        char = char,
        title = title,
        png_base64 = encoded,
        recently_added = recently_added,
    )

json.dump(emojis, open('raw-emojis.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

