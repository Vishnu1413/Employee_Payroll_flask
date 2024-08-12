from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re                           #regular expression

app=Flask(__name__)
app.secret_key='flaskclass'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='project'

mysql=MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/userlogin',methods=['GET','POST'])
def login():
    message=''
    if request.method=='POST':
        userName=request.form['name']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from empde where Name=%s and Password=%s',(userName,password))
        user=cursor.fetchone()
        if user:
            session['loggedin']=True
            session['name']=user['Name']
            session['email']=user['Email']
            message='Logged in Successfully'
            return render_template('empde.html',message=message,)
        else:
            message='UserName / password is incorrect'
    return render_template('login.html',message=message)
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route('/userregister',methods=['GET','POST'])
def userregister():
    message=''
    if request.method=='POST':
        userName=request.form['name']
        email=request.form['email']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from empde where Email=%s ',(email,))
        account=cursor.fetchone()
        if account:
            message='Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            message='Invalid email address'
        elif not userName or not password or not email:
            message='Please fill out the form'
        else:
            cursor.execute('INSERT INTO empde(Name,Email,Password) VALUES (%s,%s,%s)',
                           (userName,email,password))
            mysql.connection.commit()
            message='You have Successfully Registered'
    elif request.method=='GET':
        message='Please fill out the form'
    return render_template('register.html',message=message)

@app.route('/Auserlogin',methods=['GET','POST'])
def Alogin():
    message=''
    if request.method=='POST':
        userName=request.form['name']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from ade where Name=%s and Password=%s',(userName,password))
        user=cursor.fetchone()
        if user:
            session['loggedin']=True
            session['name']=user['Name']
            session['email']=user['Email']
            message='Logged in Successfully'
            return redirect(url_for("viewemp"))
        else:
            message='UserName / password is incorrect'
            return render_template('Alogin.html',message=message)
    else:
        return render_template('Alogin.html')

@app.route('/Auserregister',methods=['GET','POST'])
def Auserregister():
    message=''
    if request.method=='POST':
        userName=request.form['name']
        email=request.form['email']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from ade where Email=%s ',(email,))
        account=cursor.fetchone()
        if account:
            message='Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            message='Invalid email address'
        elif not userName or not password or not email:
            message='Please fill out the form'
        else:
            cursor.execute('INSERT INTO ade(Name,Email,Password) VALUES (%s,%s,%s)',
                           (userName,email,password))
            mysql.connection.commit()
            message='You have Successfully Registered'
    elif request.method=='GET':
        message='Please fill out the form'
    return render_template('Aregister.html',message=message)

 
@app.route("/viewemp")
def viewemp():
    db=MySQLdb.connect("localhost","root","","project")
    c1=db.cursor()
    c1.execute("select * from shemp")
    data=c1.fetchall()
    return render_template("ade.html",data=data)

@app.route('/update',methods=['POST'])
def update():
    db=MySQLdb.connect("localhost","root","","project")
    cur=db.cursor()
    salary=request.form['salary']
    id =request.form['id']
    cur.execute("UPDATE shemp SET Actual_salary=%s WHERE id=%s",(salary,id))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('viewemp'))
 
if __name__=='__main__':
    app.run(debug=True,port=5001) 
