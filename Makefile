SHELL := /bin/bash

.PHONY: run
run:
	source $(CURDIR)/venv/bin/activate && python -m minres.main

.PHONY: build
build:
	mkdir -p bin
	source $(CURDIR)/venv/bin/activate && \
		python -m nuitka \
			--standalone \
			--onefile \
			--enable-plugin=pyside6 \
			--windows-disable-console \
			--output-dir=dist \
			minres.py

.PHONY: pip
pip:
	source $(CURDIR)/venv/bin/activate && \
		pip install -r requirements.txt
