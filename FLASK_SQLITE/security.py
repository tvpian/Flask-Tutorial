# -*- coding: utf-8 -*-

from user import User

from werkzeug.security import safe_str_cmp

#users=[
#    {
#        'id':1,
#        'username':'bob',
#        'password':'asdf'
#    }
#]
#
#username_mapping ={ 'bob': {
#        'id' : 1,
#        'username' : 'bob',
#        'password' : 'asdf'
#        }
#}
#
#
#userid_mapping = { 1: {
#        'id' : 1,
#        'usrname' : 'bob',
#        'password': 'asdf'
#}
#}




def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password,password):       #in python 2.7 its advisable not to use '==' fro string comparison instead
        return user                              # safe_Str_cmp  of werkzeug.security can be used 
    
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

    