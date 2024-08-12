@app.route('/')
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
            return render_template('ade.html',message=message)
        else:
            message='UserName / password is incorrect'
    return render_template('login.html',message=message)

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
    return render_template('register.html',message=message)
 
