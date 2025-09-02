# footer.py

import streamlit as st
from messages import get_message # FOOTER_MESSAGE 대신 get_message 함수만 가져옵니다.

def build_footer():
    """앱 하단 정보를 빌드합니다."""
    st.markdown("---")
    footer_message_text = get_message('FOOTER_MESSAGE')
    st.markdown(
        f'<p style=\"text-align: center; color: hotpink; font-size: 15px;\"> {footer_message_text} </p>',
        unsafe_allow_html=True
    )
    
