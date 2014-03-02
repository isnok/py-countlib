

clean:
	cd src; find . -name "*.pyc" -or -name "__pycache__" -exec rm -r {} \+

test:
	cd src; py.test countlib
