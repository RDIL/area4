clean:
	-rm -rf build dist area4.egg-info area4.dist-info
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

dist: clean
	chmod +x tools/build-package.sh
	bash tools/build-package.sh
.PHONY: dist

distinfo: clean
	chmod +x tools/create-dist-info.sh
	bash tools/create-dist-info.sh
.PHONY: distinfo

test:
	python3 test-code.py
.PHONY: test

installlinkcheck: clean
	npm install -g markdown-link-check@3.7.2
.PHONY: linktest

installmdlint: clean
	npm install -g markdownlint-cli
.PHONY: installmdlint

linkcheck: clean
	find . -name \*.md -exec markdown-link-check {} \;
.PHONY: linkcheck
