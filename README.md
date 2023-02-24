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
        

Home page com informações básicas sobre a aplicação

    > Cadastro de usuário para login

    > Cadastro de solicitação de coleta

    > Login baseado em email e senha

Após logado
    Após usuário logado, terá disponiveis as opções visiveis de rotas 
    para solicitar coleta e pagina de ajuda, com orientação sobre uso 
    do aplicativo

Rotas para manutenção e usabilidade administrativa
    (/users) -> Lista todos os usuários cadastrados
    (/user/id) -> Lista perfil de usuário
    (/coleta/view) -> Lista todas as solicitações de coleta
    (/coleta/view/id) -> Lista ordem de coleta com situação de status
    (/user/id/coleta/add) -> Usuário logado pode fazer solicitação de coleta
    (/register) -> Rota para usuário se cadastrar
    (/logout) -> Somente para usuário deslogar da aplicação
    (/login) -> Rota para usuário fazer login
    (/user/delete/id) -> Rota para deletar usuário
    