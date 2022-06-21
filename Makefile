glossar.html: generate.py template.html data/*.csv
	python3 generate.py > $@
