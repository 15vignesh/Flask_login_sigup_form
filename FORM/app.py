from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app=Flask(__name__)
app.secret_key="radhakrishna"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='S1450457r$'
app.config['MYSQL_DB']= 'users'
mysql=MySQL(app)
@app.route('/')
def signup():
    return render_template('signup.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST' and 'uname' in request.form and 'email' in request.form and 'pwd' in request.form:
        username=request.form['uname']
        password=request.form['pwd']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE uname = % s',(username,))
        account=cursor.fetchone()
        if account:
            msg='Account Already Exists'
        elif not username:
            msg = 'Please fill out Username'
        elif not email:
            msg='Please fill out Email'
        elif not password:
            msg='Please fill out Password' 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'           
        else:
            cursor.execute('INSERT INTO register VALUES(NULL,% s,% s,% s)',(username,email,password,))
            mysql.connection.commit()
            msg="You've Successfully Registered"
    elif request.method=='POST':
        msg="Please Fill Your Details "
    return render_template('signup.html',msg=msg)
@app.route('/signin', methods =['GET', 'POST'])
def signin():
    msg=''
    if request.method =='POST' and 'uname' in request.form and 'pwd' in request.form:
        username= request.form['uname']
        password = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE uname = % s AND pwd = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['uname']
            msg = 'Logged in successfully !'
            return redirect(url_for('index', msg = msg))
        else:
            msg = 'Incorrect Username/Password'
    return render_template('login.html', msg = msg)
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))
@app.route('/index')
def index():
    if not session.get('username'):
        return redirect(url_for('login'))
    return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)
    