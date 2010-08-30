#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import csv
import urllib2
import BeautifulSoup

OUTPUT = 'output.csv'
TITLE = [
         u'Фамилия',
         u'Имя',
         u'Отчество',
         u'День рождения',
         u'Должность?',
         u'Состоит в комитетах',
         u'Дата подтверждения полномочий',
         u'Срок окончания полномочий',
         u'Адрес email',
         u'Телефоны',
         u'Адрес приемной в субъекте Российской Федерации',
         u'Телефоны приемной в субъекте Российской Федерации',
         u'ID региона'
         ]
HOST = 'http://www.council.gov.ru'
START_URL = '/staff/members/persons/'
PAGE_ENCODING = 'cp1251'

def writerow(data):
    data = [value.encode('utf-8').strip() for value in data]
    output.writerow(data)

output = csv.writer(open(OUTPUT, 'wb'), delimiter=';', quotechar='"', )
writerow(TITLE)

start_connection = urllib2.urlopen(HOST + START_URL + 'index.html')
start_page = ''.join(start_connection)
start_soup = BeautifulSoup.BeautifulSoup(start_page)
start_links = start_soup.findAll('a', title=re.compile('^\d{1,2}$'), href=re.compile('^\w{1,3}/index.html$'))

letters = [start_soup]

for link in start_links:
    connection = urllib2.urlopen(HOST + START_URL + link['href'])
    letters.append(BeautifulSoup.BeautifulSoup(connection))

people = []
for soup in letters:
    links = soup.findAll('a', href=re.compile('^../(../)?functionary'))
    for link in links:
        last_name = ''
        first_name = ''
        patronymic = ''
        birthday = ''
        title = ''
        started_at = ''
        expires_at = ''
        email = ''
        phones = ''
        office_address = ''
        office_phone = ''
        region_id = ''

        title = link.parent.findNextSibling().contents[0].strip()

        connection = urllib2.urlopen(HOST + START_URL + link['href'].replace('../../', '../'))
        page = ''.join([s.decode(PAGE_ENCODING) for s in connection])
        person_soup = BeautifulSoup.BeautifulSoup(page)
        name_tag = person_soup.find('h2')

        name = name_tag.string.strip()
        names = name.split(' ')
        last_name = names[0]
        first_name = names[1]
        if len(names) > 2:
            patronymic = names[2] 

        tag = name_tag.findNextSibling().findNextSibling()

        birthday = tag.contents[0][-10:]

        committees = []
        for committee in tag.findAll('a'):
            committees.append(committee.string.strip())

        expires_at = tag.contents[-1]
        match = re.compile('.*:(.+)').search(expires_at)
        if match:
            expires_at = match.group(1).strip()

        started_at = tag.contents[-3][-10:]

        h3s = person_soup.findAll('h3')
        contacts_tag = h3s[1].findNextSibling()

        phones = contacts_tag.contents[0].strip()[5:]

        email_tag = contacts_tag.find('a')
        if email_tag:
            email = email_tag.string.strip()

        if len(h3s) > 2:
            office_tag = h3s[2].findNextSibling()

            office_address = office_tag.contents[0].strip().replace('\n', ' ')

            office_phone = office_tag.contents[2].strip()

        region_tag = person_soup.find('a', href=re.compile('^subject'))

        region_id = region_tag['href']
        match = re.compile('(\d+)').search(region_id)
        if match:
            region_id = match.group(1)

        writerow([
                 last_name,
                 first_name,
                 patronymic,
                 birthday,
                 title,
                 ', '.join(committees),
                 started_at,
                 expires_at,
                 email,
                 phones,
                 office_address,
                 office_phone,
                 region_id
                 ])

