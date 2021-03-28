from marshmallow import fields


# Not in utilization, because this is a list to get the token from the body
# This version is getting the Auth Token from the request Headers
TOKEN_AUTH = {
    'Authorization': fields.Str(required=True),
}


CREATE_USER = {
    'name': fields.Str(required=True),
    'email': fields.Str(required=True),
    'password': fields.Str(required=True),
    'points': fields.Str(required=False),
    'tipo_user': fields.Str(required=False),
}


GET_USER = {
    'id_user': fields.Str(required=True),
}


LOGIN_USER = {
    'email': fields.Str(required=True),
    'password': fields.Str(required=True),
}


CHANGE_USER = {
    'name': fields.Str(required=False),
    'email': fields.Str(required=False),
    'password': fields.Str(required=False),
}

# ===============================================================================

CREATE_ITEM = {
    'id_item': fields.Str(required=True),
    'name': fields.Str(required=True),
    'material': fields.Str(required=True),
    'weight': fields.Str(required=True),
    'points': fields.Str(required=False),

}


GET_ITEM = {
    'id_item': fields.Str(required=True)

}


UPLOAD_ITEM_IMG = {
    'id_item': fields.Str(required=True),
    'img_base64': fields.Str(required=True)

}

# ===============================================================================

CREATE_INV_ITEM = {
    'id_bin': fields.Str(required=True),
    'id_item': fields.Str(required=True)
}

# ===============================================================================

CREATE_BIN = {
    'address': fields.Str(required=True),
    'capacity': fields.Str(required=False),
    'status': fields.Str(required=False),
}


GET_BIN = {
    'id_bin': fields.Str(required=True),
}


UPDATE_BIN_CAPACITY = {
    'id_bin': fields.Int(required=True),
    'capacity': fields.Int(required=True),
}
