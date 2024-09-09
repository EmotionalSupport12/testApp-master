#--------------------Importing Libraries---------------------

import os
import pandas as pd

#--------------------Importing Libraries---------------------

#-------------------Set up Main Variables--------------------

#The path to the Excel file containing the data in Google Drive.
_MAIN_DATA_FILE_PATH = "Data/MainDataFile.xlsx"

#-------------------Set up Main Variables--------------------

#------------------Set up Core Functions---------------------

#Function to read a specific sheet from the Excel file and return as a DataFrame.
def read_dataset(_SHEETNAME: str) -> pd.DataFrame:

  if _SHEETNAME == "ei_app_user_list":
    return pd.read_csv("Data/ei_app_user_list.csv")
  
  elif _SHEETNAME == "ei_app_sprint_list":
    return pd.read_csv("Data/ei_app_sprint_list.csv")

  elif _SHEETNAME == "ei_app_question_list":
    return pd.read_csv("Data/ei_app_question_list.csv")

  elif _SHEETNAME == "ei_app_mood_tracker_data":
    return pd.read_csv("Data/ei_app_mood_tracker_data.csv")

  elif _SHEETNAME == "ei_app_retro_tracker_data":
    return pd.read_csv("Data/ei_app_retro_tracker_data.csv")

#Function to read all sheets from the Excel file and return them as a dictionary of DataFrames.
def read_all_datasets() -> pd.DataFrame:
  _USER_DATA = pd.read_csv("Data/ei_app_user_list.csv")  
  _SPRINT_DATA = pd.read_csv("Data/ei_app_sprint_list.csv")
  _QUESTION_DATA = pd.read_csv("Data/ei_app_question_list.csv")
  _MOOD_DATA = pd.read_csv("Data/ei_app_mood_tracker_data.csv")
  _RETRO_DATA = pd.read_csv("Data/ei_app_retro_tracker_data.csv")
  return {"ei_app_user_list": _USER_DATA, "ei_app_sprint_list": _SPRINT_DATA, "ei_app_question_list": _QUESTION_DATA, "ei_app_mood_tracker_data": _MOOD_DATA, 
    "ei_app_retro_tracker_data": _RETRO_DATA}

#------------------Set up Core Functions---------------------

#---------------Set up Additional Functions------------------

#Function to save data to a Excel file
def save_mood_tracker_data_to_file(_NEW_DATASET: pd.DataFrame, _COMPANY_ID: str, _SPRINT: str, _USER_ID: str, _TRACKER: str, _SUBMIT_TIME: str):
  try:

    # Load the Excel file and get the sheet names
    _RETRO_DATA_FILE_PATH = "Data/ei_app_mood_tracker_data.csv"

    if os.path.exists(_RETRO_DATA_FILE_PATH):
      # Check if similar data already exists in the file
      _EXISTING_DATASET = read_dataset("ei_app_mood_tracker_data")
      _EXISTING_DATASET["submitted_on"] = pd.to_datetime(_EXISTING_DATASET["submitted_on"], format="mixed")

      _FILTERED_EXISTING_DATASET = _EXISTING_DATASET[(_EXISTING_DATASET["company_id"] == _COMPANY_ID) & (_EXISTING_DATASET["sprint_name"] == _SPRINT) &
        (_EXISTING_DATASET["user_id"] == _USER_ID) & (_EXISTING_DATASET["tracker_id"] == _TRACKER)
      #& (_EXISTING_DATASET["submitted_on"].dt.date == _SUBMIT_TIME)
      ]

      if not _FILTERED_EXISTING_DATASET.empty:
        return {
          "_STATUS": 0,
          "_MESSAGE": "Similar data already exists in the file. Data not saved!"}

      # Append the new data to the existing CSV file
      _NEW_DATASET.to_csv(_RETRO_DATA_FILE_PATH, mode='a', header=False, index=False) 
    else:
      # If the file doesn't exist, create it and write the new data with headers
      _NEW_DATASET.to_csv(_RETRO_DATA_FILE_PATH, mode='w', header=True, index=False)

    return {
      "_STATUS": 1,
      "_MESSAGE": "Data successfully saved!"}
  except Exception as _EX:
    return {
      "_STATUS": 0,
      "_MESSAGE": f"Something went wrong when saving the data: {_EX}"}

def get_user_mood_tracker_data():
  _USER_STANDUP_REVIEW_TRACKER_DATASET = read_dataset("ei_app_mood_tracker_data")
  _USER_RETRO_TRACKER_FULL_DATASET = read_dataset("ei_app_retro_tracker_data")
  _USER_RETRO_TRACKER_DATASET = _USER_RETRO_TRACKER_FULL_DATASET[["company_id", "sprint_name", "entered_user_id", "entered_user_name", "tracker_id", "question_id", 
    "question_category", "finalized_value", "entered_on"]]
  _USER_RETRO_TRACKER_DATASET = _USER_RETRO_TRACKER_DATASET.rename(columns={"entered_user_id": "user_id", "entered_user_name": "user_name", "entered_user_name": "user_name", 
    "finalized_value": "value", "entered_on": "submitted_on"})

  return pd.concat([_USER_STANDUP_REVIEW_TRACKER_DATASET, _USER_RETRO_TRACKER_DATASET]).reset_index(drop=True)

#---------------Set up Additional Functions------------------
