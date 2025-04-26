import streamlit as st

def save_basic_info(name, birth_date, job):
    st.session_state.name = name
    st.session_state.birth_date = birth_date
    st.session_state.job = job

def save_survey_data(phq9_scores):
    st.session_state.phq9_scores = phq9_scores

def save_diary_entry(diary_text):
    st.session_state.diary = diary_text   
    st.session_state.submitted = True

def load_user_data():
    if all(k in st.session_state for k in ("name", "birth_date", "job", "phq9_scores", "diary")):
        return {
            "name": st.session_state.name,
            "birth_date": st.session_state.birth_date,
            "job": st.session_state.job,
            "phq9_scores": st.session_state.phq9_scores,
            "diary": st.session_state.diary  
        }
    else:
        return None
