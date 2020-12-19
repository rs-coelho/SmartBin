from marshmallow import fields,ValidationError


def validate_access_token_master_level(access_token):
    pass
    #user_id, _ = OauthAccessTokens.authenticate(access_token)
    #user_label = User.get_group_label(user_id)
    #if user_label not in ('admin', 'master'):
    #    raise ValidationError(GIVEN_USER_HAS_NOT_THE_REQUIRED_LEVEL)



GET_USER = {
    'id_user':fields.Str(required=True)
    #'acess_token': fields.Str(required=True, validate=validate_access_token_master_level),
}