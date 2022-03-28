from flask import *
user = Blueprint('member', __name__)
import json
import pymysql
import pymysql.cursors
from pymysqlpool.pool import Pool
import ast
pymysql.install_as_MySQLdb()
from collections import OrderedDict
import os
from urllib import response
import sys, traceback
from flask_jwt_extended import *
import member


# connect to the local DB
pool = Pool(host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)
pool.init()


# get the current user's data
@user.route('/api/user', methods=['GET']) 
def getUser():
    if "id" in session :
        id = session['id']
        email = session['email'] 
        name = session['name'] 
        data = {'id':id, 'email':email, 'name':name}
        resultJSON = json.dumps({"data": data}) 
    else :
        resultJSON = json.dumps({"data": None}) 
    return Response(resultJSON, mimetype='application/json')

# sign up
@user.route('/api/user', methods=['POST']) 
def signup():
    requestJSON = request.get_json()
    name = requestJSON['name']
    email = requestJSON['email']
    password = requestJSON['password']
    if name == '' or email == '' or password == '' : 
        resultJSON = json.dumps({"error": True, "message": "資料不能為空白" })
    else:
        conn = pool.get_conn()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM user WHERE email = %s"
        cursor.execute(sql, (email))
        user = cursor.fetchone() 
        # if there is already the user saved in the db
        if user['COUNT(*)'] > 0:
            print("duplicate")
            resultJSON = json.dumps({"error": True, "message": "已被註冊的email"})
        else :
            print("insert")
            sql = "INSERT INTO user (name, email, password) VALUES (%s,%s,%s)"
            cursor.execute(sql, (name, email, password))
            conn.commit()
            resultJSON = json.dumps({"ok": True})
        pool.release(conn)
        cursor.close()
    return Response(resultJSON, mimetype='application/json')

# log in 
@user.route('/api/user', methods=['PATCH']) 
def login():
    requestJSON = request.get_json()
    email = requestJSON['email']
    password = requestJSON['Password']
    conn = pool.get_conn()
    cursor = conn.cursor()
    sql = "SELECT id , email, name, password FROM user WHERE email = %s and password = %s;"
    cursor.execute(sql, (email, password))
    user = cursor.fetchone()
    if user is None:
        resultJSON = json.dumps({"error": True, "message": "帳號或密碼錯誤" })
    else :
        session['id']= user['id']
        session['email'] = user['email']
        session['name'] = user['name']
        resultJSON = json.dumps({"ok": True})
        
    pool.release(conn)
    cursor.close()
    return Response(resultJSON, mimetype='application/json')

# log out
@user.route('/api/user', methods=['DELETE']) 
def logout():
    session.clear()
    resultJSON = json.dumps({"ok": True})
    return Response(resultJSON, mimetype='application/json')