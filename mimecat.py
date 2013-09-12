# -*_ coding: utf-8 -*-
"""mimecat - Easy catalogue of MIME types and extensions.
"""

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
    """A Catalogue object represents a list of known MIME types and
    extensions. It can be initialized with a given filename or list of
    filenames. The files are expected to be in the format of a mime.types
    file.

    This class does not know about, care about, or possess the ability to
    process, parameters after the initial MIME type. For example,
    "text/plain; charset=us-ascii."

    """

    def __init__(self, filenames = None):
        """Initializes this catalogue from the filename or filenames listed in
        ``filenames``

        If ``filenames`` is None, then a list of
        common locations is tried to find ``mime.types`` when
        one is found, the MIME type definitions are loaded and
        the object is finished initializing.

        If ``filenames`` is a list passed in as a parameter,
        then _all_ the files listed will be loaded.

        :param filenames: a filename or a list of filenames
          containing MIMEtype definitions in the style of mime.types

        :raises: IOError If unable to find any of the files.

        """
        self._types_to_exts = None
        self._exts_to_types = None
        self._known_mediatypes = None
        self._known_mimetypes = None
        self._known_extensions = None

        self.clear()

        if filenames is None:
            self.load_filenames(_KNOWNFILES, True)
        elif isinstance(filenames, str):
            self.load_filename(filenames)
        else:
            self.load_filenames(filenames)

    def clear(self):
        """Clears out catalogue of known types.
        """
        self._types_to_exts = {}
        self._exts_to_types = {}
        self._known_mediatypes = set()
        self._known_mimetypes = set()
        self._known_extensions = set()

    def load_filenames(self, filenames, stop_on_successful_load = False):
        """Loads in MIME type defitions from ``filenames`` If
        ``stop_on_successful_load`` is True, then will stop on the first
        successful loading, else it will load all the files listed.

        :param filenames: List of files that could potentially contain
          MIME type defitions.

        :param stop_on_successful_load: If False, then load all the files.

        :raises: IOError If None of the listed files can be loaded.

        """
        successful_load = False
        for filename in filenames:
            try:
                self.load_filename(filename)
                successful_load = True
                if stop_on_successful_load:
                    break
            except IOError:
                pass

        if not successful_load:
            raise IOError("Could not locate a suitable mime.types file.")

    def load_filename(self, filename):
        """Loads in MIME type definitions from ``filename``.

        :param filename: The filename to load into the class
        """
        with open(filename, "r") as filep:
            self.load_file(filep)

    def load_file(self, filep):
        """Loads in MIME type definitions from open ``filep``
        :param filep: The file to load into the class
        """
        for (mime_type, extensions) in _parse_file(filep):
            self.add_type(mime_type, extensions)

    @property
    def known_mediatypes(self):
        """Returns the set of known media types (mediatype/subtype)

        :returns: frozen set of media types
        """
        return frozenset(self._known_mediatypes)

    @property
    def known_mimetypes(self):
        """Returns the set of known mimetypes.

        :returns: frozen set of mimetypes
        """
        return frozenset(self._known_mimetypes)

    @property
    def known_extensions(self):
        """Returns the set of known extensions.

        :returns: frozen set of extensions
        """
        return frozenset(self._known_extensions)

    def get_extensions(self, typename):
        """Returns an ordered list of known extensions to the given MIME type.
        Order is determined by the order in which the extensions were
        listed in the ``mime.types`` file. First extension encountered,
        then second, and so forth.

        :param typename: String of the MIME type.
        :returns: List of known extensions. These will include a leading .
        :raises: KeyError If MIME type is unknown.

        """
        return self._types_to_exts[typename]

    def get_types(self, extension):
        """Returns an ordered list of known MIME types for the given extension.
        Order is determined by the order in which the MIME types were
        added in the ``mime.types`` file.

        :param extension: String of the extension. This can include the
          leading . or omit it.
        :returns: List of known MIME types that use the given extension.
        :raises: KeyError If the extension is unknown.

        """
        return self._exts_to_types[_canonicalize_extension(extension)]

    def add_type(self, typename, extensions):
        """Adds a new entry for ``typename`` for the given list of
        ``extensions.`` If ``typename`` is already registered, then
        appends list of extensions to existing entry.

        :param typename: The MIME type to add.

        :param extensions: String of extension or list of extensions to
          add. This can include the leading . or omit it.

        :raises: ValueError If ``typename`` is not of the format type/subtype

        """
        (mediatype, _) = typename.split("/")

        if isinstance(extensions, str):
            extensions = [extensions]

        self._known_mediatypes |= set([mediatype])
        self._known_mimetypes |= set([typename])
        self._known_extensions |= set(_canonicalize_extension(ext) \
                                      for ext in extensions)

        if typename not in self._types_to_exts:
            self._types_to_exts[typename] = []

        existing_exts  = self._types_to_exts[typename]
        for ext in extensions:
            ext = _canonicalize_extension(ext)
            if ext not in existing_exts:
                existing_exts.append(ext)

            if ext not in self._exts_to_types:
                self._exts_to_types[ext] = []
            existing_types = self._exts_to_types[ext]

            if typename not in existing_types:
                existing_types.append(typename)

def _parse_file(filep):
    """Returns a generator which yields parsed lines from a ``mime.types``
    file.

    :param filep: A file-like object opened for reading
    :yields: A tuple containing the mime_type and associated extensions.
    """
    for line in filep:
        parsed_line = _parse_line(line)
        if parsed_line is None:
            continue
        yield parsed_line

def _parse_line(line):
    """Parses a line from ``mime.types``

    :param line: The line to parse.
    :returns: Tuple with mimetype and a list of extensions. If line is blank,
      return None
    :raises: ValueError If mimetype is invalid (not type/subtype)
    """
    if "#" in line:
        line = line[:line.find("#")]

    parts = line.split()

    if not parts:
        return None

    mimetype = parts[0]

    mimetype.index("/") # check for /, raise ValueError if not found

    extensions = []
    if len(parts) > 1:
        extensions = [_canonicalize_extension(ext) for ext in parts[1:]]

    return (mimetype, extensions)

def _canonicalize_extension(ext):
    """Returns a transformed ext that has a uniform pattern.
    Specifically, if ``ext`` has a leading . then it is simply returned.
    If ``ext`` doesn't have a leading . then it is prepended.
    Exceptions to this are if ``ext`` is ``None`` or "". If ``ext``
    is "" then "" is return. If ``ext`` is None then None is returned.

    :param ext: The extension to canonicalize.
    :returns: The canonicalized extension.

    """
    if ext is None or ext == "" or ext.startswith("."):
        return ext
    return "." + ext
