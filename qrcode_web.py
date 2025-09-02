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
    set_lang_ko, # 추가
    set_lang_en, # 추가
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
from messages import get_message # get_message 함수만 가져오도록 수정

# 페이지 설정
st.set_page_config(
    page_title=get_message('APP_TITLE'), # 수정
    page_icon="🔲",
    layout="wide",
)

# 세션 상태 초기화
initialize_session_state()

# 메인 앱 헤더
header_col1, header_col2, header_col3 = st.columns([10, 1, 1])
with header_col1:
    st.title(get_message('APP_MAIN_HEADER')) # 수정
with header_col2:
    st.button("🇰🇷", key="lang_ko", on_click=set_lang_ko)
with header_col3:
    st.button("🇺🇸", key="lang_en", on_click=set_lang_en)

st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

# 각 섹션의 UI를 별도의 함수로 분리하여 호출
with col1:
    build_input_and_settings_ui()
with col2:
    build_preview_and_download_ui()

# 전체 초기화 버튼
st.markdown("---")
st.button(
    label=get_message('APP_RESET_BUTTON_LABEL'), # 수정
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help=get_message('APP_RESET_BUTTON_HELP'), # 수정
)

# 사이드바를 별도 파일에서 만든 함수로 호출
with st.sidebar:
    build_sidebar_ui()

# 하단 정보
build_footer()
