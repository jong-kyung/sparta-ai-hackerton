import streamlit as st
import openai
import os
from dotenv import load_dotenv
from logic.session_manager import load_user_data
from logic.survey_analyzer import survey_summary
from logic.diary_analyzer import analyze_diary_and_comfort, analyze_with_dsm5

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
    
    # DSM-5 기반 전문 분석 추가
    st.subheader("🔬 DSM-5 전문 분석")
    with st.spinner("DSM-5 진단 기준에 따른 전문 분석 중... 🧠"):
        dsm5_result = analyze_with_dsm5(diary, phq9_scores)
    
    if "error" in dsm5_result and dsm5_result["error"]:
        st.error(dsm5_result["error"])
    else:
        # 종합 분석 결과 표시
        severity = dsm5_result.get("severity", "분석 불가")
        positive_count = dsm5_result.get("positive_symptoms_count", 0)
        
        # 심각도에 따른 색상 설정
        severity_color = "#4CAF50"  # 초록색 (기본)
        if "가벼운" in severity:
            severity_color = "#8BC34A"  # 연두색
        elif "중등도" in severity and "심한" not in severity:
            severity_color = "#FFC107"  # 노란색
        elif "중등도-심한" in severity:
            severity_color = "#FF9800"  # 주황색
        elif "심한" in severity:
            severity_color = "#F44336"  # 빨간색
            
        # 심각도 표시
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; background-color: {severity_color}20; margin-bottom: 20px;">
            <h4 style="color: {severity_color}; margin-top: 0;">DSM-5 분석 결과: {severity}</h4>
            <p>9가지 주요 증상 중 <b>{positive_count}가지</b> 증상이 감지되었습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 전문가 의견 표시
        if "professional_opinion" in dsm5_result and dsm5_result["professional_opinion"]:
            st.markdown("#### 전문가 의견")
            st.info(dsm5_result["professional_opinion"])
        
        # 권장사항 표시
        if "recommendation" in dsm5_result and dsm5_result["recommendation"]:
            st.markdown("#### 권장사항")
            st.success(dsm5_result["recommendation"])
        
        # 증상 세부 분석 결과 표시 (확장 패널로)
        with st.expander("DSM-5 증상 세부 분석"):
            if "symptom_analysis" in dsm5_result:
                symptom_analysis = dsm5_result["symptom_analysis"]
                for symptom, details in symptom_analysis.items():
                    present = details.get("present", False)
                    evidence = details.get("evidence", "")
                    severity = details.get("severity", "")
                    
                    # 증상 존재 여부에 따른 아이콘 설정
                    icon = "✅" if present else "❌"
                    
                    # 심각도에 따른 색상 설정
                    color = "#808080"  # 회색 (기본)
                    if severity == "경미함":
                        color = "#8BC34A"  # 연두색
                    elif severity == "중간":
                        color = "#FFC107"  # 노란색
                    elif severity == "심각함":
                        color = "#F44336"  # 빨간색
                    
                    # 증상 표시
                    st.markdown(f"""
                    <div style="margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #eee;">
                        <h5 style="margin-bottom: 5px;">
                            {icon} {symptom} {f'<span style="color: {color};">({severity})</span>' if present and severity else ''}
                        </h5>
                        {f'<p style="margin-top: 5px; font-style: italic;">"{evidence}"</p>' if evidence else ''}
                    </div>
                    """, unsafe_allow_html=True)
        
        # 면책 조항
        st.caption(dsm5_result.get("disclaimer", "이 분석은 참고용으로만 사용하세요. 정확한 진단은 전문가와 상담하세요."))

    if st.button("처음으로 돌아가기 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = "home"
        st.rerun()
