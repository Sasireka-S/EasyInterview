import sqlite3 
import streamlit as st
import base64
import webbrowser
import pandas as pd 
from collections import defaultdict as dd 
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
def recruitments(comp):
    name, loc = comp.split(",")
    original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center;">Job postings</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    sqliteConnection = sqlite3.connect('interview.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT org_id FROM hl WHERE org_name = (?) AND org_location = (?)", (name, loc))
    dicti = dd(list)
    a = cursor.fetchall()
    for i in a:
        cursor.execute("SELECT DISTINCT deadline, time, pos, loc, org_meet FROM hl WHERE org_id = (?)", (i[0],))
        ans = cursor.fetchall()
        for x in ans:
            if x[0]:
                dicti["ID"].append(x[0])
                dicti["Date"].append(x[1])
                dicti["Position"].append(x[2])
                dicti["Location"].append(x[3])
                dicti["Meeting Link"].append(x[4])
    df = pd.DataFrame(dicti)
    st.table(dicti)
add_bg_from_local('bg.jpg')
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Company Sign In</p>'
sqliteConnection = sqlite3.connect('interview.db')
cursor = sqliteConnection.cursor()
with st.form("form1", clear_on_submit=True):
    cursor.execute("SELECT DISTINCT org_name, org_location FROM hl")
    options = [" "]
    ans = cursor.fetchall()
    for x in ans:
        if x[0] and x[1]:
            options.append(x[0]+","+x[1])
    comp = st.selectbox("Choose the Organization : ", options)
    submit = st.form_submit_button(label="Submit")
if submit and comp != " ":
    recruitments(comp)