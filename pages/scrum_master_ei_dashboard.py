#--------------------Importing Libraries---------------------
import ast
import menu
import time
import pandas as pd
import streamlit as st
import plotly.express as px

from datetime import datetime
from Core import data_connection as DataConn
#--------------------Importing Libraries---------------------

#Page configurations
st.set_page_config(page_title="Agile Emotion App!", page_icon="😉", layout="wide", initial_sidebar_state="expanded")

# Redirect to login page
menu.redirect_to_Login()

#-------------------Set up Main Variables--------------------
#Read CSV File
_SPRINT_DATASET = DataConn.read_dataset("ei_app_sprint_list")
_USER_STANDUP_REVIEW_TRACKER_DATASET = DataConn.read_dataset("ei_app_mood_tracker_data")
#Read Retro Manual data and combine with Other sprint reviews
_USER_MOOD_TRACKER_DATASET = DataConn.get_user_mood_tracker_data()
#-------------------Set up Main Variables--------------------

#---------------Set up Additional Functions------------------
def colorize_multiselect_options(_COLORS: list[str]) -> None:
  _RULES = ""
  _N_COLORS = len(_COLORS)
  for _I, _COLOR in enumerate(_COLORS):
    _RULES += f""".stMultiSelect div[data-baseweb="select"] span[data-baseweb="tag"]:nth-child({_N_COLORS}n+{_I}){{background-color: {_COLOR};}}"""
  st.markdown(f"<style>{_RULES}</style>", unsafe_allow_html=True)
#---------------Set up Additional Functions------------------

st.markdown(f"### Scrum Master Dashboard - {st.session_state._LOGGED_USER_FULL_NAME}")
st.markdown("""<hr style="border: none; height: 2px; background: linear-gradient(to right, rgba(255, 0, 0, 0.7), rgba(255, 165, 0, 0.7), 
rgba(255, 255, 0, 0.7), rgba(0, 128, 0, 0.7), rgba(0, 0, 255, 0.7), rgba(75, 0, 130, 0.7), rgba(148, 0, 211, 0.7));">""", unsafe_allow_html=True
)
st.markdown(f"""<div style="text-align: justify;">
  Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum 
  has been the industry's standard dummy text ever since the 1500s, when an unknown printer 
  took a galley of type and scrambled it to make a type specimen book.</div>""", unsafe_allow_html=True)

#-----------------------Dashboard Tabs-----------------------

#Change color details of the multiselect
colorize_multiselect_options(["darkcyan", "mediumpurple", "tan",])

st.markdown(f"##### 📊 Team Overall Tracking")
_TAB_1_COLUMN1, _TAB_1_COLUMN2 = st.columns((3, 3))
_TAB_1_COLUMN3, _TAB_1_COLUMN4 = st.columns((3, 3))

#Get User Sprint History with team Details
_USER_SPRINTS = _SPRINT_DATASET[(_SPRINT_DATASET["is_active"] == True) & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)]
_USER_SPRINTS["sprint_team_members"] = _USER_SPRINTS["sprint_team_members"].apply(ast.literal_eval)
_USER_SPRINTS["sprint_full_team"] = _USER_SPRINTS["sprint_scrum_master"] + ", " + _USER_SPRINTS["sprint_team_leader"] + ", " + _USER_SPRINTS["sprint_team_members"].apply(lambda x: ", ".join(x))
_USER_SPRINTS = _USER_SPRINTS[_USER_SPRINTS["sprint_full_team"].str.contains(str(st.session_state._LOGGED_USER_NAME), case=False)]

_SELECTED_SPRINT_LIST = []
_SELECTED_TRACKER_LIST = []
_SELECTED_EMOTIONAL_STATES = []
_SELECTED_SPRINT_MEMBER_LIST = []

#Change color details of the multiselect
colorize_multiselect_options(["darkcyan", "mediumpurple", "tan",])

#-------------------Team Member Selection--------------------
_SCRUM_MASTER_SPRINTS = _SPRINT_DATASET[(_SPRINT_DATASET["sprint_scrum_master"] == str(st.session_state._LOGGED_USER_NAME)) & (_SPRINT_DATASET["is_active"] == True) 
  & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)]
