mimecat
=======

A catalogue for working with MIME types and extensions.

Introduction
============

I started the mimecat package in order to solve two problems at work: determine
if a given MIME type was supported by our product and determine potential
extensions given a MIME type.

My initial solution used the `mimetypes` package included with default Python
implementations. `mimetypes` worked fine, but I eventually encountered a problem
where I had two MIME types that could potentially have the same file
extensions. The implementation of `mimetypes` only permits an extension to be
associated with one type. I had a need to know all potential types, so I created
`mimecat.`

There are also other issues with `mimetypes`, but I don't want to bag on
it. [Other](https://mail.python.org/pipermail/python-dev/2009-July/090928.html)
[people](http://lucumr.pocoo.org/2009/3/1/the-1000-speedup-or-the-stdlib-sucks/),
more talented than I, have done that already.

My goals for `mimecat` are to keep track of MIME types, their associated
extensions, and allow inspection of their associations.

This module can be found at the [Python Package
Index](https://pypi.python.org/pypi/mimecat).

Installation
============

The easiest way to install is:

```shell
$ sudo pip install mimecat
```

If you want to install as part of a virtualenv:
```shell
(venv)$ pip install mimecat
```

If you want to install from the source tarball, download the source at the
[Python Package Index](https://pypi.python.org/pypi/mimecat) and execute:

```shell
$ sudo pip install mimecat-<version>.tar.gz
```



Usage
=====

Using `mimecat` is straightforward:

```python

>>> from mimecat import Catalogue
>>> cat = Catalogue() # this will search in a number of common locations for a
                      # mime.types file. Loading will stop on first successful
                      # load.
>>> "text" in cat.known_mediatypes # Media types are the first part of a
                                   # MIME type,
                                   # (see http://www.ietf.org/rfc/rfc2046.txt)
True

>>> "garbage" in cat.known_mediatypes
False

>>> "text/plain" in cat.known_mimetypes
True

>>> cat.get_extensions("text/plain")
['.txt', '.text', '.conf', '.def', '.list', '.log', '.in']

>>> cat.get_types("txt")
['text/plain']

>>> cat.get_types(".txt")
['text/plain']

>>> cat.get_extensions("text/garbage") # KeyError is raised for unknown types.
Traceback (most recent call last):     # This is also the case for get_types(...)
  File "<stdin>", line 1, in <module>
  File "mimecat.py", line 150, in get_extensions
    return self._types_to_exts[typename]
KeyError: 'text/garbage'

>>> cat = Catalogue("/path/to/mime.types") # Catalogues can be intialized with
                                           # a custom mime.types file



>>> cat = Catalogue(["/path/to/mime.types",             # A list of filenames
                     "/path/to/additional/mime.types"]) # can also be supplied.
                                                        # This will cause Catalogue
                                                        # to load all of them.

>>> cat.add_type("text/not-so-plain", [".special_text"]) # Add custom types
>>> "text/not-so-plain" in cat.known_mimetypes
True
>>> cat.get_types(".special_text")
['text/not-so-plain']
>>> cat.add_type("text/not-so-plain2", [".special_text"]) # types can share extensions
>>> cat.get_types(".special_text")
['text/not-so-plain', 'text/not-so-plain2']
```

Caveats
=======

One caveat really. `mimecat` currently has no support for obtaining MIME type
information from the Windows registry. I don't dispute the utility of having
this support, but I currently lack both the business need and the Windows setup
for testing. If anyone wants to take a crack at coding this up and sending me a
pull request on [github](https://github.com/mizhi/mimecat), go for it.
