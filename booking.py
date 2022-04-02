from flask import *
trip = Blueprint('booking', __name__)
import json
import pymysql
import pymysql.cursors
from pymysqlpool.pool import Pool
pymysql.install_as_MySQLdb()
from flask_jwt_extended import *
import member


# connect to the local DB
pool = Pool(host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)
pool.init()

# get the trip not ordered yet
@trip.route('/api/booking', methods=['GET'])
def  getTrip():
    if "email" in session :
        print(session['email'])
        email = session['email'] 
        conn = pool.get_conn()
        cursor = conn.cursor()
        sql = "SELECT attraction_id, date, time, price, email, stitle, address, SUBSTRING_INDEX(file, ',', 1) AS image FROM booking INNER JOIN TPtrip ON TPtrip.id = booking.attraction_id WHERE email = %s" # ('https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000340.jpg'
        cursor.execute(sql, (email))
        result = cursor.fetchone()
        if not result: 
            result_JSON = json.dumps({"data": None,"message": "尚未下訂"})
        else: 
            attraction = {
                'id':result['attraction_id'],
                'name':result['stitle'],
                'address':result['address'],
                'image':result['image'][2:-1]
            } #{'id': 2, 'name': '大稻埕碼頭', 'address': '臺北市  大同區環河北路一段', 'image': "('https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000340.jpg'"}
            print(result['image'][2:-1])
            print("result: ",result['time'],result['price'])
            result_JSON = json.dumps({'data':attraction,
                                      'date':result['date'],
                                      'time':result['time'],
                                      'price':result['price']},  indent=1, default=str)     
        
    else:
        result_JSON = json.dumps({"error": True,"message": "請登入會員"})
        print("message", "請登入會員", result_JSON)
    pool.release(conn)
    cursor.close()
    return Response(result_JSON, mimetype='application/json')

# build a new trip
@trip.route('/api/booking', methods=['POST'])
def  postTrip():
    print("email: ", session['email'])
    req_data = request.get_json() #{'attractionId': '2', 'date': '2022-04-07', 'time': 'morning', 'price': '2000'}
    email = session['email']
    AttractionId = req_data['attractionId']
    Date =req_data['date']
    Price = req_data['price']
    Time = req_data['time']
    session['price'] = Price
    if Date == '' or Price == '' or Time == '' : 
        result_JSON = json.dumps({"error": bool(True) ,"message": "請填寫完整資料"})
    elif id == '':
        result_JSON = json.dumps({"error": bool(True) ,"message": "請登入會員"})
    else:
        conn = pool.get_conn()
        cursor = conn.cursor()
        sql = "select attraction_id FROM booking where (email = %s) ;"
        sql_run =  cursor.execute(sql, (email))
        # update if there has been a booking record
        if sql_run !=0: 
            try:
                sql = "UPDATE booking SET attraction_id=%s, date=%s, time=%s, price=%s WHERE email=%s;"
                sql_run = cursor.execute(sql,(AttractionId,Date,Time,Price,email))
                conn.commit() 
                print("update: ", AttractionId, Date, Price, Time) #3 2022-04-07 2000 morning
                result_JSON = json.dumps({"ok": bool(True)})
            except:
                result_JSON = json.dumps({"error": bool(True) ,"message": "下訂失敗"})
                
        # insert if there is no booking record
        else:
            try:
                sql = "INSERT INTO booking (attraction_id, date, time, price, email) VALUES (%s,%s,%s,%s,%s)"
                sql_run = cursor.execute(sql, (AttractionId, Date, Time, Price, email))
                conn.commit() 
                print("insert: ", AttractionId, Date, Price, Time)
                result_JSON = json.dumps({"ok": bool(True)})
                print("result: ", result_JSON) 
            except:
                result_JSON = json.dumps({"error": bool(True) ,"message": "下訂失敗"})
    pool.release(conn)
    cursor.close()
    return Response(result_JSON, mimetype='application/json')
  
            
# delete the trip
@trip.route('/api/booking', methods=['DELETE'])
def  deleteTrip():
    if "email" in session :
        try:
            email = session['email'] #test@gmail.com
            conn = pool.get_conn()
            cursor = conn.cursor()
            sql = "DELETE FROM booking WHERE email = %s;"
            cursor.execute(sql,(email))
            conn.commit()
            print("record(s) deleted")
            result_JSON = json.dumps({"ok": bool(True)})
        except :
            result_JSON = json.dumps({"error": bool(True),"message": "刪除失敗"})
            print("刪除失敗")
    else :
        result_JSON = json.dumps({"error": bool(True) ,"message": "流程錯誤"})
    pool.release(conn)
    cursor.close()
    return Response(result_JSON, mimetype='application/json')