PARSE_TYPE ?= html
PAGES ?= 5

up:
	@echo "Starting Crypto Watchlist script"
	/bin/bash -c 'python3 -m venv .venv \
	&& source .venv/bin/activate \
	&& python3 -m pip install -r requirements.txt \
	&& python3 main.py $(PARSE_TYPE) $(PAGES)'