Flask recicla
    Aplicação para coleta e destinação de lixo eletrônico

Database Postgres via Docker
    docker run --name <nome_container> -e "POSTGRES_PASSWORD=postgres" -p 5432:5432 -d postgres
    docker ps -a
    docker start <nome_container>
    docker exec -it <nome_container> bash
    psql -U postgres
    \l   -> lista bancos de dados
    create database <name_database>;
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@<IP container>/name_database"
    \connect <name_database>;

    Para identificar IP container:
        Com container ativo, digitar: docker inspect <id_do_container> | grep "IPAddress" 
        


