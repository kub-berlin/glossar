glossar.html: generate.py template.html data/*.csv
	python generate.py > $@