_SCRUM_MASTER_SPRINTS["sprint_team_members"] = _SCRUM_MASTER_SPRINTS["sprint_team_members"].apply(ast.literal_eval)
_SCRUM_MASTER_SPRINTS["sprint_full_team"] = _SCRUM_MASTER_SPRINTS["sprint_scrum_master"] + ", " + _SCRUM_MASTER_SPRINTS["sprint_team_leader"] + ", " + _SCRUM_MASTER_SPRINTS["sprint_team_members"].apply(lambda x: ", ".join(x))

#Get All the Team Members
_SCRUM_MASTER_SPRINT_USER_LIST = list(set([_ITEM.strip() for _SUBLIST in _SCRUM_MASTER_SPRINTS['sprint_full_team'].str.split(',') for _ITEM in _SUBLIST]))
#-------------------Team Member Selection--------------------

with _TAB_1_COLUMN1:
  _SELECTED_SPRINT_LIST = st.multiselect("Select your Sprints: ", _USER_SPRINTS["sprint_name"], _USER_SPRINTS["sprint_name"])
with _TAB_1_COLUMN2:
  _SELECTED_TRACKER_LIST = st.multiselect("Select your Trackers: ", ["Stand-Up", "Review", "Retro"], ["Stand-Up", "Review", "Retro"])

with _TAB_1_COLUMN3:
  _SELECTED_EMOTIONAL_STATES = st.multiselect("Selected Emotional States: ", _USER_MOOD_TRACKER_DATASET["question_category"].unique().tolist(), _USER_MOOD_TRACKER_DATASET["question_category"].unique().tolist())
with _TAB_1_COLUMN4:
  _SELECTED_SPRINT_MEMBER_LIST = st.multiselect("Select your Team Member: ", _SCRUM_MASTER_SPRINT_USER_LIST, _SCRUM_MASTER_SPRINT_USER_LIST)

_TAB_1_COLUMN5, _TAB_2_COLUMN6 = st.columns((5, 2))
with _TAB_1_COLUMN5:
  st.markdown(f"##### Team's Emotion Level Comparison")
  #Full Detailed Histrogram
  _SELECTED_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) &
    (_USER_MOOD_TRACKER_DATASET["user_name"].isin(_SELECTED_SPRINT_MEMBER_LIST)) & (_USER_MOOD_TRACKER_DATASET["question_category"].isin(_SELECTED_EMOTIONAL_STATES)) &
    (_USER_MOOD_TRACKER_DATASET["sprint_name"].isin(_SELECTED_SPRINT_LIST)) & (_USER_MOOD_TRACKER_DATASET["tracker_id"].isin(_SELECTED_TRACKER_LIST))]

  #Grouping Dataset
  _FIGURE1_DATASET = _SELECTED_DATASET.groupby(["user_name", "question_category"], as_index=False)["value"].mean()
  #Display Graph 02
  _DASHBOARD_FIGURE1 = px.histogram(_FIGURE1_DATASET, x="question_category", y="value", labels={"value":"Emotion Level"}, opacity=0.8, 
    color="user_name", barmode="group")
  _DASHBOARD_FIGURE1.update_layout(bargap=0.2, xaxis_title="Emotional Category", yaxis_title="Emotion Level", xaxis_tickangle=45, bargroupgap=0.1)
  st.plotly_chart(_DASHBOARD_FIGURE1)

with _TAB_2_COLUMN6:
  st.markdown(f"##### Overall Employee Emotion Average")
  #Process Dataset
  _SELECTED_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
    (_USER_MOOD_TRACKER_DATASET["user_name"].isin(_SELECTED_SPRINT_MEMBER_LIST)) & (_USER_MOOD_TRACKER_DATASET["tracker_id"].isin(_SELECTED_TRACKER_LIST)) &
    (_USER_MOOD_TRACKER_DATASET["sprint_name"].isin(_SELECTED_SPRINT_LIST)) & (_USER_MOOD_TRACKER_DATASET["question_category"].isin(_SELECTED_EMOTIONAL_STATES))]

  #Grouping Dataset
  _FIGURE2_DATASET = _SELECTED_DATASET.groupby(["question_category"], as_index=False)["value"].mean()
  _DASHBOARD_FIGURE2 = px.pie(_FIGURE2_DATASET, values='value', names='question_category')
  
  #Dispaly Figure 02
  st.plotly_chart(_DASHBOARD_FIGURE2)




