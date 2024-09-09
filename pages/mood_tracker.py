#--------------------Importing Libraries---------------------

import ast
import time
import menu
import pandas as pd
import streamlit as st
from datetime import datetime
from Core import data_connection as DataConn

#--------------------Importing Libraries---------------------

#Page configurations for the Streamlit app
st.set_page_config(page_title="Agile Emotion App!", page_icon="😉", layout="wide", initial_sidebar_state="expanded")

#Redirect to login if the user is not logged in
menu.redirect_to_Login()

#---------------------Set up Main Header---------------------

#Create a header for the application with the app name and logo
_HEADER_COLUMN1, _HEADER_COLUMN2 = st.columns((6, 1))  # Define two columns for the header
with _HEADER_COLUMN1:
  st.markdown(f"""### Welcome to Agile Emotion App!
  <div style="text-align: justify;">
  Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum 
  has been the industry's standard dummy text ever since the 1500s, when an unknown printer 
  took a galley of type and scrambled it to make a type specimen book.</div>""", unsafe_allow_html=True)
  
# Display the app logo in the second column
_HEADER_COLUMN2.image("assets/EI_APP_LOGO.png", width=130)

# Create a horizontal line with a gradient effect under the header
st.markdown("""<hr style="border: none; height: 2px; background: linear-gradient(to right, rgba(255, 0, 0, 0.7), rgba(255, 165, 0, 0.7), 
rgba(255, 255, 0, 0.7), rgba(0, 128, 0, 0.7), rgba(0, 0, 255, 0.7), rgba(75, 0, 130, 0.7), rgba(148, 0, 211, 0.7));">""", unsafe_allow_html=True)

#---------------------Set up Main Header---------------------

#-------------------Set up Main Variables--------------------

# Load data from CSV files
_QUESTIONS_DATASET = DataConn.read_dataset("ei_app_question_list")
_SPRINT_DATASET = DataConn.read_dataset("ei_app_sprint_list")

# Define a list of tracker types
_TRACKER_LIST = ["Stand-Up", "Review", "Retro"]

# Get available sprints for the logged-in user based on their role and company ID
if st.session_state._LOGGED_USER_NAME.lower() in [_ROLE.lower() for _ROLE in ["Admin", "Super Admin"]]:
  # If the user is an admin, show all ongoing sprints for the company
  _SPRINT_LIST = _SPRINT_DATASET["sprint_name"][(_SPRINT_DATASET["sprint_status"] == "Ongoing") & (_SPRINT_DATASET["is_active"] == True)
    & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)].unique().tolist()
else:
  # For non-admin users, show only the sprints they are part of
  _ONGOING_SPRINTS = _SPRINT_DATASET[(_SPRINT_DATASET["sprint_status"] == "Ongoing") & (_SPRINT_DATASET["is_active"] == True) & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)]
  _ONGOING_SPRINTS["sprint_team_members"] = _ONGOING_SPRINTS["sprint_team_members"].apply(ast.literal_eval)
  _ONGOING_SPRINTS["sprint_full_team"] = _ONGOING_SPRINTS["sprint_scrum_master"] + ", " + _ONGOING_SPRINTS["sprint_team_leader"] + ", " + _ONGOING_SPRINTS["sprint_team_members"].apply(lambda x: ", ".join(x))
  _ONGOING_SPRINTS_FOR_USER = _ONGOING_SPRINTS[_ONGOING_SPRINTS["sprint_full_team"].str.contains(str(st.session_state._LOGGED_USER_NAME), case=False)]
  _SPRINT_LIST = _ONGOING_SPRINTS_FOR_USER["sprint_name"].tolist()

#-------------------Set up Main Variables--------------------

#--------------------Tracker Page - Main---------------------
# Create columns for selecting the tracker type and sprint
_TRACKER_COLUMN1, _TRACKER_COLUMN2 = st.columns((1, 1))
with _TRACKER_COLUMN1:
  _MOOD_TRACKER = st.selectbox("Select your Mood Tracker: ", _TRACKER_LIST, index=0)  # Dropdown for tracker type
with _TRACKER_COLUMN2:
  _SPRINT = st.selectbox("Select your Sprint: ", _SPRINT_LIST, index=0)  # Dropdown for sprint
#--------------------Tracker Page - Main---------------------

