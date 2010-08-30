#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import csv
import urllib2
from BeautifulSoup import BeautifulSoup

OUTPUT = 'output.csv'
TITLE = [
         u'Фамилия',
         u'Имя',
         u'Отчество',
         u'День рождения',
         u'Выдвинувшая партия',
         u'Фракция и должность',
         u'Состоит в комитетах',
         u'Дата начала полномочий',
         u'Адрес сайта',
         ]
DOMAIN = 'http://www.duma.gov.ru/'
PATH_TEMPLATE = 'index.jsp?t=deputat/%s.html'
PAGE_ENCODING = 'cp1251'

def whitespace(string):
    return re.sub('\s+', ' ', string)
    
def camelCase(string):
    string = re.sub(u'ЕДИНАЯ РОССИЯ', u'Единая Россия', string)
    string = re.sub(u'СПРАВЕДЛИВАЯ РОССИЯ: РОДИНА/ПЕНСИОНЕРЫ/ЖИЗНЬ', u'Справедливая Россия: родина/пенсионеры/жизнь', string)
    return re.sub(u'СПРАВЕДЛИВАЯ РОССИЯ', u'Справедливая Россия', string)
    
def parseBirthday(birthday):
    birthday = re.sub(u'Родилась|Родился', '', whitespace(birthday))
    birthday = re.sub(u'года', '', birthday)
    birthday = re.sub(u' января ', '/01/', birthday)
    birthday = re.sub(u' февраля ', '/02/', birthday)
    birthday = re.sub(u' марта ', '/03/', birthday)
    birthday = re.sub(u' апреля ', '/04/', birthday)
    birthday = re.sub(u' мая ', '/05/', birthday)
    birthday = re.sub(u' июня ', '/06/', birthday)
    birthday = re.sub(u' июля ', '/07/', birthday)
    birthday = re.sub(u' августа ', '/08/', birthday)
    birthday = re.sub(u' сентября ', '/09/', birthday)
    birthday = re.sub(u' октября ', '/10/', birthday)
    birthday = re.sub(u' ноября ', '/11/', birthday)
    birthday = re.sub(u' декабря ', '/12/', birthday)
    return birthday
    
def writeRow(data):
    data = [whitespace(value.strip()).encode('utf-8') for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT, 'w'), delimiter=';', quotechar='"', )
writeRow(TITLE)


for index in range(1, 28):
    url = DOMAIN + (PATH_TEMPLATE % index);
    connection = urllib2.urlopen(url)
    soup = BeautifulSoup(connection, fromEncoding=PAGE_ENCODING)
    links = soup.findAll('a', href=re.compile('^index\.jsp\?t=deputat/\d{5,}\.html$'))
    
    for link in links:
        soup = None
        while soup == None:
            try:
                connection = urllib2.urlopen(DOMAIN + link['href'])
                soup = BeautifulSoup(connection, fromEncoding=PAGE_ENCODING)
            except: 
                pass
        
        last_name = ''
        first_name = ''
        patronymic = ''
        birthday = ''
        origin = ''
        member = ''
        started_at = ''
        site = ''

        name_tag = soup.find('div', {'class': 'fiodep'})
        names = name_tag.string.split(' ')
        last_name = names[0]
        first_name = names[1]
        if len(names) > 2:
            patronymic = names[2]

        tag = name_tag.findNext('div')
        origin = whitespace(' '.join(tag.findAll(text=True)))
        origin = re.sub(u'Депутат Государственной Думы избран в составе федерального списка кандидатов, выдвинутого (Всероссийской )?[Пп]олитической партией', '', origin)
        origin = camelCase(origin)
        origin = re.sub(' - ', '-', origin)
        
        tag = tag.findNext('div')
        member = camelCase(tag.string)
        
        tag = tag.findNext('ul')
        committees = []
        for committee in tag.findAll('li'):
            committee_string = whitespace(committee.string.strip())
            if len(committee_string) > 0:
                committees.append(committee_string)
            
        tag = tag.findNext('div')
        birthday = parseBirthday(tag.string)
        
        tag = soup.find('img', src='graphics/znakdep.gif')
        if tag:
            site = tag.parent['href']
            
        tag = soup.find('blockquote')
        texts = tag.findAll(text=True)
        started_at = whitespace(texts[-1])
        started_at = re.sub(u'Дата начала полномочий:', '', started_at)

        writeRow([
             last_name,
             first_name,
             patronymic,
             birthday,
             origin,
             member,
             ' | '.join(committees),
             started_at,
             site
             ])
