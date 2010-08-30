#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import csv
import urllib2

OUTPUT_CSV = 'output.csv'
TITLE = [
        u'Название',
        u'Регион',
        u'Район',
        u'Населённый пункт',
        u'Адрес',
        u'Широта',
        u'Долгота',
        u'Телефоны',
        u'Время работы',
         ]
START_URL = 'http://www.yadonor.ru/common/js/google_maps/google.php'

MARKER_RE = re.compile('var point = new GLatLng\((.*),(.*)\);')
DATA_RE = re.compile(".*<b>(.*)</b></font><br>(.*)<br></div>',markerOptions\);")
PART_RE = re.compile('(.*?): (.*)')

def writerow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writerow(TITLE)

start_connection = urllib2.urlopen(START_URL)

lines = []

for line in start_connection:
    lines.append(line)

while not lines[0].startswith('var point'):
	lines = lines[1:]
	
while len(lines) > 0:
	title = ''
	parts = ''
	region = ''
	subregion = ''
	town = ''
	address = ''
	lat = ''
	lng = ''
	phone = ''
	times = ''

	coords = lines[0];
	data = lines[1]
	lines = lines[3:]
	
	match = MARKER_RE.search(coords)
	if not match:
		continue
	
	lat = match.group(1)
	lng = match.group(2)
	
	match = DATA_RE.search(data.decode('utf-8'))
	if not match:
		continue
	
	title = match.group(1)
	parts = match.group(2).split('<br>')
	
	for part in parts:
		match = PART_RE.search(part)
		if not match:
			continue
		k = match.group(1)
		v = match.group(2).strip()
		if k == u'Регион':
			region = v
		if k == u'Район':
			subregion = v
		if k == u'Город':
			town = v
		if k == u'Адрес':
			address = v
		if k == u'Телефон' and len(phone) == 0:
			phone = v
		if k == u'Время работы':
			times = v
	
	writerow([
		title,
		region,
		subregion,
		town,
		address,
		lat,
		lng,
		phone,
		times
		])
	
	

