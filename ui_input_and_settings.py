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
    on_file_format_change,
    initialize_session_state_with_language,
)
from messages import get_message

def build_input_and_settings_ui():
    """입력 및 설정 섹션을 빌드합니다."""
    # 세션 상태 초기화 (언어에 맞춰 초기화)
    initialize_session_state_with_language()
    
    st.header(get_message('UI_HEADER_INPUT_AND_SETTINGS'))
    
    # QR 코드 내용 입력
    st.subheader(get_message('UI_SUBHEADER_QR_CONTENT'))
    st.info(get_message('UI_INFO_MAX_CHARS'))
    qr_data = st.text_area(
        get_message('UI_TEXT_AREA_LABEL'),
        height=200,
        placeholder=get_message('UI_TEXT_AREA_PLACEHOLDER'),
        key="qr_input_area",
        on_change=on_qr_setting_change
    )
    
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(get_message('UI_ERROR_MAX_CHARS').format(char_count=char_count))
        else:
            st.info(get_message('UI_INFO_CURRENT_CHARS').format(char_count=char_count))

    col_clear, col_strip = st.columns([1, 1.5])
    with col_clear:
        st.button(get_message('UI_BUTTON_CLEAR_TEXT'), on_click=clear_text_input, use_container_width=True)
    with col_strip:
        st.checkbox(get_message('UI_CHECKBOX_STRIP_TEXT'), value=True, key="strip_option", on_change=on_qr_setting_change)
    
    st.markdown("---")
    st.subheader(get_message('UI_SUBHEADER_QR_SETTINGS'))

    file_format_is_svg = (st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'))

    # 언어에 맞춰 오류 보정 레벨 옵션 설정
    error_correction_levels = [
        get_message('UI_ERROR_CORRECTION_LEVEL_L'),
        get_message('UI_ERROR_CORRECTION_LEVEL_M'),
        get_message('UI_ERROR_CORRECTION_LEVEL_Q'),
        get_message('UI_ERROR_CORRECTION_LEVEL_H'),
    ]

    st.selectbox(
        get_message('UI_SELECTBOX_ERROR_CORRECTION'),
        options=error_correction_levels,
        key="error_correction_select",
        on_change=on_qr_setting_change
    )

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.number_input(get_message('UI_NUMBER_INPUT_BOX_SIZE'), min_value=1, max_value=50, value=20, step=1, key="box_size_input", on_change=on_qr_setting_change)
    with col1_2:
        st.number_input(get_message('UI_NUMBER_INPUT_BORDER'), min_value=1, max_value=10, value=2, step=1, key="border_input", on_change=on_qr_setting_change)

    st.markdown("---")
    st.subheader(get_message('UI_SUBHEADER_COLOR_SETTINGS'))
    st.info(get_message('UI_INFO_COLOR_SETTINGS'))

    color_options = [
        get_message('UI_COLOR_OPTION_DIRECT_INPUT'),
        "black", "white", "gray", "red", "green", "blue", "yellow", "purple", "cyan", "magenta", "orange",
        "lime", "navy", "teal", "indigo"
    ]
    
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        st.selectbox(get_message('UI_SELECTBOX_PATTERN_COLOR'), options=color_options, key="pattern_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)
    with col1_4:
        st.selectbox(get_message('UI_SELECTBOX_BG_COLOR'), options=color_options, key="bg_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(get_message('UI_TEXT_INPUT_PATTERN_COLOR_HEX'), placeholder=get_message('UI_TEXT_INPUT_PLACEHOLDER_HEX'), disabled=(st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or file_format_is_svg, key="custom_pattern_color_input_key", on_change=on_qr_setting_change)
    with col1_6:
        st.text_input(get_message('UI_TEXT_INPUT_BG_COLOR_HEX'), placeholder=get_message('UI_TEXT_INPUT_PLACEHOLDER_HEX'), disabled=(st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or file_format_is_svg, key="custom_bg_color_input_key", on_change=on_qr_setting_change)
        
    st.markdown("---")
    st.subheader(get_message('UI_SUBHEADER_PATTERN_STYLE'))
    st.selectbox(get_message('UI_SELECTBOX_DOT_STYLE'), options=[get_message('UI_DOT_STYLE_SQUARE'), get_message('UI_DOT_STYLE_CIRCLE'), get_message('UI_DOT_STYLE_ROUNDED'), get_message('UI_DOT_STYLE_DIAMOND')], key="dot_style_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    st.markdown("---")
    st.subheader(get_message('UI_SUBHEADER_FILE_SETTINGS'))
    col_filename_input, col_filename_delete = st.columns([3, 1.1])
    with col_filename_input:
        st.text_input(get_message('UI_TEXT_INPUT_FILENAME'), placeholder=get_message('UI_TEXT_INPUT_FILENAME_PLACEHOLDER'), key="filename_input_key")
    with col_filename_delete:
        st.button(get_message('UI_BUTTON_CLEAR_FILENAME'), use_container_width=True, on_click=clear_filename_callback)
    
    st.selectbox(get_message('UI_SELECTBOX_FILE_FORMAT'), options=[get_message('UI_FILE_FORMAT_PNG'), get_message('UI_FILE_FORMAT_SVG')], key="file_format_select", on_change=on_file_format_change)
    
