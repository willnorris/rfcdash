#!/usr/bin/env python

import copy, os, re, sqlite3, string, urllib
from bs4 import BeautifulSoup, NavigableString, Tag 

DOCUMENTS_DIR = os.path.join('RFCs.docset', 'Contents', 'Resources', 'Documents')
HTML_DIR = os.path.join('tools.ietf.org', 'html')
RFC_DIR = os.path.join('tools.ietf.org', 'rfc')

db = sqlite3.connect('RFCs.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')


# build search index and tables of contents
for filename in os.listdir(os.path.join(DOCUMENTS_DIR, HTML_DIR)):
    page = open(os.path.join(DOCUMENTS_DIR, HTML_DIR, filename)).read()

    soup = BeautifulSoup(page, 'html5lib')

    # add each RFC to the search index, using the contents of the <title> tag
    for tag in soup.find_all('title'):
        name = tag.text.strip()

        if len(name) > 0:
            path = os.path.join(HTML_DIR, filename)
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Guide', path))
            print 'name: %s, path: %s' % (name, path)

    # support table of contents by adding dash <a> tags for each header in the file
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


# build index file
index = open(os.path.join(DOCUMENTS_DIR, RFC_DIR, 'index.html')).read()
soup = BeautifulSoup(index)

# strip unecessary sidebar and javascript
content = soup.find('div', class_='content').extract()
soup.find('div', class_='page').append(content)
[t.extract() for t in soup(['script', 'table'])]

# rewrite all absolute links for RFCs to be local relative links
for a in soup('a'):
    if u'href' in a.attrs and a[u'href'].startswith(u'http://tools.ietf.org'):
        id = string.split(a[u'href'], '/')[-1].lstrip("0")
        a[u'href'] = "../html/rfc" + id + ".html"

# unfortunately, bs4 doesn't seem to be able to find non-standard tag names like <block> so we have
# to use a regex :(
soup = re.sub(r"<block>.*<\/block>", "", str(soup), flags=re.DOTALL)

fp = open(os.path.join(DOCUMENTS_DIR, RFC_DIR, 'index.html'), 'w')
fp.write(soup)
fp.close()
