# 이 파일은 Streamlit의 session_state를 관리하여 앱의 상태를 제어합니다.
# state_manager.py

import streamlit as st
import qrcode
from messages import get_message, get_current_language

def initialize_session_state_with_language():
    """언어 설정을 고려하여 세션 상태를 초기화합니다."""
    # 언어에 따라 동적으로 메시지 설정
    current_lang = get_current_language()
    
    if "is_initialized" not in st.session_state or st.session_state.current_language != current_lang:
        st.session_state.is_initialized = True
        st.session_state.current_language = current_lang
        
        # QR 코드 입력 및 설정
        st.session_state.qr_input_area = ""
        st.session_state.strip_option = True
        st.session_state.box_size_input = 20
        st.session_state.border_input = 2
        st.session_state.mask_pattern_select = 7
        st.session_state.pattern_color_select = "black"
        st.session_state.bg_color_select = "white"
        st.session_state.custom_pattern_color_input_key = ""
        st.session_state.custom_bg_color_input_key = ""
        st.session_state.dot_style_select = get_message('UI_DOT_STYLE_SQUARE')
        st.session_state.file_format_select = get_message('UI_FILE_FORMAT_PNG')
        st.session_state.filename_input_key = ""
        st.session_state.error_correction_select = get_message('UI_ERROR_CORRECTION_LEVEL_M')
        
        # UI 상태
        st.session_state.qr_image_bytes = None
        st.session_state.qr_svg_bytes = None
        st.session_state.qr_generated = False
        st.session_state.error_message = None
        st.session_state.generate_button_clicked = False
        st.session_state.show_generate_success = False
        st.session_state.download_initiated = False

def clear_text_input():
    """QR 코드 내용 입력창을 초기화합니다."""
    st.session_state.qr_input_area = ""

def clear_filename_callback():
    """파일명 입력창을 초기화합니다."""
    st.session_state.filename_input_key = ""

def on_qr_setting_change():
    """QR 코드 설정 변경 시 미리보기를 새로고침합니다."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False

def on_file_format_change():
    """파일 형식 변경 시 상태를 재설정합니다."""
    on_qr_setting_change()
    if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
        st.session_state.pattern_color_select = "black"
        st.session_state.bg_color_select = "white"

def set_download_initiated():
    """다운로드 버튼 클릭 시 다운로드 완료 메시지 표시를 위한 상태를 설정합니다."""
    st.session_state.download_initiated = True

def reset_all_settings():
    """모든 설정을 초기 상태로 재설정합니다."""
    st.session_state.is_initialized = False
    # 언어 재설정 후 다시 초기화 함수 호출
    initialize_session_state_with_language()
    
