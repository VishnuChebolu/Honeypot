# from utilities.sendmail import sendmail
from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
import pytz
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password='vishnu',
    database='honeypot'
    )
cursor = connection.cursor()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("login.html")

@app.route("/getmyip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr})

@app.route("/",methods=["POST"])
def username_print():
    input_username = request.form["username"]
    input_password = request.form["password"]
    try:
        cursor.execute(f"select * from user_data where username='{input_username}' and password='{input_password}';")
    except mysql.connector.errors.ProgrammingError as e:
        return render_template('failure.html', result=e)  
    b = cursor.fetchall()
    if len(b)>0:
        return render_template("success.html",result=b)
    else:
        return render_template('failure.html', result="Credentials Incorrect.")    

def run():
    timenow = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")
    print(f'[{timenow}] : Started HTTP Webserver on port 5500.')
    app.run(debug=True, host='0.0.0.0', port=5500)
