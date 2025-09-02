# state_manager.py

import streamlit as st
import qrcode
from functions import (
    generate_qr_code_png,
    generate_qr_code_svg,
    is_valid_color,
)
from messages import get_message
import io

def initialize_session_state():
    """세션 상태를 초기화합니다."""
    # 언어 선택 초기화
    if 'current_lang' not in st.session_state:
        st.session_state.current_lang = 'ko'
    if 'qr_generated' not in st.session_state:
        st.session_state.qr_generated = False
    if 'qr_image_bytes' not in st.session_state:
        st.session_state.qr_image_bytes = None
    if 'qr_svg_bytes' not in st.session_state:
        st.session_state.qr_svg_bytes = None
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
        st.session_state.box_size_input = 20
    if 'border_input' not in st.session_state:
        st.session_state.border_input = 2
    if 'error_correction_select' not in st.session_state:
        st.session_state.error_correction_select = get_message('UI_ERROR_CORRECTION_LEVEL_L')
    if 'mask_pattern_select' not in st.session_state:
        st.session_state.mask_pattern_select = 2
    if 'pattern_color_select' not in st.session_state:
        st.session_state.pattern_color_select = "black"
    if 'bg_color_select' not in st.session_state:
        st.session_state.bg_color_select = "white"
    if 'strip_option' not in st.session_state:
        st.session_state.strip_option = True
    if 'file_format_select' not in st.session_state:
        st.session_state.file_format_select = get_message('UI_FILE_FORMAT_PNG')
    if 'dot_style_select' not in st.session_state:
        st.session_state.dot_style_select = get_message('UI_DOT_STYLE_SQUARE')

def set_download_initiated():
    """다운로드 버튼 클릭 시 상태를 업데이트합니다."""
    st.session_state.download_initiated = True
    
def clear_text_input():
    """텍스트 입력 필드를 초기화하는 콜백 함수입니다."""
    st.session_state.qr_input_area = ""
    generate_and_store_qr()
    
def clear_filename_callback():
    """파일명 초기화 콜백 함수입니다."""
    st.session_state.filename_input_key = ""
    generate_and_store_qr()

def reset_all_settings():
    """모든 설정을 초기화하는 콜백 함수입니다."""
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.error_correction_select = get_message('UI_ERROR_CORRECTION_LEVEL_L')
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = get_message('UI_FILE_FORMAT_PNG')
    st.session_state.dot_style_select = get_message('UI_DOT_STYLE_SQUARE')
    st.session_state.qr_generated = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.error_message = None
    
def on_qr_setting_change():
    """QR 코드 설정값 변경 시 호출됩니다."""
    generate_and_store_qr()

def on_file_format_change():
    """파일 형식 변경 시 호출됩니다."""
    generate_and_store_qr()

def generate_and_store_qr():
    """QR 코드를 생성하고 세션 상태에 저장합니다."""
    st.session_state.qr_generated = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.error_message = None

    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data

    file_format_is_svg = (st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'))
    
    is_pattern_color_valid = (st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or \
                            (st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
    is_bg_color_valid = (st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or \
                        (st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))

    if current_data:
        if not is_pattern_color_valid or not is_bg_color_valid:
            st.session_state.error_message = get_message('UI_ERROR_INVALID_QR_INPUT')
            return

        pattern_color_final = st.session_state.custom_pattern_color_input_key if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.pattern_color_select
        bg_color_final = st.session_state.custom_bg_color_input_key if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.bg_color_select

        try:
            if file_format_is_svg:
                qr_img_buffer, _ = generate_qr_code_svg(
                    data=current_data,
                    box_size=st.session_state.box_size_input,
                    border=st.session_state.border_input,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    mask_pattern=st.session_state.mask_pattern_select,
                    fill_color=pattern_color_final,
                    back_color=bg_color_final
                )
                st.session_state.qr_svg_bytes = qr_img_buffer.getvalue()
            else:
                qr_img, _ = generate_qr_code_png(
                    data=current_data,
                    box_size=st.session_state.box_size_input,
                    border=st.session_state.border_input,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    mask_pattern=st.session_state.mask_pattern_select,
                    fill_color=pattern_color_final,
                    back_color=bg_color_final,
                    dot_style=st.session_state.dot_style_select
                )
                buf = io.BytesIO()
                qr_img.save(buf, format="PNG")
                st.session_state.qr_image_bytes = buf.getvalue()

            st.session_state.qr_generated = True
        except Exception as e:
            st.session_state.qr_generated = False
            st.session_state.error_message = f"QR 코드 생성 중 오류가 발생했습니다: {e}"
            
