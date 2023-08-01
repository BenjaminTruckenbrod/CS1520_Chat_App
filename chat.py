from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from app_models import Base, RegisteredUser


app = Flask(__name__)



engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# RegisteredUser.__table__.drop(engine)

# Select username, password FROM RegisteredUser WHERE username = username AND password=password

@app.route("/")
def index():
    return redirect(url_for("login_controller"))

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    return render_template("login.html")

@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    return render_template("register.html")

@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", username=username)

@app.route("/profile/", methods=["POST"])
def profile_user():

    # session.query(RegisteredUser).delete()
    # session.commit()

    username = request.form.get("username")
    password = request.form['password']

    # check if its a sign in or registration form

    # sign in form
    if 'sign-in' in request.form:

        #query data base for username and password pair
        names = session.query(RegisteredUser).filter_by(username=username, password=password).all()

        # if there is one then go to profile, otherwise reload page
        if len(names) == 0:
            print("username not registered")
            return redirect(url_for("login_controller"))
        elif len(names) == 1:
            return redirect(url_for("profile", username=username))
        else:
            print("unforseen error checking database for username and password")

    # registration form
    elif 'register' in request.form: 
        print('register')
        password = request.form['password']
        password2 = request.form['password2']

        if password=='':
            print('blank password')
            return render_template("register.html")
        elif password2=='':
            print('blank password')
            return render_template("register.html")

        elif password!=password2 :
            print('passwords do no match')
            return render_template("register.html")
        
        elif password==password2 :
            print('its a match')
            new_user = RegisteredUser(username=username, password=password)
            try:
                session.add(new_user)
                session.commit()
                return redirect(url_for("profile", username=username))
            except:
                return 'There was an issue adding your task'
        else:
            print ('unforseen error comparing passwords with eachother')
            return render_template("register.html")


# @app.route("/profile/<username>", methods=["POST"])
# def profile(username):
#     username = request.form.get("username")
#     return redirect(url_for("profile_user"), username=username)

# @app.route("/logout/")
# def unlogger():
#     return

# @app.route("/new_message/", methods=["POST"])
# def new_message():
#     return

# @app.route("/messages/")
# def messages():
#     return

if __name__ == "__main__":
    app.run(debug=True)

