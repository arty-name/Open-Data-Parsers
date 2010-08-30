#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import csv
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
CONTENTS_URL = 'http://www.cikrf.ru/newsite/politparty/reg_politparty.jsp'
ENCODING = 'cp1251'
TITLE = [
    u'Наименование',
    u'Дата регистрации',
    u'Регистрационный номер',
    u'Адрес интернет-сайта',
]

def writeRow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writeRow(TITLE)

connection = urllib2.urlopen(CONTENTS_URL)
contents = BeautifulSoup(connection, fromEncoding=ENCODING, convertEntities=BeautifulSoup.HTML_ENTITIES)
header = contents.find('h3')
table = header.findNext('table')
rows = table.findAll('tr')[1:]

for row in rows:
    cells = row.findAll('td')[1:]
    values = [' '.join(cell.findAll(text=True)).replace('\n', ' ') for cell in cells]
    writeRow(values)