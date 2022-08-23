from Transaction import *
import os

os.system('cls' if os.name == 'nt' else 'clear')

print("ATM!\n\n")
print("OPTIONS: \n")
print("1. WITHDRAW")
print("2. DEPOSIT")
print("3. BALANCE CHECK\n")

CHOICE = int(input("Enter Choice: "))

if CHOICE==1:
    change = input("ENTER THE AMOUNT TO WITHDRAW: ")
    Balance_update(int(change),"W")
elif CHOICE==2:
    change = input("ENTER AMOUNT TO DEPOSIT: ")
    Balance_update(int(change),"D")
elif CHOICE==3:
    BalanceCheck()
else:
    print("WRONG CHOICE!!!")
    quit()




