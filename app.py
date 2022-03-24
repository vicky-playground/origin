from flask import *
from numpy import integer
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

app=Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False


# connect to the local DB
pool = Pool(host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)
pool.init()


# conenct the pool
conn = pool.get_conn()
cursor = conn.cursor()

# create a table in the database
sql="CREATE TABLE IF NOT EXISTS TPtrip (id INT AUTO_INCREMENT, info VARCHAR(255), stitle VARCHAR(10) UNIQUE, longitude VARCHAR(10), latitude VARCHAR(10), MRT VARCHAR(10), CAT2 VARCHAR(10), MEMO_TIME LONGTEXT, file LONGTEXT, xbody LONGTEXT, address VARCHAR(255), PRIMARY KEY (id))"
cursor.execute(sql)
# release the connection back to the pool for reuse
pool.release(conn)
cursor.close()

# conenct the pool
conn = pool.get_conn()
cursor = conn.cursor()

sql = "ALTER TABLE TPtrip AUTO_INCREMENT=1"
cursor.execute(sql)
# release the connection back to the pool for reuse
pool.release(conn)
cursor.close()


# import the JSON file
with open('data/taipei-attractions.json', 'r') as f:   	
    data = json.load(f)
# attraction list
dataList = data["result"]["results"] 

# insert values into database without duplicate values
sql = "INSERT IGNORE INTO TPtrip (info, stitle , longitude, latitude, MRT, CAT2, MEMO_TIME, file, xbody, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %r, %s, %s)"

# add the data into the database
for k in range(len(dataList)):
    image =  ["https" + e for e in dataList[k]["file"].split("https") if e]
    # conenct the pool
    conn = pool.get_conn()
    cursor = conn.cursor()
	# filter out URLs which are not ended with jpg or png
    for i in image:
        if not (i.endswith("JPG") or i.endswith("jpg") or i.endswith("png") or i.endswith("PNG")):
            image.remove(i)
    val = (dataList[k]["info"], dataList[k]["stitle"], dataList[k]["longitude"], dataList[k]["latitude"], dataList[k]["MRT"], dataList[k]["CAT2"], dataList[k]["MEMO_TIME"],image, dataList[k]["xbody"], dataList[k]["address"])
    cursor.execute(sql, val)
    conn.commit()
    # release the connection back to the pool for reuse
    pool.release(conn)
    cursor.close()



# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions", methods=["GET"])
def attractionAPI():
	# API parameter: page & keyword
    keyword = request.args.get('keyword')
    page = int(float(request.args.get("page")))
    # if there is a keyword
    if keyword != None and keyword != "":
        # conenct the pool
        conn = pool.get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.TPtrip WHERE stitle LIKE %s LIMIT %s, %s",(("%"+str(keyword)+"%"),(page+1)*12-12,(page+1)*12))
        result = cursor.fetchall()
        # release the connection back to the pool for reuse
        pool.release(conn)
        cursor.close()

        dataLen = len(result)
        rowcount = cursor.rowcount
        # the organized result
        finalResult = []
        for site in result:
            data = OrderedDict(id = site["id"], name = site["stitle"], category = site["CAT2"], description = site["xbody"], address = site["address"], transport = site["info"], mrt = site["MRT"], latitude = site["latitude"], longitude = site["longitude"], images = site["file"])
            # convert the set of images to a list
            data["images"] = ast.literal_eval(data["images"])
            finalResult.append(data)
        if dataLen > 0:
            # output
            if rowcount < 12 :
                return jsonify({"nextPage": None, 'data' : finalResult}) 
            else:
                return jsonify({"nextPage": page+1, 'data' : finalResult})        
        return jsonify({"error":True, "message": "No relevant data"})
    # if there is no input of keyword
    else:
        if page == None:
            page = 0
        conn = pool.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.TPtrip LIMIT %s, %s",((page+1)*12-11,(page+1)*12))
        result = cursor.fetchall()
        # release the connection back to the pool for reuse
        pool.release(conn)
        cursor.close()

        dataLen = len(result)
        rowcount = cursor.rowcount
        # the organized result
        finalResult = []
        # convert the set of images to a list
        for site in result:
            data = OrderedDict(id = site["id"], name = site["stitle"], category = site["CAT2"], description = site["xbody"], address = site["address"], transport = site["info"], mrt = site["MRT"], latitude = site["latitude"], longitude = site["longitude"], images = site["file"])
            # convert the set of images to a list
            data["images"] = ast.literal_eval(data["images"])
            finalResult.append(data)
        if dataLen > 0:
            # output
            if rowcount < 12 :
                return jsonify({"nextPage": None, 'data' : finalResult}) 
            else:
                return jsonify({"nextPage": page+1, 'data' : finalResult})
        return jsonify({"error":True, "message": "No relevant data"})
		

@app.route("/api/attraction/<attractionId>", methods=["GET"])
def attractionIdApi(attractionId):
    try:
        # conenct the pool
        conn = pool.get_conn()
        cursor = conn.cursor()
	    # API parameter: page & keyword
        cursor.execute("SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.TPtrip WHERE id = %s",(attractionId))
        result=cursor.fetchone()
        if result != 0:   
            finalResult = {"data":OrderedDict(id = result["id"], name = result["stitle"], category = result["CAT2"], description = result["xbody"], address = result["address"], transport = result["info"], mrt = result["MRT"], latitude = result["latitude"], longitude = result["longitude"], images = result["file"])}
            # convert the set of images to a list
            finalResult["data"]["images"] = ast.literal_eval(finalResult["data"]["images"])
            return jsonify(finalResult)
    except:
        return jsonify({"error":True,"message":"No relevant data"})
    finally:
       # release the connection back to the pool for reuse
        pool.release(conn)
        cursor.close()

# get the current user's data
@app.route('/api/user', methods=['GET']) 
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
@app.route('/api/user', methods=['POST']) 
def signup():
    req_data = request.get_json()
    name =req_data['name']
    email = req_data['email']
    password = req_data['password']
    if name == '' or email == '' or password == '' : 
        resultJSON = json.dumps({"error": True, "message": "資料不能為空白" })
    else:
        conn = pool.get_conn()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM user WHERE email = %s"
        cursor.execute(sql, (email))
        result = cursor.fetchone() 
        # if there is already the user saved in the db
        if result['COUNT(*)'] > 0:
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
@app.route('/api/user', methods=['PATCH']) 
def login():
    req_data = request.get_json()
    email =req_data['email']
    password = req_data['Password']
    conn = pool.get_conn()
    cursor = conn.cursor()
    sql = "SELECT id , email, name, password FROM user WHERE email = %s and password = %s;"
    cursor.execute(sql, (email, password))
    result = cursor.fetchone()
    if result['email'] == email :
        session['id']= result['id']
        session['email'] = result['email']
        session['name'] = result['name']
        resultJSON = json.dumps({"ok": True})
    else :
        resultJSON = json.dumps({"error": True, "message": "帳號或密碼錯誤" })
    pool.release(conn)
    cursor.close()
    return Response(resultJSON, mimetype='application/json')

# log out
@app.route('/api/user', methods=['DELETE']) 
def logout():
    session.clear()
    resultJSON = json.dumps({"ok": True})
    return Response(resultJSON, mimetype='application/json')


if __name__=="__main__":
	app.run(host='0.0.0.0',port=3000, use_reloader=False)

#conn.close()