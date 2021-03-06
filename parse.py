#!/usr/bin/env python
#-*- coding: utf-8 -*-

from xml.dom import minidom
import os

def findData(dates, record):
	list = record.split('=')
	for date in dates:
		if date in list[0]:
			try:	
				return list[1]
			except:
				return None
	return None


def compare(politics, record):
	for politic in politics:
		if (u'{{' + politic) in record:
			return True
	return False

def main():
	countRecords = 10
	politics = [u'Политик', u'Государственный деятель']
	dates = [u'дата рождения', u'Дата рождения']
	parts = [u'Партия', u'партия']
	works = [u'деятельность', u'Деятельность', u'должность']
	cships = [u'гражданство', u'гражданство']

	f = open('result.csv', 'w+')
	
	xml = minidom.parse(os.path.join('../', 'ruwiki-20140306-pages-articles1.xml'))
#	xml = minidom.parse(os.path.join('../', 'test.xml'))
	pages = xml.getElementsByTagName('mediawiki')[0].childNodes
	for page in pages:
		if page.localName == 'page':
			text = page.getElementsByTagName('text')
			if text.length > 0 and text[0].childNodes.length > 0:
				list = text[0].childNodes[0].nodeValue.split('|')
				count = 0
				flag = False
				title = None
				date = None
				part = None
				work = None
				cship = None
				for record in list:
					if count >= countRecords and not flag:
						break				

					if  not flag and compare(politics, record):
						title = page.getElementsByTagName('title')[0].childNodes[0].nodeValue.replace(',','')
						flag = len(title.split(' '))==3

					if flag and date is None:
						date = findData(dates, record)

					if flag and part is None:
						part = findData(parts, record)

					if flag and work is None:
						work = findData(works, record)

					if flag and cship is None:
						cship = findData(cships, record)
					
					if not part is None and not title is None and not date is None and not work is None and not cship is None:
						break

					count = count+1
				if flag:
					try:
						print title

						if title is None:
							f.write(';')					
						if not title is None:
							f.write('%s;' % title.replace('\n','').encode('utf8'))

						if date is None:
							f.write(';')					
						if not date is None:
							f.write('%s;' %  date.replace('\n','').encode('utf8'))

						if work is None:
							f.write(';')					
						if not work is None:
							f.write('%s;' %  work.replace('\n','').encode('utf8'))

						if cship is None:
							f.write(';')					
						if not cship is None:
							f.write('%s;' %  cship.replace('\n','').encode('utf8'))

						if part is None:
							f.write('\n')					
						if not part is None:
							f.write('%s\n' % part.replace('\n','').encode('utf8'))
					except:
						r=0

	print 'complete'
	f.close()

if __name__ == '__main__':
	main()
