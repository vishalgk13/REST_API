from flask import Flask, render_template, url_for, request, redirect,session
from database import get_database
from werkzeug.security import generate_password_hash,check_password_hash
import os

app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = os.urandom(24)
def current_user():
    user = None
    if "user" in session:
        user = session["user"]
        db = get_database()
        user_cur = db.execute('select * from users where name = ?',[user])
        user = user_cur.fetchone()
    return user

@app.route('/')
def index():
    user = current_user()
    return render_template('home.html',user=user)
@app.route('/login',methods=["POST","GET"])
def login():
    user = current_user()
    error = None
    if request.method=="POST":
        name = request.form["name"]
        password=request.form["password"]
        db= get_database()
        user_cursor = db.execute('select * from users where name = ?',[name])
        user=user_cursor.fetchone()
        if user:
            if check_password_hash(user["password"],password):
                session["user"]=user["name"]
                return redirect(url_for("dashboard"))
            else:
                error = "password and username did not matched"
        else:
            error = "invalid username or password"


    return render_template('login.html',loginerror = error,user=user)
@app.route('/register',methods=["POST","GET"])
def register():
    user=current_user()
    db = get_database()
    if request.method=="POST":
        name=request.form["name"]
        password =request.form["password"]
        h_password =generate_password_hash(password)
        dbusers = db.execute('select * from users where name = ?',[ name ])
        existing_username=dbusers.fetchone()
        if existing_username:
            return render_template("register.html" , registererror = "username already taken try another one")
        else:
            db.execute("insert into users(name,password) values(?,?)",[name , h_password] )
            db.commit()
            return redirect(url_for("index"))

    return render_template('register.html',user=user)
@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    user=current_user()
    db = get_database()
    emp_cur=db.execute("select * from emp")
    allemp = emp_cur.fetchall()
    return render_template('dashboard.html',user=user,allemp=allemp)
@app.route('/addnewemployee',methods=["POST","GET"])
def addnewemployee():
    user = current_user()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        db = get_database()
        db.execute('insert into emp (name,email,phone,address) values (?,?,?,?)', [name,email,phone,address])
        db.commit()
        return redirect(url_for("dashboard"))

    return render_template('addnewemployee.html',user=user)
@app.route('/singleemployeeprofile/<int:id>')
def singleemployeeprofile():
    user=current_user()
    db = get_database()
    emp_cur=db.execute("select * from emp where id = ?",[id])
    single_emp=emp_cur.fetchone()
    return render_template('singleemployeeprofile.html',user=user,single_emp=single_emp)
@app.route('/update',methods=["GET","POST"])
def updateemployee():
    user=current_user()
    if request.method=="POST":
        id = request.form["id"]
        name = request.form["name"]
        email = request.form("email")
        phone = request.form("phone")
        address = request.form("address")
        db=get_database()
        db.execute("insert into emp set name = ?, email=? , phone=?, address=? where id=?",[name,email,phone,address,id])
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template('updateemplyoee.html',user=user)
@app.route("/fetchone/<int:empid>")
def fetchone(id):
    user= current_user()
    db=get_database()
    emp_cur=db.execute("select * from emp where id=?" [id])
    single_emp=emp_cur.fetchone()
    return render_template("updateemployee.html",user=user,single_emp=single_emp)

@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete(id):
    user=current_user()
    if request.method=="GET":
        db=get_database()
        db.execute("delete from emp where id =?",[id])
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html",user=user)

@app.route("/login")
def logout():
    session.pop('user',None)
    render_template('home.html')
app.run(debug=True)