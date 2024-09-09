import menu
import streamlit as st

def run_page_header():
  #---------------------Set up Main Header---------------------
  _HEADER_COLUMN1, _HEADER_COLUMN2 = st.columns((6, 1))
  with _HEADER_COLUMN1:
    st.markdown(f"""### Welcome to Agile Emotion App!
  <div style="text-align: justify;">
  Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum 
  has been the industry's standard dummy text ever since the 1500s, when an unknown printer 
  took a galley of type and scrambled it to make a type specimen book.</div>""", unsafe_allow_html=True)
    
  _HEADER_COLUMN2.image("assets/EI_APP_LOGO.png", width=130)
  st.markdown("""<hr style="border: none; height: 2px; background: linear-gradient(to right, rgba(255, 0, 0, 0.7), rgba(255, 165, 0, 0.7), 
  rgba(255, 255, 0, 0.7), rgba(0, 128, 0, 0.7), rgba(0, 0, 255, 0.7), rgba(75, 0, 130, 0.7), rgba(148, 0, 211, 0.7));">""", unsafe_allow_html=True
  )
  #---------------------Set up Main Header---------------------

def run_main_page():
  run_page_header()
  #---------------------Set up Main Details--------------------
  _DETAIL_COLUMN1, _DETAIL_COLUMN2 = st.columns((6, 1))
  with _DETAIL_COLUMN1:
    if "_LOGGED_USER_FULL_NAME" in st.session_state:
      st.markdown(f"""### Hello, {st.session_state._LOGGED_USER_FULL_NAME.split()[0]}!""")

  with _DETAIL_COLUMN2:
    if st.button("Logout"):
      st.session_state._LOGGED_USER_NAME = None
      st.session_state._LOGGED_USER_ROLE = None
      st.session_state._USER_COMPANY_ID = None
      st.session_state._LOGGED_USER_ID = None
      st.session_state._LOGGED_USER_FULL_NAME = None
      st.session_state._LOGIN_POPUP_VISIBILITY = True
      menu.run_menu()
      st.rerun()
  
  st.markdown(f"""<div style="text-align: justify;">
  Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever 
  since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only 
  five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. Contrary to popular belief, Lorem Ipsum 
  is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard 
  McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a 
  Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes 
  from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This 
  book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit 
  amet..", comes from a line in section 1.10.32.</div>""", unsafe_allow_html=True)

  #---------------------Set up Main Details--------------------