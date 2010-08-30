#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import csv
import urllib2
import json
import BeautifulSoup

OUTPUT_CSV = 'output.csv'
OUTPUT_JSON = 'output.json'
TITLE = [
        u'Название',
        u'Номер аттестата аккредитации',
        u'Срок действия аттестата',
        u'Адрес центра',
        u'Телефоны центра',
        u'Руководитель',
         ]
START_URL = 'http://www.rossvyaz.ru/activity/correlation/certification/registerLabs/'
PAGE_ENCODING = 'cp1251'

def writerow(data):
    data = [value.encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writerow(TITLE)

start_connection = urllib2.urlopen(START_URL)
start_page = ''.join(start_connection)
start_soup = BeautifulSoup.BeautifulSoup(start_page)
start_links = start_soup.findAll('a', href=re.compile('^./\?id=\d+$'))

centers = []

for link in start_links:
    connection = urllib2.urlopen(START_URL + link['href'][2:])
    soup = BeautifulSoup.BeautifulSoup(connection)

    title = ''
    accreditation_type = ''
    date = ''
    address = ''
    phones = ''
    head = ''

    title = soup.find('h1').string
    title, accreditation_type, date = title.split(',')
    title = title.replace(u'╚', u'«').replace(u'╩', u'»').strip()
    date = date.strip()

    match = re.search('(\S+)$', accreditation_type)
    accreditation_type = match.group(1)

    h3s = soup.findAll('h3')

    areas_tag = h3s[0].findNextSibling()
    areas = map(lambda node: node.string.strip(), areas_tag.findAll(text=True))

    address_tag = h3s[1].findNextSibling()

    address = address_tag.contents[0].strip()

    if len(address_tag.contents) > 2:
        phones = address_tag.contents[2].strip()
    else:
        parts = address.split('\n')
        address = parts[0]
        phones = parts[1]

    head = h3s[2].findNextSibling().string.strip()

    writerow([
             title,
             accreditation_type,
             date,
             address,
             phones,
             head,
             ])
    centers.append({
        'title': title,
        'accreditation_type': accreditation_type,
        'date': date,
        'address': address,
        'phones': phones,
        'head': head,
        'areas': areas
    })

open(OUTPUT_JSON, 'wb').write(json.dumps(centers, indent=2, ensure_ascii=False).encode('utf-8'))