#------------------Tracker Page - Stand-Up-------------------
# Stand-Up tracker logic
if _MOOD_TRACKER == "Stand-Up":
    
  # Define additional variables to hold question data
  _QUESTION_VARIABLE_LIST = []
  _QUESTION_DATA_WITH_VALUES = []
    
  # Form for Stand-Up tracker
  with st.form("stand_up_form"):
    st.markdown(f"##### {_MOOD_TRACKER} Tracker")
    
    # Filter questions based on company and tracker type
    _FILTERED_QUESTIONS_DATASET = _QUESTIONS_DATASET[(_QUESTIONS_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
    (_QUESTIONS_DATASET["tracker_id"] == _MOOD_TRACKER) & (_QUESTIONS_DATASET["is_active"] == True)]
    for _INDEX, _ROW in _FILTERED_QUESTIONS_DATASET.iterrows():
      _VARIABLE_NAME = "_QUESTION_" + str(_ROW["question_id"])
      _QUESTION_VARIABLE_LIST.append({
        "_VARIABLE_NAME": _VARIABLE_NAME, 
        "_QUESTION_CATEGORY": _ROW["question_category"]})
      # Create a slider for each question
      globals()[_VARIABLE_NAME] = st.slider(_ROW["question"], value=1, min_value=_ROW["min_value"], max_value=_ROW["max_value"])
  
    # Save data when the form is submitted
    if st.form_submit_button("Save Data"):
      if _SPRINT is not None:
        for _ITEM in _QUESTION_VARIABLE_LIST:
          # Append question responses to the dataset
          _QUESTION_DATA_WITH_VALUES.append({
            "company_id": st.session_state._USER_COMPANY_ID,
            "sprint_name": _SPRINT,
            "user_id": st.session_state._LOGGED_USER_ID,
            "user_name": st.session_state._LOGGED_USER_NAME,
            "tracker_id": _MOOD_TRACKER,
            "question_id": int(_ITEM["_VARIABLE_NAME"].replace("_QUESTION_", "")),
            "question_category": _ITEM["_QUESTION_CATEGORY"],
            "value": globals()[_ITEM["_VARIABLE_NAME"]],
            "submitted_on": datetime.now()
          })

        # Save the dataset to a CSV file
        _RESULT = DataConn.save_mood_tracker_data_to_file(pd.DataFrame(_QUESTION_DATA_WITH_VALUES), st.session_state._USER_COMPANY_ID, _SPRINT, 
          st.session_state._LOGGED_USER_ID, _MOOD_TRACKER, datetime.now().date())
        
        _MESSAGE = st.empty()
        if _RESULT["_STATUS"] == 1:
          _MESSAGE.success(_RESULT["_MESSAGE"])
        else:
          _MESSAGE.error(_RESULT["_MESSAGE"])
        time.sleep(5)
        _MESSAGE.empty()
      else:
        _MESSAGE = st.empty()
        _MESSAGE.error("Select Your Sprint. If you don't have access, Please check with your Scrum Master!")
        time.sleep(5)
        _MESSAGE.empty()
#------------------Tracker Page - Stand-Up-------------------

#-------------------Tracker Page - Review--------------------
# Review tracker logic (similar to Stand-Up)
if _MOOD_TRACKER == "Review":
    
  # Define additional variables to hold question data
  _QUESTION_VARIABLE_LIST = []
  _QUESTION_DATA_WITH_VALUES = []
    
  # Form for Review tracker
  with st.form("review_form"):
    st.markdown(f"##### {_MOOD_TRACKER} Tracker")
      
    # Filter questions based on company and tracker type
    _FILTERED_QUESTIONS_DATASET = _QUESTIONS_DATASET[(_QUESTIONS_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
    (_QUESTIONS_DATASET["tracker_id"] == _MOOD_TRACKER) & (_QUESTIONS_DATASET["is_active"] == True)]
    for _INDEX, _ROW in _FILTERED_QUESTIONS_DATASET.iterrows():
      _VARIABLE_NAME = "_QUESTION_" + str(_ROW["question_id"])
      _QUESTION_VARIABLE_LIST.append({
        "_VARIABLE_NAME": _VARIABLE_NAME, 
        "_QUESTION_CATEGORY": _ROW["question_category"]})
        # Create a slider for each question
      globals()[_VARIABLE_NAME] = st.slider(_ROW["question"], value=1, min_value=_ROW["min_value"], max_value=_ROW["max_value"])
  
    # Save data when the form is submitted
    if st.form_submit_button("Save Data"):
      if _SPRINT is not None:
        for _ITEM in _QUESTION_VARIABLE_LIST:
          # Append question responses to the dataset
          _QUESTION_DATA_WITH_VALUES.append({
            "company_id": st.session_state._USER_COMPANY_ID,
            "sprint_name": _SPRINT,
            "user_id": st.session_state._LOGGED_USER_ID,
            "user_name": st.session_state._LOGGED_USER_NAME,
            "tracker_id": _MOOD_TRACKER,
            "question_id": int(_ITEM["_VARIABLE_NAME"].replace("_QUESTION_", "")),
            "question_category": _ITEM["_QUESTION_CATEGORY"],
            "value": globals()[_ITEM["_VARIABLE_NAME"]],
            "submitted_on": datetime.now()
          })

        # Save the dataset to a CSV file
        _RESULT = DataConn.save_mood_tracker_data_to_file(pd.DataFrame(_QUESTION_DATA_WITH_VALUES), st.session_state._USER_COMPANY_ID, _SPRINT, st.session_state._LOGGED_USER_ID,
          _MOOD_TRACKER, datetime.now().date())
        _MESSAGE = st.empty()
        if _RESULT["_STATUS"] == 1:
          _MESSAGE.success(_RESULT["_MESSAGE"])
        else:
          _MESSAGE.error(_RESULT["_MESSAGE"])
        time.sleep(5)
        _MESSAGE.empty() 
      else:
        _MESSAGE = st.empty()
        _MESSAGE.error("Select Your Sprint. If you don't have access, Please check with your Scrum Master!")
        time.sleep(5)
        _MESSAGE.empty()
#-------------------Tracker Page - Review--------------------

#-------------------Tracker Page - Retro---------------------
# Retro tracker logic (not implemented in detail)
if _MOOD_TRACKER == "Retro":
    
  st.markdown(f"""##### {_MOOD_TRACKER} Tracker
  <div style="text-align: justify;">
  This process is created using 360-degree review logic. Due to the coding complexity, the process is currently handled manually in Excel.</div>""", unsafe_allow_html=True)
  
#-------------------Tracker Page - Retro---------------------
