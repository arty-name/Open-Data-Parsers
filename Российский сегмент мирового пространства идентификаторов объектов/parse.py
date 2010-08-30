#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import csv
from BeautifulSoup import BeautifulSoup

OUTPUT_CSV = 'output.csv'
CONTENTS_URL = 'http://www.ctel.msk.ru/x500/OIDS/inform.htm'
ENCODING = 'cp1251'
TITLE = [
    u'Категория эмитента',
    u'Идентификатор',
    u'Имя',
    u'Организация-эмитент',
    u'Область использования',
]

def writeRow(data):
    data = [unicode(value).encode('utf-8').strip() for value in data]
    output.writerow(data)

def collapse(string):
    return re.sub('\s+', ' ', re.sub('^\s*-+\s*$', '', string))

output = csv.writer(open(OUTPUT_CSV, 'wb'), delimiter=';', quotechar='"', )
writeRow(TITLE)

connection = urllib2.urlopen(CONTENTS_URL)
contents = BeautifulSoup(connection, fromEncoding=ENCODING, convertEntities=BeautifulSoup.HTML_ENTITIES)
tables = contents.findAll('table')[2:]

for table in tables:
    category = ''
    category_node = table.findPrevious('h3')
    category = collapse(category_node.find(text=True))
    rowSpan = 1
    
    rows = table.findAll('tr')[1:]
    for row in rows:
        cells = row.findAll('td')
        
        if rowSpan > 1:
            rowSpan -= 1
            continue

        try:
            rowSpan = int(cells[0]['rowspan'])
        except:
            pass
        
        
        cells = cells[1:]
        
        if len(cells) <= 2:
            category = collapse(' '.join(cells[-1].findAll(text=True)))
            continue
        
        values = [collapse(' '.join(cell.findAll(text=True))) for cell in cells]
        values[0] = re.sub('\s+', '', values[0])
        values[1] = re.sub(u'[cсС]=', 'C=', values[1])
        values[1] = re.sub('=ru,', '=RU,', values[1])
        values[1] = re.sub('\s+=', '=', values[1])
        values[1] = re.sub('=\s+', '=', values[1])
        values[1] = re.sub('\s+,', ',', values[1])
        values[1] = re.sub(',\s+', ',', values[1])
        values[1] = re.sub(u'[«“”»]', '"', values[1])
        
        
        if ''.join(values).strip() == '':
            continue
        for value in values:
            if value.strip().strip('-') == '':
                value = '' 
        
        values.insert(0, category)
        
        writeRow(values)

            