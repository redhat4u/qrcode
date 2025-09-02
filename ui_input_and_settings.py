# 이 파일은 QR 코드 생성에 필요한 입력 및 설정 UI를 정의합니다.
# ui_input_and_settings.py

import streamlit as st
import qrcode
from functions import (
    sanitize_filename,
    is_valid_color,
)
from state_manager import (
    clear_text_input,
    clear_filename_callback,
    on_qr_setting_change,
    on_file_format_change, # <-- 추가
)
from messages import * # <-- 추가

def build_input_and_settings_ui():
    """입력 및 설정 섹션을 빌드합니다."""
    st.header(UI_HEADER_INPUT_AND_SETTINGS) # <-- 수정
    
    # QR 코드 내용 입력
    st.subheader(UI_SUBHEADER_CONTENT) # <-- 수정
    st.info(UI_INFO_CHAR_LIMIT) # <-- 수정
    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=200,
        placeholder=UI_PLACEHOLDER_CONTENT, # <-- 수정
        key="qr_input_area",
        on_change=on_qr_setting_change
    )
    
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(UI_ERROR_CHAR_COUNT_OVER.format(char_count)) # <-- 수정
        elif char_count > 2400:
            st.warning(UI_WARNING_CHAR_COUNT_NEAR.format(char_count)) # <-- 수정
        else:
            st.success(UI_SUCCESS_CHAR_COUNT_OK.format(char_count)) # <-- 수정
    else:
        st.caption(UI_CAPTION_CHAR_COUNT_ZERO) # <-- 수정
        
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            UI_BUTTON_DELETE, # <-- 수정
            help=UI_BUTTON_DELETE_HELP, # <-- 수정
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.checkbox(
        UI_CHECKBOX_STRIP, # <-- 수정
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change
    )

    st.markdown("---")
    st.markdown("---")
    
    # QR 코드 설정
    st.subheader(UI_SUBHEADER_SETTINGS) # <-- 수정
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.number_input(UI_LABEL_BOX_SIZE, min_value=1, max_value=100, key="box_size_input", on_change=on_qr_setting_change) # <-- 수정
        st.number_input(UI_LABEL_BORDER, min_value=0, max_value=10, key="border_input", on_change=on_qr_setting_change) # <-- 수정
    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        st.selectbox(
            UI_LABEL_EC, # <-- 수정
            options=list(error_correction_options.keys()),
            key="error_correction_select",
            on_change=on_qr_setting_change,
        )
        st.selectbox(
            UI_LABEL_MP, # <-- 수정
            options=[0, 1, 2, 3, 4, 5, 6, 7],
            key="mask_pattern_select",
            on_change=on_qr_setting_change,
        )

    st.markdown("---")
    st.subheader(UI_SUBHEADER_COLORS) # <-- 수정
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        st.selectbox(UI_LABEL_PATTERN_COLOR, options=["black", "white", "red", "green", "blue", UI_COLOR_OPTION_DIRECT_INPUT], key="pattern_color_select", on_change=on_qr_setting_change) # <-- 수정
    with col1_4:
        st.selectbox(UI_LABEL_BG_COLOR, options=["white", "black", "red", "green", "blue", UI_COLOR_OPTION_DIRECT_INPUT], key="bg_color_select", on_change=on_qr_setting_change) # <-- 수정

    st.markdown(UI_INFO_HEX_INPUT) # <-- 수정
    st.caption(UI_CAPTION_HEX_EXAMPLE) # <-- 수정
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input("패턴 색상 HEX 값", placeholder=UI_PLACEHOLDER_HEX_PATTERN, disabled=(st.session_state.pattern_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or file_format_is_svg, key="custom_pattern_color_input_key", on_change=on_qr_setting_change) # <-- 수정
    with col1_6:
        st.text_input("배경 색상 HEX 값", placeholder=UI_PLACEHOLDER_HEX_BG, disabled=(st.session_state.bg_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or file_format_is_svg, key="custom_bg_color_input_key", on_change=on_qr_setting_change) # <-- 수정
        
    # 새로운 패턴 스타일 선택 드롭다운 메뉴 추가
    st.markdown("---")
    st.subheader(UI_SUBHEADER_DOT_STYLE)
    st.selectbox(UI_LABEL_DOT_STYLE, options=[UI_DOT_STYLE_SQUARE, UI_DOT_STYLE_CIRCLE, UI_DOT_STYLE_ROUNDED], key="dot_style_select", on_change=on_qr_setting_change, disabled=file_format_is_svg) # <-- 수정

    st.markdown("---")
    st.subheader(UI_SUBHEADER_FILE) # <-- 수정
    col_filename_input, col_filename_delete = st.columns([3, 1.1])
    with col_filename_input:
        st.text_input(UI_LABEL_FILE_NAME, placeholder=UI_PLACEHOLDER_FILE_NAME, key="filename_input_key") # <-- 수정
    with col_filename_delete:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(
            UI_BUTTON_CLEAR_FILE_NAME, # <-- 수정
            help=UI_BUTTON_CLEAR_FILE_NAME_HELP, # <-- 수정
            use_container_width=True,
            on_click=clear_filename_callback,
        )

    st.selectbox(
        UI_LABEL_FILE_FORMAT, # <-- 수정
        options=[UI_FILE_FORMAT_PNG, UI_FILE_FORMAT_SVG], # <-- 수정
        key="file_format_select",
        on_change=on_file_format_change,
    )
    
