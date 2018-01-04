from werkzeug.security import safe_str_cmp
from models.user import UserModel



def authenticate(username, password):
    '''
    if user means if user is not None (if user exists)
    '''
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password): # if user means if user is not None
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

