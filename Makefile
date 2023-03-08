SHELL := /bin/bash


exp:
	export FLASK_APP=app

	export FLASK_ENV=development
	
run:
	export FLASK_APP=app

	export FLASK_ENV=development

	flask run

start_db:
	docker start flask-rec01
	
 
test:
	pytest tests/ -v --cov=app


test -w:
	FLASK_ENV ward

