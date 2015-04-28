rfcdash
=======

rfcdash is a docset for [Dash.app][] containing all published RFCs from the IETF.

![Dash screenshot showing RFC 2324](screenshot.png)


Installing
----------

Install by opening Dash.app preferences, switch to `Downloads`, open `User Contributed`, and search
for "RFCs".  If you prefer, you can also subscribe to the docset feed URL at
`https://raw.githubusercontent.com/willnorris/rfcdash/master/RFCs.xml`.  The unpacked docset will
take a little over 500 MB on disk.


Updating the Docset
-------------------

Most people generally shouldn't need to update the docset on their own. It's generally easier for me
to do it, so these notes are mainly for myself.  If you notice that the docset is missing an RFC
that you need, just [open an issue][] and I'm happy to update it.

Updating requires:

 - [httrack](http://www.httrack.com/)
 - python, with [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)
   and [html5lib](https://pypi.python.org/pypi/html5lib) modules

To grab the latest RFCs, run the [`sync`][] script.  This will use httrack to download all published
RFCs from the IETF website.  This typically takes about half an hour because it downloads everything
every time.  This is necessary because new RFCs sometimes update or obsolete older RFCs, so we grab
everything to make sure we have the latest.

Once everything is downloaded, run [`rebuild.py`][] to build the index file, rebuild the search
index, and add tables of contents to each RFC.

Manually update the index page to use relative links by running:

    gsed -r -i 's/href="http:\/\/tools\.ietf\.org\/html\/0*([[:alnum:]]+)"/href="..\/html\/rfc\1\.html"/g' RFCs.docset/Contents/Resources/Documents/tools.ietf.org/rfc/index.html

[Dash.app]: http://kapeli.com/dash
[open an issue]: https://github.com/willnorris/rfcdash/issues
[`sync`]: https://github.com/willnorris/rfcdash/blob/master/sync
[`rebuild.py`]: https://github.com/willnorris/rfcdash/blob/master/rebuild.py
