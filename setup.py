# -*- coding: utf-8 -*-
from setuptools import setup

setup(name="mimecat",
      version="0.1.0",
      author="Mitchell Peabody",
      description=("A simple module for handling a catalogue of MIME types and"
                   " extensions"),
      url = "https://github.com/mizhi/mimecat",
      license="MIT",
      keywords="MIME types extensions",
      py_modules=["mimecat"],
      classifiers = [
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          "Topic :: Internet",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Software Development"
      ])
