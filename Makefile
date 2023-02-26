SHELL := /bin/bash

run:
	FLASK_APP=projeto
	FLASK_ENV=development
	
	python projeto/app.py

start_db:
	docker start flask-rec01
	
 
