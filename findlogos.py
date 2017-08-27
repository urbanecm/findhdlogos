#!/usr/bin/env python
#-*- coding: utf-8 -*-

FAMILY = 'wikiquote'
DBLIST = FAMILY + '.dblist'
if DBLIST == 'wiki.dblist':
    DBLIST = 'wikipedia.dblist'
COMLOGOS = {
    'wiki': 'File:Wikipedia-logo-v2-@@LANG@@.svg',
    'wikibooks': 'File:Wikibooks-logo-@@LANG@@.svg',
    'wikinews': 'File:WikiNews-Logo-@@LANG@@.svg',
    'wikiquote': 'File:Wikiquote-logo-@@LANG@@.svg',
    'wikisource': 'File:Wikisource-logo-@@LANG@@.svg',
    'wikiversity': 'File:Wikiversity-logo-@@LANG@@.svg',
    'wikivoyage': 'File:Wikivoyage-Logo-v3-@@LANG@@.svg',
    'wiktionary': 'File:Wiktionary-logo-@@LANG@@.svg',
}

import os
import requests
import shutil

logos = os.listdir('/home/urbanecm/Documents/wikimedia/developer/operations/mediawiki-config/static/images/project-logos')
hdprojects = []
for logo in logos:
    if FAMILY in logo and '2x' in logo:
        hdprojects.append(logo)

f = open('/home/urbanecm/Documents/wikimedia/developer/operations/mediawiki-config/dblists/' + DBLIST)
allprojects = f.read().split('\n')
f.close()
if allprojects[-1] == '':
    allprojects.pop()

nonhdprojects = []
for project in allprojects:
    if project not in hdprojects:
        nonhdprojects.append(project)

try:
    shutil.rmtree('logos')
except:
    pass

os.mkdir('logos')
for project in nonhdprojects:
    lang = project.replace(FAMILY, '')
    filename = COMLOGOS[FAMILY].replace('@@LANG@@', lang)
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'imageinfo',
        'titles': filename,
        'iiprop': 'url'
    }
    r = requests.get('https://commons.wikimedia.org/w/api.php', params=params)
    data = r.json()['query']['pages']
    if data.keys()[0] == u'-1':
        print 'Skipping ' + project
        continue
    url = data[data.keys()[0]]['imageinfo'][0]['url']
    basicsize = 135
    sizes = [1.5, 2]
    for size in sizes:
        px = int(round(size*basicsize))
        pngurl = url.replace('wikipedia/commons', 'wikipedia/commons/thumb') + '/' + str(px) + 'px-' + filename.replace('File:', '') + '.png'
        r = requests.get(pngurl)
        with open('logos/' + lang + DBLIST.replace('.dblist', '') + '-' + str(size) + 'x.png', 'wb') as f:
            f.write(r.content)

os.system('optipng logos/*.png')
