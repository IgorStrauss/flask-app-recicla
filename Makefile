SHELL := /bin/bash

run -d:

	export FLASK_APP=projeto

	export FLASK_ENV=development
	
	python projeto/app.py

run -p:
	export FLASK_APP=projeto

	export FLASK_ENV=production
	
	python projeto/app.py

start_db:
	docker start flask-rec01
	
 
