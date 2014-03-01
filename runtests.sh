#!/bin/sh

set -e

find . -name "*.pyc" -delete
py.test countlib
