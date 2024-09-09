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

st.markdown(f"### My Dashboard - {st.session_state._LOGGED_USER_FULL_NAME}")
st.markdown("""<hr style="border: none; height: 2px; background: linear-gradient(to right, rgba(255, 0, 0, 0.7), rgba(255, 165, 0, 0.7), 
rgba(255, 255, 0, 0.7), rgba(0, 128, 0, 0.7), rgba(0, 0, 255, 0.7), rgba(75, 0, 130, 0.7), rgba(148, 0, 211, 0.7));">""", unsafe_allow_html=True
)
st.markdown(f"""<div style="text-align: justify;">
  Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum 
  has been the industry's standard dummy text ever since the 1500s, when an unknown printer 
  took a galley of type and scrambled it to make a type specimen book.</div>""", unsafe_allow_html=True)

#-----------------------Dashboard Tabs-----------------------
_DASHBOARD_TAB1, _DASHBOARD_TAB2, _DASHBOARD_TAB3 = st.tabs(["🕵️ My Recent Analysis", " 📊 Overall Emotion Tracker", "🌞 Improve My Skills"])

with _DASHBOARD_TAB1:
    
  _TAB_1_COLUMN1, _TAB_1_COLUMN2 = st.columns((2, 3))
  with _TAB_1_COLUMN1:
    #Filter Last record
    _FILTERED_LAST_UPDATE = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID)]
    _LAST_UPDATED_TRACKER_AND_SPRINT = _FILTERED_LAST_UPDATE.loc[(_FILTERED_LAST_UPDATE["submitted_on"].idxmax())][["sprint_name", "tracker_id", "submitted_on"]]
    st.markdown(f"##### {st.session_state._LOGGED_USER_FULL_NAME.split()[0]}'s Recent EI State - {_LAST_UPDATED_TRACKER_AND_SPRINT['tracker_id']}")
    _USER_MOOD_TRACKER_DATASET["submitted_on"] = pd.to_datetime(_USER_MOOD_TRACKER_DATASET["submitted_on"], format="mixed")

    #Process data to create the visualization
    _FIGURE_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
      (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID) & (_USER_MOOD_TRACKER_DATASET["tracker_id"] == _LAST_UPDATED_TRACKER_AND_SPRINT["tracker_id"]) &
      (_USER_MOOD_TRACKER_DATASET["sprint_name"] == _LAST_UPDATED_TRACKER_AND_SPRINT["sprint_name"]) & (_USER_MOOD_TRACKER_DATASET["submitted_on"].dt.date == 
      pd.to_datetime(_LAST_UPDATED_TRACKER_AND_SPRINT["submitted_on"], format="mixed").date())]

    #Display Graph 01
    _DASHBOARD_FIGURE1 = px.histogram(_FIGURE_DATASET, x="question_category", y="value", labels={"value":"Emotion Level"}, opacity=0.8)
    _DASHBOARD_FIGURE1.update_layout(bargap=0.2, xaxis_title="Emotional Category", yaxis_title="Emotion Level", xaxis_tickangle=45)
    st.plotly_chart(_DASHBOARD_FIGURE1)

  with _TAB_1_COLUMN2:

    #Process Dataset
    _COMPLETED_SPRINTS = _SPRINT_DATASET[(_SPRINT_DATASET["sprint_status"] == "Completed") & (_SPRINT_DATASET["is_active"] == True) & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)]
    _COMPLETED_SPRINTS["sprint_team_members"] = _COMPLETED_SPRINTS["sprint_team_members"].apply(ast.literal_eval)
    _COMPLETED_SPRINTS["sprint_full_team"] = _COMPLETED_SPRINTS["sprint_scrum_master"] + ", " + _COMPLETED_SPRINTS["sprint_team_leader"] + ", " + _COMPLETED_SPRINTS["sprint_team_members"].apply(lambda x: ", ".join(x))
    _COMPLETED_SPRINTS_FOR_USER = _COMPLETED_SPRINTS[_COMPLETED_SPRINTS["sprint_full_team"].str.contains(str(st.session_state._LOGGED_USER_NAME), case=False)]
    _LAST_COMPLETED_SPRINT = _COMPLETED_SPRINTS_FOR_USER.sort_values(by="sprint_completed_on", ascending=False).iloc[0]
    
    _FIGURE2_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
      (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID) & (_USER_MOOD_TRACKER_DATASET["sprint_name"] == _LAST_COMPLETED_SPRINT["sprint_name"])]
    st.markdown(f"##### My EI State for Last Sprint - {_LAST_COMPLETED_SPRINT['sprint_name']}")

    #Display Graph 02
    
    _DASHBOARD_FIGURE2 = px.histogram(_FIGURE2_DATASET, x="question_category", y="value", labels={"value":"Emotion Level"}, opacity=0.8, 
      color="tracker_id", barmode="group")
    _DASHBOARD_FIGURE2.update_layout(bargap=0.2, xaxis_title="Emotional Category", yaxis_title="Emotion Level", xaxis_tickangle=45, bargroupgap=0.1)
    st.plotly_chart(_DASHBOARD_FIGURE2)

  #Display activity Gantt Chart
  st.markdown(f"##### My Sprint Activity Timeline")

  #Process Dataset
  _ACTIVITY_DATASET = _SPRINT_DATASET[(_SPRINT_DATASET["is_active"] == True) & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)]
  _ACTIVITY_DATASET["sprint_team_members"] = _ACTIVITY_DATASET["sprint_team_members"].apply(ast.literal_eval)
  _ACTIVITY_DATASET["sprint_full_team"] = _ACTIVITY_DATASET["sprint_scrum_master"] + ", " + _ACTIVITY_DATASET["sprint_team_leader"] + ", " + _ACTIVITY_DATASET["sprint_team_members"].apply(lambda x: ", ".join(x))
  _USER_ACTIVITY_DATASET = _ACTIVITY_DATASET[_ACTIVITY_DATASET["sprint_full_team"].str.contains(str(st.session_state._LOGGED_USER_NAME), case=False)]
  _USER_ACTIVITY_DATASET = _USER_ACTIVITY_DATASET[["sprint_name", "sprint_status", "sprint_completed_on", "sprint_started_on"]]
  _USER_ACTIVITY_DATASET["sprint_completed_on"].fillna(datetime.now(), inplace=True)
  _USER_ACTIVITY_DATASET["sprint_started_on"].fillna(datetime.now(), inplace=True)
  _USER_ACTIVITY_DATASET["sprint_completed_on"] = pd.to_datetime(_USER_ACTIVITY_DATASET["sprint_completed_on"], format="mixed").dt.date
  _USER_ACTIVITY_DATASET["sprint_started_on"] = pd.to_datetime(_USER_ACTIVITY_DATASET["sprint_started_on"], format="mixed").dt.date

  #Display Graph 03
  _DASHBOARD_FIGURE3 = px.timeline(_USER_ACTIVITY_DATASET, x_start="sprint_started_on", x_end="sprint_completed_on", y="sprint_name", color="sprint_status")
  _DASHBOARD_FIGURE3.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=200, xaxis_title="Time Frame", yaxis_title="Activity Name")
  _DASHBOARD_FIGURE3.update_yaxes(autorange="reversed") 
  st.plotly_chart(_DASHBOARD_FIGURE3)

