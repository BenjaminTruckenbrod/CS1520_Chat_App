from flask import Flask, render_template, url_for, request, redirect, jsonify
from sqlalchemy import create_engine, delete, func
from sqlalchemy.orm import sessionmaker
from app_models import Base, RegisteredUser, ChatHistory
import json
from datetime import datetime
from datetime import timedelta
# import pytz

app = Flask(__name__)

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

timeStamp = datetime.now()
d2 = timeStamp + timedelta(hours = 4)

timeStampList = list()
timeStampList.insert(0, timeStamp)

# RegisteredUser.__table__.drop(engine)
# ChatHistory.__table__.drop(engine)

# default routing redirects to homepage 
@app.route("/")
def index():
    return redirect(url_for("login_controller"))

#route for login
@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    return render_template("login.html")

#route for register
@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    return render_template("register.html")

#route for profile method is Get 
@app.route("/profile/<username>")
def chat_page(username):
    return render_template("chat_page.html", username=username)

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
            return redirect(url_for("chat_page", username=username))
        else:
            print("unforseen error checking database for username and password")

    # registration form
    elif 'register' in request.form: 
        print('register')

        #check if passwords match
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
            
            # create a new user and send to database
            try:
                session.add(new_user)
                session.commit()
                return redirect(url_for("chat_page", username=username))
            except:
                return 'There was an issue registering your user'
        else:
            print ('unforseen error comparing passwords with eachother')
            return render_template("register.html")

# @app.route("/logout/")
# def unlogger():
#     return

@app.route("/new_message/", methods=["POST"])
def new_message():
    if request.method == 'POST':
        # Get the values of 'author' and 'message' from the request form data
        author = request.form.get('username')
        message = request.form.get('message')
               
        print("Received new message from:", author)
        print("Message content:", message)

        # Create a new ChatHistory object and add it to the session
        new_chat = ChatHistory(author=author, message=message)

        data = {'Key1': author, 'Key2':message}

        try:
            session.add(new_chat)
            session.commit()
            return jsonify(data)
        
        except Exception as e:
            print("Error:", e)
            session.rollback()  # Roll back the changes in case of an error
            return 'There was an issue adding your chat'

@app.route("/messages/")
def messages():
    # chats = session.query(ChatHistory).all()
    counter = request.args.get('counter')
    print('This is the counter ' + counter)
    testchats2 = session.query(ChatHistory).filter(ChatHistory.id>counter).all()



    # print(chats)
    chats_as_json_objects = []
    for chat in testchats2:
        json_object = {}
        json_object[chat.author] = chat.message
        chats_as_json_objects.append(json_object)
        print(json_object)
    
    return json.dumps(chats_as_json_objects)
    # return jsonify("hello World")

# @app.route("/get_new_messages/")
# def get_new_messages():
#     chats = session.query(ChatHistory).filter(ChatHistory.timestamp>timeStampList[0]).all()
#     testchats = session.query(ChatHistory).all()

#     testchats2 = session.query(ChatHistory).filter(ChatHistory.id>last_id).all()

#     # print(last_id)
#     print("THESE ARE SUPPOSED TO BE THE CHATS WITH ID HIGHER THAN LAST ID")
#     print(last_id)
#     print(testchats2)

#     # for chat in testchats2:
#     #     print('\n')
#     #     print("This is the chat ID")
#     #     print(chat.id)

#     # for chat in testchats:
#     #     print('\n')
#     #     print("This is the chat timestamp")
#     #     print(chat.timestamp)
#     #     print("This is the program timestamp")
#     #     print(timeStampList[0])

#     #     if chat.timestamp<timeStampList[0]:
#     #         print("Time stamp is newer")
#     #     elif chat.timestamp>timeStampList[0]:
#     #         print("Chat is newer")

#     #     print('\n')

#     chats_as_json_objects = []
#     for chat in testchats2:
#         json_object = {}
#         json_object[chat.author] = chat.message
#         chats_as_json_objects.append(json_object)
    
#     updateTimeStamp()

#     # print(timeStampList)
#     return json.dumps(chats_as_json_objects)
#     # return jsonify("hello World")


def updateTimeStamp():
    new_datetime = datetime.now()
    d3 = new_datetime + timedelta(hours = 4)

    elem = timeStampList.pop(0)
    # timeStampList.insert(1, elem)
    timeStampList.insert(0, d3)

if __name__ == "__main__":
    app.run(debug=True)

