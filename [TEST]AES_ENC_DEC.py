import mysql.connector as mysql
from Crypto.Cipher import AES
import base64,random,string,os, base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def msg_pad(msg):
    while len(msg)%16 !=0:
        msg = msg +' '
    return msg

def to_bytes(s):
    if type(s) is bytes:
        return s
    elif type(s) is str or (sys.version_info[0] < 3 and type(s) is unicode):
        return s.encode('utf-8')
    else:
        raise TypeError("Expected bytes or string, but got %s." % type(s))       
    


def Key_enc_key(passw):
    password = passw.encode()

    salt = b"\xb9\x1f|}'S\xa1\x96\xeb\x154\x04\x88\xf3\xdf\x05"

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                length=24,
                salt=salt,
                iterations=100000,
                backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(password))
    #print(key)
    return key

def AES_ENCRYPT(data,key):
    #key = key.encode('utf-8')
    iv = os.urandom(16)
    #iv = iv.encode('utf-8')
    cipher = AES.new(key,AES.MODE_CBC,iv)
    msg = msg_pad(data)
    msg = to_bytes(msg)
    enc = cipher.encrypt(msg)
    return iv+enc

def AES_DECRYPT(encd,key):
    iv = encd[:16]
    newencd = encd[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print(newencd)
    decd = cipher.decrypt(newencd)
    print(decd)
    return decd


#Generating Key Encryption Key KEK
Fkey = ''.join(random.choices(string.ascii_letters+string.digits,k=32))
kekkey = Key_enc_key("QWERTY")
#print("keklen"+str(len(kekkey)))
encd = AES_ENCRYPT("LOSSANTOS",kekkey)
print(encd)

temp = AES_DECRYPT(encd,kekkey)
temp = temp.decode()
print(temp)