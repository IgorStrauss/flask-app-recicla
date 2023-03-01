from app.models import User, Telefone, Endereco, SolicitaColeta


def test_user(user: User):
    assert isinstance(user, User)
    

def test_return_str_user(user: User):
    """Assert retorno __str__"""
    assert user.__str__() == 'peter'


def test_return_firstname_formatado(user: User):
    """Assert first_name.title"""
    assert user.firstname == 'Peter'


def test_return_last_name(user: User):
    """Assert last_name"""
    assert user.last_name == 'parker'


def test_return_lastname_formatado(user: User):
    """Assert last_name.title"""
    assert user.lastname == 'Parker'


def test_return_user_email(user: User):
    """Assert email user"""
    assert user.email == 'spider@icloud.com'


def test_return_user_password(user: User):
    assert user.password == 'password'


def test_return_username(user: User):
    """Assert retorno username"""
    assert user.username == 'PARKERPETER'


# def test_return_datetime_created_user(user: User):
#     """Assert retorno data e hora formatados"""
#     assert user.formata_data == '28/2/2023 as             15:24'


def test_fone(telefone: Telefone):
    assert isinstance(telefone, Telefone)


def test_return_str_telefone(telefone: Telefone):
    """Return __str__ telefone"""
    assert telefone.__str__() == '11912345678'


def test_return_repr_telefone(telefone: Telefone):
    """Return __repr__ telefone"""
    assert telefone.__repr__() == 'classe telefone <11912345678>'


def test_return_telefone_celular(telefone: Telefone):
    """Assert inserção telefone.celular"""
    assert telefone.celular == '11912345678'


def test_return_telefone_formatado(telefone: Telefone):
    """Assert retorno numero celular formatado"""
    assert telefone.formata_celular == '(11)    9 1234-5678'


def test_endereco(endereco: Endereco):
    assert isinstance(endereco, Endereco)


def test_return_str_endereco(endereco: Endereco):
    assert endereco.__str__() == 'Rua A'


def test_endereco_street(endereco: Endereco):
    """Assert endereço"""
    assert endereco.street == 'Rua A'


def test_endereco_bairro(endereco: Endereco):
    """Assert bairro"""
    assert endereco.bairro == 'Bairro A'


def test_endereco_cidade(endereco: Endereco):
    """Assert cidade"""
    assert endereco.cidade == 'Cidade A'


def test_endereco_estado(endereco: Endereco):
    """Assert estado"""
    assert endereco.estado == 'BR'


def test_endereco_cep(endereco: Endereco):
    """Assert cep"""
    assert endereco.cep == '01234999'


def test_coleta(coleta: SolicitaColeta):
    assert isinstance(coleta, SolicitaColeta)


def test_return_str_coleta(coleta: SolicitaColeta):
    assert coleta.__str__() == 'produto'


def test_return_coleta_tipo_formatada(coleta: SolicitaColeta):
    """Assert retorno tipo coleta.title"""
    assert coleta.formata_tipo == 'Produto'


def test_return_coleta_situacao_formatada(coleta: SolicitaColeta):
    """Assert situação coleta.title"""
    assert coleta.formata_situacao == 'Situação'


# def test_return_coleta_data_formatada(coleta: SolicitaColeta):
#     """Assert retorno data e hora fortamados"""
#     assert coleta.formata_data == '28/2/2023 ás             15:24'


def test_return_coleta_descricao_formatada(coleta: SolicitaColeta):
    """Assert descrição coleta.title"""
    assert coleta.formata_descricao == 'Descrição'
