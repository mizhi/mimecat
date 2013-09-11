# -*_ coding: utf-8 -*-

#
# taken from mimetypes.py
#
_KNOWNFILES = [
    "/etc/mime.types",
    "/etc/httpd/mime.types",                    # Mac OS X
    "/etc/httpd/conf/mime.types",               # Apache
    "/etc/apache/mime.types",                   # Apache 1
    "/etc/apache2/mime.types",                  # Apache 2
    "/usr/local/etc/httpd/conf/mime.types",
    "/usr/local/lib/netscape/mime.types",
    "/usr/local/etc/httpd/conf/mime.types",     # Apache 1.2
    "/usr/local/etc/mime.types",                # Apache 1.3
    ]


class Catalogue(object):
    def __init__(self, mimetype_filenames = None):
        """Initializes this catalogue from the filenames listed in
        ``mimetype_filenames``

        :param mimetype_filenames: a list of filenames containing MIMEtype
          definitions in the style of mime.types

        """
        self._types_to_exts = {}
        self._exts_to_types = {}

    @property
    def known_mimetypes(self):
        """Returns the set of known mimetypes.
        """
        pass

    @property
    def known_extensions(self):
        """Returns the set of known extensions.
        """
        pass

    def get_extensions(self, typename):
        """Returns an ordered list of known extensions to the given MIME type.
        Order is determined by the order in which the extensions were
        listed in the ``mime.types`` file. First extension encountered,
        then second, and so forth.

        :param typename: String of the MIME type.
        :returns: List of known extensions. These will include a leading .
        :raises KeyError: If MIME type is unknown.

        """
        pass

    def get_types(self, extension):
        """Returns an ordered list of known MIME types for the given extension.
        Order is determined by the order in which the MIME types were
        added in the ``mime.types`` file.

        :param extension: String of the extension. This can include the
          leading . or omit it.
        :returns: List of known MIME types that use the given extension.
        :raises KeyError: If the extension is unknown.

        """
        pass

    def add_type(self, typename, extensions):
        """Adds a new entry for ``typename`` for the given list of
        ``extensions`` If ``typename`` is already registered, then
        appends list of extensions to existing entry.

        :param typename: The MIME type to add.

        :param extensions: List of extensions to add. This can include
          the leading . or omit it.

        """
        pass
