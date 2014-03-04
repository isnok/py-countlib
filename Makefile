

clean:
	cd src; find . -name "__pycache__" -exec rm -r {} \+
	cd src; find . -name "*.pyc" -exec rm {} \+

test: clean
	cd src; py.test countlib
