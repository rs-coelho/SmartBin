import configparser
import os

from sqlalchemy import Column, ForeignKey, Text, String, DateTime, DECIMAL, create_engine, MetaData, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.mysql import INTEGER
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from model.DB_Build import Base, schema_name

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../settings/settings.ini'))

engine = create_engine(
    'mysql+pymysql://' + config.get('db', 'local_user') + ':' + config.get('db', 'local_pass') + '@' +
    config.get('db', 'local_host') + '', convert_unicode=True)
metadata = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_session.configure(bind=engine)

# The __init__ were created just as an example of a first add to the DB, those functions are not to be used


class ListaHubs(Base):
    __tablename__ = 'lista_hubs'
    __table_args__ = {'schema': schema_name}

    id_hub = Column(INTEGER(unsigned=True), primary_key=True)
    id_lixeira = Column(INTEGER(unsigned=True), nullable=False)
    nome = Column(String(50), nullable=False)
    ip = Column(String(15), nullable=False)
    enderesso_fisico = Column(String(70), nullable=False)

    def __init__(self):
        self.id_hub = 0
        self.id_lixeira = 1
        self.nome = 'central'
        self.ip = '127.0.0.1'
        self.enderesso_fisico = 'Av. Ficticia n420'


class ListaLixeiras(Base):
    __tablename__ = 'lista_lixeiras'
    __table_args__ = {'schema': schema_name}

    id_lixeira = Column(INTEGER(unsigned=True), primary_key=True)
    address = Column(String(70), nullable=False)
    capacity = Column(INTEGER(unsigned=True), nullable=False)
    status = Column(INTEGER(unsigned=True), nullable=False)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self):
        self.id_lixeira = 1
        self.address = ''
        self.capacity = 100
        self.status = 0
        self.last_updated = datetime.now()

    @staticmethod
    def create_lixeira(address=None, capacity=0, status=0):
        # chercher l'implementation pur changer quelque chose oú DB

        list_size = len(db_session.query(ListaLixeiras).all())
        item = ListaLixeiras()
        item.id_lixeira = list_size + 1
        item.address = address
        item.capacity = capacity
        item.status = status
        item.last_updated = datetime.now()
        db_session.add(item)
        db_session.commit()
        return item

    @staticmethod
    def get_lixeira(id_lixeira):
        lixeira = db_session.query(ListaLixeiras).filter_by(id_lixeira=id_lixeira).all()
        return lixeira

    @staticmethod
    def update_lixeiera_capacidade(id_lixeira, capacity):
        lixeira = db_session.query(ListaLixeiras).filter_by(id_lixeira=id_lixeira).all()
        lixeira[0].capacity = capacity
        lixeira[0].last_updated = datetime.now()
        db_session.commit()
        return lixeira


class ListaItens(Base):
    __tablename__ = 'lista_itens'
    __table_args__ = {'schema': schema_name}

    id_item = Column(String(12), primary_key=True)  # codigo de barras
    nome = Column(String(40), nullable=False)
    material = Column(String(2), nullable=False)
    peso = Column(DECIMAL(4, 4), nullable=False)
    pontos = Column(INTEGER(unsigned=True), nullable=False)
    img_base64 = Column(Text(100000), nullable=True)

    def __init__(self):
        self.id_item = '123456789'
        self.nome = 'nome produto'
        self.material = 'ME'  # PL/PA 'metal/plastico/papel'
        self.peso = 0
        self.pontos = 10
        self.img_base64 = ''

    @staticmethod
    def create_item(nome=None, material=None, peso=None, pontos=0):
        # chercher l'implementation pur changer quelque chose oú DB

        list_size = len(db_session.query(ListaItens).all())
        item = ListaItens()
        item.id_item = list_size + 1
        item.nome = nome
        item.material = material
        item.peso = peso
        item.pontos = pontos
        item.img_base64 = None
        print(item.nome, item.material, item.peso)
        db_session.add(item)
        db_session.commit()
        return item

    @staticmethod
    def get_item(id_item):
        item = db_session.query(ListaItens).filter_by(id_item=id_item).all()
        return item

    @staticmethod
    def upload_item_img(id_item, img_base64):
        item = db_session.query(ListaItens).filter_by(id_item=id_item).all()
        item[0].img_base64 = img_base64
        db_session.commit()
        return item[0]

    @staticmethod
    def get_full_item_list():
        return db_session.query(ListaItens).all()


