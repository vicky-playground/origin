from flask import *
user = Blueprint('member', __name__)
import json
import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB
pymysql.install_as_MySQLdb()
from flask_jwt_extended import *


# connect to the local DB
pool = PooledDB(creator=pymysql, host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)



# get the current user's data from session  
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
        conn = pool.connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE email = %s"
        cursor.execute(sql, (email))
        user = cursor.fetchone() 
        msg = ''
        # if there is already the user saved in the db
        if user is not None:
            print("duplicate")
            msg = "已被註冊的email"
            resultJSON = json.dumps({"error": True, "message": msg})
        else:
            print("insert")
            sql = "INSERT INTO user (name, email, password) VALUES (%s,%s,%s)"
            cursor.execute(sql, (name, email, password))
            conn.commit()
            resultJSON = json.dumps({"ok": True})
        conn.close()
        cursor.close()
    return Response(resultJSON, mimetype='application/json')

"""
        if not checkPassword(password):
            print("psw not strong")
            if msg != "":
                msg = msg+"、密碼強度不符"
            else:
                msg = "密碼強度不符"
            resultJSON = json.dumps({"error": True, "message": msg})
        """
#Function to validate the password
"""
def checkPassword(passwd):   
    SpecialSym =['$', '@', '#', '%']
    val = True
      
    if len(passwd) < 6:
        print('length should be at least 6')
        val = False
          
    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False
          
    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False
          
    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val
"""

# log in 
@user.route('/api/user', methods=['PATCH']) 
def login():
    requestJSON = request.get_json()
    email = requestJSON['email']
    password = requestJSON['Password']
    conn = pool.connection()
    cursor = conn.cursor()
    sql = "SELECT id , email, name, password FROM user WHERE email = %s and password = %s;"
    cursor.execute(sql, (email, password))
    user = cursor.fetchone()
    if user is None:
        resultJSON = json.dumps({"error": True, "message": "帳號或密碼錯誤" })
    else :
        session['id']= user[0]
        session['email'] = user[1]
        session['name'] = user[2]
        resultJSON = json.dumps({"ok": True})
        
    conn.close()
    cursor.close()
    return Response(resultJSON, mimetype='application/json')

# log out
@user.route('/api/user', methods=['DELETE']) 
def logout():
    session.clear()
    resultJSON = json.dumps({"ok": True})
    return Response(resultJSON, mimetype='application/json')