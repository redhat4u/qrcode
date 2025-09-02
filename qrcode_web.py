# 이 파일은 앱의 전체적인 구조를 담당하는 메인 실행 파일이며,
# 다른 파일의 함수를 불러와서 화면을 구성합니다.
# qrcode_web.py

import streamlit as st
import qrcode
from datetime import datetime
from zoneinfo import ZoneInfo

# 분리된 파일에서 함수 불러오기
from state_manager import (
    initialize_session_state,
    reset_all_settings,
    clear_text_input,
    clear_filename_callback,
    on_qr_setting_change,
    set_download_initiated,
)

from functions import (
    sanitize_filename,
    is_valid_color,
    generate_qr_code_png,
    generate_qr_code_svg,
)

from ui_input_and_settings import build_input_and_settings_ui
from ui_preview_and_download import build_preview_and_download_ui
from sidebar import build_sidebar_ui
from footer import build_footer
from messages import *

# 페이지 설정
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔲",
    layout="wide",
)

# 세션 상태 초기화
initialize_session_state()

# 메인 앱 헤더
st.title(APP_TITLE)
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col_left, col_right = st.columns([1, 1], gap="medium") 

# 사이드바
with st.sidebar:
    build_sidebar_ui()
    st.markdown("---")
# 이전 턴에서 여기에 있던 초기화 버튼 코드를 아래로 이동했습니다.

# 메인 UI
with col_left:
    build_input_and_settings_ui()
    # ⏪ 모든 설정 초기화 버튼을 이곳으로 다시 이동
    st.markdown("---")
    if st.button("⏪ 모든 설정 초기화", use_container_width=True, type="secondary", on_click=reset_all_settings):
        st.session_state.show_generate_success = False

with col_right:
    build_preview_and_download_ui()
    
# 푸터
build_footer()
