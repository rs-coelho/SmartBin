# API LixeiraInteligente
### This is a simple API with JWT and DataBase Manipulation. 

The API functions as follows input MySQL access data in settings.ini then create the database
with __db_init __.py, with that database set up that run the __api __.py

### Explaining what is what
Under the control module are all the functions responsible for the manipulation, response display, calling the DB and verifying JWT. 
The package view is where the response display is defined, the request_list is the full list of the items accepted by each request,
and finally the control package, responsible for manipulation, calling the DB and JWT verification.

Now the model module is where the Database is defined and its functions, 

Obs: Later a .json will be added containing all the routes that are contemplated in the current version

### Below are the libraries necessary for this project

 - datetime
 - flask
 - flask_cors
 - flask_bcrypt
 - jwt
 - marshmallow
 - pymysql
 - sqlachemy
 - webargs

## API Routes
This API only works with 'Content-type' = "application/json", and that is to send all requests via text/json
### User

[POST] - /create/user

    "nome": "John Doe",
    "email": "johndoe@email.com",
    "password": "johnDpass"


[GET] - /get/user

    "id_user": 16


[POST] - /login/user

    "email": "johndoe@email.com",
    "password": "johnDpass"


[DELETE] - /delete/user
    
    "id_user": 16

[POST] - /change/user

    "id_user": 16
    "nome": "John Doe",
    "email": "johndoe@email.com",
    "password": "johnDpass"
    "pontos": 4059
    "tipo_user": "CL"

-------------------------------------------
### Itens

[POST] - /create/item  # Admin


    "nome": "Veja Mult"
    "material": "PL"
    "peso": 0.100
    "pontos": 35



[GET] - /get/item

    "id_item": 584557


[GET] - /get/item/full

     '''''Empty'''''''


-------------------------------------------
#### Lixeira 

[POST] - /create/lixeira

    "endereco_fisico": Av. Ficticia 36
    "capacidade": 50
    "status": 0


[GET] - /get/lixeira

    "id_lixeira": 12


[GET] - /get/lixeira/capacidade

    "id_lixeira": 12


[POST] - /update/lixeira/capacidade  # Admin

    "id_lixeira": 12
    "capacidade": 50
