import streamlit as st

def display_authenticated_menu_items():
  #Show a navigation menu for authenticated users
  st.sidebar.markdown(f"##### **:blue[Resources]** ")
  
  st.sidebar.page_link("app.py", label="Home")
  st.sidebar.page_link("pages/user.py", label="Your Profile")
  st.sidebar.page_link("pages/mood_tracker.py", label="EI Mood Tracker")

  st.sidebar.markdown(f"##### **:blue[Dashboards]** ")
  st.sidebar.page_link("pages/user_ei_dashboard.py", label="My EI Dashboard")
  st.sidebar.page_link("pages/scrum_master_ei_dashboard.py", label="Scrum Master Dashboard", disabled=st.session_state._LOGGED_USER_ROLE not in ["Scrum Master", "Super Admin"])

  st.sidebar.markdown(f"##### **:blue[Customizations]** ")
  st.sidebar.page_link("pages/settings.py", label="Settings")
  st.sidebar.page_link("pages/testpage.py", label="Test page")

  if st.session_state._LOGGED_USER_ROLE in ["Admin", "Super Admin"]:
    st.sidebar.page_link("pages/user_manager.py", label="Manage Admin Access", disabled=st.session_state._LOGGED_USER_ROLE != "Super Admin")

def display_unauthenticated_menu_items():
  st.sidebar.page_link("app.py", label="Log in")

def run_menu():
  #Check if a user is logged in or not, then show the correct navigation menu
  if "_LOGGED_USER_ROLE" not in st.session_state or st.session_state._LOGGED_USER_ROLE is None:
    display_unauthenticated_menu_items()
    return
  display_authenticated_menu_items()

def redirect_to_Login():
  # Redirect users to the main page if not logged in
  if "_LOGGED_USER_ROLE" not in st.session_state or st.session_state._LOGGED_USER_ROLE is None:
    st.switch_page("app.py")
  run_menu()