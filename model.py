import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import MySQLdb
import csv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class titanic_data(Base):
    __tablename__ = 'titanic_data'
    id = Column(Integer, primary_key=True)
    PassengerId = Column(Integer)
    Survived = Column(Integer)
    Pclass = Column(Integer)
    Name = Column(String(50))
    Sex = Column(String(50))
    Age = Column(Integer)
    SibSp = Column(Integer)
    Parch = Column(Integer)
    Ticket = Column(Integer)
    Fare = Column(String(50))
    Cabin = Column(String(50))
    Embarked = Column(String(50))

Base.metadata.create_all(engine)
with open('titanic_train.csv','r') as file:
    data = csv.DictReader(file)
    for i in data:
        row = titanic_data(PassengerId = i['PassengerId'] , Survived = i['Survived'] ,Pclass = i['Pclass'] , Name = i['Name'] , Sex = i['Sex'],Age = i['Age'] , SibSp = i['SibSp'] , Parch = i['Parch'] , Ticket = i['Ticket'] , Fare = i['Fare'] , Cabin = i['Cabin'] , Embarked = i['Embarked'])
        session.add(row)
session.commit()

data = pd.read_sql('select * from titanic_data',engine ,index_col='id')

data.replace(f'^\s*$',np.nan,regex=True,inplace=True)
data['Age'].fillna(data['Age'].mean(),inplace=True)
data['Age'] = data['Age'].astype(int)
#print(data['Age'].head())

gender = pd.get_dummies(data['Sex'],drop_first=True)
data['Gender'] = gender
data.drop('Sex',axis=1,inplace=True)
data.drop(['Ticket','Embarked','PassengerId','Cabin','Name','Fare'],axis=1,inplace=True)

#print(data.head(5))
#choosing the target variable
x= data[['Pclass','Age','SibSp','Parch','Gender']] #independent variables
y= data['Survived'] #Dependent variables

#4.Data Modelling
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2 , random_state=42)

#logistic regression
from sklearn.linear_model import LogisticRegression
lr1 = LogisticRegression(random_state=1).fit(x_train, y_train)
#predict = lr1.predict(x_test)
#print(predict)

pickle.dump(lr1,open('model.pkl','wb'))
accuracy=round(lr1.score(x_train, y_train) * 100, 2)
#print(accuracy)
#from sklearn.metrics import confusion_matrix
#confusion_matrix(y_test,predict)
#pd.DataFrame(confusion_matrix(y_test,predict),columns=['Predicted no','predicted yes'],index=['Actual no','Actual yes'])
