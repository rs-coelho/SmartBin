import configparser
import os

from sqlalchemy import Column, ForeignKey, Date, Time, String, DateTime, DECIMAL, TIMESTAMP, BOOLEAN, \
    ForeignKeyConstraint, Index, create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.mysql import INTEGER

from model.DB_Build import Base, schema_name

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../settings/settings.ini'))

engine = create_engine(
    'mysql+pymysql://' + config.get('db', 'local_user') + ':' + config.get('db', 'local_pass') + '@' +
    config.get('db', 'local_host') + '', convert_unicode=True)
metadata = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_session.configure(bind=engine)


# Foram criados init apenas para visualização do que estará, essas funções não serão utilizadas


class ListaHubs(Base):
    __tablename__ = 'lista_hubs'
    __table_args__ = {'schema': schema_name}

    id_hub = Column(INTEGER(unsigned=True), primary_key=True)
    id_lixeira = Column(INTEGER(unsigned=True), nullable=False)
    nome = Column(String(50), nullable=False)
    ip = Column(String(15), nullable=False)
    enderesso_fisico = Column(String(70), nullable=False)

    # def __init__(self):
    #     self.id_hub = 0
    #     self.id_lixeira = 1
    #     self.nome = 'central'
    #     self.ip = '127.0.0.1'
    #     self.enderesso_fisico = 'Av. Ficticia n420'


class ListaLixeiras(Base):
    __tablename__ = 'lista_lixeiras'
    __table_args__ = {'schema': schema_name}

    id_lixeira = Column(INTEGER(unsigned=True), primary_key=True)
    enderesso_fisico = Column(String(70), nullable=False)
    capacidade = Column(INTEGER(unsigned=True), nullable=False)
    status = Column(INTEGER(unsigned=True), nullable=False)
    # Não tem id do hab pois ele já está na tabela do hub jutamente com o id da lixeira

    # def __init__(self):
    #     self.id_lixeira = 1
    #     self.enderesso_fisico = ''
    #     self.capacidade = 100
    #    self.status = 0


class ListaItens(Base):
    __tablename__ = 'lista_itens'
    __table_args__ = {'schema': schema_name}

    id_item = Column(String(12), primary_key=True)  # codigo de barras
    nome = Column(String(40), nullable=False)
    material = Column(String(2), nullable=False)
    peso = Column(DECIMAL(4, 4), nullable=False)
    pontos = Column(INTEGER(unsigned=True), nullable=False)

    # def __init__(self):
    #    self.id_item = '123456789'
    #    self.nome = 'nome produto'
    #    self.material = 'ME'  # PL/PA 'metal/plastico/papel'
    #    self.peso = 0
    #    self.pontos = 10


class ListaUsers(Base):
    __tablename__ = 'lista_users'
    __table_args__ = {'schema': schema_name}

    id_user = Column(INTEGER(unsigned=True), primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(30), nullable=False)
    pontos = Column(INTEGER(unsigned=True), nullable=False)
    tipo_user = Column(String(2), nullable=False)

    # def __init__(self):
    #     self.id_user = 1234
    #     self.nome = 'Cleitin Corta Giro'
    #     self.email = 'nomealeatorio@empresa.com'
    #     self.password = 'batat1nh4'
    #     self.pontos = 1000
    #     self.tipo_user = 'CL'

    @staticmethod
    def create_user(id_user, nome=None, email=None, password=None, pontos=None, tipo_user=None):
        # chercher l'implementation pur changer quelque chose oú DB

        user = ListaUsers()
        user.nome = nome if nome is not None else user.nome
        user.email = email if email is not None else user.email
        user.password = password if password is not None else user.password
        user.nome = pontos if pontos is not None else user.pontos
        user.nome = tipo_user if tipo_user is not None else user.tipo_user
        db_session.insertorm(user)
        db_session.commit()
        return user

    @staticmethod
    def get_user(id_user):
        user = db_session.query(ListaUsers).filter(ListaUsers.id_user == id_user)
        return user

    @staticmethod
    def delete_user(id_user):
        # https://stackoverflow.com/questions/27158573/how-to-delete-a-record-by-id-in-flask-sqlalchemy
        user = db_session.query(ListaUsers).filter(ListaUsers.id_user == id_user).delete()
        return user

    @staticmethod
    def change_user(id_user, nome=None, email=None, password=None, pontos=None, tipo_user=None):
        # chercher l'implementation pur changer quelque chose oú DB
        # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
        user = db_session.query(ListaUsers).filter(ListaUsers.id_user == id_user)
        user.nome = nome if nome is not None else user.nome
        user.email = email if email is not None else user.email
        user.password = password if password is not None else user.password
        user.nome = pontos if pontos is not None else user.pontos
        user.nome = tipo_user if tipo_user is not None else user.tipo_user
        db_session.commit()
        return user



class TipoUser(Base):
    __tablename__ = 'tipo_user'
    __table_args__ = {'schema': schema_name}

    tipo_user = Column(String(2), primary_key=True)
    nome = Column(String(15), nullable=False)

    # def __init__(self):
    #    self.tipo_user = 'CL'  # CO/A
    #    self.nome = 'client'  # colector/admin


class InventarioItens(Base):
    __tablename__ = 'inventario_itens'
    __table_args__ = {'schema': schema_name}

    id_lixeira = Column(INTEGER(unsigned=True), ForeignKey(schema_name + '.lista_lixeiras.id_lixeira'), primary_key=True)
    id_item = Column(String(12), ForeignKey(schema_name + '.lista_itens.id_item'), nullable=False)
    id_user = Column(INTEGER(unsigned=True), ForeignKey(schema_name + '.lista_users.id_user'), nullable=False)

    # def __init__(self):
    #     self.id_lixeira = 1
    #     self.id_item = '123456789'
    #     self.id_user = 1234
