# 이 파일은 사이드바 UI를 구성하는 함수를 정의합니다.
# sidebar.py

import streamlit as st
from messages import get_message # <-- 이 부분을 수정했습니다.

def build_sidebar_ui():
    """사이드바를 빌드합니다."""
    
    # 언어 선택 드롭다운 메뉴
    st.sidebar.header(get_message('SIDEBAR_HEADER_LANG')) # <-- 수정
    lang_options = [get_message('LANG_KO'), get_message('LANG_EN')] # <-- 수정
    
    # 현재 선택된 언어에 따라 index를 설정
    if st.session_state.current_lang == 'ko':
        default_index = 0
    else:
        default_index = 1
        
    selected_lang = st.sidebar.selectbox(
        get_message('SELECTBOX_LANG_LABEL'), # <-- 수정
        options=lang_options,
        index=default_index,
    )

    if selected_lang == get_message('LANG_KO'):
        st.session_state.current_lang = 'ko'
    else:
        st.session_state.current_lang = 'en'
    
    st.markdown("---")

    st.header(get_message('SIDEBAR_HEADER_HOWTO')) # <-- 수정
    st.markdown(get_message('SIDEBAR_HOWTO_CONTENT')) # <-- 수정

    st.markdown("---")

    st.header(get_message('SIDEBAR_HEADER_TIPS')) # <-- 수정
    st.markdown(get_message('SIDEBAR_TIPS_CONTENT')) # <-- 수정

    st.markdown("---")
    
    st.header(get_message('SIDEBAR_HEADER_TECH_INFO')) # <-- 수정
    st.markdown(get_message('SIDEBAR_TECH_INFO_CONTENT')) # <-- 수정
