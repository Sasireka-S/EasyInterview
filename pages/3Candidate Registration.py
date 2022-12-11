import sqlite3 
import streamlit as st
import base64
st.set_page_config(page_title='Candidate Registration', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)

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
sql_command = """CREATE TABLE IF NOT EXISTS cand (
name VARCHAR(50),
email VARCHAR(50),
password VARCHAR(15),
degree VARCHAR(50),
department VARCHAR(50),
college VARCHAR(80),
disability VARCHAR(20),
skill1 VARCHAR(20),
skill2 VARCHAR(20),
skill3 VARCHAR(20),
skill4 VARCHAR(20),
skill5 VARCHAR(20),
skill6 VARCHAR(20),
skill7 VARCHAR(20),
skill8 VARCHAR(20),
skill9 VARCHAR(20),
skill10 VARCHAR(20),
intro VARCHAR(500),
extra VARCHAR(50),
extra2 VARCHAR(50),
yop VARCHAR(20),
loc VARCHAR(50));"""
cursor.execute(sql_command)
with st.form("form1", clear_on_submit=True):
    name = text_field("Name : ")
    email = text_field("Email : ")
    loc = text_field("Location : ")
    college = text_field("College Name : ")
    deg = text_field("Degree : ")
    dept = text_field("Branch : ")
    yop = text_field("Year of Passing : ")
    options = [" ", "Deaf", "Dumb", "Deaf and Dumb", "None"]
    comp = (st.selectbox('Disability : ',(options)))
    password = text_field("Password : ", type = "password")
    submit = st.form_submit_button(label="Submit")
if submit:
    cursor.execute("INSERT INTO cand(name, email, loc, college, degree, department, yop, disability, password) values(?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, email, loc, college, deg, dept, yop, comp, password))
    sqliteConnection.commit()
    sqliteConnection.close()
    st.success("Registration Successful")