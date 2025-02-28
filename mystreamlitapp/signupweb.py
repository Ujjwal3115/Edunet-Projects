import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector

try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ujjwal*3115",
        database="dcebatch4"
    )
    cur = con.cursor()

    st.title("Signup Page")

    with st.form(key='signup_form'):
        roll = st.number_input("Enter Roll Number", min_value=1)
        name = st.text_input("Enter Name")
        password = st.text_input("Enter Password", type='password')
        branch = st.text_input("Enter Branch")
        admission_year = st.number_input("Enter Year of Admission", min_value=2000, max_value=2100)
        tenth_percentage = st.number_input("Enter Class 10 Percentage", min_value=0.0, max_value=100.0)
        twelth_percentage = st.number_input("Enter Class 12 Percentage", min_value=0.0, max_value=100.0)
        
        submit_button = st.form_submit_button("Sign Up")

        if submit_button:
            cur.execute("SELECT * FROM student_record WHERE roll = %s;", (roll,))
            existing_record = cur.fetchone()
            if existing_record:
                st.error("A user with this Roll Number already exists. Use a different Roll Number.")
            else:
                cur.execute("INSERT INTO student_record VALUES (%s, %s, %s, %s, %s, %s, %s);",
                            (roll, name, password, branch, admission_year, tenth_percentage, twelth_percentage))
                con.commit()
                st.success("Sign Up Successful!")

except Exception as e:
    st.error(f"An error occurred: {e}")
