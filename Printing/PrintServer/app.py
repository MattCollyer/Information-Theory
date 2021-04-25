"""
	Author: Matthew Collyer (matthewcollyer@bennington.edu)
	Date: April 22 2021
"""
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	their_ip = request.remote_addr
	if(request.method == 'POST'):
		message = request.form['message']
		add_message(message, their_ip)
		responded = True
	else:
		responded = False
	return render_template('index.html', their_ip=their_ip, my_ip=request.host, has_responded = responded)



def add_message(message, ip):
	db = mysql.connector.connect(
  	host='print.db',
  	user='kingrat',
		database= 'messages'
	)
	
	cursor = db.cursor()
	sql = "INSERT INTO sent (Message, IP) VALUES (%s, %s)"
	val = (message, ip)
	cursor.execute(sql, val)
	db.commit()

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=80)