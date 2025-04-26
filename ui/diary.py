import streamlit as st
from logic.session_manager import save_diary_entry

def show_diary():
    st.title("✍️ 감정 일기 작성")

    diary_entry = st.text_area("오늘 느낀 감정이나 생각을 자유롭게 작성해보세요.", height=300)

    if st.button("분석하기 🚀"):
        if not diary_entry.strip():
            st.warning("⚠️ 일기를 작성해주세요.")
        else:
            save_diary_entry(diary_entry)
            st.session_state.page = "result"
            st.rerun()
