# 이 파일은 st.session_state 상태를 관리하고,
# 사용자 상호 작용에 따라 호출되는 콜백 함수들을 정의합니다.
# state_manager.py

import streamlit as st
import qrcode
import hashlib
from messages import *

def initialize_session_state():
    """세션 상태를 초기화합니다."""
    if 'current_lang' not in st.session_state:
        st.session_state.current_lang = 'ko' # 기본 언어는 한국어

    if 'download_initiated' not in st.session_state:
        st.session_state.download_initiated = False
    if 'show_generate_success' not in st.session_state:
        st.session_state.show_generate_success = False
    if 'qr_generated' not in st.session_state:
        st.session_state.qr_generated = False
    if 'qr_image_bytes' not in st.session_state:
        st.session_state.qr_image_bytes = None
    if 'qr_svg_bytes' not in st.session_state:
        st.session_state.qr_svg_bytes = None
    if 'generate_button_clicked' not in st.session_state:
        st.session_state.generate_button_clicked = False
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'qr_input_area' not in st.session_state:
        st.session_state.qr_input_area = ""
    if 'custom_pattern_color_input_key' not in st.session_state:
        st.session_state.custom_pattern_color_input_key = ""
    if 'custom_bg_color_input_key' not in st.session_state:
        st.session_state.custom_bg_color_input_key = ""
    if 'filename_input_key' not in st.session_state:
        st.session_state.filename_input_key = ""
    if 'box_size_input' not in st.session_state:
        st.session_state.box_size_input = UI_DEFAULT_BOX_SIZE
    if 'border_input' not in st.session_state:
        st.session_state.border_input = UI_DEFAULT_BORDER
    if 'error_correction_select' not in st.session_state:
        st.session_state.error_correction_select = UI_DEFAULT_ERROR_CORRECTION
    if 'mask_pattern_select' not in st.session_state:
        st.session_state.mask_pattern_select = UI_DEFAULT_MASK_PATTERN
    if 'pattern_color_select' not in st.session_state:
        st.session_state.pattern_color_select = UI_DEFAULT_PATTERN_COLOR
    if 'bg_color_select' not in st.session_state:
        st.session_state.bg_color_select = UI_DEFAULT_BG_COLOR
    if 'strip_option' not in st.session_state:
        st.session_state.strip_option = UI_DEFAULT_STRIP_OPTION
    if 'file_format_select' not in st.session_state:
        st.session_state.file_format_select = UI_FILE_FORMAT_PNG
    if 'dot_style_select' not in st.session_state:
        st.session_state.dot_style_select = UI_DEFAULT_DOT_STYLE

def set_download_initiated():
    """다운로드 버튼 클릭 상태를 True로 설정하는 콜백 함수입니다."""
    st.session_state.download_initiated = True

def clear_text_input():
    """입력 내용 초기화 콜백 함수입니다."""
    st.session_state.qr_input_area = ""
    # 입력 내용 삭제 시 다운로드 및 생성 상태도 초기화
    st.session_state.download_initiated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_generated = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.error_message = None

def clear_filename_callback():
    """파일명 초기화 콜백 함수입니다."""
    st.session_state.filename_input_key = ""

def reset_all_settings():
    """모든 설정을 초기화하는 콜백 함수입니다."""
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    st.session_state.box_size_input = UI_DEFAULT_BOX_SIZE
    st.session_state.border_input = UI_DEFAULT_BORDER
    st.session_state.error_correction_select = UI_DEFAULT_ERROR_CORRECTION
    st.session_state.mask_pattern_select = UI_DEFAULT_MASK_PATTERN
    st.session_state.pattern_color_select = UI_DEFAULT_PATTERN_COLOR
    st.session_state.bg_color_select = UI_DEFAULT_BG_COLOR
    st.session_state.strip_option = UI_DEFAULT_STRIP_OPTION
    st.session_state.file_format_select = UI_FILE_FORMAT_PNG
    st.session_state.dot_style_select = UI_DEFAULT_DOT_STYLE
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False
    st.session_state.error_message = None

def on_qr_setting_change():
    """QR 코드 설정값 변경 시 다운로드 관련 상태를 초기화합니다."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False
    st.session_state.error_message = None

def on_file_format_change():
    """파일 형식 변경 시 상태를 초기화합니다."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False
    st.session_state.error_message = None

def set_lang_ko():
    """언어를 한국어로 변경하는 콜백 함수입니다."""
    st.session_state.current_lang = 'ko'

def set_lang_en():
    """언어를 영어로 변경하는 콜백 함수입니다."""
    st.session_state.current_lang = 'en'
    
