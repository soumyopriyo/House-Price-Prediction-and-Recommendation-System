from flask import Flask, render_template, url_for, request, Response,jsonify
import sqlite3
import os
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

filenumber = int(os.listdir('saved_conversations')[-1])
filenumber = filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a house chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()


english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                         {
                            'import_path': 'chatterbot.logic.BestMatch'
                         },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM admin WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('home.html')

    return render_template('index.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS admin(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO admin VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('signup.html')
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
    

model = pickle.load(open("model.pkl", "rb"))

@app.route("/predict", methods=["GET", "POST"])
# @cross_origin()
def predict():
    global city
    if request.method == "POST":
        Area = request.form['Area']
        bhk = request.form['bhk']
        LiftAvailable = request.form['LiftAvailable']
        Resale = request.form['Resale']
        loc = request.form.get('Location')
        city = request.form.get('City')
        
        global prediction
        prediction = model.predict([[float(Area),float(bhk),float(LiftAvailable),float(Resale)]])
        #prediction = "{:.2f}".format(prediction)
        return render_template('logged_in.html', prediction_text="The house price is Rs. {} ".format(prediction))

    return render_template("logged_in.html")
@app.route("/recommend",methods=['GET','POST'])
def recommend():
    #load the dataset
    place= city
    df=pd.read_csv('house1.csv')
    df=df.drop(columns='Unnamed: 0')
    # selecting rows based on condition 
    df = df.loc[df['City'] == place] 
    rf=df.head(10).reset_index()
    return render_template("recommend.html",n=len(rf),price=rf.Price,city=rf.City,area=rf.Area,noofbedrooms=rf.NoofBedrooms,location=rf.Location)


@app.route("/logout")
def logout():
   return render_template("home.html")

@app.route('/chatbot')
def chatbot():
   return render_template('chat.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response
   
if __name__ == "__main__":
    app.run(debug=True)
