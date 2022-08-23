from Insertion import *
import os

os.system('cls' if os.name == 'nt' else 'clear')

print("ADMINSTRATION!\n")
print("OPTIONS: \n")
print("1.CREATE ACCOUNT")

CHOICE = int(input("Enter Choice: "))

if CHOICE==1:
    Insert_Customer_Entry()
else:
    print("WRONG CHOICE!!!")
    quit()