class ListaUsers(Base):
    __tablename__ = 'lista_users'
    __table_args__ = {'schema': schema_name}

    id_user = Column(INTEGER(unsigned=True), primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(80), nullable=False)
    pontos = Column(INTEGER(unsigned=True), nullable=False)
    tipo_user = Column(String(2), nullable=False)

    def __init__(self):
        self.id_user = 1234
        self.nome = 'Cleitin Corta Giro'
        self.email = 'nomealeatorio@empresa.com'
        self.password = 'batat1nh4'
        self.pontos = 1000
        self.tipo_user = 'CL'

    @staticmethod
    def create_user(nome=None, email=None, password=None, pontos=0, tipo_user='CL'):
        # chercher l'implementation pur changer quelque chose oú DB

        list_size = len(db_session.query(ListaUsers).all())
        email_list = db_session.query(ListaUsers.email).all()
        if (email,) in email_list:
            return 0
        user = ListaUsers()
        user.id_user = list_size + 1
        user.nome = nome
        user.email = email
        user.password = generate_password_hash(password)
        user.pontos = pontos
        user.tipo_user = tipo_user
        db_session.add(user)
        db_session.commit()
        return user

    @staticmethod
    def get_user(id_user):
        user = db_session.query(ListaUsers).filter_by(id_user=id_user).all()
        return user

    @staticmethod
    def get_user_type(id_user):
        user = db_session.query(ListaUsers).filter_by(id_user=id_user).first()
        return user.tipo_user

    @staticmethod
    def login_user(email, password):
        filter_ = [ListaUsers.email == email, ]
        user = db_session.query(ListaUsers).filter(and_(*filter_)).first()
        authorization = check_password_hash(user.password, password)
        if authorization:
            return user
        return False

    @staticmethod
    def update_user_pontos(id_user, pontos):
        user = db_session.query(ListaLixeiras).filter_by(id_user=id_user).all()
        user[0].pontos = pontos
        db_session.commit()
        return user

    @staticmethod
    def delete_user(id_user):
        # https://stackoverflow.com/questions/27158573/how-to-delete-a-record-by-id-in-flask-sqlalchemy
        user = db_session.query(ListaUsers).filter(ListaUsers.id_user == id_user).delete()
        db_session.commit()
        return user

    @staticmethod
    def change_user(id_user, args):
        # chercher l'implementation pur changer quelque chose oú DB
        # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
        user = db_session.query(ListaUsers).filter(ListaUsers.id_user == id_user).first()
        if 'nome' in args.keys():
            user.nome = args['nome']
        if 'email' in args.keys():
            user.email = args['email']
        if 'password' in args.keys():
            user.password = generate_password_hash(str(args['password']))
        db_session.commit()
        return user


# Enumerator
class TipoUser(Base):
    __tablename__ = 'tipo_user'
    __table_args__ = {'schema': schema_name}

    tipo_user = Column(String(2), primary_key=True)
    nome = Column(String(15), nullable=False)

    def __init__(self):
        self.tipo_user = 'CL'  # CO/AD
        self.nome = 'client'  # colector/admin


class InventarioItens(Base):
    __tablename__ = 'inventario_itens'
    __table_args__ = {'schema': schema_name}

    id_inventory = Column(INTEGER(unsigned=True), primary_key=True)
    id_lixeira = Column(INTEGER(unsigned=True), ForeignKey(schema_name + '.lista_lixeiras.id_lixeira'),
                        primary_key=True)
    id_item = Column(String(12), ForeignKey(schema_name + '.lista_itens.id_item'), nullable=False)
    id_user = Column(INTEGER(unsigned=True), ForeignKey(schema_name + '.lista_users.id_user'), nullable=False)
    colected = Column(INTEGER(unsigned=True), nullable=False)

    def __init__(self):
        self.id_inventory = 0
        self.id_lixeira = 1
        self.id_item = '123456789'
        self.id_user = 1234
        self.colected = 0

    @staticmethod
    def get_items_from_user(id_user):
        items = db_session.query(InventarioItens).filter_by(id_user=id_user).all()
        return items

    @staticmethod
    def insert_item_from_user(id_user, id_lixeira, id_item):
        item = InventarioItens()
        item.id_inventory = len(db_session.query(InventarioItens).all())
        item.id_user = id_user
        item.id_lixeira = id_lixeira
        item.id_item = id_item
        db_session.add(item)
        db_session.commit()
        return item

    @staticmethod
    def empty_trash(id_lixeira):
        items = db_session.query(InventarioItens).filter_by(id_lixeira=id_lixeira).all()
        for item in items:
            if item.colected == 0:
                item.colected = 1
        db_session.commit()
        return items


class RequestLog(Base):
    __tablename__ = 'request_log'
    __table_args__ = {'schema': schema_name}

    request = Column(String(50), primary_key=True)
    date = Column(DateTime, nullable=False)
    status = Column(String(3), nullable=False)
    data = Column(String(80), nullable=False)

    def __init__(self):
        self.request = 'First Entry'
        self.date = datetime.now()
        self.status = '200'
        self.data = 'inset request data here'

    @staticmethod
    def insert_log(request_type, date, status, data):
        request = RequestLog()
        request.request = request_type
        request.date = date
        request.status = status
        request.data = data
        db_session.add(request)
        db_session.commit()
        return request

    # Maybe implement a remove method, but I believe, that in this case, any removal should be done by SQL directly
