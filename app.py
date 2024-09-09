#--------------------Importing Libraries---------------------

import menu
import pandas as pd
import streamlit as st

from Core import header
from Core import data_connection as DataConn

#--------------------Importing Libraries---------------------

#Page basic configurations
st.set_page_config(page_title="Agile Emotion App!", page_icon="😉", layout="wide", initial_sidebar_state="expanded")

#-------------------Set up Main Variables--------------------

#Initialize the visibility of the login popup.
if "_LOGIN_POPUP_VISIBILITY" not in st.session_state:
  st.session_state._LOGIN_POPUP_VISIBILITY = True

#Load the user login dataset into the session
if "_USER_LOGINS_DATASET" not in st.session_state:
  st.session_state._USER_LOGINS_DATASET = DataConn.read_dataset("ei_app_user_list")

#Initialize user session variables. These store information about the logged-in user.
if "_LOGGED_USER_ROLE" not in st.session_state:
  st.session_state._LOGGED_USER_ROLE = None  #Role of the logged-in user (e.g., Admin, User)

if "_LOGGED_USER_NAME" not in st.session_state:
  st.session_state._LOGGED_USER_NAME = None  #Username of the logged-in user

if "_USER_COMPANY_ID" not in st.session_state:
  st.session_state._USER_COMPANY_ID = None  #Company ID associated with the user

if "_LOGGED_USER_ID" not in st.session_state:
  st.session_state._LOGGED_USER_ID = None  #Unique ID of the logged-in user

if "_LOGGED_USER_FULL_NAME" not in st.session_state:
  st.session_state._LOGGED_USER_FULL_NAME = None  #Full name of the logged-in user

#-------------------Set up Main Variables--------------------

#---------------Set up Additional Functions------------------

#Login Validation Function - checks if the provided username and password are valid.
def user_authentication(_USERNAME: str, _PASSWORD: str):

  #Filter the dataset to find the user record.
  _USER_RECORD = st.session_state._USER_LOGINS_DATASET[
    (st.session_state._USER_LOGINS_DATASET["user_name"] == _USERNAME) & 
    (st.session_state._USER_LOGINS_DATASET["user_active_password"] == _PASSWORD) & 
    (st.session_state._USER_LOGINS_DATASET["is_acive"] == True)]

  #Check if the user exists in the dataset.
  if not _USER_RECORD.empty:
    #If the user is found, return a dictionary with the user's details and a status of 200 (success).
    return {
      "_STATUS": 200,
      "_USERNAME": _USER_RECORD["user_name"].values[0],
      "_USER_ID": _USER_RECORD["user_id"].values[0],
      "_USER_ROLE": _USER_RECORD["user_role"].values[0],
      "_USER_FULL_NAME": _USER_RECORD["user_full_name"].values[0],
      "_USER_COMPANY_ID": _USER_RECORD["company_id"].values[0]
    }
  else:
    #If the user is not found, return an error message and a status of 400 (bad request).
    return {
      "_STATUS": 400,
      "_MESSAGE": "Invalid username or password!"
    }

#Login Form
def display_login_popup():

  #Create columns to center the login form in the page layout.
  _LOGIN_COLUMN1, _LOGIN_COLUMN2, _LOGIN_COLUMN3 = st.columns([1, 6, 1])
    
  #The form will be displayed in the middle column.
  with _LOGIN_COLUMN2:
    #The login form is wrapped inside an expander that is initially expanded.
    with st.expander("Login", expanded=True):
      # Text inputs for username and password. The password field masks the input.
      _TXT_USERNAME = st.text_input("Enter Username: ", key="_USERNAME")
      _TXT_PASSWORD = st.text_input("Enter password: ", key="_PASSWORD", type="password")

      # When the login button is clicked, the credentials are validated.
      if st.button("Login"):
        # Authenticate the user using the provided credentials.
        _LOGIN_RESULT = user_authentication(_TXT_USERNAME, _TXT_PASSWORD)
          
        # If the authentication is successful:
        if _LOGIN_RESULT["_STATUS"] == 200:
          # Store the user's details in the session state.
          st.session_state._LOGGED_USER_ROLE = _LOGIN_RESULT["_USER_ROLE"]
          st.session_state._LOGGED_USER_NAME = _LOGIN_RESULT["_USERNAME"]
          st.session_state._LOGGED_USER_ID = _LOGIN_RESULT["_USER_ID"]
          st.session_state._LOGGED_USER_FULL_NAME = _LOGIN_RESULT["_USER_FULL_NAME"]
          st.session_state._USER_COMPANY_ID = _LOGIN_RESULT["_USER_COMPANY_ID"]
            
          # Hide the login popup and refresh the app to reflect the new state.
          st.session_state._LOGIN_POPUP_VISIBILITY = False
          st.rerun()  # Refresh the Streamlit app to update the UI.
        else:
          # If authentication fails, display an error message.
          st.error(_LOGIN_RESULT["_MESSAGE"])

#---------------Set up Additional Functions------------------

#-------------------------Main Page--------------------------

#If the login popup is visible, display it.
if st.session_state._LOGIN_POPUP_VISIBILITY:
  display_login_popup()

#Run the menu function to display the app's menu.
menu.run_menu()

#If the user is logged in (login popup is not visible), display the main page content.
if st.session_state._LOGIN_POPUP_VISIBILITY is False:
  header.run_main_page()

#-------------------------Main Page--------------------------