#!/usr/bin/env python3

# This should be run against a saved copy of https://sites.grenadine.co/sites/nineworlds/en/2018/set_view/list?dest=%2Fsites%2Fnineworlds%2Fen%2F2018%2Fschedule

from bs4 import BeautifulSoup
import json, sys

soup = None
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        soup = BeautifulSoup(f, 'lxml')
else:
    soup = BeautifulSoup(sys.stdin, 'lxml')

byTitle = {}
for item in soup.select('#timeline .list-item'):
    a = item.find(class_='list-item-details-container').a
    title = a.string.strip()
    itemOut = {
        #'title': title,
        'url': a['href'],
        'speakers': []
    }
    first_sp = True
    for speaker in item.select('.list-item-speakers-container .speaker'):
        itemOut['speakers'].append({
            'moderator': bool(first_sp and speaker.find_previous_sibling('span', text='Moderator')),
            'name': speaker.get_text().strip(),
            'url': speaker.a['href'],
        })
        first_sp = False
    byTitle[title] = byTitle.get(title, []) + [itemOut]

json.dump(byTitle, sys.stdout)
