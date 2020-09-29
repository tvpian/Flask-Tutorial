# -*- coding: utf-8 -*-


from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT ,jwt_required
#import base64
#import glob

from security import authenticate , identity
from user import UserRegister

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key='jose'
api=Api(app)


jwt = JWT(app,authenticate,identity)#creates a new endpoint /auth

items = []


class Item(Resource):
    #@jwt_required()#Make sure authenctication is asked befor ethe request
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                            required=True,
                            help="This Field cannot be left Blank!")
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x:x['name'] == name,items),None)
#        for i in items:
#            if i['name']==name:
#                return i
        return {'Item':item}, 200 if item is not None else 404  ## Jasonfy is not necessary for Flask restful, henceforth dictionary can be send as such without being converted to json format.
    
    def post(self,name):
        if next(filter(lambda x:x['name'] == name, items), None): #is not None:
            return {'message': "An item with name '{}' already exists,".format(name)}, 404
       # data = request.get_json()#silence=True)#force=True) # this statement will give an error if the content type is not mentioned or json data is attached
        data =Item.parser.parse_args()
        price = data['price']
        item = {'name':name,'price':price}
        items.append(item)
        return items, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x : x['name'] != name, items))
        return {'message':'Item deleted'}
    
    def put(self,name):
        #data=request.get_json()
        
        data =Item.parser.parse_args()
        item=next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item={'name':name,'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
        
class ItemList(Resource):
    @jwt_required()
    def get(self):   
       return {'Items':items}

    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')



#if __name__ == '__main__':
app.run(port=5000)
