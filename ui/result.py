import streamlit as st
import streamlit.components.v1 as components
import openai
import os
from dotenv import load_dotenv
from logic.session_manager import load_user_data
from logic.survey_analyzer import survey_summary
from logic.diary_analyzer import analyze_diary_and_comfort, analyze_with_dsm5
from datetime import date

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def show_result():
    # 1) 공통 CSS 주입
    st.markdown(
        """
        <style>
        /* 전체 컨테이너 */
        .result-container {
            max-width: 800px;
            margin: 0 auto 40px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 12px;
        }
        /* 섹션 카드 스타일 */
        .card {
            background: #fff;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 24px;
        }
        /* 헤더 중앙 정렬 */
        .header h1, .header p {
            text-align: center;
            margin: 4px 0;
        }
        /* 컬럼 간격 */
        .stColumns > div {
            padding: 0 8px;
        }
        /* Progress 바 색상 재정의 */
        .stProgress > div > div > div > div {
            background-color: #4CAF50 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # — 2) 헤더
    st.title("📈 감정 분석 결과")
    st.markdown(
        """
        > 당신은 현재 어떤 감정을 느끼고 있나요?  
        > 오늘의 감정 일기를 통해 당신의 마음을 들여다보세요.
        """
    )

    # — 3) 사용자 기본 정보 및 우울 지수 (컬럼)
    user_data = load_user_data()
    if not user_data:
        st.toast("입력된 데이터가 없습니다. 처음부터 다시 시작해주세요.")
        st.session_state.page = "home"
        st.rerun()

    name        = user_data["name"]
    birth_date  = user_data["birth_date"]
    job         = user_data["job"]
    phq9_scores = user_data["phq9_scores"]
    diary       = user_data["diary"]

    total_score  = sum(phq9_scores)
    severity_pct = int((total_score / 27) * 100)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("👤 나의 정보")
        st.write(f"- **이름:** {name}")
        st.write(f"- **생년월일:** {birth_date}")
        st.write(f"- **직군:** {job}")

    with col2:
        st.subheader("🧮 PHQ-9 지수")
        st.metric("총점", f"{total_score} / 27")
        st.progress(severity_pct)

    # — 4) 설문 분석 결과
    st.subheader("🩺 설문 분석 결과")
    st.info(survey_summary(phq9_scores))

    # — 5) 일기 기반 감정 상태 분석
    with st.spinner("감정 상태 분석 및 위로 메시지를 생성하는 중... ✨"):
        analysis_result, comfort_message = analyze_diary_and_comfort(diary)
    st.subheader("💬 감정 상태 분석")
    st.info(analysis_result)

    # — 6) DSM-5 전문 분석
    st.subheader("🔬 DSM-5 전문 분석")
    with st.spinner("DSM-5 진단 기준에 따른 전문 분석 중... 🧠"):
        dsm5_result = analyze_with_dsm5(diary, phq9_scores)

    if dsm5_result.get("error"):
        st.error(dsm5_result["error"])
    else:
        # 종합 분석 결과 표시 (간단한 카드)
        severity       = dsm5_result.get("severity", "분석 불가")
        positive_count = dsm5_result.get("positive_symptoms_count", 0)
        st.markdown(f"""
        <div style="padding: 12px; border-radius: 6px; background-color: #e0f7fa;">
          <strong>DSM-5 분석 결과:</strong> {severity}  
          (감지 증상 {positive_count} / 9)
        </div>
        """, unsafe_allow_html=True)

        # 전문가 의견
        if dsm5_result.get("professional_opinion"):
            st.markdown("#### 전문가 의견")
            st.info(dsm5_result["professional_opinion"])

        # 권장사항
        if dsm5_result.get("recommendation"):
            st.markdown("#### 권장사항")
            st.success(dsm5_result["recommendation"])

        # 증상 세부 분석 (확장 패널)
        with st.expander("DSM-5 증상 세부 분석"):
            for symptom, details in dsm5_result.get("symptom_analysis", {}).items():
                present  = details.get("present", False)
                evidence = details.get("evidence", "")
                sev      = details.get("severity", "")
                icon     = "✅" if present else "❌"
                color    = "#808080"
                if sev == "경미함":
                    color = "#8BC34A"
                elif sev == "중간":
                    color = "#FFC107"
                elif sev == "심각함":
                    color = "#F44336"

                st.markdown(f"""
                <div style="margin-bottom:10px;">
                  <strong style="color:{color};">{icon} {symptom} {f'({sev})' if present else ''}</strong><br>
                  <em>{evidence}</em>
                </div>
                """, unsafe_allow_html=True)

        # 면책 조항
        st.caption(dsm5_result.get(
            "disclaimer",
            "이 분석은 참고용입니다. 정확한 진단은 전문가와 상담하세요."
        ))


    # — 7) 따뜻한 위로
    st.subheader("💖 따뜻한 위로")
    st.success(comfort_message)

    # — 8) 다시 시작 버튼
    if st.button("처음으로 돌아가기"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state.page = "home"
        st.rerun()


