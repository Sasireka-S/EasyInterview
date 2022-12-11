import sqlite3 
import streamlit as st
import base64
st.set_page_config(page_title='Company Registration', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)

def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])
    c1.markdown("##")
    c1.markdown(label)
    input_params.setdefault("key", label)
    return c2.text_input("", **input_params)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('bg.jpg')
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Company Registration</p>'
st.markdown(original_title, unsafe_allow_html=True)
sqliteConnection = sqlite3.connect('interview.db')
cursor = sqliteConnection.cursor()
sql_command = """CREATE TABLE IF NOT EXISTS hl (
org_name VARCHAR(50),
org_location VARCHAR(50),
org_id VARCHAR(15),
org_email VARCHAR(30),
org_meet VARCHAR(50),
org_password VARCHAR(50),
time VARCHAR(20),
pos VARCHAR(30),
des VARCHAR(400),
deadline VARCHAR(50),
loc VARCHAR(50));"""
cursor.execute(sql_command)
with st.form("form1", clear_on_submit=True):
    name = text_field("Organization Name : ")
    email = text_field("Organization Mail ID : ")
    loc = text_field("Organization location : ")
    id = text_field("Organization ID : ")
    password = text_field("Password : ", type = "password")
    submit = st.form_submit_button(label="Submit")
if submit:
    cursor.execute("SELECT org_id FROM hl")
    ans = cursor.fetchall()
    f = 0
    for x in ans:
        if x[0] == id:
            st.error("Some other organization with same ID exists please change your ID")
            f = 1
            break 
    cursor.execute("INSERT INTO hl(org_name, org_email, org_location, org_id, org_password) values(?, ?, ?, ?, ?)", (name, email, loc, id, password))
    sqliteConnection.commit()
    sqliteConnection.close()
    if(f == 0):
        st.success("Registration Successful")