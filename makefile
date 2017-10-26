all:
	/bin/time -p pypy3 main.py > output.ppm
	convert output.ppm output.png
	convert output.png -resize 1920x1080 scaled.png
	feh scaled.png output.png 
