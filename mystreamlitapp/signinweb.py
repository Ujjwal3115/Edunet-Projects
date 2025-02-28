import streamlit as st
import sqlite3
import pandas as pd

def connect_db():
    return sqlite3.connect("mydb.db")

def create_table(conn):
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS student(name TEXT, password TEXT, roll INTEGER, branch TEXT)')
    conn.commit()

def addrecord(conn):
    cur = conn.cursor()
    name = st.text_input("Enter your name")
    password = st.text_input("Enter your password")
    roll = st.number_input("Enter your roll")
    branch = st.selectbox("Select your branch", ["CSE", "ECE", "AIML", "IOT", "IT", "MECHANICAL", "ROBOTICS"])
    submit_button = st.button("Add Record")
    if submit_button:
        try:
            cur.execute("INSERT INTO student(name, password, roll, branch) VALUES (?, ?, ?, ?)", (name, password, roll, branch))
            conn.commit()
            st.success("Record Added Successfully")
        except Exception as e:
            st.error(f"Error adding record: {e}")

def viewrecord(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    st.table(df)

def deleterec():
    conn = connect_db()
    cur = conn.cursor()


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

# Main execution
conn = connect_db()
create_table(conn)

# Add record or sign in based on user choice
option = st.selectbox("Choose an option", ["Add Record", "Sign In","View Record"])
if option == "Add Record":
    addrecord(conn)
elif option == "Sign In":
    signin(conn)
elif option=="View Record":
    viewrecord(conn)

conn.close()


# make the project too display the signup page 
# make the project too display the signin page
# make the project too display the view record page
# make the project too display the delete record page
#  reset password 
#  search record in the left menu i.e. filter using the chekbox 


