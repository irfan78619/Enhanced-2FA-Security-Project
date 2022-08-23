import mysql.connector as mysql
from pyotp import totp
from Insertion import AES_ENCRYPT,AES_DECRYPT, Key_enc_key
import os, pyotp,base64

#SQL connection to use the required database
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "pydbtest"
)

#Cursor initialized to use the current connection
cursor = db.cursor()

#Authentication Function
def Authentication():
    Account_Name = input("ENTER ACCOUNT NAME: ")
    Cust_ID = str(input("ENTER CUSTOMER ID: "))
    Pass = input("ENTER PASSWORD: ")

    query = "SELECT USER_PASSWORD FROM CUSTOMER WHERE CUSTOMER_ID= " + Cust_ID
    cursor.execute(query)

    #The encrypted File Encryption key is grabbed from the database for the customer
    encFEK = cursor.fetchone()
    encFEK = encFEK[0]
    
    #Key encryption key is generated  for the password the user enters
    KEK = Key_enc_key(Pass)
    
    #The FEK is decrypted and then converted to string format from it's UTF-8 encoding
    FEK = AES_DECRYPT(encFEK,KEK)
    FEK = FEK.decode('utf-8')
    #print(FEK)

    query = "SELECT CAST(AES_DECRYPT(ACCOUNT_NAME," +"'" + FEK + "'"+ ") AS CHAR) FROM ACCOUNT WHERE CUSTOMER_ID = " + Cust_ID
    cursor.execute(query)
    Acc_Name_Auth = cursor.fetchone()
    Acc_Name_Auth = Acc_Name_Auth[0]
    
    #Checks if the account name provided by the user is the same as the account name in the database
    #This will not proceed with a wrong password since the decryption would be wrong for the FEK
    if(Acc_Name_Auth!= Account_Name):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("WRONG ACCOUNT!")
        quit()

    '''OTP System Implementation'''

    #SELECTS THE TOTP KEY STORED IN THE DATABASE
    query = "SELECT CAST(AES_DECRYPT(TOTP_KEY," + "'" + FEK + "'" +") AS CHAR) FROM AUTH WHERE CUSTOMER_ID = " + Cust_ID
    cursor.execute(query)
    TOTP_KEY = cursor.fetchone()
    TOTP_KEY = TOTP_KEY[0]
    
    #DETERMINES THE CURRENT TIME BASED OTP USING THE USERS TOTP-KEY
    totp = pyotp.TOTP(base64.b32encode(bytearray(TOTP_KEY,'ascii')).decode('utf-8'))
    
    TOTP_VERIFY = input("ENTER THE KEY FROM YOUR AUTHENTICATOR APP :")
    
    # NOW THE USER HAS TO ENTER HIS TOTP-KEY IN THE AUTHENTICATION APP AND GET THE CURRENT TOTP WHICH IS THEN VERIFIED
    if totp.verify(TOTP_VERIFY) !=True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("WRONG AUTHENTICATION KEY!")
        quit()
    
    print("AUTHENTICATION SUCCESS!")
    return (True,FEK,Cust_ID)

#Authentication()

def Balance_update(chan,mode):
    (AuthStatus,FEK,Cust_ID) = Authentication()

    if AuthStatus!= True:
        print("AUTHENTICATION FAILURE")
        quit()

    query = "SELECT CAST(AES_DECRYPT(BALANCE,"+ "'" + FEK + "'" +")AS CHAR) FROM ACCOUNT WHERE CUSTOMER_ID = " + Cust_ID
    cursor.execute(query)
    BALANCE = cursor.fetchone()
    BALANCE = BALANCE[0]
    print("INITIAL BALANACE: "+BALANCE)
    BALANCE = int(BALANCE)

    if mode == 'W':
        if BALANCE>chan:  
            BALANCE = BALANCE - chan
            print("DEDUCTED AMOUNT: "+str(chan))
        else:
            print("INSUFFICIENT BALANCE!")
            return
    elif mode == "D":
        BALANCE = BALANCE + chan
        print("ADDED AMOUNT: "+str(chan))
    
    
    print("UPDATED BALANCE IS: "+ str(BALANCE))

    query1 = "UPDATE ACCOUNT SET BALANCE = aes_encrypt(%s,%s) WHERE CUSTOMER_ID = " +Cust_ID
    values1 = (str(BALANCE),FEK)

    cursor.execute(query1,values1)
    db.commit()


def BalanceCheck():
    (AuthStatus,FEK,Cust_ID) = Authentication()

    if AuthStatus!= True:
        print("AUTHENTICATION FAILURE")
        quit()
    
    query = "SELECT CAST(AES_DECRYPT(BALANCE,"+ "'" + FEK + "'" +")AS CHAR) FROM ACCOUNT WHERE CUSTOMER_ID = " + Cust_ID
    cursor.execute(query)
    BALANCE = cursor.fetchone()
    BALANCE = BALANCE[0]
    print("CURRENT BALANACE: "+BALANCE)
    


    