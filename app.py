import newtrain
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
d=5
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        flash(str(x))
        if(x==1):
        	y="nphi.html"

        else:
        	y="phi.html"
        return render_template(y)
 
@app.route('/login', methods=['POST'])
def do_admin_login():
	url=request.form['username']
	global x
	x=newtrain.main(url)
	print ("ans")
	
	print(x)
	session['logged_in'] = True
	return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
    