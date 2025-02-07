#creating database.

import mysql.connector
mydb=mysql.connector.connect (host="localhost",user="root", passwd="#ritesh@09")
mycursor=mydb.cursor(buffered = True)
mycursor.execute("create database if not exists library1")
mycursor.execute("use mybank")

if mydb.is_connected():
    print('Connected succesfully with database.')
else:
    print('Not connected with database.')

#creating required tables 
mycursor.execute("create table if not exists bank_master(acno char(4) primary key,name varchar(30),city char(20),mobileno char(10),balance int(6))")
mycursor.execute("create table if not exists banktrans(acno char (4),amount int(6),dot date,ttype char(6),foreign key (acno) references bank_master(acno))")
mycursor.execute("create table if not exists user (user_id varchar(15),password varchar(8))")
mydb.commit()

#functions.

# generating otp.

def otp_func():
    import random
    global otp
    otp=""
    for i in range(8):
        otp += str(random.randint(1,9))
    print ("Your one time password for transaction is : ",otp)
    #return otp

# to create new account.

def account():
    print("All information prompted are mandatory to be filled*")
    print()
    acno=str(input("Enter account number(eg.0000): "))
    name=input("Enter name(limit 35 characters): ")
    city=str(input("Enter city name: "))
    mn=str(input("Enter mobile no.: "))
    balance=0
    mycursor.execute("insert into bank_master values('"+acno+"','"+name+"','"+city+"','"+mn+"','"+str(balance)+"')")
    mydb.commit()
    print()
    print("Account is successfully created!!!")
    print()

#for deposit.

def deposit():
    acno=str(input("Enter account number: "))
    dp=int(input("Enter amount to be deposited: "))
    dot=str(input("Enter date of Transaction: (YYYY-MM-DD) "))
    ttype="Debit"
    mycursor.execute("insert into banktrans values('"+acno+"','"+str(dp)+"','"+dot+"','"+ttype+"')")
    mycursor.execute("update bank_master set balance=balance+'"+str(dp)+"' where acno='"+acno+"'")
    mydb.commit()
    print()
    print("money has been deposited successully!!!")
    print()

#for withdrawl.

def withdrawl():
    acno=str(input("Enter account number: "))
    wd=int(input("Enter amount to be withdrawn: "))
    dot=str(input("enter date of transaction: (YYYY-MM-DD) "))
    print()
    #otp = otp_func()
    otp_func()
    print()
    check = input("Enter otp : ")
    if check == otp:
        ttype="Credit"
        print("""
        Withdrawn successful
            Thank-you
              """)
        mycursor.execute("insert into banktrans values('"+acno+"','"+str(wd)+"','"+dot+"','"+ttype+"')")
        mycursor.execute("update bank_master set balance=balance-'"+str(wd)+"' where acno='"+acno+"'")
        mydb.commit()
    else:
        print()
        print("Transaction failed!!")

#for details of account.

def details_account():
    acno=str(input("Enter account number: "))
    print()
    mycursor.execute("select * from bank_master where acno='"+acno+"'")
    for r in mycursor:
        print("Account number : ",r[0])
        print("Account holder name :",r[1])
        print("City : ",r[2])
        print("Mobile number : ",r[3])
        print("Total amount : ",r[4])
        print()

#for statement.

def statement():
    print("(1) Bank Statement")
    print("(2) Account Statement")
    print()
    op=int(input("Enter your choice: "))
    print()

    #Bank statement

    if op == 1:
        cho1 = input("Enter the starting date : (YYYY-MM-DD) ")
        cho2 = input("Enter the starting date : (YYYY-MM-DD) ")
        mycursor.execute("select * from banktrans Where DATE (dot) BETWEEN '"+cho1+"' AND '"+cho2+"'")
        Credit = 0
        Debit = 0
        print()
        print("All transactions :- ")
        print()
        for i in mycursor:
            if i[3] == "Credit":
                Credit += i[1]
            elif i[3] == "Debit":
                Debit += i[1]
            print(i)
        print()
        print("Total amount Debit to bank : ",Debit)
        print("Total amount Credit from bank : ",Credit)
        print("Total amount left in bank : ",(Debit-Credit))
        print()

    #Account statement.

    elif op == 2:
        acno=str(input("Enter account number:"))
        print()
        mycursor.execute("select * from banktrans where acno='"+acno+"'")
        for i in mycursor:
            print("Total Amount ",i[1],"(Credit/Debit) ",i[3],"(Date) ",i[2])
        mycursor.execute("select * from bank_master where acno='"+acno+"'")
        for r in mycursor:
            print()
            print("Total amount : ",r[4])
        print()

# for close account.

def close_account ():
    print("Please withdraw your money from account before closing account.")
    print()
    acno = input("Enter the acount number : ")
    mycursor.execute("delete from banktrans where acno='"+acno+"'")
    mycursor.execute("delete from bank_master where acno='"+acno+"'")
    print()
    print("Your account is successful closed.")

# main_program.

def main_program():
    while True:
        print("""
        =======================
           WELCOME TO MYBANK    
        =======================
                """)

        print("(1) Create account")
        print("(2) Deposit money")
        print("(3) Withdraw money")
        print("(4) Display account")
        print("(5) Statement")
        print("(6) Close account")
        print("(7) Exit")
        print()
        ch=int(input("Enter your choice: "))
        print()

        if ch == 1:
            account()
        elif ch == 2:
            deposit()
        elif ch == 3:
            withdrawl()
        elif ch == 4:
            details_account()
        elif ch == 5:
            statement()
        elif ch == 6:
            close_account ()
        else:
            break

# for create user id.

def user_id():
    user = input("Enter user id : ")
    password = input("Enter password : ")
    mob = int(input("Enter your mobile number : "))
    otp_func()
    check = input("Enter otp : ")
    if check == otp:
        mycursor.execute("insert into user values('"+str(user)+"','"+str(password)+"')")
        mydb.commit()
        print("user id created sucesfuly!!")
    else:
        print("Incorrect OTP")

# main 2.

def main2():
    print()
    print("(1) User Login")
    print("(2) Create User Login")
    print("(3) Logout")
    print()
    global ch
    ch = int(input("Enter your choice : "))
    print()

# login #Starting interfce.

while True :
    main2()
    if ch == 1 :
        user = input("Enter user id : ")
        pas = input("Enter password : ")
        print()
        mycursor.execute("select * from user where user_id='"+user+"'and'"+pas+"'")
        for i in mycursor :
            if user == i[0] and pas == i[1] :
                otp_func()
                print()
                check = input("Enter otp : ")
                if check == otp :
                    main_program()
                    break
                else:
                    print("Incorrect otp")
            else:
                print("User id or password is invalide")
    elif ch == 2:
        user_id()
    else:
        break
