from flask import *
trip = Blueprint('booking', __name__)
import json
import pymysql
import pymysql.cursors
from pymysqlpool.pool import Pool
pymysql.install_as_MySQLdb()
from flask_jwt_extended import *

@trip.route('/api/booking', methods=['GET']) 
def getBooking():
    # see if the user logins or not first
    if 