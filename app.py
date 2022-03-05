from flask import *
app=Flask(__name__, template_folder="templates")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
from flask_restx import Api, Resource, reqparse, fields
import json
from flaskext.mysql import MySQL
import pymysql
pymysql.install_as_MySQLdb()
import pymysql.cursors

# connect to the local DB
db = pymysql.connect(host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)
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

# fetch the data 
for k in range(len(dataList)):
	image =  ["https"+e for e in dataList[k]["file"].split("https") if e]
	# filter out URLs which are not ended with jpg or png
	for i in image:
		if not (i.endswith("JPG") or i.endswith("jpg") or i.endswith("png") or i.endswith("PNG")):
			image.remove(i)
	val = (dataList[k]["info"], dataList[k]["stitle"], dataList[k]["longitude"], dataList[k]["latitude"], dataList[k]["MRT"], dataList[k]["CAT2"], dataList[k]["MEMO_TIME"],image, dataList[k]["xbody"], dataList[k]["address"])
	cursor.execute(sql, val)
	db.commit()

api = Api(app, description="Attraction API")
parser = reqparse.RequestParser()
parser.add_argument(
    "page", type=int,  help='要取得的分頁，每頁 12 筆資料', required=True, nullable=False
)
parser.add_argument(
    "keyword", type=str,  help='篩選景點名稱的關鍵字，沒有給定則不做篩選'
)
@api.route('/api/attractions')
class AttractionApi(Resource):
    @api.doc(parser=parser)
    def get(self):
        # API parameter: page & keyword
        arg = parser.parse_args()
        keyword = arg['keyword']
        if keyword is not None:
            cursor.execute("SELECT * FROM website.TPtrip WHERE stitle LIKE %s",("%"+keyword+"%"))
            result = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM website.TPtrip")
            result = cursor.fetchall()
        # the organized result
        finalResult = []
        # convert the set of images to a list
        for d in result:
            d["file"] = image
        for site in result:
            data = {"id":site["id"],"name":site["stitle"],"category":site["CAT2"],"description":site["xbody"],"address":site["address"],"transport":site["info"],"mrt":site["MRT"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["file"]}
            finalResult.append(data)
        # calculate how many pages should be
        if len(finalResult)%12 == 0:
            pages = len(finalResult)//12  
        else:
            pages = len(finalResult)//12 + 1 
        # check the page input and result output
        if arg['page'] < pages:
            finalResult = [val for idx, val in enumerate(finalResult) if (idx < 12*arg['page'] and idx >= (arg['page']-1)*12)]
            return jsonify({"nextPage": arg['page']+1, 'data' : finalResult})
        elif arg['page'] == pages:
            finalResult = [val for idx, val in enumerate(result) if (idx >= (len(result)//12-1)*12)]
            return jsonify({"nextPage": None, 'data' : finalResult})
        else:
            return jsonify({"error":True, "message": "No relevant data"})

@api.route('/api/attraction/<attractionId>')
class AttractionID(Resource):
    def get(self, attractionId):
        # API parameter: page & keyword
        cursor.execute("SELECT * FROM website.TPtrip WHERE id = %s",(attractionId))
        result=cursor.fetchone()
        if result != 0:   
            result["file"] = image
            finalResult={"data":{"id":result["id"],"name":result["stitle"],"category":result["CAT2"],"description":result["xbody"],"address":result["address"],"transport":result["info"],"mrt":result["MRT"],"latitude":result["latitude"],"longitude":result["longitude"],"images":result["file"]}}
            #summary["data"]["images"]=ast.literal_eval(summary["data"]["images"])
            return jsonify(finalResult)
        return jsonify({"error":True,"message":"No relevant data"})

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

# Run the RESTful API server
app.run(port= 3000)


