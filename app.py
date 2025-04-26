# app.py

import streamlit as st
from ui import home, survey, diary, result

st.set_page_config(page_title="마인드 닥터", layout="centered")  

# 세션 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

# 페이지 라우팅
if st.session_state.page == "home":
    home.show_home()

elif st.session_state.page == "survey":
    survey.show_survey()

elif st.session_state.page == "diary":
    diary.show_diary()

elif st.session_state.page == "result":
    result.show_result()
