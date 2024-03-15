import pandas as pd
import streamlit as st
import mysql.connector
import requests
from streamlit_lottie import st_lottie

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'test_db'
}
def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()


def create_connection():
    """Create a connection to the MySQL database."""
    db = mysql.connector.connect(**config)
    return db


def create_database(db):
    """Create the 'userdb' database if it doesn't exist."""
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
    cursor.close()

def create_user_data_table(db):
    """Create the user table in the database."""
    cursor = db.cursor()

    create_user_data_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    contact_number VARCHAR(255),
    address VARCHAR(255),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(255)
    )
    """

    cursor.execute(create_user_data_table_query)
    db.commit()
    st.write("user table created successfully.")
def modify_user_data_table(db):
    cursor = db.cursor()

    alter_user_data_table_query = """
    ALTER TABLE user_data
    ADD COLUMN race VARCHAR(255),
    ADD COLUMN Nationality VARCHAR(255),
    ADD COLUMN Gender INTEGER(5)
    """

    cursor.execute(alter_user_data_table_query)
    db.commit()
    st.write("User data table modified successfully.")


def insert_user_data_record(db, name, age, contact_number, email, address):
    """Insert a new patient record into the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE test_db")

    insert_user_data_query = """
    INSERT INTO user_data (name, age, contact_number, email, address)
    VALUES (%s, %s, %s, %s, %s)
    """

    user_data = (name, age, contact_number, email, address)

    cursor.execute(insert_user_data_query, user_data)
    db.commit()
    st.write("User record inserted successfully.")

def fetch_all_user_data(db):
    """Fetch all records from the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE test_db")

    # Fetch all patients
    select_user_data_query = "SELECT * FROM user_data"
    cursor.execute(select_user_data_query)
    user_data = cursor.fetchall()

    return user_data

def fetch_user_by_user_attribute(db, user_attribute):
    """Fetch a user's record from the 'user_data' table based on user attribute name."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE test_db")

    # Fetch the user by user attribute
    select_user_data_query = "SELECT * FROM user_data WHERE id = %s"
    cursor.execute(select_user_data_query, (user_attribute,))
    user_data = cursor.fetchone()

    return user_data

def delete_user_record(db, delete_option, delete_value):
    """Delete a user record from the 'user_data' table based on attributes ."""
    global delete_user_data_query
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE user_data")

    # Delete the patient record
    if delete_option == "ID":
        delete_user_data_query = "DELETE FROM patients WHERE id = %s"
    elif delete_option == "Name":
        delete_user_data_query = "DELETE FROM patients WHERE name = %s"
    elif delete_option == "Contact Number":
        delete_user_data_query = "DELETE FROM patients WHERE contact_number = %s"
    cursor.execute(delete_user_data_query, (delete_value,))
    db.commit()
    st.write("Patient record deleted successfully.")
def show_all_user_data(db):
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE user_data")
    select_query = """
    SELECT id, name, age, contact_number, address, email FROM user_data
    """
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        st.subheader("All User Records")
        df = pd.DataFrame(records,
                          columns=['ID', 'Name', 'Age', 'Contact Number', 'Address', 'Email'])
        st.dataframe(df)
    else:
        st.write("No user record found")



def main():
    st.title('User Data Collection')
    lott1 = loti("https://assets6.lottiefiles.com/packages/lf20_olluraqu.json")
    lotieuser = loti("https://assets6.lottiefiles.com/packages/lf20_vPnn3K.json")
    db = create_connection()

    create_database(db)

    config['database'] = 'test_db'  # Update the database name
    db = create_connection()

    create_user_data_table(db)

    menu = ["Home", "Add User Record", "Show user Records", "Search and Edit user", "Delete user Record"]
    options = st.sidebar.radio("Select an Option :dart:", menu)
    if options == "Home":
        st.subheader("Welcome to User Management System")
        st.write("Navigate from sidebar to access database")
        st_lottie(lott1, height=500)
        # st.image('hospital.jpg', width=600)

    elif options == "Add user Record":
        st.subheader("Enter user details :woman_in_motorized_wheelchair:")
        st_lottie(lotieuser, height=200)

        name = st.text_input('Enter your name:')
        age = st.number_input('Enter your age:')
        contact_no = st.number_input('Enter user contact :')
        email = st.text_input('Enter email : ')
        address = st.text_input('Enter user address')
        if st.button('Save'):
            cursor = db.cursor()
            select_query = """
              SELECT * FROM user_data WHERE contact_number=%s
              """
            cursor.execute(select_query, (contact_no,))
            existing_user = cursor.fetchone()
            if existing_user:
                st.warning("A user with the same contact number already exist")
            else:
                insert_user_data_record(db, name, age, contact_no, email, address)
    elif options == "Show user Records":
        user = fetch_all_user_data(db)
        if user:
            st.subheader("All User Records :magic_wand:")
            df = pd.DataFrame(user,
                              columns=['ID', 'Name', 'Age', 'Contact Number', 'Address','Email'])
            st.dataframe(df)
        else:
            st.write("No user found")
        '''elif options == "Search and Edit Patient":
        update_patient_record(db)


    elif options == "Deetel Patients Record":
        st.subheader("Search a patient to delate :skull_and_crossbones:")
        delete_option = st.selectbox("Select delete option", ["ID", "Name", "Contact Number"], key="delete_option")
        delete_value = st.text_input("Enter delete value", key="delete_value")

        if st.button("Delete"):
            delete_patient_record(db, delete_option, delete_value)

    elif options == "Add patients Appointments":
        patient_id = st.number_input("Enter patient ID:", key="appointment_patient_id")
        appointment_date = st.date_input("Enter appointment date:", key="appointment_date")
        appointment_time = st.time_input("Enter appointment time:", key="appointment_time")
        doctor_name = st.text_input("Enter doctor's name:", key="appointment_doctor_name")
        notes = st.text_area("Enter appointment notes:", key="appointment_notes")
    
    '''



main()