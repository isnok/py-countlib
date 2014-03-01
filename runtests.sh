#!/bin/sh

set -e

cd src
find . -name "*.pyc" -delete

#py.test countlib
python countlib/__init__.py
