import streamlit as st
import base64
st.set_page_config(page_title='Home', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)

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


add_bg_from_local('bg4.jpg')
original_title = '<p style="font-family:Georgia; color:white; font-size: 70px; text-align : center; margin-top : 50px;">Easy Interview</p>'
st.markdown(original_title, unsafe_allow_html=True)

original_title = '<p style="font-family:Georgia; color:violet; font-size: 50px; text-align : center;">Platform Which Brings Your Dream Career Near</p>'
st.markdown(original_title, unsafe_allow_html=True)

original_title = '<p style="font-family:Georgia; color:yellow; font-size: 30px; text-align : center;">GET SET GO GRAB IT</p>'
st.markdown(original_title, unsafe_allow_html=True)