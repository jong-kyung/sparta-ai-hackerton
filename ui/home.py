import streamlit as st
import base64
from pathlib import Path

def get_base64_of_bin_file(path):
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode()


def show_home():
    # 1) 공통 CSS 주입
    st.markdown("""
    <style>
    /* 전체 래퍼 */
    .home-wrapper {
        max-width: 820px;
        margin: 40px auto;
        padding: 0 20px;
    }
    /* 그라데이션 헤더 카드 */
    .hero-card {
        background: linear-gradient(135deg, #6A11CB, #2575FC);
        border-radius: 14px;
        color: #fff !important;
        padding: 40px 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 32px;
    }
    .hero-card h1 {
        font-size: 2.8rem;
        margin-bottom: 8px;
    }
    .hero-card h2 {
        font-size: 1.25rem;
        font-weight: 300;
    }
    /* 소개 카드 */
    .features-card {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 20px;
        margin-bottom: 32px;
    }
    .feature {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        transition: transform .2s;
    }
    .feature:hover {
        transform: translateY(-4px);
    }
    .feature h3 {
        margin-top: 0;
        font-size: 1.1rem;
        color: #333;
    }
    .feature p {
        margin: 8px 0 0;
        color: #555;
        line-height: 1.4;
    }
    /* 시작 버튼 */
    .start-btn {
        text-align: center;
        margin-bottom: 40px;
    }
    .start-btn button {
        background: #2575FC;
        color: #fff !important;
        padding: 14px 40px;
        font-size: 1.1rem;
        border: none;
        border-radius: 8px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: background .2s, transform .2s;
    }
    .start-btn button:hover {
        background: #1a5fd1;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)


    HOME_LOGO = "assets/logo.png"


    # 1) 로고를 Base64로 읽어서 HTML로 인라인 임베드
    logo_b64 = get_base64_of_bin_file(HOME_LOGO)
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        ">
            <img src="data:image/png;base64,{logo_b64}" 
                 style="width:180px; height:auto; margin-right:12px;" />
            <h1 style="margin:0; font-size:2.5rem; line-height:1;">
                마인드 닥터
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.subheader("당신의 마음을 돌보는 스마트 감정 관리 서비스")

    # — 주요 기능 카드 그리드
    st.markdown('<div class="features-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="feature">
      <h3>🩺 PHQ-9 설문</h3>
      <p>간단한 9문항으로 나의 정신 건강 상태를 빠르게 체크할 수 있어요.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature">
      <h3>📝 감정 일기</h3>
      <p>오늘의 감정을 자유롭게 기록하여, 나만의 심리 로그를 만들어보세요.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature">
      <h3>🤖 AI 분석</h3>
      <p>일기와 설문 데이터를 AI가 분석하여, 맞춤형 인사이트를 제공합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature">
      <h3>🚨 위험 신호 알림</h3>
      <p>고위험 신호 감지 시, 즉각적인 대응 가이드를 안내합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # — 시작 버튼
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    if st.button("지금 내 마음 살펴보기 🌸"):
        st.session_state.page = "survey"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

