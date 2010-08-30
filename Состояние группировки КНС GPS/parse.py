#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import csv
import urllib2
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
TITLE = [
        u'Номер по реестру',
        u'Наименование государственного первичного эталона',
        u'Институт-хранитель государственного первичного эталона',
         ]
START_URL = 'http://www.gost.ru/wps/portal/pages.root.Activity?WCM_GLOBAL_CONTEXT=/gost/GOSTRU/Activity/Metrology/StateMasterBase'

def writerow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writerow(TITLE)

start_connection = urllib2.urlopen(START_URL)
start_page = ''.join(start_connection)
start_page = start_page.replace('valign="top"style', 'valign="top" style')
start_soup = BeautifulSoup(start_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
table = start_soup.find('table', {'class': 'MsoNormalTable'})
rows = table.findAll('tr')
rows = rows[1:]

for row in rows:
    # region = '' do not reset region: it goes for a few next items
    title = ''
    number = ''
    date = ''
    number2 = ''

    spans = row.findAll('td')[1:]
    strings = map(lambda span: ' '.join(span.findAll(text=True)), spans)
    strings = map(lambda s: re.sub(r'\s+', ' ', s).strip().replace(u'¸', u'–'), strings)
    strings = filter(lambda s: len(s) > 0, strings)
    writerow(strings)
