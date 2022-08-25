.PHONY:
	init test

init:
	pip install -r requirements.txt

test:
	echo "no test implemented yet!!"

fix_headers:
# Exemple
	sed -i -e 's/Hefferson Campos/Jefferson Campos/g' jeff_stats.csv
