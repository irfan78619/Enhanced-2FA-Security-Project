import pyotp,base64,os

os.system('cls' if os.name == 'nt' else 'clear')

TOTP_KEY = input("ENTER YOUR 2FA PASSWORD: ")
#TOTP IS GENERATED FROM THE TOTP-KEY ENTERED BY THE USER
totp = pyotp.TOTP(base64.b32encode(bytearray(TOTP_KEY,'ascii')).decode('utf-8'))

#THE TOTP IS PRINTED WHENEVER IT CHANGES WHICH IS EVERY 30 SECONDS
print(totp.now())
k = totp.now()
i = 0
while(i<10):
    k = totp.now()
    if k != totp.now():
        print(totp.now())
        k = totp.now()
