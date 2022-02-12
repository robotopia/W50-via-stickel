FILES = $(shell find . -name "*.txt")
PNGS = $(patsubst %.txt,%.png,$(FILES))

all: $(PNGS)

%.png: %.txt
	python smooth_profiles.py $<
