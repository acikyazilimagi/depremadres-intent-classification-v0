install-reqs:
	pip3 install --upgrade-strategy=only-if-needed -r requirements.txt

test:
	pytest
