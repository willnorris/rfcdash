#!/usr/bin/env python3

import json
import sqlite3
import urllib
from bs4 import BeautifulSoup
from pathlib import Path
from shutil import rmtree

DOCUMENTS_DIR = Path(
    "RFCs.docset", "Contents", "Resources", "Documents", "www.rfc-editor.org", "rfc"
)
METADATA_DIR = Path("rfcs")

db = sqlite3.connect("RFCs.docset/Contents/Resources/docSet.dsidx")
cur = db.cursor()

cur.execute("DROP TABLE IF EXISTS searchIndex;")
cur.execute(
    "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);"
)
cur.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")


# Remove existing HTML files
if DOCUMENTS_DIR.exists():
    rmtree(DOCUMENTS_DIR)
DOCUMENTS_DIR.mkdir()

# build search index and tables of contents
for html_path in METADATA_DIR.glob("*.html"):
    json_path = html_path.with_suffix(".json")
    metadata = json.loads(json_path.read_text())
    rfc_id = metadata["doc_id"]
    title = metadata["title"].strip()
    relative_path = f"www.rfc-editor.org/rfc/{html_path.name}"

    print(f"name: {title}, path: {relative_path}")

    # Add title of the RFC to search index
    cur.execute(
        "INSERT INTO searchIndex(name, type, path) VALUES (?, ?, ?);",
        (
            f"{rfc_id}: {title}",
            "Guide",
            relative_path,
        ),
    )

    contents = html_path.read_bytes()
    soup = BeautifulSoup(contents, "html5lib")

    # support table of contents by adding dash <a> tags for each header in the file
    for tag in soup.find_all("span"):
        if tag.get("class"):
            for c in tag.get("class"):
                if c in {"h2", "h3", "h4", "h5", "h6"}:
                    text = tag.text.strip()
                    # convert non-breaking space to regular space
                    text = text.replace("\xa0", " ")

                    # print 'adding toc tag for section: %s' % text
                    name = f"//apple_ref/cpp/Section/{urllib.parse.quote(text, '')}"
                    dashAnchor = BeautifulSoup(
                        f'<a name="{name}" class="dashAnchor"></a>',
                        features="html5lib",
                    ).a
                    tag.insert(0, dashAnchor)

    DOCUMENTS_DIR.joinpath(html_path.name).write_text(str(soup))

db.commit()
db.close()
