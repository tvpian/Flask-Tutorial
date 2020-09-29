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


user = [
        User(1, 'bob' , 'asdf'),
        User(2, 'ashley' , 'df')
        ]


username_mapping = {
        u.username: u for u in user
        }

userid_mapping = {
        u.id : u for u in user
        }

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password,password):       #in python 2.7 its advisable not to use '==' fro string comparison instead
        return user                              # safe_Str_cmp  of werkzeug.security can be used 
    
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

    