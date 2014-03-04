#!/bin/sh

#make clean
cd src
#python countlib/__init__.py "$@"
py.test -x countlib "$@"
