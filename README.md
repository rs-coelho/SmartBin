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