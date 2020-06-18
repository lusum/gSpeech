.PHONY: unittest flake8 test deploy clean

mo:
	./compile_language.sh

unittest:
	python3 -m unittest

flake8:
	flake8 --filename="*.py,./gspeech,./gspeech-cli"

test:
	make unittest
	make flake8

deploy:
	debuild -S
	dput ppa:jerem-ferry/tts ../gspeech*.changes

clean:
	rm -f MANIFEST
	rm -rf build dist
