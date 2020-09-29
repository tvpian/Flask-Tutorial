# -*- coding: utf-8 -*-


import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#import app


class Item(Resource):
    #@jwt_required()#Make sure authenctication is asked befor ethe request
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                            required=True,
                            help="This Field cannot be left Blank!")
    @jwt_required()
    def get(self,name):
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        
        #item = next(filter(lambda x:x['name'] == name,items),None)
#        for i in items:
#            if i['name']==name:
#                return i
        if row:
            return {'item':{'name':row[0], 'price':row[1]}}
        return {'message' : 'Item not found'}, 404
    
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        
        row = result.fetchone()
        
        connection.close()
        
        if row:
            return {'item':{'name':row[0],'price':row[1]}}
    
    @classmethod
    def insert(cls,item):
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close() 
    
    def post(self,name):
        if self.find_by_name(name):
            return {'message':"An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        item = {'name': name, 'price':data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occured inserting the item"}, 500 #Internal server error
#        connection =  sqlite3.connect('data.db')
#        cursor = connection.cursor()
#        query = "INSERT INTO items VALUES (?,?)"
#        cursor.execute(query,(item['name'],item['price']))
#        connection.commit()
#        connection.close()
       # data = request.get_json()#silence=True)#force=True) # this statement will give an error if the content type is not mentioned or json data is attached
        return item,201
    
    def delete(self, name):
        #global items
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        
        connection.commit()
        connection.close()
        return {'message':'Item deleted'}
    
    def put(self,name):
        #data=request.get_json()
        
        data =Item.parser.parse_args()
        #item=next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item={'name':name,"price":data['price']}
        
        if item is None:
#            item={'name':name,'price':data['price']}
#            items.append(item)
            try:
                self.insert(updated_item)
            except:
                return {"message":"An Error Occured"},500
        else:
            
            try:
                self.update(updated_item)
            except:
                return {"message":"An Error Occured"},500
        return updated_item
    @classmethod
    def update(cls,item):
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))
        
        connection.commit()
        connection.close()
        
        
class ItemList(Resource):
    @jwt_required()
    def get(self):   
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items "
        result = cursor.execute(query)
        items=[]
        for row in result:
            items.append({'name':row[0],'price':row[1]})
        connection.close()
        
        return {'Items':items}