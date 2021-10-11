from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
# mysql db connecting
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lekha@123'
app.config['MYSQL_DB'] = 'titanic'

mysql =MySQL(app)
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
    survival_value = int(predicted_value[0])
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO TitanicPredictedDatas(Survival,t_class, age, sibsp, parch, gender) VALUES (%s,%s, %s,%s,%s,%s)", (survival_value,t_class,age,sibsp,parch,gender))
    mysql.connection.commit()

    if predicted_value[0] == 0:
        return (' Your chances of survival rate is low!!...you will NOT SURVIVE.')
    elif predicted_value[0] == 1:
        return (' Your chances of survival rate is high!!...you will SURVIVE.')
    #cur.close()
    
if __name__ == '__main__':
    app.run(debug = True)