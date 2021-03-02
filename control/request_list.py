from marshmallow import fields

TOKEN_AUTH = {
    'token': fields.Str(required=True),
}


CREATE_USER = {
    'nome': fields.Str(required=True),
    'email': fields.Str(required=True),
    'password': fields.Str(required=True),
    'pontos': fields.Str(required=False),
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
    'id_user': fields.Str(required=True),
    'nome': fields.Str(required=False),
    'email': fields.Str(required=False),
    'password': fields.Str(required=False),
    'pontos': fields.Str(required=False),
    'tipo_user': fields.Str(required=False),
}

# ===============================================================================

CREATE_ITEM = {
    'nome': fields.Str(required=True),
    'material': fields.Str(required=True),
    'peso': fields.Str(required=True),
    'pontos': fields.Str(required=False),

}


GET_ITEM = {
    'id_item': fields.Str(required=True)

}

# ===============================================================================

CREATE_INV_ITEM = {
    'id_lixeira': fields.Str(required=True),
    'id_item': fields.Str(required=True),
    'id_user': fields.Str(required=True),
}

# ===============================================================================

CREATE_LIXEIRA = {
    'address': fields.Str(required=True),
    'capacity': fields.Str(required=False),
    'status': fields.Str(required=False),
}


GET_LIXEIRA = {
    'id_lixeira': fields.Str(required=True),
}


UPDATE_LIXEIRA_CAPACIDADE = {
    'id_lixeira': fields.Str(required=True),
    'capacity': fields.Str(required=True),
}
