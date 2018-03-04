all:
	-apt-get update -y
	-apt-get install python3 -y
	apt-get install --reinstall python-pkg-resources
	python3 -m compileall read.py
