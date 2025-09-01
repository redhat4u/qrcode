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


# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔲",
    layout="wide",
)

# 세션 상태 초기화
initialize_session_state()

# 메인 앱 헤더
st.title("🔲 QR 코드 생성기")
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

# 각 섹션의 UI를 별도의 함수로 분리하여 호출
with col1:
    build_input_and_settings_ui() # <-- 함수 이름 변경
with col2:
    build_preview_and_download_ui()

# 전체 초기화 버튼
st.markdown("---")
st.button(
    label="🔄 전체 초기화",
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help="모든 내용을 초기화 합니다.",
)

# 사이드바를 별도 파일에서 만든 함수로 호출
with st.sidebar:
    build_sidebar_ui()

# 하단 정보
build_footer()
