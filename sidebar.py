# sidebar.py

import streamlit as st
from messages import get_message

def build_sidebar_ui():
    """사이드바를 빌드합니다."""
    
    # 언어 선택 드롭다운 메뉴
    st.sidebar.header(get_message('SIDEBAR_HEADER_LANG'))
    lang_options = [get_message('LANG_KO'), get_message('LANG_EN')]
    
    # 현재 선택된 언어에 따라 index를 설정
    if st.session_state.current_lang == 'ko':
        default_index = 0
    else:
        default_index = 1
        
    selected_lang = st.sidebar.selectbox(
        get_message('SELECTBOX_LANG_LABEL'),
        options=lang_options,
        index=default_index,
    )

    if selected_lang == get_message('LANG_KO'):
        st.session_state.current_lang = 'ko'
    else:
        st.session_state.current_lang = 'en'
    
    st.markdown("---")

    st.header(get_message('SIDEBAR_HEADER_HOWTO'))
    st.markdown(get_message('SIDEBAR_HOWTO_CONTENT'))

    st.markdown("---")

    st.header(get_message('SIDEBAR_HEADER_TIPS'))
    st.markdown(get_message('SIDEBAR_TIPS_CONTENT'))

    st.markdown("---")
    
    st.header(get_message('SIDEBAR_HEADER_TECH_INFO'))
    st.markdown(get_message('SIDEBAR_TECH_INFO_CONTENT'))
    
