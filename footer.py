# 이 파일은 화면 하단의 제작 정보를 나타내는 함수를 정의합니다.
# footer.py

import streamlit as st
from messages import * # <-- 추가

def build_footer():
    """앱 하단 정보를 빌드합니다."""
    st.markdown("---")
    st.markdown(
        f'<p style="text-align: center; color: hotpink; font-size: 15px;">{FOOTER_TEXT}</p>', # <-- 수정
        unsafe_allow_html=True
    )
    
