SHELL := /bin/bash

run -d:

	export FLASK_APP=app

	export FLASK_ENV=development
	
	<adicionar caminho>

run -p:
	export FLASK_APP=projeto

	export FLASK_ENV=production
	
	<adicionar caminho>

start_db:
	docker start flask-rec01
	
 
test:
	pytest tests/ -v --cov=app


test -w:
	FLASK_ENV ward