#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import csv
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
CONTENTS_URL = 'http://www.favt.ru/airl/airl_r/'
ENCODING = 'cp1251'
TITLE = [
    u'Номер сертификата',
    u'Название',
    u'Полное название',
    u'Юридический адрес',
    u'Аэропорты базирования',
    u'Контролирующее МТУ',
    u'Типы ВС'
]

def writeRow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writeRow(TITLE)

connection = urllib2.urlopen(CONTENTS_URL)
contents = BeautifulSoup(connection, fromEncoding=ENCODING)
links = contents.findAll('a', href=re.compile('index.php\?idmd='))

for link in links:
    connection = urllib2.urlopen(CONTENTS_URL + link['href'])
    contents = BeautifulSoup(connection, fromEncoding=ENCODING)
    table = contents.find('table', cellpadding='3')
    rows = table.findAll('tr')
    rows = rows[1:]
    
    for row in rows:
        writeRow([' '.join(td.findAll(text=True)) for td in row.findAll('td')])