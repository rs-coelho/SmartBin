# API Smart Bin
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

    {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "password": "johnDpass"
    }

[GET] - /get/user # Authorization Required

    {
        "id_user": "16"
    }

[POST] - /login/user 

    {
        "email": "johndoe@email.com",
        "password": "johnDpass"
    }

[DELETE] - /delete/user # Authorization Required

    {
        "id_user": "16"
    }

[POST] - /change/user  # Authorization Required

    {
        "id_user": "16",
        "name": "John Doe",
        "email": "johndoe@email.com",
        "password": "johnDpass",
        "pontos": "4059",
        "tipo_user": "CL"
    }

-------------------------------------------
### Items

[POST] - /create/item  # Admin Authorization Required

    {
        "name": "Veja Mult",
        "material": "PL",
        "weight": "0.100",
        "pontos": "35"
    }

[GET] - /get/item # Authorization Required

    {
        "id_item": "584557"
    }

[POST] - /post/item/img # Admin Authorization Required

    {
        "id_item": "584557"
        "img_base64": "LONG_x64_STRING"
    }

[GET] - /get/item/full # Authorization Required

    {
        "token": "TOKEN_RETURNED_BY_LOGIN"
    }

-------------------------------------------
### Inventory

[POST] - /insert/item/inventory # Authorization Required

    {
        "id_user": "16",
        "id_bin": "12",
        "id_item": "584557"
    }

[GET] - /get/user/inventory # Authorization Required
    
    {
        "id_user": "16"
    }

[POST] - /empty/bin # Authorization Required

    {
         "id_bin": "12"
    }

-------------------------------------------
### Bin 

[POST] - /create/bin #Admin Authorization Required

    {
        "address": "Av. Far Far Away 36",
        "capacity": "50",
        "status": "0"
    }

[GET] - /get/bin

    {
        "id_bin": "12"
    }

[GET] - /get/bin/capacity # Authorization Required

    {
        "id_bin": "12"
    }

[POST] - /update/bin/capacity  # Admin or Bin Authorization Required

    {
        "id_bin": "12",
        "capacity": "50"
    }
