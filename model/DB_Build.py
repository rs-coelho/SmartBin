import configparser
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../settings/settings.ini'))
Base = declarative_base()
schema_name = 'LixeiraIntDB'


class DBBuild:
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://" +
            config.get('db', 'local_user') + ":" +
            config.get('db', 'local_pass') + "@" +
            config.get('db', 'local_host') + "/" +
            config.get('db', 'local_db_name'), pool_timeout=1000, encoding='latin1', echo=True)
        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        session = sessionmaker()
        session.configure(bind=self.engine, autoflush=False, autocommit=False)
        self.session = session()

    def createbase(self):
        Base.metadata.create_all(bind=self.engine)

    def insertorm(self, obj):
        self.session.add(obj)

    def getsession(self):
        return self.session

    def getengine(self):
        return self.engine

    def commit(self):
        self.trans.commit()
        self.session.commit()
        self.trans = self.conn.begin()

    def rollback(self):
        self.session.rollback()
        self.trans.rollback()
        self.trans.rollback()
        self.trans = self.conn.begin()

    def close(self):
        self.trans.commit()
        self.session.commit()
        self.conn.close()
        self.session.close()
