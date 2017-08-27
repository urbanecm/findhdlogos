#!/usr/bin/env python
#-*- coding: utf-8 -*-

FAMILY = 'wikiquote'

import os

f = open('/home/urbanecm/Documents/wikimedia/developer/operations/mediawiki-config/wmf-config/InitialiseSettings.php')
lines = []
for line in f.readlines():
    if '2x' in line and FAMILY in line:
        lines.append(line.replace('\n', '').replace('\t', ''))
f.close()

files = os.listdir('logos')
for f in files:
    if '2x' in f:
        wiki = f.replace('-2x.png', '')
        lines.append("'@@WIKI@@' => [ '1.5x' => '/static/images/project-logos/@@WIKI@@-1.5x.png', '2x' => '/static/images/project-logos/@@WIKI@@-2x.png' ], // T150618".replace('@@WIKI@@', wiki))

lines.sort()
for line in lines:
    print line
