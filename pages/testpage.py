import menu
import streamlit as st

from Core import header

#Page configurations
st.set_page_config(page_title="Agile Emotion App!", page_icon="😉", layout="wide", initial_sidebar_state="expanded")

menu.redirect_to_Login()
#Run Page header function
header.run_page_header()

st.markdown(f"""<div style="text-align: justify;"> test page. 😉😉😉 </div>""", unsafe_allow_html=True)