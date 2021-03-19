from model.DB_Build import DBBuild
from model.model import *


if __name__ == '__main__':
    c = DBBuild()
    c.createbase()
    # RequestLog.insert_log('CS', datetime.now(), '200', 'sdfggdfgdfgdfgdfgf')

    c.insertorm(ListaLixeiras())
    c.insertorm(ListaItens())
    c.insertorm(ListaHubs())
    c.insertorm(TipoUser())
    c.insertorm(ListaUsers())
    c.insertorm(RequestLog)
    c.insertorm(InventarioItens())
    c.createbase()
    c.commit()
