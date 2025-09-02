# 이 파일은 사이드바 UI를 구성하는 함수를 정의합니다.
# sidebar.py

import streamlit as st
from messages import * # <-- 추가

def build_sidebar_ui():
    """사이드바를 빌드합니다."""
    st.header(SIDEBAR_HEADER_HOWTO) # <-- 수정
    st.markdown(SIDEBAR_INSTRUCTIONS) # <-- 수정

    st.markdown("---")

    st.header(SIDEBAR_HEADER_TIPS) # <-- 수정
    st.markdown(SIDEBAR_TIPS) # <-- 수정
    
    st.markdown("---")

    st.header("⚙️ 참고 사항")
    st.markdown("- QR 코드 생성에 문제가 있으면, 새로고침 후 다시 시도해주세요.")
    st.markdown("- 문자열이 길어지면 QR 코드의 복잡도가 높아져서 인식률이 낮아질 수 있습니다. 간결하게 작성해주세요.")
    
