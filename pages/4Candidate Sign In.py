import sqlite3 
import streamlit as st
import base64
import webbrowser
import pandas as pd 
from collections import defaultdict as dd 
st.set_page_config(page_title='Candidate Sign', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)

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
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Candidate Sign In</p>'
sqliteConnection = sqlite3.connect('interview.db')
cursor = sqliteConnection.cursor()
f = 0
submit = False
txt = st.empty()
with txt.form(key='form3'):
    st.markdown(original_title, unsafe_allow_html=True)
    email = text_field("Email ID : ")
    password = text_field("Password : ", type = "password")
    submit = st.form_submit_button(label="Submit")
if submit:
    txt.empty()
    cursor.execute("SELECT email, password FROM cand")
    ans = cursor.fetchall()
    for x in ans:
        if(x[0] == email and x[1] == password):
            f = 1
            break 
    if f == 0:
        st.error("Invalid ID or Password")
    else:
        original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Self Introduction</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        cursor.execute("SELECT INTRO FROM cand WHERE email = (?)", (email,))
        ans = cursor.fetchall()
        dicti = dd(str)
        for x in ans:
            if x[0]:
                dicti["Self Intro"] = x[0]
        st.table(dicti)
        original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Skills</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        cursor.execute("SELECT skill1 FROM cand WHERE email = (?)", (email,))
        ans = cursor.fetchall()
        dicti = dd(list)
        for x in ans:
            if x[0]:
                s = x[0].split(",")
                for i in s:
                    dicti["Skills"].append(i)
        st.table(dicti)
        original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Projects</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        cursor.execute("SELECT skill2, skill3, skill4, skill5, skill6 FROM cand WHERE email = (?)", (email,))
        ans = cursor.fetchall()
        dicti = dd(list)
        for x in ans:
            if x[0]:
                dicti["Projects"].append(x[0])
            if x[1]:
                dicti["Projects"].append(x[1])
            if x[2]:
                dicti["Projects"].append(x[2])
            if x[3]:
                dicti["Projects"].append(x[3])
            if x[4]:
                dicti["Projects"].append(x[4])
        st.table(dicti)
original_title = '<p style="font-family:Georgia; font-size: 40px; text-align : center; margin-top : 50px;">Update Profile (After Sign)</p>'
st.markdown(original_title, unsafe_allow_html=True)
with st.form(key="form4", clear_on_submit=True):
    skills = text_field("Skills seperated by Commas : ")
    hobby = text_field("Hobbies seperated by Commas : ")
    achievements = st.text_area("Achievements : ")
    experience = st.text_area("Experience if applicable : ")
    project1 = st.text_area("Details about Project1  if available : ")
    project2 = st.text_area("Details about Project2 if available : ")
    project3= st.text_area("Details about Project3 if available : ")
    project4 = st.text_area("Details about Project4 if available : ")
    project5 = st.text_area("Details about Project5 if available : ")
    submit2 = st.form_submit_button(label="Submit")
if submit2:
    cursor.execute("UPDATE cand SET skill1 = (?) WHERE email = (?)", (skills, email))
    cursor.execute("UPDATE cand SET extra = (?) WHERE email = (?)", (hobby, email))
    cursor.execute("UPDATE cand SET extra2 = (?) WHERE email = (?)", (achievements, email))
    cursor.execute("UPDATE cand SET skill7 = (?) WHERE email = (?)", (experience, email))
    cursor.execute("UPDATE cand SET skill2 = (?) WHERE email = (?)", (project1, email))
    cursor.execute("UPDATE cand SET skill3 = (?) WHERE email = (?)", (project2, email))
    cursor.execute("UPDATE cand SET skill4 = (?) WHERE email = (?)", (project3, email))
    cursor.execute("UPDATE cand SET skill5 = (?) WHERE email = (?)", (project4, email))
    cursor.execute("UPDATE cand SET skill6 = (?) WHERE email = (?)", (project5, email))
    st.success("Profile Updated")
sqliteConnection.commit()
sqliteConnection.close()
#, extra = (?), extra2 = (?), skill7 = (?), skill2 = (?), skill3 = (?), skill4 = (?), skill5 (?), skill6 = (?)
# hobby, achievements, experience, project1, project2, project3, project4, project5,