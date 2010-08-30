#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import csv
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
CONTENTS_URL = 'http://www.federalspace.ru/main.php?id=10&year=%s'
LAST_INDEX = 14
ENCODING = 'cp1251'
TITLE = [
    u'Дата',
    u'Запуск',
    u'Космодром',
    u'Стартовый комплекс',
    u'Ракета-носитель',
    u'Результат',
]

def writeRow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writeRow(TITLE)

for index in range(0, LAST_INDEX + 1):
    connection = urllib2.urlopen(CONTENTS_URL % index)
    contents = BeautifulSoup(connection, fromEncoding=ENCODING, convertEntities=BeautifulSoup.HTML_ENTITIES)
    span = contents.find('span', {'class': 'launch_title'})
    table = span.findNextSibling('table')
    
    rows = table.findAll('tr')[1:]
    for row in rows:
        cells = row.findAll('td')
        values = [' '.join(cell.findAll(text=True)).replace('\n', ' ') for cell in cells]
        writeRow(values)
