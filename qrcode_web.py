# 이 파일은 QR 코드 생성 웹 앱의 메인 진입점입니다.
# qrcode_web.py

import streamlit as st
import qrcode
from messages import get_message
from state_manager import (
    initialize_session_state_with_language,
    on_qr_setting_change,
    on_file_format_change,
    reset_all_settings,
    set_download_initiated,
)
from ui_input_and_settings import build_input_and_settings_ui
from ui_preview_and_download import build_preview_and_download_ui

# --- Streamlit Functions ---
def build_footer_ui():
    """앱의 푸터 섹션을 빌드합니다."""
    st.markdown("---")
    st.markdown(
        """
        <style>
        .footer {
            font-size: 0.8rem;
            text-align: center;
            color: #808080;
            padding-top: 20px;
        }
        </style>
        <div class="footer">
            <p>개발자: [여기에 개발자 이름 또는 이메일] | 버전 1.0.0</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- Main Page Configuration ---
st.set_page_config(
    page_title=get_message("APP_TITLE"),
    page_icon="✍️",
    layout="wide",
)

# 세션 상태 초기화 (최상단에서 호출)
initialize_session_state_with_language()

# 사이드바
with st.sidebar:
    st.header(get_message("UI_SIDEBAR_HEADER_GUIDE"))
    st.markdown(get_message("UI_SIDEBAR_GUIDE_CONTENT"))
    st.markdown("---")
    st.header(get_message("UI_SIDEBAR_HEADER_TIPS"))
    st.markdown(get_message("UI_SIDEBAR_TIPS_CONTENT"))
    st.markdown("---")
    st.header(get_message("UI_SIDEBAR_HEADER_SETTINGS_GUIDE"))
    st.markdown(get_message("UI_SIDEBAR_SETTINGS_GUIDE_CONTENT"))

# 메인 UI
st.title(get_message("APP_TITLE"))
# 언어 선택 드롭다운을 메인 화면 타이틀 아래에 배치합니다.
st.selectbox(
    get_message('UI_LANG_SELECT_LABEL'),
    options=get_message('UI_LANG_SELECT_OPTIONS'),
    key='language_select',
    on_change=reset_all_settings
)
st.markdown("---")

# 메인 화면을 2개의 열로 나누어 설정 부분과 미리보기를 5:5로 배치합니다.
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # 입력 및 설정 섹션
    build_input_and_settings_ui()

with col2:
    # 미리보기 및 다운로드 섹션
    build_preview_and_download_ui()

# 푸터 섹션 호출
build_footer_ui()
