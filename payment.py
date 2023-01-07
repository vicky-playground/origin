from random import random
from flask import *
pay = Blueprint('payment', __name__)
from numpy import integer
import json
import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB
import ast
pymysql.install_as_MySQLdb()
from collections import OrderedDict
import os
from urllib import response
import sys, traceback
from flask_jwt_extended import *
import member
from datetime import datetime
import urllib.request
import random
import requests,json

# connect to the local DB
pool = PooledDB(creator=pymysql, host = "127.0.0.1", user = "root", password="12345678", database='website', port= 3306)

"""
 {
  "data": {
    "number": "20210425121135",
    "payment": {
      "status": 0,
      "message": "付款成功"
    }
  }
}
"""
@pay.route('/api/orders', methods=['POST']) 
def getPrime():
    requestJSON = request.get_json() 
    # store to the server
    userID = session['id']
    email = session['email']
    attractionID = requestJSON['order']['trip']['attraction']['id']
    orderNumber = str(datetime.now().strftime('%Y%m%d%H%M%S'))+str(random.randint(1000,9999))
    contactName = requestJSON['order']['contact']['name']
    contactMail = requestJSON['order']['contact']['email']
    contactPhone = requestJSON['order']['contact']['phone']
    conn = pool.connection()
    cursor = conn.cursor()
    sql = "insert into orders (user_id,attraction_id,order_number,contact_name,contact_mail,contact_phone) values (%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (userID,attractionID,orderNumber,contactName,contactMail,contactPhone)) 
        conn.commit()
        payURL = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        payByPrime = {
            "prime": requestJSON["prime"],
            "partner_key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM", #"partner_0jYjqDcsRxtYsOMHRk8ttXzS64wYkjRL4FnRueeKsZueMbWXDDGwBJpS",
            "merchant_id": "GlobalTesting_CTBC",#"kyc_Swingvy_NCCC_KYC_Verification_Only",
            "details":"TapPay Test",
            "amount": requestJSON['order']['price'],
            "cardholder": {
                "phone_number": contactPhone,
                "name": contactName,
                "email": contactMail,
                "zip_code": "",
                "address": "",
                "national_id": ""
            },
            "remember": True
        }
        
        result = requests.post(payURL,headers={
                "Content-Type":"application/json",
                "x-api-key":"partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM"
            },data=json.dumps(payByPrime))
        res = result.json()
        print("res['status']:", res['status'])
        # if the transaction succeeds
        if res['status'] !=0: 
            print("booking email", email)
            sql = "UPDATE booking SET paid=1 WHERE email=%s"
            cursor.execute(sql,(email))
            conn.commit()
            sql = "UPDATE orders SET payment_status=0 WHERE order_number=%s"
            cursor.execute(sql,orderNumber)
            conn.commit()
            resultJSON = json.dumps({
                    "data":{
                    "number":orderNumber,
                    "payment":{
                        "status":res['status'],
                        "message":"付款成功"
                    }}})

            print("OK!!!!")
        
        # if the transaction fails
        else: 
            resultJSON = json.dumps({"error": True,"number":orderNumber,"message": res['msg']}) 
 
    except:
        resultJSON = json.dumps({"error": True, "message": "建立訂單失敗"})
    finally:
        conn.close()
        cursor.close()   
        return Response(resultJSON, mimetype='application/json')
    
 
    

        
@pay.route('/api/order/<orderNumber>', methods=['GET'])
def getOrder(orderNumber):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM orders WHERE order_number = %s ;"
    cursor.execute(sql,(orderNumber))
    orderResult = cursor.fetchone() 
    #print("get method: ",orderResult)
    attractionID = orderResult['attraction_id']
    cursor.execute("SELECT * FROM booking WHERE attraction_id = %s",attractionID)
    bookingResult = cursor.fetchone()
    cursor.execute("SELECT id,stitle,address, SUBSTRING_INDEX(file, ',', 1) AS image FROM TPtrip WHERE id = %s",attractionID)
    tripResult = cursor.fetchone()
    #print("orderResult: ", orderResult) #{'user_id': 8, 'attraction_id': 3, 'order_number': '202204101642565631', 'contact_name': 'Vicky', 'contact_mail': 'test@gmail.com', 'contact_phone': '23', 'payment_status': 1}
    #print("bookingResult: ", bookingResult) #{'attraction_id': 3, 'date': datetime.date(2022, 3, 30), 'time': 'morning', 'price': 2000, 'email': 'test1234@gmail.com'}
    #print("tripResult: ", tripResult) #{'id': 3, 'stitle': '士林官邸', 'address': '臺北市  士林區福林路60號', 'image': "('https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D7/E150/F719/71eb4b56-f771-43bc-856c-2fb265a5cc6e.jpg'"}
    if orderResult != None :      
        data = {
            "number": orderResult['order_number'],
            "price": bookingResult['price'],
            "trip": {
                "attraction": {
                    "id": tripResult['id'],
                    "name": tripResult['stitle'],
                    "address": tripResult['address'],
                    "image": tripResult['image'][2:-1]
                },
            "date": bookingResult['date'],
            "time": bookingResult['time']
            },
            "contact": {
                "name": orderResult['contact_name'],
                "email": orderResult['contact_mail'],
                "phone": orderResult['contact_phone']
            },
            "status": 1
        }
        
        resultJSON = json.dumps({'data':data}, default = str)
        conn.close()
        cursor.close()
        return Response(resultJSON, mimetype='application/json')
    else :
        resultJSON = json.dumps({"error": True,"message": "no data or without signin"}) 
        conn.close()
        cursor.close()
        return Response(resultJSON, mimetype='application/json')
            



        
    

"""
CREATE TABLE orders(
	user_id BIGINT NOT NULL,
    attraction_id int NOT NULL,
    order_number varchar(30) NOT NULL UNIQUE,
    contact_name varchar(200) NOT NULL,
    contact_mail varchar(200) NOT NULL,
    contact_phone varchar(200) NOT NULL,
    payment_status tinyint NOT NULL default 0,
    payment_message varchar(20),
    error_message varchar(20),
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(attraction_id) REFERENCES TPtrip(id),
    FOREIGN KEY(attraction_id) REFERENCES booking(attraction_id)
);
"""


        
