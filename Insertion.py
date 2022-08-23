import mysql.connector as mysql
from Crypto.Cipher import AES
import base64,random,string,os,base64,datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


#SQL connection to use the required database
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "pydbtest"
)

#Cursor initialized to use the current connection
cursor = db.cursor()

#VALUE FOR AUTO INCREMENT SEQUENCING IN TABLE
seqgen = 0

#Function used to generate the KEK for the User's password. This will generate the same key everytime the same password is provided
def Key_enc_key(passw):
    password = passw.encode() #Encoding to utf-8/bytes format

    #a salt is random data that is used as an additional input to a one-way function that hashes data, a password or passphrase
    # A salt is added to the hashing process to force their uniqueness, increase their complexity without increasing user requirements, and to mitigate password attacks like hash tables

    salt = b"\xb9\x1f|}'S\xa1\x96\xeb\x154\x04\x88\xf3\xdf\x05" #This is just randomly generated and in bytes format
    
    #PBKDF2 is Password based key derivation function 2
    #We are basically creating a HASH of the user password to use as the KEK, the final length is 32 bytes
    #kdf is a hash object, we will use it to derive the hash of the desired password
    kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=24,
                salt=salt,
                iterations=100000,
                backend=default_backend())
   
    key = base64.urlsafe_b64encode(kdf.derive(password)) #Encode to base64-binary format
    return key

#Msg_pad Used to pad a message to the nearest multiple of 16 i.e. the AES block size
def msg_pad(msg):
    while len(msg)%16 !=0:
        msg = msg +' '
    return msg


#Used to convert a string to bytes if it is not of that form
def to_bytes(s):
    if type(s) is bytes:
        return s
    elif type(s) is str or (sys.version_info[0] < 3 and type(s) is unicode):
        return s.encode('utf-8')
    else:
        raise TypeError("Expected bytes or string, but got %s." % type(s))       
    

def AES_ENCRYPT(data,key):
    iv = os.urandom(16) #Generates an initialization vector in Bytes array format, needed for AES
    cipher = AES.new(key,AES.MODE_CBC,iv) 
    msg = msg_pad(data) #MSG PADDING TO A MULTIPLE OF 16
    msg = to_bytes(msg) #CONVERTS MSG STRING TO BYTES ARRAY FORMAT
    enc = cipher.encrypt(msg) # MESSAGE ENCRYPTION
    return iv+enc  #Returns a combination of iv and encrypted msg, iv is needed for decryption
    
def AES_DECRYPT(encd,key):
    iv = encd[:16] #SEPERATING INIT. VECTOR FROM THE CIPHER TXT
    newencd = encd[16:] #CUTTING OUT THE SEPERATED CIPHER TXT
    cipher = AES.new(key, AES.MODE_CBC, iv) 
    decd = cipher.decrypt(newencd) #DECODING OF CIPHER TXT
    return decd

def Insert_Customer_Entry():
    dump = input("PRESS ENTER TO CONTINUE!")
    name = input("Insert Customer Name\n")
    Phone = input("Insert Customer Phone Number\n")
    Email = input("Insert Customer Email\n")
    Date_Of_Birth = input("Insert Customer DOB\n")
    Pass = input("Insert USER PASSWORD\n") #PASSWORD WOULD ONLY BE SAVED BY THE CUSTOMER
    Conf_Pass = input("Confirm USer Password\n")


    #PASSWORD CONFIRMATION
    if Pass != Conf_Pass:
        print("Password Does Not Match!")
        while Pass != Conf_Pass:
            Pass = input("Insert USER PASSWORD\n")
            Conf_Pass = input("Confirm USer Password\n")

    # File Encryption Key, used to Encrypt the Database objects
    key = ''.join(random.choices(string.ascii_letters+string.digits,k=32))

    #Generating Key Encryption Key KEK, it is used to encrypt the File encryption key
    kekkey = Key_enc_key(Pass)
    
    #Encrypted version of FEK is generated here, this one is stored in the database in the CUSTOMER table
    encFEK= AES_ENCRYPT(key,kekkey)

    #QUERY, using MYSQL AES_ENCRYPT FUNCTION TO ENCRYPT THE DATA USING THE FEK
    query  = "INSERT INTO CUSTOMER VALUES(%s,aes_encrypt(%s,%s),aes_encrypt(%s,%s),aes_encrypt(%s,%s),%s,%s)"
    
    #VALUE DEF.
    values = (seqgen,name,key,Phone,key,Email,key,Date_Of_Birth,encFEK)
    
    #CURSOR EXECUTION
    cursor.execute(query,values)

    db.commit()

    ''' ADDING VALUES TO ACCOUNT TABLE'''

    Acc_Type = str(input("ENTER ACCOUNT TYPE(SAV/CRE/DEB) :  "))
    Balance = input("ENTER INITIAL BALANCE: ")
    
    #CURRENT TIME IS ADDED USING THE DATETIME MODULE
    current_time = datetime.datetime.now() 
    #ACCOUNT NAME IS GENERATED USING FIRST 3 LETTERS OF THE NAME, THE ACCOUNT TYPE AND THE CURRENT YEAR, SIMILIAR TO VIT ROLL NO 
    Acc_Name = name[:3]+Acc_Type+str(current_time.year)
    print("\nYour Account Name is: "+ Acc_Name)
    
    #Date of Joining, for current Date in MYSQL Date Format
    DOJ = str(current_time.day) +"-"+str(current_time.month)+"-" +str(current_time.year)[2:]
    cursor.execute("SELECT CUSTOMER_ID FROM CUSTOMER ORDER BY CUSTOMER_ID DESC LIMIT 1")

    #Fetches the latest customer ID from the table, this is the same one as in the previous part
    Cust_ID = cursor.fetchone()
    Cust_ID = Cust_ID[0]
    print("Your Customer ID is: "+str(Cust_ID))

    query1 = "INSERT INTO ACCOUNT VALUES(%s,aes_encrypt(%s,%s),%s,aes_encrypt(%s,%s),%s,aes_encrypt(%s,%s))"
    values1 = (seqgen,Acc_Name,key,DOJ,Acc_Type,key,Cust_ID,Balance,key)

    cursor.execute(query1,values1)
    db.commit()

    #Time based OTP key is randomly generated in string format
    totp_key = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
    print("Your 2FA Key iS: " + totp_key)

    cursor.execute("SELECT CUSTOMER_ID FROM CUSTOMER ORDER BY CUSTOMER_ID DESC LIMIT 1")
    Cust_ID = cursor.fetchone()
    Cust_ID = Cust_ID[0]
    
    # TOTP Key is given to the user and then stored in an encrypted form in the database's AUTH Table
    query2 = "INSERT INTO AUTH VALUES(%s,aes_encrypt(%s,%s))"
    values2 = (Cust_ID,totp_key,key)
    
    cursor.execute(query2,values2)
    db.commit()


    

