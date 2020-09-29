# -*- coding: utf-8 -*-


from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT ,jwt_required
#import base64
#import glob

from security import authenticate , identity
from user import UserRegister

from item import Item,ItemList

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key='jose'
api=Api(app)


jwt = JWT(app,authenticate,identity)#creates a new endpoint /auth




    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')



if __name__ == '__main__':
    app.run(port=5000)
