all:
	/bin/time -p pypy3 main.py > output.ppm
	convert output.ppm output.png
	feh output.png
