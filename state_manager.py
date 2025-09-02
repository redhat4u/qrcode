# state_manager.py

import streamlit as st
import qrcode
from messages import get_message, MESSAGES

def initialize_session_state_with_language():
    """언어에 따라 세션 상태를 초기화하고 기본값을 설정합니다."""
    # 언어 선택 드롭다운은 항상 존재해야 하므로 여기에 정의합니다.
    if 'language_select' not in st.session_state:
        st.session_state.language_select = MESSAGES['ko']['UI_LANG_SELECT_OPTIONS'][0] # 기본값 '한국어'
    
    # 언어에 따라 동적으로 메시지 함수를 업데이트합니다.
    st.session_state.current_language = 'ko' if st.session_state.language_select == '한국어' else 'en'
    
    # 다른 세션 상태 변수들이 초기화되지 않았다면 설정합니다.
    if 'qr_input_area' not in st.session_state:
        st.session_state.qr_input_area = ""
    if 'strip_option' not in st.session_state:
        st.session_state.strip_option = True
    if 'error_correction_select' not in st.session_state:
        st.session_state.error_correction_select = get_message('UI_ERROR_CORRECTION_LEVEL_H')
    if 'box_size_input' not in st.session_state:
        st.session_state.box_size_input = 20
    if 'border_input' not in st.session_state:
        st.session_state.border_input = 2
    if 'pattern_color_select' not in st.session_state:
        st.session_state.pattern_color_select = 'black'
    if 'bg_color_select' not in st.session_state:
        st.session_state.bg_color_select = 'white'
    if 'custom_pattern_color_input_key' not in st.session_state:
        st.session_state.custom_pattern_color_input_key = ""
    if 'custom_bg_color_input_key' not in st.session_state:
        st.session_state.custom_bg_color_input_key = ""
    if 'dot_style_select' not in st.session_state:
        st.session_state.dot_style_select = get_message('UI_DOT_STYLE_SQUARE')
    if 'filename_input_key' not in st.session_state:
        st.session_state.filename_input_key = ""
    if 'file_format_select' not in st.session_state:
        st.session_state.file_format_select = get_message('UI_FILE_FORMAT_PNG')
    if 'qr_generated' not in st.session_state:
        st.session_state.qr_generated = False
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'download_initiated' not in st.session_state:
        st.session_state.download_initiated = False
    if 'show_generate_success' not in st.session_state:
        st.session_state.show_generate_success = False
    if 'generate_button_clicked' not in st.session_state:
        st.session_state.generate_button_clicked = False
    if 'qr_image_bytes' not in st.session_state:
        st.session_state.qr_image_bytes = None
    if 'qr_svg_bytes' not in st.session_state:
        st.session_state.qr_svg_bytes = None
    # 마스크 패턴을 세션 상태에 추가
    if 'mask_pattern_select' not in st.session_state:
        st.session_state.mask_pattern_select = 0

def on_qr_setting_change():
    """QR 설정 변경 시 미리보기 업데이트를 위한 플래그를 리셋합니다."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False

def on_file_format_change():
    """파일 형식 변경 시 상태를 업데이트합니다."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.download_initiated = False
    
def clear_text_input():
    """입력 내용을 지웁니다."""
    st.session_state.qr_input_area = ""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False

def clear_filename_callback():
    """파일명을 지웁니다."""
    st.session_state.filename_input_key = ""
    st.session_state.qr_generated = False

def set_download_initiated():
    """다운로드 버튼 클릭 시 상태를 변경합니다."""
    st.session_state.download_initiated = True

def reset_all_settings():
    """
    모든 설정을 초기 상태로 되돌립니다.
    언어 선택 시 호출됩니다.
    """
    # 언어 선택 상태만 유지
    lang_select = st.session_state.get('language_select', '한국어')
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.session_state.language_select = lang_select
    # 초기화 후 다시 기본 상태를 설정
    initialize_session_state_with_language()
    
    st.rerun()
    
