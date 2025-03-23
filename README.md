# MyBank Management System

## Overview
This is a simple bank management system implemented using Python and MySQL. The system allows users to create accounts, deposit and withdraw money, view account details, generate statements, and close accounts. Additionally, it features a user authentication system with OTP verification.

## Features
- User authentication with OTP verification
- Create a new bank account
- Deposit and withdraw money
- View account details
- Generate bank and account statements
- Close an account

## Prerequisites
Ensure you have the following installed on your system:
- Python (version 3.x recommended)
- MySQL Server
- MySQL Connector for Python (`pip install mysql-connector-python`)

## Database Setup
1. Install MySQL and create a database.
2. Run the script to create required tables (`bank_master`, `banktrans`, `user`).

### Creating the Database
```python
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="#")
mycursor = mydb.cursor(buffered=True)
mycursor.execute("CREATE DATABASE IF NOT EXISTS library1")
mycursor.execute("USE mybank")

if mydb.is_connected():
    print('Connected successfully with database.')
else:
    print('Not connected with database.')
```

### Creating Required Tables
```python
mycursor.execute("""
CREATE TABLE IF NOT EXISTS bank_master (
    acno CHAR(4) PRIMARY KEY,
    name VARCHAR(30),
    city CHAR(20),
    mobileno CHAR(10),
    balance INT(6)
)""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS banktrans (
    acno CHAR(4),
    amount INT(6),
    dot DATE,
    ttype CHAR(6),
    FOREIGN KEY (acno) REFERENCES bank_master(acno)
)""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    user_id VARCHAR(15),
    password VARCHAR(8)
)""")
mydb.commit()
```

## Functions
### OTP Generation
```python
def otp_func():
    import random
    global otp
    otp = ""
    for i in range(8):
        otp += str(random.randint(1, 9))
    print("Your one-time password for transaction is: ", otp)
```

### Account Creation
```python
def account():
    acno = input("Enter account number (e.g., 0000): ")
    name = input("Enter name (limit 35 characters): ")
    city = input("Enter city name: ")
    mn = input("Enter mobile no.: ")
    balance = 0
    mycursor.execute(f"INSERT INTO bank_master VALUES ('{acno}', '{name}', '{city}', '{mn}', '{balance}')")
    mydb.commit()
    print("Account successfully created!")
```

### Deposit Money
```python
def deposit():
    acno = input("Enter account number: ")
    dp = int(input("Enter amount to be deposited: "))
    dot = input("Enter date of Transaction (YYYY-MM-DD): ")
    mycursor.execute(f"INSERT INTO banktrans VALUES ('{acno}', '{dp}', '{dot}', 'Debit')")
    mycursor.execute(f"UPDATE bank_master SET balance = balance + {dp} WHERE acno = '{acno}'")
    mydb.commit()
    print("Money has been deposited successfully!")
```

### Withdraw Money
```python
def withdrawl():
    acno = input("Enter account number: ")
    wd = int(input("Enter amount to be withdrawn: "))
    dot = input("Enter date of transaction (YYYY-MM-DD): ")
    otp_func()
    check = input("Enter OTP: ")
    if check == otp:
        mycursor.execute(f"INSERT INTO banktrans VALUES ('{acno}', '{wd}', '{dot}', 'Credit')")
        mycursor.execute(f"UPDATE bank_master SET balance = balance - {wd} WHERE acno = '{acno}'")
        mydb.commit()
        print("Withdraw successful! Thank you.")
    else:
        print("Transaction failed!!")
```

### Account Details
```python
def details_account():
    acno = input("Enter account number: ")
    mycursor.execute(f"SELECT * FROM bank_master WHERE acno = '{acno}'")
    for r in mycursor:
        print(f"Account Number: {r[0]}\nName: {r[1]}\nCity: {r[2]}\nMobile: {r[3]}\nBalance: {r[4]}")
```

### Closing an Account
```python
def close_account():
    acno = input("Enter account number: ")
    mycursor.execute(f"DELETE FROM banktrans WHERE acno = '{acno}'")
    mycursor.execute(f"DELETE FROM bank_master WHERE acno = '{acno}'")
    mydb.commit()
    print("Your account has been successfully closed.")
```

## Running the Program
### User Authentication
```python
def user_id():
    user = input("Enter user ID: ")
    password = input("Enter password: ")
    otp_func()
    check = input("Enter OTP: ")
    if check == otp:
        mycursor.execute(f"INSERT INTO user VALUES ('{user}', '{password}')")
        mydb.commit()
        print("User ID created successfully!")
    else:
        print("Incorrect OTP")
```

### Main Program Loop
```python
def main_program():
    while True:
        print("""
        =======================
           WELCOME TO MYBANK    
        =======================
        """)
        print("(1) Create Account\n(2) Deposit Money\n(3) Withdraw Money\n(4) Display Account\n(5) Statement\n(6) Close Account\n(7) Exit")
        ch = int(input("Enter your choice: "))
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
            close_account()
        else:
            break
```

## Conclusion
This system provides basic banking functionalities. Future improvements can include a GUI interface, enhanced security features, and integration with external APIs for better user experience.

### Author
- **Ritesh Kumar**

### License
This project is open-source under the MIT License.

