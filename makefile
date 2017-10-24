all: build

build:
	python3 main.py > output.ppm
	convert output.ppm output.png
	feh output.png
