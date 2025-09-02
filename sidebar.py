# 이 파일은 사이드바 UI를 구성하는 함수를 정의합니다.
# sidebar.py

import streamlit as st
from messages import * # <-- 추가

def build_sidebar_ui():
    """사이드바를 빌드합니다."""
    st.header(SIDEBAR_HEADER_HOWTO)
    st.markdown(SIDEBAR_GUIDE_HOWTO)

    st.markdown("---")

    st.header(SIDEBAR_HEADER_USAGE_TIPS)
    st.markdown(SIDEBAR_GUIDE_USAGE_TIPS)

    st.markdown("---")

    st.header(SIDEBAR_HEADER_SETTINGS_GUIDE)
    st.markdown(SIDEBAR_GUIDE_ERROR_CORRECTION)
    st.markdown(SIDEBAR_GUIDE_ERROR_CORRECTION_DESC)

    st.markdown(SIDEBAR_GUIDE_MASK_PATTERN)
    st.markdown(SIDEBAR_GUIDE_MASK_PATTERN_DESC)

    st.markdown(SIDEBAR_GUIDE_DOT_STYLE)
    st.markdown(SIDEBAR_GUIDE_DOT_STYLE_DESC)

    st.markdown(SIDEBAR_GUIDE_COLOR_INPUT)
    st.markdown(SIDEBAR_GUIDE_COLOR_INPUT_DESC)
    
