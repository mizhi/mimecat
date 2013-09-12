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
more talented than me, have done that already.

My goals for `mimecat` are to keep track of MIME types, their associated
extensions, and allow inspection of their associations.

Usage
=====

Using `mimecat` is straightforward.

```python
from mimecat import Catalogue

cat = Catalogue() # this will search in a number of common locations for a
                  # mime.types file. Loading will stop on first successful
                  # load.

# Media types are the major part of a MIME type, (see [RFC2046](http://www.ietf.org/rfc/rfc2046.txt))
print "text" in cat.known_mediatypes



```
