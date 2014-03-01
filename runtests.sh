#!/bin/sh

set -e

find . -name "*.pyc" -delete
py.test countlib
python countlib/__init__.py
