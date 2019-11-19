#!/usr/bin/env python

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-catch-server",
    version="0.1.0",
    author="Jan Bednařík",
    author_email="jan.bednarik@gmail.com",
    maintainer="Jan Bednařík",
    maintainer_email="jan.bednarik@gmail.com",
    license="MIT",
    url="https://github.com/kiwicom/pytest-catch-server",
    description="Pytest plugin with server for catching HTTP requests.",
    long_description=read("README.rst"),
    py_modules=["pytest_catch_server"],
    python_requires=">=3.4",
    install_requires=["pytest>=3.5.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["catch-server = pytest_catch_server",],},
)
