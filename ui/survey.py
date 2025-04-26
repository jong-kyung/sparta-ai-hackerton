import streamlit as st
from logic.session_manager import save_basic_info, save_survey_data
from datetime import date

def show_survey():
    st.markdown(
        """
        <style>
        /* 전체 설문 컨테이너 */
        .survey-container {
            max-width: 700px;
            margin: 40px auto;
            padding: 0 16px;
        }
        /* 카드 스타일 */
        .card {
            background: #fff;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            margin-bottom: 32px;
        }
        /* 섹션 제목 */
        .card h2, .card h3 {
            margin-top: 0;
        }
        /* 필드 컨테이너 */
        .field-container {
            margin-bottom: 20px;
        }
        /* 텍스트/데이트 입력 스타일 */
        .field-container input {
            width: 100% !important;
            padding: 12px !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: inset 0 1px 4px rgba(0,0,0,0.1) !important;
            font-size: 16px !important;
        }
        /* Radio 버튼 컨테이너 스타일 */
        .stRadio > div {
            background: #fafafa;
            padding: 12px;
            border-radius: 8px;
            box-shadow: inset 0 1px 4px rgba(0,0,0,0.05);
            margin-bottom: 16px;
        }
        /* 버튼 영역 중앙 정렬 */
        #button_container {
            text-align: center;
            margin-top: 24px;
        }
        /* 다음 버튼 스타일 */
        #button_container button {
            background-color: #4CAF50;
            color: #fff !important;
            padding: 12px 32px;
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            font-size: 16px;
            cursor: pointer;
        }
        #button_container button:hover {
            background-color: #45A049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # — 카드: 제목 & 설명
    st.title("당신의 하루와 마음을 들려주세요.")
    st.subheader("1. 기본 정보 입력")
    st.markdown("> 당신을 더 알고 싶어요. 간단한 정보를 알려주세요!")

    # — 이름 입력
    name = st.text_input("이름을 알려주세요.")

    # — 생일 입력
    birth_date = st.date_input("생일이 언제에요?", min_value=date(1960, 1, 1))

    # — 직업 입력
    job = st.text_input("무슨 일을 하고 계신가요?", placeholder="예: 개발자, 디자이너 등")

    # — PHQ-9 설문
    st.subheader("2. PHQ-9 설문 검사")
    st.markdown(
        """
        > 최근 2주 동안 당신의 마음은 어땠나요?  
        > 작은 변화라도 괜찮으니, 느낀 그대로 편하게 답해 주세요.  
        """
    )
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
    score_options = {"전혀 없음": 0, "가끔": 1, "종종": 2, "거의 매일": 3}
    phq9_scores = []
    for idx, question in enumerate(phq9_questions):
        selected = st.radio(f"**{question}**", list(score_options.keys()),
                             horizontal=True, key=f"q{idx}")
        phq9_scores.append(score_options[selected])


    invalid_name  = not name
    invalid_birth = not birth_date

    # — 버튼
    st.markdown('<div id="button_container">', unsafe_allow_html=True)
    if st.button("다음", type="primary"):
        if invalid_name or invalid_birth:
            # 필드 강조
            css = "<style>"
            if invalid_name:
                css += """
                .field-container:nth-of-type(2) input {
                    box-shadow: 0 0 0 3px rgba(226,76,76,0.6) !important;
                }"""
            if invalid_birth:
                css += """
                .field-container:nth-of-type(3) input {
                    box-shadow: 0 0 0 3px rgba(226,76,76,0.6) !important;
                }"""
            css += "</style>"
            st.markdown(css, unsafe_allow_html=True)
            st.toast("⚠️ 이름과 생년월일은 필수입니다.")
        else:
            save_basic_info(name, birth_date, job)
            save_survey_data(phq9_scores)
            st.session_state.page = "diary"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
