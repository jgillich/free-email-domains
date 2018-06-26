#!/bin/bash
set -ue
if [ ! -d tmp/env ]; then python3 -m venv tmp/env; fi
./tmp/env/bin/pip install -Ur scripts/requirements.txt
if [ ! -d tmp/disposable-email-domains ]; then
	cd tmp
	git clone --depth=1 https://github.com/ivolo/disposable-email-domains.git
	cd ..
else
	cd tmp/disposable-email-domains
	git pull
	cd ../..
fi

./tmp/env/bin/python scripts/check.py

echo 'OK'
