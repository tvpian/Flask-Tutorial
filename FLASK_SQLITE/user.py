import sqlite3
from flask_restful import Resource
from flask_restful import Api,reqparse



# -*- coding: utf-8 -*-
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod#helps to avoid hardcoding of the class name
    def find_by_username(cls,username):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM USERS WHERE username=?"
        result = cursor .execute(query, (username,)) 
        row = result.fetchone()
        if row:
            user= cls(*row)#(row[0],row[1],row[2])
        else:
            user = None
        connection.close()
        return user
        
    @classmethod#helps to avoid hardcoding of the class name    
    def find_by_id(cls,_id):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM USERS WHERE id=?"
        result = cursor .execute(query, (_id,)) 
        row = result.fetchone()
        if row:
            user= cls(*row)#(row[0],row[1],row[2])
        else:
            user = None
        connection.close()
        return user
    
    
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                            required=True,
                            help="This Field cannot be left Blank!")
    parser.add_argument('password', type=str,
                            required=True,
                            help="This Field cannot be left Blank!")
    def post(self):
        data =UserRegister.parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {"Message":"A user with the username already exists"},400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO USERS VALUES(NULL,?,?)"
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()
        
        return {"message":"User Created Successfully"}
        