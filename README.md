mimecat
=======

A catalogue for working with MIME types and extensions.

Introduction
============

I started the mimecat package in order to support a need at work to determine
what MIME types our product supported and what potential extensions belonged to
those MIME types. I grew frustrated with the ``mimetypes`` package, included
with default Python implementations. Specifically, I needed the capability to
support extensions that may belong to one or more MIME types. I also needed the
capability to load very specific subsets of MIME types.