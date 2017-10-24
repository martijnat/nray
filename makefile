all: test build

test:
	python3 ray_math.py
build:
	python3 main.py > output.ppm
	convert output.ppm output.png
	feh output.png
