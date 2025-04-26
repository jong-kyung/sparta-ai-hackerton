import streamlit as st
import openai
import os
from dotenv import load_dotenv
from logic.session_manager import load_user_data
from logic.survey_analyzer import survey_summary
from logic.diary_analyzer import analyze_diary_and_comfort

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def show_result():
    st.title("📈 감정 분석 결과")

    user_data = load_user_data()

    if not user_data:
        st.warning("입력된 데이터가 없습니다. 처음부터 다시 시작해주세요.")
        st.session_state.page = "home"
        st.rerun()

    name = user_data["name"]
    birth_date = user_data["birth_date"]
    job = user_data["job"]
    phq9_scores = user_data["phq9_scores"]
    diary = user_data["diary"]

    total_score = sum(phq9_scores)
    severity_percentage = int((total_score / 27) * 100)

    st.write(f"**이름:** {name}")
    st.write(f"**생년월일:** {birth_date}")
    st.write(f"**직군:** {job}")
    st.write(f"**PHQ-9 총점:** {total_score}점")
    st.info(f"**오늘의 감정 일기:**\n\n{diary}")

    st.markdown("### 우울 지수")
    st.progress(severity_percentage)

    st.subheader("🩺 설문 분석 결과")
    st.info(survey_summary(phq9_scores))

    with st.spinner("감정 상태 분석 및 위로 메시지를 생성하는 중... ✨"):
        analysis_result, comfort_message = analyze_diary_and_comfort(diary)

    st.subheader("💬 감정 상태 분석")
    st.info(analysis_result)

    st.subheader("💖 따뜻한 위로")
    st.success(comfort_message)

    if st.button("처음으로 돌아가기 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = "home"
        st.rerun()
