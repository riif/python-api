import psycopg2
import os
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

username =  os.getenv("USERNAME")
password = os.getenv("PASSWORD")

app = Flask(__name__)
#basic auth
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    if username == username and password == password:
        return username

conn = psycopg2.connect(
    host= os.getenv('DB_HOSTNAME'),
    database = os.getenv('DB_NAME'),
    user= os.getenv('DB_USERNAME'),
    password = os.getenv('DB_PASSWORD'), 
    port = os.getenv('DB_PORT')
)

@app.route('/')
def home():
    return "Hi, I am using Flask"

@app.route("/api/get-employee")
def get_user():
    cur = conn.cursor()

    cur.execute(f"select * from {os.getenv('DB_TABLE_NAME')}")
    data = cur.fetchall()
    
    return jsonify(data), 200

@app.route("/api/insert-employee", methods=["POST"])
@auth.login_required
def insert_employee():
    
    '''employee_id = request.form.get('employee_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    hire_date = request.form.get('hire_date')
    salary = request.form.get('salary')'''

    data = request.get_json()
    employee_id = data["employee_id"]
    first_name = data['first_name']
    last_name = data['last_name']
    address = data['address']
    email = data['email']
    phone = data['phone']
    gender = data['gender']
    hire_date = data['hire_date']
    salary = data['salary']


    cur = conn.cursor()
    cur.execute(f"INSERT INTO {os.getenv('DB_TABLE_NAME')} (employee_id, first_name, last_name, address, email, phone, gender, hire_date, salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        (employee_id, first_name, last_name, address, email, phone, gender, hire_date, salary,))
    conn.commit()
 
    return jsonify(data), 201


if __name__ == "__main__":
    app.run(debug=True)