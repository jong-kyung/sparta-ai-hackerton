import streamlit as st
from logic.session_manager import save_basic_info, save_survey_data

def show_survey():
    st.title("📋 기본 정보 및 PHQ-9 감정 설문")

    # 1. 기본 정보 입력
    st.markdown("## 1. 기본 정보 입력")
    name = st.text_input("이름을 입력하세요")
    birth_date = st.date_input("생년월일을 선택하세요")
    job = st.selectbox("직군을 선택하세요", ["사무직", "서비스직", "전문직", "생산직", "기타"])

    # 2. PHQ-9 검사
    st.markdown("## 2. PHQ-9 검사")
    phq9_questions = [
        "1. 최근 2주 동안 우울하거나 기분이 처진 느낌이 있었나요?",
        "2. 일상적인 활동에 대한 흥미나 즐거움이 줄어들었나요?",
        "3. 수면에 문제가 있었나요? (과도한 수면 또는 불면)",
        "4. 피곤함이나 에너지가 부족했나요?",
        "5. 식욕 변화가 있었나요?",
        "6. 자신에 대해 나쁘게 느끼거나 실패자로 느낀 적이 있었나요?",
        "7. 집중하는 데 어려움을 겪었나요?",
        "8. 느리거나 초조해 보였나요?",
        "9. 자신을 해치거나 죽이고 싶은 생각이 있었나요?"
    ]

    score_options = {"0 - 전혀 없음": 0, "1 - 가끔": 1, "2 - 종종": 2, "3 - 거의 매일": 3}
    phq9_scores = []

    for idx, question in enumerate(phq9_questions):
        st.markdown(f"**{question}**")
        selected = st.radio("", list(score_options.keys()), horizontal=True, key=f"q{idx}")
        phq9_scores.append(score_options[selected])

    if st.button("다음 단계로 ➡️"):
        if not name or not birth_date:
            st.warning("⚠️ 이름과 생년월일은 필수입니다.")
        else:
            save_basic_info(name, birth_date, job)
            save_survey_data(phq9_scores)
            st.session_state.page = "diary"
            st.rerun()
