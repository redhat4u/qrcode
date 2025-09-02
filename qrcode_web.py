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
from messages import get_message

# 세션 상태 초기화
initialize_session_state()

def on_lang_change_callback():
    """언어 변경 시 호출되는 콜백 함수입니다."""
    lang_options = [get_message('LANG_KO'), get_message('LANG_EN')]
    selected_lang = st.session_state.lang_select_box
    
    if selected_lang == lang_options[0]:
        st.session_state.current_lang = 'ko'
    else:
        st.session_state.current_lang = 'en'
    
    # QR 코드 미리보기 및 기타 설정을 초기화하여 UI를 갱신
    on_qr_setting_change()

# 페이지 설정
st.set_page_config(
    page_title=get_message('APP_TITLE'),
    page_icon="🔲",
    layout="wide",
)

# 메인 앱 헤더
st.title("🔲 " + get_message('APP_TITLE'))

# 언어 선택 드롭다운 메뉴
lang_options = [get_message('LANG_KO'), get_message('LANG_EN')]
if st.session_state.current_lang == 'ko':
    default_index = 0
else:
    default_index = 1
    
st.selectbox(
    get_message('SELECTBOX_LANG_LABEL'),
    options=lang_options,
    index=default_index,
    key='lang_select_box',
    on_change=on_lang_change_callback
)
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col_input, col_preview = st.columns([1.5, 1])

with col_input:
    build_input_and_settings_ui()
with col_preview:
    build_preview_and_download_ui()

# 사이드바 UI 빌드
with st.sidebar:
    build_sidebar_ui()

# 푸터 빌드
build_footer()
