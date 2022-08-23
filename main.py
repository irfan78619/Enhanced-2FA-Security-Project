'''References https://www.w3schools.com/python/python_mysql_getstarted.asp'''


#Start mysql server before running the program

#main.py is just used for database setup

import mysql.connector as mysql

#Initial SQL Server Connection
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
)

#Cursor Initialization
cursor = db.cursor()
#DAtabase creation if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS pydbtest")

#IMPORT INSERTION FUNCTIONS
'''from Insertion import Insert_Customer_Entry'''

#IMPORT DB FILLOUT FUNCTIONS
from Fillout import Account_type_Setup

#Second SQL connection to use the required database
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "pydbtest"
)

#Cursor initialized to use the current connection
cursor = db.cursor()

#DESCRIBE THE CUSTOMER TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS CUSTOMER(CUSTOMER_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,CUSTOMER_NAME VARCHAR(200) NOT NULL,PHONE_NUMBER CHAR(100),EMAIL VARCHAR(300),DATE_OF_BIRTH DATE,USER_PASSWORD MEDIUMBLOB NOT NULL ) engine = innodb default charset = latin1")

#CREATE THE ACCOUNT TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ACCOUNT(ACCOUNT_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,ACCOUNT_NAME VARCHAR(300) NOT NULL,DATE_OF_JOINING DATE,ACCOUNT_TYPE VARCHAR(100),CUSTOMER_ID INT NOT NULL,BALANCE VARCHAR(150) NOT NULL, FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID) ON DELETE NO ACTION) engine = innodb default charset = latin1")

#CREATE THE ACCOUNT_TYPE TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ACCOUNT_TYPE(ACCOUNT_TYPE CHAR(3), DESCRIPTION VARCHAR(100)) engine = innodb default charset = latin1")

#CREATE TABLE AUTH
cursor.execute("CREATE TABLE IF NOT EXISTS AUTH(CUSTOMER_ID INT NOT NULL,TOTP_KEY MEDIUMBLOB NOT NULL,FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID)) engine = innodb default charset = latin1")

#ACCOUNT_TYPE TABLE INITIALIZATION
Account_type_Setup()
db.commit()