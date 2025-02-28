import sqlite3

def connect_db():
    con = sqlite3.connect("mydb1.db")
    return con

def user():
    b = 0
    print("*" * 20 + " User Interface " + "*" * 20)
    while (b != 3):
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        b = int(input("Enter your choice: "))
        if b == 1:
            print("*" * 20 + " Sign Up " + "*" * 20)
            roll = int(input("Enter roll: "))
            cur = connect_db().cursor()
            cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
            existing_record = cur.fetchone()
            if existing_record:
                print("A user with this Roll Number already Exists. Use any other Roll Number.")
            else:
                name = input("Enter name: ")
                pswrd = input("Enter password: ")
                branch = input("Enter the branch: ")
                admission = int(input("Enter the year of admission: "))
                tenth = int(input("Enter the class 10 percentage: "))
                twelth = int(input("Enter the class 12 percentage: "))
                cur.execute("INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?);", (roll, name, pswrd, branch, admission, tenth, twelth))
                connect_db().commit()
                print("Sign Up Successful")

        elif b == 2:
            print("*" * 20 + " Login " + "*" * 20)
            roll = int(input("Enter roll: "))
            pswrd = input("Enter the Password: ")
            cur = connect_db().cursor()
            cur.execute("SELECT * FROM student WHERE roll = ? AND password = ?", (roll, pswrd))
            existing_record = cur.fetchone()
            if existing_record:
                print("Login Successful")
            else:
                print("Invalid Roll Number or Password")

        elif b == 3:
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def developer():
    print("*" * 20 + " Developer Menu " + "*" * 20)
    c = 0
    while (c != 7):
        print("1. View all records")
        print("2. Delete a record")
        print("3. Update a record")
        print("4. Add a new record")
        print("5. View a record")
        print("6. Filter Record")
        print("7. Exit")
        c = int(input("Enter your choice: "))
        cur = connect_db().cursor()
        if c == 1:
            cur.execute("SELECT * FROM student;")
            records = cur.fetchall()
            for record in records:
                print(record)
        elif c == 2:
            roll = int(input("Enter the roll number of the user you want to delete: "))
            cur.execute("DELETE FROM student WHERE roll = ?", (roll,))
            connect_db().commit()
            print("Record deleted successfully")
        elif c == 3:
            roll = int(input("Enter the roll number of the user you want to update: "))
            cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
            existing_record = cur.fetchone()
            if existing_record:
                d = 0
                print("***** Update Menu *****")
                while (d != 8):
                    print("1. Update Name")
                    print("2. Update branch")
                    print("3. Update Roll")
                    print("4. Update Password")
                    print("5. Update Admission Year")
                    print("6. Update Class 10 percentage")
                    print("7. Update Class 12 percentage")
                    print("8. Exit")
                    d = int(input("Enter What you want to update: "))
                    if d == 1:
                        name = input("Enter the new name: ")
                        cur.execute("UPDATE student SET name = ? WHERE roll = ?", (name, roll))
                    if d == 2:
                        branch = input("Enter the new branch: ")
                        cur.execute("UPDATE student SET branch = ? WHERE roll = ?", (branch, roll))
                    if d == 3:
                        new_roll = int(input("Enter the new roll number: "))
                        cur.execute("UPDATE student SET roll = ? WHERE roll = ?", (new_roll, roll))
                    if d == 4:
                        password = input("Enter the new password: ")
                        cur.execute("UPDATE student SET password = ? WHERE roll = ?", (password, roll))
                    if d == 5:
                        year = int(input("Enter the new admission year: "))
                        cur.execute("UPDATE student SET admission_year = ? WHERE roll = ?", (year, roll))
                    if d == 6:
                        percentage = int(input("Enter the new class 10 percentage:__ %: "))
                        cur.execute("UPDATE student SET per_10 = ? WHERE roll = ?", (percentage, roll))
                    if d == 7:
                        percentage = int(input("Enter the new class 12 percentage:__ %: "))
                        cur.execute("UPDATE student SET per_12 = ? WHERE roll = ?", (percentage, roll))
                    if d == 8:
                        print("Returning to Developer Menu")
                        break
                    else:
                        print("Invalid choice")
            else:
                print("No User with Such Roll Number Found. Try using Another Roll Number.")

        elif c == 4:
            roll = int(input("Enter roll of the user to be added: "))
            cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
            existing_record = cur.fetchone()
            if existing_record:
                print("A user with this Roll Number already Exists. Use any other Roll Number.")
            else:
                name = input("Enter name: ")
                pswrd = input("Enter password: ")
                branch = input("Enter the branch: ")
                admission = int(input("Enter the year of admission: "))
                tenth = int(input("Enter the class 10 percentage: "))
                twelth = int(input("Enter the class 12 percentage: "))
                cur.execute("INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?);", (roll, name, pswrd, branch, admission, tenth, twelth))
                connect_db().commit()
                print("Successfully Added")
        elif c == 5:
            roll = int(input("Enter roll of the user whose details you want to see:"))
            cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
        elif c == 6:
            print("***** Filter Record Menu *****")
            print("Syntax ::")
            print("SELECT column_name from Table_name where conditions ;")
            st = input("Enter the Statement Here: ")
            cur.execute(st)
        elif c == 7:
            break
        else:
            print("Invalid choice")

print("*" * 20 + " Welcome to my app " + "*" * 20)
a = 0
while (a != 3):
    print("*" * 20 + " Main Menu " + "*" * 20)
    print("1. User Mode")
    print("2. Developer Mode")
    print("3. Exit")
    a = int(input("Enter your choice: "))
    if a == 1:
        user()
    if a == 2:
        developer()
