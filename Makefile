SHELL := /bin/bash

run:

	export FLASK_APP=projeto

	export FLASK_ENV=development

	python projeto/app.py

start_db:
	docker start flask-rec01
	
 
