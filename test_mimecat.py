# -*- coding: utf-8 -*-
import os
import unittest

from mimecat import Catalogue, _canonicalize_extension, _parse_line

TEST_MIME_TYPES = """
# This file maps Internet media types to unique file extension(s).
# Although created for httpd, this file is used by many software systems
# and has been placed in the public domain for unlimited redisribution.
#
# The table below contains both registered and (common) unregistered types.
# A type that has no unique extension can be ignored -- they are listed
# here to guide configurations toward known types and to make it easier to
# identify "new" types.  File extensions are also commonly used to indicate
# content languages and encodings, so choose them carefully.
#
# Internet media types should be registered as described in RFC 4288.
# The registry is at <http://www.iana.org/assignments/media-types/>.
#
# MIME type (lowercased)			Extensions
# ============================================	==========
# application/activemessage
application/andrew-inset			ez
application/json				json
# application/kpml-request+xml
# audio/amr
audio/midi					mid midi kar rmi
# audio/mobile-xmf
audio/mp4					mp4a
audio/mp4a-latm			m4a m4p
audio/ogg					oga ogg spx
image/jpeg					jpeg jpg jpe
# image/jpm
# message/cpim
# message/delivery-status
message/rfc822					eml mime
text/css					css
text/plain					txt text conf def list log in
# text/xml
video/3gpp					3gp
video/3gpp2					3g2
video/ogg					ogv
"""

class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_filename = "test.mime.types"
        cls.test_filename_shibboleth = "test-shibboleth.mime.types"
        with open(cls.test_filename, "w") as filep:
            filep.write(TEST_MIME_TYPES)

        with open(cls.test_filename_shibboleth, "w") as filep:
            filep.write("shibboleth/plain            shib")

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.test_filename)
        os.unlink(cls.test_filename_shibboleth)

    def setUp(self):
        self.catalogue = Catalogue(self.test_filename)

    def test_init(self):
        cat = Catalogue(self.test_filename)
        self.assertIsNotNone(cat)

    def test_init_fails(self):
        cat = None
        with self.assertRaises(IOError):
            cat = Catalogue(["BOGUS_FILE"])
        self.assertIsNone(cat)

    def test_clear(self):
        self.catalogue.clear()
        self.assertEqual( {}, self.catalogue._types_to_exts)
        self.assertEqual( {}, self.catalogue._exts_to_types)
        self.assertEqual(set(), self.catalogue._known_mediatypes)
        self.assertEqual(set(), self.catalogue._known_mimetypes)
        self.assertEqual(set(), self.catalogue._known_extensions)

    def test_load_filenames_stops(self):
        cat = Catalogue(self.test_filename)
        cat.clear()
        cat.load_filenames([self.test_filename_shibboleth, self.test_filename],
                           True)

        self.assertEqual(len(cat._known_mediatypes), 1)
        self.assertEqual(len(cat._known_mimetypes), 1)
        self.assertEqual(len(cat._known_extensions), 1)

    def test_load_filenames_does_not_stop(self):
        cat = Catalogue(self.test_filename)
        cat.clear()
        cat.load_filenames([self.test_filename_shibboleth, self.test_filename],
                           False)

        self.assertGreater(len(cat._known_mediatypes), 1)
        self.assertGreater(len(cat._known_mimetypes), 1)
        self.assertGreater(len(cat._known_extensions), 1)

    def test_load_filenames_fail(self):
        with self.assertRaises(IOError):
            self.catalogue.load_filenames(["BOGUS_FILE", "BOGUS_FILE2"])

    def test_load_filename(self):
        cat = Catalogue(self.test_filename_shibboleth)
        self.assertEqual(len(cat._known_mediatypes), 1)
        self.assertEqual(len(cat._known_mimetypes), 1)
        self.assertEqual(len(cat._known_extensions), 1)

    def test_load_filename_fails(self):
        with self.assertRaises(IOError):
            self.catalogue.load_filename("BOGUS_FILE")

    def test_load_file(self):
        cat = Catalogue(self.test_filename)
        cat.clear()

        with open(self.test_filename_shibboleth) as filep:
            cat.load_file(filep)

        self.assertEqual(len(cat._known_mediatypes), 1)
        self.assertEqual(len(cat._known_mimetypes), 1)
        self.assertEqual(len(cat._known_extensions), 1)

    def test_parse_line(self):
        result = _parse_line("#")
        self.assertIsNone(result)

        result = _parse_line("# more")
        self.assertIsNone(result)

        result = _parse_line("text/plain")
        self.assertEqual(("text/plain", []), result)

        result = _parse_line("text/plain ext1 ext2 ext3")
        self.assertEqual(("text/plain", [".ext1", ".ext2", ".ext3"]), result)

        result = _parse_line("text/plain ext1 ext2 ext3 # with comment")
        self.assertEqual(("text/plain", [".ext1", ".ext2", ".ext3"]), result)

        result = _parse_line("# text/plain ext1 ext2 ext3")
        self.assertIsNone(result)

        result = _parse_line("# text/plain ext1 ext2 ext3 # with comment")
        self.assertIsNone(result)

    def test_parse_line_fails(self):
        with self.assertRaises(ValueError):
            _ = _parse_line("invalid exts")

    def test_known_mimetypes(self):
        pass

    def test_known_extensions(self):
        pass

    def test_get_extensions(self):
        pass

    def test_get_extensions_fails(self):
        pass

    def test_get_types(self):
        pass

    def test_get_types_fails(self):
        pass

    def test_add_type(self):
        cat = Catalogue(self.test_filename)

        cat.clear()
        cat.add_type("text/plain", "txt")
        self.assertIn("text", cat._known_mediatypes)
        self.assertIn("text/plain", cat._known_mimetypes)
        self.assertIn(".txt", cat._known_extensions)

        cat.clear()
        cat.add_type("text/plain", ".txt")
        self.assertIn("text", cat._known_mediatypes)
        self.assertIn("text/plain", cat._known_mimetypes)
        self.assertIn(".txt", cat._known_extensions)

        cat.clear()
        cat.add_type("text/plain", [".txt"])
        self.assertIn("text", cat._known_mediatypes)
        self.assertIn("text/plain", cat._known_mimetypes)
        self.assertIn(".txt", cat._known_extensions)

    def test_add_types_with_duplicate_extensions(self):
        cat = Catalogue(self.test_filename)

        cat.clear()
        cat.add_type("text/plain", "txt")
        cat.add_type("text/doc", "txt")
        self.assertIn("text/plain", cat._exts_to_types[".txt"])
        self.assertIn("text/doc", cat._exts_to_types[".txt"])

        self.assertIn(".txt", cat._types_to_exts["text/plain"])
        self.assertIn(".txt", cat._types_to_exts["text/doc"])

    def test_add_type_fails(self):
        cat = Catalogue(self.test_filename)
        with self.assertRaises(ValueError):
            cat.add_type("textplain", ".txt")

    def test_canonicalize_extension(self):
        ret = _canonicalize_extension("test")
        self.assertEqual(ret, ".test")

        ret = _canonicalize_extension(".test")
        self.assertEqual(ret, ".test")

        ret = _canonicalize_extension("")
        self.assertEqual(ret, "")

        ret = _canonicalize_extension(None)
        self.assertIsNone(ret)
