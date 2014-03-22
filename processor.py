#!/usr/bin/env python

from xml.dom import minidom
import sys
from subprocess import Popen, PIPE
from optparse import OptionParser


def levenshtein(s, t):
    m, n = len(s), len(t)
    D = [range(n + 1)] + [[x + 1] + [None] * n for x in xrange(m)]
    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1):
            if s[i - 1] == t[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                before_insert = D[i][j - 1]
                before_delete = D[i - 1][j]
                before_change = D[i - 1][j - 1]
                D[i][j] = min(before_insert, before_delete, before_change) + 1
    prescription = []
    prescription_s = []
    prescription_t = []
    i, j = m, n
    while i and j:
        insert = D[i][j - 1]
        delete = D[i - 1][j]
        match_or_replace = D[i - 1][j - 1]
        best_choice = min(insert, delete, match_or_replace)
        if best_choice == match_or_replace:
            if s[i - 1] == t[j - 1]:  # match
                prescription.append('M')
            else: # replace
                prescription.append('R')
            prescription_s.append(s[i - 1])
            prescription_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif best_choice == insert:
            prescription.append('I')
            prescription_s.append('-')
            prescription_t.append(t[j - 1])
            j -= 1
        elif best_choice == delete:
            prescription.append('D')
            prescription_s.append(s[i - 1])
            prescription_t.append('-')
            i -= 1
    prescription.reverse()
    prescription_s.reverse()
    prescription_t.reverse()
    return D[m][n]


def tomita(article):
	p = Popen(["tomita/tomita", "tomita/config.proto"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate(article)
	return stdout


def process(xml, article):
	fdo = xml.getElementsByTagName('fdo_objects')[0]
	doc = fdo.getElementsByTagName('document')[0]
	facts = doc.getElementsByTagName('facts')[0]
	for pol in facts.getElementsByTagName('Politician'):
		start = int(pol.getAttribute('pos'))
		sz = int(pol.getAttribute('len'))
		who = pol.getElementsByTagName('Who')[0]
		name = who.getAttribute('val').lower().split()
		yield start, start + sz, name


def compare_names(name1, name2):
	eqs = 0
	for e1 in name1:
		for e2 in name2:
			dist = levenshtein(e1, e2)
			if dist <= 1:
				eqs += 1
	return eqs >= 2


def get_data(politicians, csvfile):
	with open(csvfile, "r") as db:
		for line in db:
			data = line.rstrip('\n').decode('utf8').split(u';')
			name = data[0].lower().split()
			
			for s, e, ename in politicians:
				if compare_names(ename, name):
					yield s, e, name, data[1].strip(), data[2].replace(u'[', u'').strip()


def insert(article, data):
	offset = 0
	for start, end, name, dr, par in sorted(data, key=lambda x: x[1]):
		string = u' '.join(name) + u', ' + dr
		if par != u'':
			string += u', ' + par
		article = article[:offset + end] + u'(' + string + u')' + article[offset + end:]
		offset += len(string) + 2

	return article


def main():
	parser = OptionParser()
	parser.add_option("-d", "--db", dest="db", metavar="FILE", default="result.csv")
	(options, args) = parser.parse_args()
	if not args:
		print 'Select file'
		return

	with open(args[0], "r") as artfile:
		article = artfile.read()

	tout = tomita(article)

	article = article.decode('utf8')

	politicians = list(process(minidom.parseString(tout), article))

	data = get_data(politicians, options.db)

	result = insert(article, list(data))
	print result


if __name__ == '__main__':
	main()
