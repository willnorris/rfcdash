#!/usr/bin/env python

import os, re, sqlite3, urllib
from bs4 import BeautifulSoup, NavigableString, Tag 

db = sqlite3.connect('rfc.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

DOCUMENTS_DIR = os.path.join('rfc.docset', 'Contents', 'Resources', 'Documents')
HTML_DIR = os.path.join('tools.ietf.org', 'html')

for filename in os.listdir(os.path.join(DOCUMENTS_DIR, HTML_DIR)):
    page = open(os.path.join(DOCUMENTS_DIR, HTML_DIR, filename)).read()

    soup = BeautifulSoup(page, 'html5lib')

    for tag in soup.find_all('title'):
        name = tag.text.strip()

        if len(name) > 0:
            path = os.path.join(HTML_DIR, filename)
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Guide', path))
            print 'name: %s, path: %s' % (name, path)

    for tag in soup.find_all('span'):
        if tag.get('class'):
            for c in tag.get('class'):
                if c in ['h2', 'h3', 'h4', 'h5', 'h6']:
                    dashAnchor = tag.find('a', class_='dashAnchor')
                    if dashAnchor:
                        continue

                    text = tag.text.strip()
                    text = text.replace(u'\xa0', u' ') # convert non-breaking space to regular space

                    #print 'adding toc tag for section: %s' % text
                    name = '//apple_ref/Section/' + urllib.quote(text, '')
                    dashAnchor = BeautifulSoup('<a name="%s" class="dashAnchor"></a>' % name).a
                    tag.insert(0, dashAnchor)

    fp = open(os.path.join(DOCUMENTS_DIR, HTML_DIR, filename), 'w')
    fp.write(str(soup))
    fp.close()

db.commit()
db.close()
