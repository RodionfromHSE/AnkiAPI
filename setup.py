#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ankiapi",
    version="0.1.0",
    description="A simple Python wrapper for interacting with the AnkiConnect API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RodionfromHSE",
    url="https://github.com/RodionfromHSE/AnkiAPI",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
)