with _DASHBOARD_TAB2:
  st.markdown(f"##### My Overall Tracking")
  _TAB_2_COLUMN1, _TAB_2_COLUMN2 = st.columns((3, 3))

  #Get User Sprint History with team Details
  _USER_SPRINTS = _SPRINT_DATASET[(_SPRINT_DATASET["is_active"] == True) & (_SPRINT_DATASET["company_id"] == st.session_state._USER_COMPANY_ID)]
  _USER_SPRINTS["sprint_team_members"] = _USER_SPRINTS["sprint_team_members"].apply(ast.literal_eval)
  _USER_SPRINTS["sprint_full_team"] = _USER_SPRINTS["sprint_scrum_master"] + ", " + _USER_SPRINTS["sprint_team_leader"] + ", " + _USER_SPRINTS["sprint_team_members"].apply(lambda x: ", ".join(x))
  _USER_SPRINTS = _USER_SPRINTS[_USER_SPRINTS["sprint_full_team"].str.contains(str(st.session_state._LOGGED_USER_NAME), case=False)]

  _SELECTED_SPRINT_LIST = []
  _SELECTED_TRACKER_LIST = []
  _SELECTED_EMOTIONAL_STATES = []

  #Change color details of the multiselect
  colorize_multiselect_options(["darkcyan", "mediumpurple", "tan",])

  with _TAB_2_COLUMN1:
    _SELECTED_SPRINT_LIST = st.multiselect("Select your Sprints: ", _USER_SPRINTS["sprint_name"], _USER_SPRINTS["sprint_name"])
  with _TAB_2_COLUMN2:
    _SELECTED_TRACKER_LIST = st.multiselect("Select your Trackers: ", ["Stand-Up", "Review", "Retro"], ["Stand-Up", "Review", "Retro"])

  _SELECTED_EMOTIONAL_STATES = st.multiselect("Selected Emotional States: ", _USER_MOOD_TRACKER_DATASET["question_category"].unique().tolist(), _USER_MOOD_TRACKER_DATASET["question_category"].unique().tolist())

  _TAB_2_COLUMN3, _TAB_2_COLUMN4 = st.columns((3, 2))
  with _TAB_2_COLUMN3:

    #Process Dataset
    _USER_SELECTED_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
      (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID) & (_USER_MOOD_TRACKER_DATASET["tracker_id"].isin(_SELECTED_TRACKER_LIST)) &
      (_USER_MOOD_TRACKER_DATASET["sprint_name"].isin(_SELECTED_SPRINT_LIST)) & (_USER_MOOD_TRACKER_DATASET["question_category"].isin(_SELECTED_EMOTIONAL_STATES))]

    #Grouping Dataset
    _FIGURE4_DATASET = _USER_SELECTED_DATASET.groupby(["sprint_name", "question_category"], as_index=False)["value"].mean()

    st.markdown(f"##### My Sprint wise Emotion Average")
    #Dispaly Figure 04
    _DASHBOARD_FIGURE4 = px.line(_FIGURE4_DATASET, x="question_category", y="value", color="sprint_name", markers=True)
    _DASHBOARD_FIGURE4.update_layout(xaxis_title="Activity Name", yaxis_title="Average", showlegend=True)
    st.plotly_chart(_DASHBOARD_FIGURE4)

  with _TAB_2_COLUMN4:
    st.markdown(f"##### My Overall Emotions")
    _USER_SELECTED_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
    (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID) & (_USER_MOOD_TRACKER_DATASET["tracker_id"].isin(_SELECTED_TRACKER_LIST)) &
    (_USER_MOOD_TRACKER_DATASET["sprint_name"].isin(_SELECTED_SPRINT_LIST)) & (_USER_MOOD_TRACKER_DATASET["question_category"].isin(_SELECTED_EMOTIONAL_STATES))]

    #Dispaly Figure 05
    _FIGURE5_DATASET = _USER_SELECTED_DATASET.groupby(["question_category"], as_index=False)["value"].mean()
    _DASHBOARD_FIGURE5 = px.pie(_FIGURE5_DATASET, values='value', names='question_category')
    st.plotly_chart(_DASHBOARD_FIGURE5)

  st.markdown(f"""#### Compare My Average to My team's Emotion""")
  
  _USER_SELECTED_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
    (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID) & (_USER_MOOD_TRACKER_DATASET["tracker_id"].isin(_SELECTED_TRACKER_LIST)) &
    (_USER_MOOD_TRACKER_DATASET["sprint_name"].isin(_SELECTED_SPRINT_LIST)) & (_USER_MOOD_TRACKER_DATASET["question_category"].isin(_SELECTED_EMOTIONAL_STATES))]

  _USER_OVERALL_EMOTION_DATASET = _USER_SELECTED_DATASET.groupby(["question_category"], as_index=False)["value"].mean().reset_index()
  _USER_OVERALL_EMOTION_DATASET["group"] = "My Average"

  #Get the team members for the sprint the user is part of (excluding the logged-in user)
  _SPRINT_ROW = _USER_SPRINTS[_USER_SPRINTS["sprint_full_team"].str.contains(st.session_state._LOGGED_USER_NAME)]
  _TEAM_MEMBERS = _SPRINT_ROW["sprint_full_team"].values[0].split(',')
  _TEAM_MEMBERS = [_MEMBER.strip() for _MEMBER in _TEAM_MEMBERS if _MEMBER.lower().strip() != st.session_state._LOGGED_USER_NAME.lower()]
  #Map team member names to user IDs
  _TEAM_MEMBER_IDS = st.session_state._USER_LOGINS_DATASET[st.session_state._USER_LOGINS_DATASET["user_name"].isin(_TEAM_MEMBERS)]["user_id"].tolist()

  #Filter mood data for the team members only
  _TEAM_MOOD_TRACKER_DATASET = _USER_MOOD_TRACKER_DATASET[_USER_MOOD_TRACKER_DATASET["user_id"].isin(_TEAM_MEMBER_IDS) & 
    (_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & (_USER_MOOD_TRACKER_DATASET["tracker_id"].isin(_SELECTED_TRACKER_LIST)) &
    (_USER_MOOD_TRACKER_DATASET["sprint_name"].isin(_SELECTED_SPRINT_LIST)) & (_USER_MOOD_TRACKER_DATASET["question_category"].isin(_SELECTED_EMOTIONAL_STATES))]
  _TEAM_OVERALL_EMOTION_DATASET = _TEAM_MOOD_TRACKER_DATASET.groupby(["question_category"], as_index=False)["value"].mean().reset_index()
  _TEAM_OVERALL_EMOTION_DATASET["group"] = "My Team Average"

  _FIGURE6_DATASET = pd.concat([_USER_OVERALL_EMOTION_DATASET, _TEAM_OVERALL_EMOTION_DATASET], ignore_index=True)
  _DASHBOARD_FIGURE6 = px.line(_FIGURE6_DATASET, x="question_category", y="value", color="group", markers=True)
  _DASHBOARD_FIGURE6.update_layout(xaxis_title="Activity Name", yaxis_title="Average", showlegend=True)
  st.plotly_chart(_DASHBOARD_FIGURE6)

with _DASHBOARD_TAB3:
  st.markdown(f"""### Hi, {str(st.session_state._LOGGED_USER_FULL_NAME).split()[0]}!

  <div style="text-align: justify;">
  According to our system analysis, you have a positive emotional status. Below is a detailed analysis of your emotional intelligence across 
  different categories. Keep reading for personalized feedback and recommendations.</div>""", unsafe_allow_html=True)
  st.divider()
  
  _USER_SELECTED_DATASET = _USER_MOOD_TRACKER_DATASET[(_USER_MOOD_TRACKER_DATASET["company_id"] == st.session_state._USER_COMPANY_ID) & 
    (_USER_MOOD_TRACKER_DATASET["user_id"] == st.session_state._LOGGED_USER_ID)]

  _INSIGHTS_DATASET = _USER_SELECTED_DATASET.groupby(["question_category"], as_index=False)["value"].mean().reset_index()

  _SUCCESS_MESSAGE = ""
  _WARNING_MESSAGE = ""
  _SUCCESS_DETAIL = ""
  _WARNING_DETAIL = ""
  _RECOMMENDATIONS = {
    "Emotional State": "Practice mindfulness and stress management techniques.",
    "Self Awareness": "Regular self-reflection can help you understand your emotions better.",
    "Self Regulation": "Techniques like deep breathing can help in managing impulses.",
    "Social Awareness": "Engage in active listening and empathy-building exercises.",
    "Empathy": "Put yourself in others' shoes to better understand their perspectives.",
    "Motivation": "Set clear goals and celebrate small achievements to stay motivated."
  }

  for _, _ROW in _INSIGHTS_DATASET.iterrows():
    _CATEGORY = _ROW["question_category"]
    _AVG_VALUE = _ROW["value"]

    if _AVG_VALUE > 3.5:
      _SUCCESS_DETAIL += f"""- **{_CATEGORY}**: Your average score is **{_AVG_VALUE:.1f}**\n\n"""
      st.toast(f"Congratulations on your **{_CATEGORY}** Score!", icon = "🥳")
      time.sleep(1)
    elif _AVG_VALUE < 3.0:
      _WARNING_DETAIL += f"""- **{_CATEGORY}**: Your average score is **{_AVG_VALUE:.1f}**. Consider exploring additional training or coaching sessions. Please
      refer to the following. {_RECOMMENDATIONS[_CATEGORY]}\n\n"""

  #Display messagees with expandable details
  if _SUCCESS_DETAIL:
    st.success(f"Congratulations on your excellent performance in the following areas, Keep up the great work!\n\n{_SUCCESS_DETAIL}")
  if _WARNING_DETAIL:
    st.warning(f"There are some areas where improvement is possible. Don't be discouraged, here are some recommendations to help you improve:\n\n{_WARNING_DETAIL}")



