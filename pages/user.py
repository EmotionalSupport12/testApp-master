import menu
import streamlit as st

from Core import header

#Page configurations
st.set_page_config(page_title="Agile Emotion App!", page_icon="😉", layout="wide", initial_sidebar_state="expanded")

menu.redirect_to_Login()
#Run Page header function
header.run_page_header()

if "_LOGGED_USER_NAME" not in st.session_state:
  st.session_state._LOGGED_USER_NAME = None
#-----------------------Load User Data-----------------------
if "_USER_LOGINS_DATASET" in st.session_state and "_LOGGED_USER_NAME" in st.session_state:
  #Search for the user in the dataset
  _USER_RECORD = st.session_state._USER_LOGINS_DATASET[(st.session_state._USER_LOGINS_DATASET["user_name"] == st.session_state._LOGGED_USER_NAME) & 
    (st.session_state._USER_LOGINS_DATASET["is_acive"] == True)]

  #Check if user exists
  if not _USER_RECORD.empty:
    st.markdown(f"""### Hi, {str(_USER_RECORD["user_full_name"].values[0]).split()[0]}!""")
    st.text_input("User ID: ", str(_USER_RECORD["user_id"].values[0]), disabled=False)
    st.text_input("Username: ", str(_USER_RECORD["user_name"].values[0]), disabled=True)
    st.text_input("Full Name: ", str(_USER_RECORD["user_full_name"].values[0]), disabled=False)
    st.text_input("Email: ", str(_USER_RECORD["user_active_email"].values[0]), disabled=False)
    st.text_input("Your Supervisor: ", str(_USER_RECORD["supervisor"].values[0]), disabled=True)
    st.text_input("Your Scrum Master: ", str(_USER_RECORD["user_scrum_master"].values[0]), disabled=True)
  else:
    st.error("Something went wrong! User details cannot fetch at this time.")
else:
  st.error("Something went wrong! User details cannot fetch at this time.")
#-----------------------Load User Data-----------------------

