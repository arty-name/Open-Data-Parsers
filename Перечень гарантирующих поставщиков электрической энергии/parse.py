#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import csv
import urllib2
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
TITLE = [
        u'Субъект РФ',
        u'Наименование организации',
        u'Рег. № в Реестре',
        u'Дата приказа ФСТ России',
        u'Номер приказа ФСТ России',
         ]
START_URL = 'http://www.fstrf.ru/about/activity/gp/perechen'
PAGE_ENCODING = 'cp1251'

def writerow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writerow(TITLE)

start_connection = urllib2.urlopen(START_URL)
start_page = ''.join(start_connection)
start_soup = BeautifulSoup(start_page, fromEncoding=PAGE_ENCODING, convertEntities=BeautifulSoup.HTML_ENTITIES)
table = start_soup.find('table', {'class': 'ramka'})
rows = table.findAll('tr')
rows = rows[2:]

for row in rows:
    # region = '' do not reset region: it goes for a few next items
    title = ''
    number = ''
    date = ''
    number2 = ''

    cells = row.findAll('td')[1:]
    Ps = map(lambda cell: cell.find('p'), cells)
    strings = map(lambda p: p and ''.join(p.find(text=True)) or '', Ps)
    if len(strings[0]) > 3:
        region = strings[0]
    else:
        strings[0] = region

    writerow(strings)
