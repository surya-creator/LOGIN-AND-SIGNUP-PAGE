
from flask import Flask, render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "12345"


app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] ="mysqleight"
app.config["MYSQL_DB"] ="login"
app.config["MYSQL_HOST"] ="localhost"
db= MySQL(app)

@app.route("/",methods = ["GET","POST"])
def index():
    if request.method =="POST":
        if "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from user where email = %s AND password = %s", (username, password))
            data = cursor.fetchone()
            print(data)
            if data is not None:
                if data["email"] == username and data["password"] == password:
                    session['loginsucess']= True
                    return redirect(url_for("profile"))
                else:
                    return redirect(url_for("index"))


    return render_template("form_ex.html")

#inserting new users details

@app.route("/new",methods = ["GET","POST"])
def new_user():
    if request.method =="POST":
        if "one" in request.form and "two" in request.form and "three" in request.form:
            username = request.form["one"]
            email = request.form["two"]
            password = request.form["three"]
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("Insert into user(name,email,password) values(%s,%s,%s)",(username,email,password))
            db.connection.commit()
            return redirect(url_for("index"))


    return render_template("register.html")

@app.route("/new/profile")
def profile():
    if session['loginsucess'] == True:
        return render_template("profile.html")


@app.route("/new/logout")
def logout():
    if session.pop("loginsucess",None):
        return redirect(url_for("index"))


if (__name__ == '__main__'):
    app.run(debug=True)



