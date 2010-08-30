#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import csv
import urllib2
import BeautifulSoup

OUTPUT = 'output.csv'
TITLE = [u'АВС/DEF', u'От', u'До', u'Емкость', 	u'Оператор', u'Регион']
HOST = 'http://www.rossvyaz.ru'
START_URL = '/activity/num_resurs/registerNum/'
PAGE_ENCODING = 'cp1251'
RE = re.compile('<tr>\s*<td>(.*)</td>\s*<td>(.*)</td>\s*<td>(.*)</td>\s*<td>(.*)</td>\s*<td>(.*)</td>\s*<td>(.*)</td>\s*</tr>')

def writerow(data):
    data = [value.encode('utf-8').strip() for value in data]
    output.writerow(data)

start_connection = urllib2.urlopen(HOST + START_URL)
start_page = ''.join(start_connection)
start_soup = BeautifulSoup.BeautifulSoup(start_page)
start_links = start_soup.findAll('a', href=re.compile('^/docs/num/'))

output = csv.writer(open(OUTPUT, 'wb'), delimiter=';', quotechar='"')
writerow(TITLE)

for link in start_links:
    link_url = HOST + link['href']
    link_connection = urllib2.urlopen(link_url)
    for line in link_connection:
        if not line.startswith('<tr>'):
            continue
        decoded = line.decode(PAGE_ENCODING)
        match = RE.search(decoded)
        if not match:
            print sys.stderr, 'Nonmatched: ' + line
            continue
        writerow([match.group(index) for index in range(1,7)])
