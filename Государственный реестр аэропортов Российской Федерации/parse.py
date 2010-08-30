#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import csv
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
CONTENTS_URL = 'http://www.favt.ru/ap/ap_rga/'
ENCODING = 'cp1251'
TITLE = [
    u'Управление',
    u'Реестровый номер',
    u'Номер сертификата соответствия аэропорта',
    u'Наименование юридического лица',
    u'Наименование аэропорта',
]

def writeRow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writeRow(TITLE)

connection = urllib2.urlopen(CONTENTS_URL)
contents = BeautifulSoup(connection, fromEncoding=ENCODING, convertEntities=BeautifulSoup.HTML_ENTITIES)
tables = contents.findAll('table', {'class': 'TblListBrd'})

for table in tables:
    region = ''
    region_node = table.parent.findPreviousSibling().findPreviousSibling().findPreviousSibling()
    if region_node.string != None:
        region = re.sub(r'\s.*', '', region_node.string)
    
    rows = table.findAll('tr')[1:]
    for row in rows:
        cells = row.findAll('td')[1:]
        values = [' '.join(cell.findAll(text=True)).replace('\n', ' ') for cell in cells]
        values.insert(0, region)
        if values[2] != u'  3  ' and values[2] != u'  5  ':
            writeRow(values)