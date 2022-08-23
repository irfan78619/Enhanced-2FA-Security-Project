'''References https://www.w3schools.com/python/python_mysql_getstarted.asp and SQL'''

from datetime import datetime
import mysql.connector as mysql

#SQL connection to use the required database
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "pydbtest"
)

#Cursor initialized to use the current connection
cursor = db.cursor()


#JUST CREATES THE ACCOUNT TYPES
def Account_type_Setup():
    query1 = "INSERT INTO ACCOUNT_TYPE(ACCOUNT_TYPE,DESCRIPTION) VALUES(%s,%s)"
    values1 = ("SAV","Savings Account")
    cursor.execute(query1,values1)
    
    query2 = "INSERT INTO ACCOUNT_TYPE(ACCOUNT_TYPE,DESCRIPTION) VALUES(%s,%s)"
    values2 = ("CRE","Credit Account")
    cursor.execute(query2,values2)

    query3 = "INSERT INTO ACCOUNT_TYPE(ACCOUNT_TYPE,DESCRIPTION) VALUES(%s,%s)"
    values3 = ("DEB","Debit Account")
    cursor.execute(query3,values3)
    db.commit()    




