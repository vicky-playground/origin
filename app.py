from flask import *
import os
import member
import attraction
from attraction import site

app=Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False



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

if __name__=="__main__":
	app.run(host='0.0.0.0',port=3000, use_reloader=False)
