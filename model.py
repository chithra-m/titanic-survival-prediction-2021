import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import MySQLdb
import csv
#import mysql.connector as msql
#from mysql.connector import Error
#1.Data capture
data = pd.read_csv('titanic_train.csv')
#print(data.head(7))

#print(data.isna().sum())
data['Age'].fillna(data['Age'].mean(),inplace=True)
data['Age'] = data['Age'].astype(int)
#print(data['Age'].head())

gender=pd.get_dummies(data['Sex'],drop_first=True)
data['Gender'] = gender
data.drop('Sex',axis=1,inplace=True)
data.drop(['Ticket','Embarked','PassengerId','Cabin','Name','Fare'],axis=1,inplace=True)

#print(data.head(5))
"""
try:
    conn = MySQLdb.connect(host='localhost', database='titanic', user='root', password='Lekha@123')
    #if conn.is_connected():
    cursor = conn.cursor()
    for i,row in data.iterrows():
        cursor.execute('INSERT INTO TitanicActualData(Survived,Pclass, Age, SibSp, Parch, Gender)VALUES (%s,%s, %s,%s,%s,%s)', row)
        conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)
"""


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
#model = pickle.load(open('model.pkl','rb'))
#print(model.predict([[1,22,1,1,1 ]]),'hi')
"""
while(1):
    age = int(input('Enter your age :'))
    t_class = int(input('What kind of class you wish to go(1/2/3):')) 
    if t_class != 1 and t_class !=2 and t_class !=3 :
        print('choose the correct option(1/2/3).')
        continue
    gen = input('Enter your Gender(M/F):')
    if gen == 'M' or gen == 'm':
        gen = 1
    elif gen == 'F' or gen == 'f':
        gen = 0
    else:
        print('choose the correct option(M/F).')
        continue
    
    familysize = input('Single or Family(S/F):')
    if familysize == 'S' or familysize == 's':
        familysize = 1
        break
    elif familysize == 'F' or familysize == 'f':
        size = int(input('Enter your no.of family members:'))
        familysize = size
        break
    else:
        print('choose the correct option(S/F).') 
"""

#test = np.array([[t_class,age,0,gender]])
#predict = lr1.predict(test)
#print('Your chances of surviving is :',int(predict*100),'%')

accuracy=round(lr1.score(x_train, y_train) * 100, 2)
#print(accuracy)

#from sklearn.metrics import confusion_matrix
#confusion_matrix(y_test,predict)
#pd.DataFrame(confusion_matrix(y_test,predict),columns=['Predicted no','predicted yes'],index=['Actual no','Actual yes'])
