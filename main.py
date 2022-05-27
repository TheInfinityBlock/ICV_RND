"""
from flask import Flask, jsonify, request
  
app = Flask(__name__)
  
  
@app.route('/hello', methods=['GET'])
def helloworld():
    if(request.method == 'GET'):
        data = {"data": "Hello World"}
        return jsonify(data)
  
  
if __name__ == '__main__':
    app.run(debug=True)
"""

from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import mysql.connector


app =   Flask(__name__)
  
api =   Api(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="My$ql12345",
  database="TestSchema"
)
 
class Customer:
    name = ""
    address = ""

class HelloWorld(Resource):
    def get(self):
        mycursor = mydb.cursor()
        #mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
        mycursor.execute("SELECT * FROM customers")
        myresult = mycursor.fetchall()
        #lstCustomer= list(myresult)
        #return lc
        lstCustomer=[]
        for x in myresult:
            data={"Name":x[0],"Address":x[1]}
            lstCustomer.append(data);
        return lstCustomer

    def post(self):
        json_data = request.get_json(force=True)
        name = json_data['name']
        address = json_data['address']
        mycursor = mydb.cursor()
        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = (name, address)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="Record inserted successfully"
        return jsonify(message=msg)
  
api.add_resource(HelloWorld,'/hello')
  
  
if __name__=='__main__':
    app.run(debug=True)