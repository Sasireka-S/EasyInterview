import sqlite3 
import streamlit as st
import base64
import webbrowser
import pandas as pd 
from collections import defaultdict as dd 
st.set_page_config(page_title='Company Sign', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)

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
def recruitments(id):
    original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center;">Job postings</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    sqliteConnection = sqlite3.connect('interview.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT DISTINCT deadline, time, pos, loc FROM hl WHERE org_id = (?)", (id,))
    dicti = dd(list)
    ans = cursor.fetchall()
    for x in ans:
        if x[0]:
            dicti["ID"].append(x[0])
            dicti["Date"].append(x[1])
            dicti["Position"].append(x[2])
            dicti["Location"].append(x[3])
    df = pd.DataFrame(dicti)
    st.table(dicti)
add_bg_from_local('bg.jpg')
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Company Sign In</p>'
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
f = 0
submit = False
txt = st.empty()
with txt.form(key='form3'):
    st.markdown(original_title, unsafe_allow_html=True)
    id = text_field("Organization ID : ")
    password = text_field("Password : ", type = "password")
    v = st.checkbox("Start meeting for Recruitment")
    submit = st.form_submit_button(label="Submit")
if submit:
    txt.empty()
    cursor.execute("SELECT org_id, org_password FROM hl")
    ans = cursor.fetchall()
    for x in ans:
        if(x[0] == id and x[1] == password):
            f = 1
            if v:
                webbrowser.open('videochat2.html')
            recruitments(id)
            break 
    if f == 0:
        st.error("Invalid ID or Password")
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center;">Post new Job (After Sign In)</p>'
st.markdown(original_title, unsafe_allow_html=True)
with st.form(key='form4', clear_on_submit=True):
    job_id = text_field("Enter Job ID : ")
    pos = text_field("Enter Job Position : ")
    des = text_field("Enter Job description : ")
    date = text_field("Enter Interview Date and Time : ")
    loc = text_field("Enter Location : ")
    submit = st.form_submit_button(label="Submit")
if submit:
    try:
        cursor.execute("INSERT INTO hl(org_id, deadline, pos, des, time, loc) VALUES(?,?,?,?,?,?)", (id, job_id, pos, des, date,loc))
    except:
        st.error("Login to Post the Job")
    if not id:
        st.error("Please Log in to Post the Job")
    else:
        st.success("LJob Posted Successfully")
sqliteConnection.commit()
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center;">Give Meeting Link (After Sign In)</p>'
st.markdown(original_title, unsafe_allow_html=True)
with st.form(key='form5', clear_on_submit=True):
    job_id = text_field("Enter the Job ID : ")
    link = text_field("Enter meeting link : ")
    submit = st.form_submit_button(label="Submit")
if submit:
    try:
        cursor.execute("UPDATE hl SET org_meet = (?) WHERE org_id = (?) AND deadline = (?)", (link, id, job_id))
    except:
        st.error("Login to Post the Link")
    if not id:
        st.error("Please Log in to Post the Link")
    else:
        st.success("Link Posted Successfully")
sqliteConnection.commit()
sqliteConnection.close()