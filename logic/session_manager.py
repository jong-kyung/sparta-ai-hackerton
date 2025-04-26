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

def save_analysis_result(analysis_result):
    st.session_state.analysis_result = analysis_result

def save_music_link(music_link):
    st.session_state.music_link = music_link

def load_analysis_result():
    return st.session_state.get("analysis_result", None)

def load_music_link():
    return st.session_state.get("music_link", None)

def save_dsm5_result(dsm5_result):
    st.session_state.dsm5_result = dsm5_result


def load_dsm5_result():
    return st.session_state.get("dsm5_result", None)