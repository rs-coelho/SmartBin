# This is a sample Python script.
from model.DB_Build import DBBuild
from model.model import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    c = DBBuild()
    c.createbase()

    c.insertorm(ListaLixeiras())
    c.insertorm(ListaItens())
    c.insertorm(ListaHubs())
    c.insertorm(TipoUser())
    c.insertorm(ListaUsers())
    c.insertorm(InventarioItens())
    c.createbase()
    c.commit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
