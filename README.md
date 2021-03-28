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
 - flasgger
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
[GET] - /token # Authorization Required

This route test the validity of the user token

- CODE: [200]

        {
            "connected": "true",
            "message": "This token is valid"
        }
 


[POST] - /create/user

    {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "password": "johnDpass"
    }

 - CODE: [200]

        {
            "connected": "true",
            "data": {
                "id_user": X,
                "name": "John Doe",
                "email": "johnd@email.com"
            }
        }

[GET] - /get/user # Authorization Required

 - CODE: [200]
   
        {
            "connected": "true",
            "data": [
                {
                    "id_user": X,
                    "name": "YOUR NAME",
                    "email": "your_email@email.com"
                }
            ]
        }

[POST] - /login/user 

    {
        "email": "johndoe@email.com",
        "password": "johnDpass"
    }
 - CODE: [200]
   
         {
             "connected": "true",
             "data": {
                 "token": "YOUR_TOKEN",
                 "email": "your_email@email.com"
             }
         }

[DELETE] - /delete/user # Authorization Required

This route deletes the user

    {
        "id_user": "16"
    }

[POST] - /change/user  # Authorization Required

This route updates a user's info

    {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "password": "johnDpass",
    }

-------------------------------------------
### Items

[POST] - /create/item  # Admin Authorization Required

This route creates an items in our catalog

    {
        "item_id": "UNIQUE_BAR_CODE"
        "name": "PRODUCT_NAME",
        "material": "PL",
        "weight": "WEIGHT",
        "pontos": "POINTS"
    }

 - CODE: [200]
   
         {
             "connected": "true",
             "data": {
                 "id_item": "UNIQUE_BAR_CODE",
                 "name": "PRODUCT_NAME",
                 "material": "PL"
             }
         }

[GET] - /get/item # Authorization Required

This route return an items in our catalog

    {
        "id_item": "UNIQUE_BAR_CODE"
    }

- CODE: [200]
   
         {
             "connected": "true",
             "data": [
                    {
                        "id_item": "UNIQUE_BAR_CODE",
                        "name": "PRODUCT_NAME",
                        "material": "PL",
                        "points": POINTS,
                        "img_base64": "LONG_x64_STRING"
                    }
             ]
         }


[POST] - /post/item/img # Admin Authorization Required

    {
        "id_item": "584557"
        "img_base64": "LONG_x64_STRING"
    }

[GET] - /get/item/full # Authorization Required

This route return all items in our catalog

- CODE: [200]
  
          {
              "connected": "true",
              "data": [
                    {
                        "id_item": "UNIQUE_BAR_CODE",
                        "name": "PRODUCT_NAME",
                        "material": "PL",
                        "points": POINTS,
                        "img_base64": "LONG_x64_STRING"
                    }, ...
          }

-------------------------------------------
### Inventory

[POST] - /insert/item/inventory # Authorization Required

This route registers an item disposed by the user

    {
        "id_bin": "12",
        "id_item": "584557"
    }

 - CODE: [200]
   
         {
             "connected": "true",
             "data": {
                 "id_user": X,
                 "id_bin": 12,
                 "id_item": "584557"
             }
         }
}


[GET] - /get/user/inventory # Authorization Required

This route returns all item associated to the user

 - CODE: [200]
   
         {
             "connected": "true",
             "data":[
               {
                 "id_bin": 12,
                 "id_item": "584557"
               }, ...
            ]
         }
}

[POST] - /empty/bin # Authorization Required

This route marks all items of a certain bin as collected

    {
         "id_bin": "12"
    }

- CODE: [200]
   
         {
             "connected": "true",
             "data":[
               {
                 "id_bin": 12,
                 "id_item": "584557"
               }, ...
            ]
         }
}

-------------------------------------------
### Bin 

[POST] - /create/bin #Admin Authorization Required

This route creates a bin

    {
        "address": "Av. Far Far Away 36",
        "capacity": "50",
        "status": "0"
    }

[GET] - /get/bin

This route gets all bin info

    {
        "id_bin": "12"
    }

 - CODE: [200]
         
         {
             "connected": "true",
             "data": {
                 "id_bin": 12,
                 "address": "YOUR_BIN_ADDRESS"
             }
         }

[GET] - /get/bin/capacity # Authorization Required

This route gets a certain bin's capacity

    {
        "id_bin": "12"
    }

 - CODE: [200]
         
         {
             "connected": "true",
             "data": {
                 "id_bin": 12,
                 "capacity": "YOUR_BIN_CAPACITY"
             }
         }

[POST] - /update/bin/capacity  # Admin or Bin Authorization Required

This route updates a certain bin's capacity

    {
        "id_bin": "12",
        "capacity": "50"
    }

 - CODE: [200]
         
         {
             "connected": "true",
             "data": {
                 "id_bin": 1,
                 "capacity": 76,
                 "last_updated": "Sun, 28 Mar 2021 15:12:29 GMT"
             }
         }
