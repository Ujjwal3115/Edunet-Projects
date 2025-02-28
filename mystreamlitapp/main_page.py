import streamlit as st
import sqlite3
import pandas as pd


# st.image("./Ujjwal.png",width=200),
# st.markdown('''
# <style>
# body {
# background-image: url("./bg.png");
# z-index=3;
# background-size: cover;
# }
# </style>
# ''', unsafe_allow_html=True)

def connect_db():
    return sqlite3.connect("mydb1.db")

def create_table(conn):
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS student(name TEXT, password TEXT, roll INTEGER PRIMARY KEY, branch TEXT, admission_year INTEGER, per_10 INTEGER, per_12 INTEGER)')
    conn.commit()

def add_record(conn):
    cur = conn.cursor()
    name = st.text_input("Enter your name")
    password = st.text_input("Enter your password", type='password')
    roll = st.number_input("Enter your roll", min_value=1)
    branch = st.selectbox("Select your branch", ["CSE", "ECE", "AIML", "IOT", "IT", "MECHANICAL", "ROBOTICS"])
    admission_year = st.number_input("Enter Admission Year", min_value=2000, max_value=2100)
    per_10 = st.number_input("Enter Class 10 Percentage", min_value=0, max_value=100)
    per_12 = st.number_input("Enter Class 12 Percentage", min_value=0, max_value=100)
    submit_button = st.button("Add Record")
    if submit_button:
        try:
            cur.execute("INSERT INTO student(name, password, roll, branch, admission_year, per_10, per_12) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, password, roll, branch, admission_year, per_10, per_12))
            conn.commit()
            st.success("Record Added Successfully")
        except Exception as e:
            st.error(f"Error adding record: {e}")

def view_records(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["Name", "Password", "Roll", "Branch", "Admission Year", "Class 10 Percentage", "Class 12 Percentage"])
    st.table(df)

def delete_record(conn):
    roll = st.number_input("Enter Roll Number to Delete", min_value=1)
    if st.button("Delete Record"):
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE roll = ?", (roll,))
        conn.commit()
        st.success("Record Deleted Successfully")

def update_record(conn):
    roll = st.number_input("Enter Roll Number to Update", min_value=1)
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
    existing_record = cur.fetchone()
    if existing_record:
        name = st.text_input("Enter new name", value=existing_record[0])
        password = st.text_input("Enter new password", type='password', value=existing_record[1])
        branch = st.selectbox("Select new branch", ["CSE", "ECE", "AIML", "IOT", "IT", "MECHANICAL", "ROBOTICS"], index=["CSE", "ECE", "AIML", "IOT", "IT", "MECHANICAL", "ROBOTICS"].index(existing_record[3]))
        admission_year = st.number_input("Enter new Admission Year", value=existing_record[4], min_value=2000, max_value=2100)
        per_10 = st.number_input("Enter new Class 10 Percentage", value=existing_record[5], min_value=0, max_value=100)
        per_12 = st.number_input("Enter new Class 12 Percentage", value=existing_record[6], min_value=0, max_value=100)
        if st.button("Update Record"):
            cur.execute("UPDATE student SET name = ?, password = ?, branch = ?, admission_year = ?, per_10 = ?, per_12 = ? WHERE roll = ?", (name, password, branch, admission_year, per_10, per_12, roll))
            conn.commit()
            st.success("Record Updated Successfully")
    else:
        st.error("No record found with that roll number.")

def signin(conn):
    cur = conn.cursor()
    st.title("Signin Page")

    with st.form(key='signin_form'):
        roll = st.number_input("Enter Roll Number", min_value=1)
        password = st.text_input("Enter Password", type='password')
        submit_button = st.form_submit_button("Sign In")

        if submit_button:
            try:
                cur.execute("SELECT * FROM student WHERE roll = ? AND password = ?", (roll, password))
                existing_record = cur.fetchone()
                if existing_record:
                    st.success("Sign In Successful!")
                    st.write(existing_record)
                else:
                    st.error("Invalid Roll Number or Password")
            except Exception as e:
                st.error(f"Error during sign in: {e}")

def reset_password(conn):
    cur = conn.cursor()
    roll = st.number_input("Enter Roll Number to Reset Password", min_value=1)
    new_password = st.text_input("Enter New Password", type='password')
    submit_button = st.button("Reset Password")

    if submit_button:
        try:
            cur.execute("UPDATE student SET password = ? WHERE roll = ?", (new_password, roll))
            conn.commit()
            st.success("Password Reset Successfully")
        except Exception as e:
            st.error(f"Error resetting password: {e}")

def filter_records(conn):
    cur = conn.cursor()
    st.subheader("Filter Records")
    
    branch_filter = st.multiselect("Select Branches to Filter", ["CSE", "ECE", "AIML", "IOT", "IT", "MECHANICAL", "ROBOTICS"])
    admission_year = st.number_input("Filter by Admission Year", min_value=2000, max_value=2100, value=2000)
    per_10_min = st.number_input("Minimum Class 10 Percentage", min_value=0, max_value=100, value=0)
    per_10_max = st.number_input("Maximum Class 10 Percentage", min_value=0, max_value=100, value=100)
    per_12_min = st.number_input("Minimum Class 12 Percentage", min_value=0, max_value=100, value=0)
    per_12_max = st.number_input("Maximum Class 12 Percentage", min_value=0, max_value=100, value=100)

    if st.button("Apply Filters"):
        query = "SELECT * FROM student WHERE 1=1"
        params = []
        
        if branch_filter:
            query += " AND branch IN ({})".format(','.join('?' * len(branch_filter)))
            params.extend(branch_filter)
        
        query += " AND admission_year = ?"
        params.append(admission_year)
        
        query += " AND per_10 BETWEEN ? AND ?"
        params.extend([per_10_min, per_10_max])
        
        query += " AND per_12 BETWEEN ? AND ?"
        params.extend([per_12_min, per_12_max])
        
        cur.execute(query, params)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["Name", "Password", "Roll", "Branch", "Admission Year", "Class 10 Percentage", "Class 12 Percentage"])
        st.table(df)

conn = connect_db()
create_table(conn)

st.sidebar.title("Menu")
option = st.sidebar.selectbox("Choose an option", ["Sign Up", "Sign In", "View Records", "Update Record", "Delete Record", "Reset Password", "Filter Records"])

if option == "Sign Up":
    add_record(conn)
elif option == "Sign In":
    signin(conn)
elif option == "View Records":
    view_records(conn)
elif option == "Update Record":
    update_record(conn)
elif option == "Delete Record":
    delete_record(conn)
elif option == "Reset Password":
    reset_password(conn)
elif option == "Filter Records":
    filter_records(conn)

conn.close()
