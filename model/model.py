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


class ListHubs(Base):
    __tablename__ = 'list_hubs'
    __table_args__ = {'schema': schema_name}

    id_hub = Column(INTEGER(unsigned=True), primary_key=True)
    id_bin = Column(INTEGER(unsigned=True), nullable=False)
    name = Column(String(50), nullable=False)
    ip = Column(String(15), nullable=False)
    address = Column(String(70), nullable=False)

    def __init__(self):
        self.id_hub = 0
        self.id_bin = 1
        self.name = 'central'
        self.ip = '127.0.0.1'
        self.address = 'Av. Far Far Away n420'


class ListBins(Base):
    __tablename__ = 'list_bins'
    __table_args__ = {'schema': schema_name}

    id_bin = Column(INTEGER(unsigned=True), primary_key=True)
    address = Column(String(70), nullable=False)
    capacity = Column(INTEGER(unsigned=True), nullable=False)
    status = Column(INTEGER(unsigned=True), nullable=False)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self):
        self.id_bin = 1
        self.address = ''
        self.capacity = 100
        self.status = 0
        self.last_updated = datetime.now()

    @staticmethod
    def create_bin(address=None, capacity=0, status=0):
        list_size = len(db_session.query(ListBins).all())
        item = ListBins()
        item.id_bin = list_size + 1
        item.address = address
        item.capacity = capacity
        item.status = status
        item.last_updated = datetime.now()
        db_session.add(item)
        db_session.commit()
        return item

    @staticmethod
    def get_bin(id_bin):
        rec_bin = db_session.query(ListBins).filter_by(id_bin=id_bin).all()
        return rec_bin

    @staticmethod
    def update_bin_capacity(id_bin, capacity):
        rec_bin = db_session.query(ListBins).filter_by(id_bin=id_bin).all()
        rec_bin[0].capacity = capacity
        rec_bin[0].last_updated = datetime.now()
        db_session.commit()
        return rec_bin


class ListItems(Base):
    __tablename__ = 'list_items'
    __table_args__ = {'schema': schema_name}

    id_item = Column(String(12), primary_key=True)  # bar code
    name = Column(String(40), nullable=False)
    material = Column(String(2), nullable=False)
    weight = Column(DECIMAL(4, 4), nullable=False)
    points = Column(INTEGER(unsigned=True), nullable=False)
    img_base64 = Column(Text(100000), nullable=True)

    def __init__(self):
        self.id_item = '123456789'
        self.name = 'name product'
        self.material = 'ME'  # PL/PA 'metal/plastic/paper'
        self.weight = 0
        self.points = 10
        self.img_base64 = ''

    @staticmethod
    def create_item(id_item, name=None, material=None, weight=None, points=0):
        item = ListItems()
        item.id_item = id_item
        item.name = name
        item.material = material
        item.weight = weight
        item.points = points
        item.img_base64 = None
        db_session.add(item)
        db_session.commit()
        return item

    @staticmethod
    def get_item(id_item):
        item = db_session.query(ListItems).filter_by(id_item=id_item).first()
        return item

    @staticmethod
    def upload_item_img(id_item, img_base64):
        item = db_session.query(ListItems).filter_by(id_item=id_item).all()
        item[0].img_base64 = img_base64
        db_session.commit()
        return item[0]

    @staticmethod
    def get_full_item_list():
        return db_session.query(ListItems).all()

    @staticmethod
    def get_item_list(id_item_list):
        final_list = []
        for id_item in id_item_list:
            final_list.append(db_session.query(ListItems).filter_by(id_item=id_item).first())
        return final_list


class ListUsers(Base):
    __tablename__ = 'list_users'
    __table_args__ = {'schema': schema_name}

    id_user = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(80), nullable=False)
    points = Column(INTEGER(unsigned=True), nullable=False)
    type_user = Column(String(2), nullable=False)

    def __init__(self):
        self.id_user = 1234
        self.name = 'John Doe'
        self.email = 'johndoe@gmail.com'
        self.password = 'johnDpass'
        self.points = 1000
        self.type_user = 'CL'

    @staticmethod
    def create_user(name=None, email=None, password=None, points=0, type_user='CL'):
        list_id = int(db_session.query(ListUsers.id_user).all()[-1][0])
        email_list = db_session.query(ListUsers.email).all()

        if (email,) in email_list:
            return 0

        user = ListUsers()
        user.id_user = list_id + 1
        user.name = name
        user.email = email
        user.password = generate_password_hash(password)
        user.points = points
        user.type_user = type_user
        db_session.add(user)
        db_session.commit()
        return user

    @staticmethod
    def get_user(id_user):
        user = db_session.query(ListUsers).filter_by(id_user=id_user).all()
        return user

    @staticmethod
    def get_user_type(id_user):
        user = db_session.query(ListUsers).filter_by(id_user=id_user).first()
        return user.type_user

    @staticmethod
    def login_user(email, password):
        filter_ = [ListUsers.email == email, ]
        user = db_session.query(ListUsers).filter(and_(*filter_)).first()
        if user:
            authorization = check_password_hash(user.password, password)
            if authorization:
                return user

        return False

    @staticmethod
    def update_user_points(id_user, points):
        user = db_session.query(ListUsers).filter_by(id_user=id_user).all()
        user[0].points += points
        db_session.commit()
        return user

    @staticmethod
    def delete_user(id_user):
        user = db_session.query(ListUsers).filter(ListUsers.id_user == id_user).delete()
        db_session.commit()
        return user

    @staticmethod
    def change_user(id_user, args):
        user = db_session.query(ListUsers).filter(ListUsers.id_user == id_user).first()

        if 'name' in args.keys():
            user.name = args['name']

        if 'email' in args.keys():
            user.email = args['email']

        if 'password' in args.keys():
            user.password = generate_password_hash(str(args['password']))

        db_session.commit()
        return user


# Enumerator
class TypeUser(Base):
    __tablename__ = 'type_user'
    __table_args__ = {'schema': schema_name}

    type_user = Column(String(2), primary_key=True)
    name = Column(String(15), nullable=False)

    def __init__(self):
        self.type_user = 'CL'  # CO/AD
        self.name = 'client'  # collector/admin


class InventoryItems(Base):
    __tablename__ = 'inventory_items'
    __table_args__ = {'schema': schema_name}

    id_inventory = Column(INTEGER(unsigned=True), primary_key=True)
    id_bin = Column(INTEGER(unsigned=True), ForeignKey(schema_name + '.list_bins.id_bin'), primary_key=True)
    id_item = Column(String(12), ForeignKey(schema_name + '.list_items.id_item'), nullable=False)
    id_user = Column(INTEGER(unsigned=True), ForeignKey(schema_name + '.list_users.id_user'), nullable=False)
    collected = Column(INTEGER(unsigned=True), nullable=False)

    def __init__(self):
        self.id_inventory = 0
        self.id_bin = 1
        self.id_item = '123456789'
        self.id_user = 1234
        self.collected = 0

    @staticmethod
    def get_items_from_user(id_user):
        items = db_session.query(InventoryItems).filter_by(id_user=id_user).all()
        return items

    @staticmethod
    def insert_item_from_user(id_user, id_bin, id_item):
        item = InventoryItems()
        item.id_inventory = len(db_session.query(InventoryItems).all())
        item.id_user = id_user
        item.id_bin = id_bin
        item.id_item = id_item
        db_session.add(item)
        db_session.commit()
        return item

    @staticmethod
    def empty_trash(id_bin):
        items = db_session.query(InventoryItems).filter_by(id_bin=id_bin).all()
        for item in items:
            if item.collected == 0:
                item.collected = 1
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
