import streamlit as st
import time
from logic.session_manager import (
    load_user_data,
    save_analysis_result,
    save_music_link,
    load_analysis_result,
    load_music_link,
    load_dsm5_result,
    save_dsm5_result
)
from logic.survey_analyzer import survey_summary
from logic.diary_analyzer import analyze_diary_and_comfort, analyze_with_dsm5
from base64 import b64encode
from logic.alert_manager import send_alert_email  
from logic.diary_analyzer import analyze_diary  

def get_base64_gif(path):
    with open(path, "rb") as f:
        data = f.read()
    return b64encode(data).decode()

gif_base64 = get_base64_gif("assets/loading.gif")


def show_result():
    # 1) 공통 CSS 주입
    st.markdown("""
    <style>
    /* 전체 컨테이너 */
    body {
        background-color: #fdfcfc; /* AliceBlue 색상 */
    }
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
    """, unsafe_allow_html=True)

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

    # — 5) AI 분석용 GIF 플레이스홀더
    gif_placeholder = st.empty()
    has_analysis = load_analysis_result() is not None
    has_dsm5     = load_dsm5_result()     is not None

    if not (has_analysis and has_dsm5):
        # GIF 표시
        with gif_placeholder.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/gif;base64,{gif_base64}" alt="Loading..." width="100%">
        </div>
        """,
        unsafe_allow_html=True
        ):
            # 감정 상태 분석
            if not has_analysis:
                analysis_result = analyze_diary_and_comfort(diary)
                save_analysis_result(analysis_result)
            # DSM-5 전문 분석
            if not has_dsm5:
                dsm5_result = analyze_with_dsm5(diary, phq9_scores)
                save_dsm5_result(dsm5_result)
        # GIF 제거
        gif_placeholder.empty()

    # 6) 분석 결과 불러오기
    analysis_result = load_analysis_result()
    dsm5_result      = load_dsm5_result()

    # — 7) 감정 상태 분석 표시
    st.subheader("💬 감정 상태 분석")
    st.info(analysis_result)

    # — 8) DSM-5 전문 분석 표시
    if "error" in dsm5_result and dsm5_result["error"]:
        st.error(dsm5_result["error"])
    else:
        severity       = dsm5_result.get("severity", "분석 불가")
        positive_count = dsm5_result.get("positive_symptoms_count", 0)
        st.markdown(f"""
        <div style="padding: 12px; border-radius: 6px; background-color: #e0f7fa;">
          <strong>DSM-5 분석 결과:</strong> {severity}  
          (감지 증상 {positive_count} / 9)
        </div>
        """, unsafe_allow_html=True)

        if dsm5_result.get("professional_opinion"):
            st.markdown("#### 전문가 의견")
            st.info(dsm5_result["professional_opinion"])
        if dsm5_result.get("recommendation"):
            st.markdown("#### 권장사항")
            st.success(dsm5_result["recommendation"])

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

        st.caption(dsm5_result.get(
            "disclaimer",
            "이 분석은 참고용입니다. 정확한 진단은 전문가와 상담하세요."
        ))

    st.markdown("---")

    # — 9) 이메일 입력 및 전송
    st.subheader("이메일을 알려주세요.")
    receiver_email = st.text_input(
        "✉️ 당신을 위한 작은 위로와 음악을 준비했어요. 이메일로 받아보고 싶다면 알려주세요.",
        placeholder="이메일 주소를 입력하세요."
    )

    if st.button("이메일 전송하기", type="primary"):
        if not diary or not receiver_email.strip():
            st.warning("⚠️ 감정 일기와 이메일 주소를 모두 입력해주세요.")
        else:
            if load_music_link() is None:
                with st.spinner("음악 추천 링크를 생성하는 중... 🎶"):
                    comfort_msg, music_link = analyze_diary(diary)
                    save_music_link(music_link)
            music_link = load_music_link()

            email_subject = "🎵 당신의 감정에 어울리는 음악 추천입니다!"
            email_body = f"""
                <div style="font-family: Arial, sans-serif; background-color: #fff8f0; 
                            padding: 20px; border-radius: 10px; line-height: 1.6;">
                    <h3 style="color: #ff8c94;">💖 따뜻한 위로</h3>
                    <p style="font-size: 16px; color: #555;">{comfort_msg}</p>
                    <h3 style="color: #6a5acd;">🎵 추천 음악 링크</h3>
                    <p style="font-size: 16px;">
                        <a href="{music_link}" 
                           style="text-decoration: none; color: #1e90ff;">
                           👉 여기서 음악 듣기 🎶
                        </a>
                    </p>
                </div>
            """

            st.markdown("### 🎵 지금 바로 음악 감상하기")
            if "youtube.com" in music_link or "youtu.be" in music_link:
                st.video(music_link)
            elif music_link.endswith((".mp3", ".wav")):
                st.audio(music_link)
            else:
                st.info(f"[👉 추천 음악 링크로 이동하기 🎶]({music_link})")

            time.sleep(10)
            with st.spinner("이메일 전송 중... 📧"):
                success = send_alert_email(email_subject, email_body,receiver_email)

            if success:
                st.toast(f"✅ 이메일이 {receiver_email}로 성공적으로 전송되었습니다!")
                st.balloons()

    st.markdown("---")

    # — 10) 다시 시작 버튼
    if st.button("처음으로 돌아가기"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state.page = "home"
        st.rerun()
