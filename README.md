# rfcdash

rfcdash is a docset for [Dash.app][] containing all published RFCs from the IETF.

![Dash screenshot showing RFC 2324](screenshot.png)


## Installing

Install by opening Dash.app preferences, switch to `Downloads`, open `User Contributed`, and search
for "RFCs".

If you prefer, you can also subscribe to the docset feed URL at:

    https://raw.githubusercontent.com/willnorris/rfcdash/master/RFCs.xml

The unpacked docset will take a little over 700 MB on disk.


## Updating the Docset

Most people generally shouldn't need to update the docset on their own. It's generally easier for me
to do it, so these notes are mainly for myself.  If you notice that the docset is missing an RFC
that you need, just [open an issue][] and I'm happy to update it.

Updating requires:

 - [rsync](https://rsync.samba.org/)
 - Python 3, with [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)
   and [html5lib](https://pypi.python.org/pypi/html5lib) modules

To grab the latest RFCs, run the [`sync`][] script. This will use rsync to fetch all RFCs from the IETF website. This is necessary because new RFCs sometimes update or obsolete older RFCs, so we grab everything to make sure we have the latest.

The script might need running a few times because of rate limiting, but keep going.

Once everything is downloaded, run [`rebuild.py`][] to rebuild the search index, and add tables of contents to each RFC.

It has a pyproject.toml file to define the dependencies, so you can choose your own adventure as to how to install the dependencies and run [`rebuild.py`][]. But `uv run rebuild.py` is straightforward.

## License

The RFCs themselves contained in this repo are subject to the [IETF IPR policy][].  The scripts used
to construct the docset are released under an [Apache 2.0 license][].

[Dash.app]: http://kapeli.com/dash
[open an issue]: https://github.com/willnorris/rfcdash/issues
[`sync`]: https://github.com/willnorris/rfcdash/blob/master/sync
[`rebuild.py`]: https://github.com/willnorris/rfcdash/blob/master/rebuild.py
[IETF IPR policy]: https://www.ietf.org/ipr/
[Apache 2.0 license]: LICENSE
