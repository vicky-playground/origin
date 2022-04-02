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
import member
from attraction import site
from booking import trip

app=Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False


# connect to the local DB
pool = Pool(host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)
pool.init()

"""
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
"""

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

app.register_blueprint(member.user, url_prefix='')
app.register_blueprint(site)
app.register_blueprint(trip)

if __name__=="__main__":
	app.run(host='0.0.0.0',port=3000, use_reloader=False)

#conn.close()