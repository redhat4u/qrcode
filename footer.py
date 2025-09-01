# 이 파일은 화면 하단의 제작 정보를 나타내는 함수를 정의합니다.
# footer.py

import streamlit as st

def build_footer():
    """앱 하단 정보를 빌드합니다."""
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #f08080; font-size: 15px;">© 2025 QR 코드 생성기 | Streamlit으로 제작 | 제작: 류종훈(redhat4u@gmail.com)</p>',
        unsafe_allow_html=True
    )
