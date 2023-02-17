SHELL := /bin/bash

run:
	python projeto/app.py

start_db:
	docker start flask-rec01
	
 
