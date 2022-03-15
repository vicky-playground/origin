import string
from flask import *
from numpy import integer
app=Flask(__name__, template_folder="templates")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
import json
import pymysql
import pymysql.cursors
from pymysqlpool.pool import Pool
import ast
pymysql.install_as_MySQLdb()
from collections import OrderedDict

# connect to the local DB
pool = Pool(host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)
pool.init()
db = pool.get_conn()
cursor = db.cursor(pymysql.cursors.DictCursor)

# create a table in the database
sql="CREATE TABLE IF NOT EXISTS TPtrip (id INT AUTO_INCREMENT, info VARCHAR(255), stitle VARCHAR(10) UNIQUE, longitude VARCHAR(10), latitude VARCHAR(10), MRT VARCHAR(10), CAT2 VARCHAR(10), MEMO_TIME LONGTEXT, file LONGTEXT, xbody LONGTEXT, address VARCHAR(255), PRIMARY KEY (id))"
cursor.execute(sql)
sql = "ALTER TABLE TPtrip AUTO_INCREMENT=1"
cursor.execute(sql)

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
	# filter out URLs which are not ended with jpg or png
	for i in image:
		if not (i.endswith("JPG") or i.endswith("jpg") or i.endswith("png") or i.endswith("PNG")):
			image.remove(i)
	val = (dataList[k]["info"], dataList[k]["stitle"], dataList[k]["longitude"], dataList[k]["latitude"], dataList[k]["MRT"], dataList[k]["CAT2"], dataList[k]["MEMO_TIME"],image, dataList[k]["xbody"], dataList[k]["address"])
	cursor.execute(sql, val)
	db.commit()

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
    if keyword != None and keyword != "":
        cursor.execute("SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.TPtrip WHERE stitle LIKE %s LIMIT %s, %s",(("%"+str(keyword)+"%"),(page+1)*12-12,(page+1)*12))
        result = cursor.fetchall()
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
    else:
        if page == None:
            page = 0
        cursor.execute("SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.TPtrip WHERE id>=%s AND id<=%s",((page+1)*12-11,(page+1)*12))
        result = cursor.fetchall()
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
	# API parameter: page & keyword
    cursor.execute("SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude,file FROM website.TPtrip WHERE id = %s",(attractionId))
    result=cursor.fetchone()
    if result != 0:   
        finalResult={"data":OrderedDict(id = result["id"], name = result["stitle"], category = result["CAT2"], description = result["xbody"], address = result["address"], transport = result["info"], mrt = result["MRT"], latitude = result["latitude"], longitude = result["longitude"], images = result["file"])}
          # convert the set of images to a list
        data["images"] = ast.literal_eval(data["images"])
        return jsonify(finalResult)
    return jsonify({"error":True,"message":"No relevant data"})



if __name__=="__main__":
	app.run(host='0.0.0.0',port=3000, use_reloader=False)


