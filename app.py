from flask import Flask,render_template,url_for,request
import numpy as np
import pickle
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
import pymysql
import MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@127.0.0.1:3306/titanic'
db = SQLAlchemy(app)

class titanic_predicted_data(db.Model):
    __tablename__ = 'titanic_predicted_data'
    PassengerId = db.Column(db.Integer, primary_key=True,autoincrement=True)
    t_class = db.Column(db.Integer)
    age = db.Column(db.Integer)
    sibsp = db.Column(db.Integer)
    parch = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    survival = db.Column(db.Integer)
    def __init__(self,t_class, age, sibsp, parch, gender,survival):
      self.t_Class = t_class
      self.age= age
      self.sibsp = sibsp
      self.parch = parch
      self.gender = gender
      self.survival = survival

model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    fullName = request.values['fullName']
    gender = int(request.values['gender'])
    age = int(request.values['age'])
    t_class = int(request.values['t_class'])
    sibsp = int(request.values['sibsp'])
    parch = int(request.values['parch'])
    
    predicted_value = model.predict([[t_class, age, sibsp, parch, gender]])
    survival = int(predicted_value[0])
    value = titanic_predicted_data(t_class, age, sibsp, parch, gender,survival)
    
    db.session.add(value)
    db.session.commit()

    if predicted_value[0] == 0:
        return (' Your chances of survival rate is low!!...you will NOT SURVIVE.')
    elif predicted_value[0] == 1:
        return (' Your chances of survival rate is high!!...you will SURVIVE.')
    
if __name__ == '__main__':
    app.run(debug = True)