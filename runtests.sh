#!/bin/sh

set -e

cd src
find . -name "*.pyc" -or -name "__pycache__" -exec rm -r {} \+

#py.test countlib
python countlib/__init__.py
