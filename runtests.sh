#!/bin/sh

make clean
cd src
python countlib/__init__.py "$@"
