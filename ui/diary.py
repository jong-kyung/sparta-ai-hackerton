import streamlit as st
from logic.session_manager import save_diary_entry

def show_diary():
    st.markdown(
    """
    <style>
    body {
        background-color: #fdfcfc; /* AliceBlue 색상 */
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.title("감정 일기")
    st.markdown(
    """
    > 오늘, 당신의 마음은 어땠나요?
    > 편하게 떠오르는 `생각`이나 `감정`을 적어주세요.
    """
    )

    diary_entry = st.text_area("", height=300)

    if st.button("저장", type="primary"):
        if not diary_entry.strip():
            st.toast("⚠️ 당신의 이야기를 들려주세요.")
        else:
            save_diary_entry(diary_entry)
            st.session_state.page = "result"
            st.rerun()
