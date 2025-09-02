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
    generate_and_store_qr,
)
from messages import get_message

def build_input_and_settings_ui():
    """입력 및 설정 섹션을 빌드합니다."""
    st.header(get_message('UI_HEADER_INPUT_AND_SETTINGS'))
    
    # QR 코드 내용 입력
    st.subheader(get_message('UI_SUBHEADER_QR_CONTENT'))
    st.info(get_message('UI_INFO_QR_DATA_LIMIT'))
    qr_data = st.text_area(
        get_message('UI_TEXT_AREA_LABEL'),
        height=200,
        placeholder=get_message('UI_TEXT_AREA_PLACEHOLDER'),
        key="qr_input_area",
        on_change=generate_and_store_qr
    )
    
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(get_message('UI_TEXT_CHAR_COUNT_OVER').format(char_count=char_count))
        elif char_count > 2400:
            st.warning(get_message('UI_TEXT_CHAR_COUNT_NEAR').format(char_count=char_count))
        else:
            st.success(get_message('UI_TEXT_CHAR_COUNT_OK').format(char_count=char_count))
    else:
        st.caption(get_message('UI_CAPTION_CHAR_COUNT_ZERO'))
    
    col_1, col_2 = st.columns([1, 1])
    with col_1:
        is_qr_input_empty = st.session_state.qr_input_area == ""
        st.button(
            get_message('UI_BUTTON_DELETE_TEXT_LABEL'),
            use_container_width=True,
            help=get_message('UI_BUTTON_DELETE_TEXT_HELP'),
            on_click=clear_text_input,
            disabled=is_qr_input_empty
        )
    with col_2:
        st.checkbox(get_message('UI_CHECKBOX_STRIP_TEXT'), value=True, key='strip_option', on_change=generate_and_store_qr)

    st.markdown("---")

    # QR 패턴 모양 설정
    st.subheader(get_message('UI_SUBHEADER_DOT_STYLE'))
    file_format_is_svg = (st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'))
    st.selectbox(
        get_message('UI_SELECTBOX_DOT_STYLE_LABEL'),
        options=[
            get_message('UI_DOT_STYLE_SQUARE'),
            get_message('UI_DOT_STYLE_CIRCLE'),
            get_message('UI_DOT_STYLE_ROUNDED'),
            get_message('UI_DOT_STYLE_DIAMOND'),
        ],
        key="dot_style_select",
        on_change=generate_and_store_qr,
        disabled=file_format_is_svg
    )

    st.markdown("---")
    
    # QR 코드 설정
    st.subheader(get_message('UI_SUBHEADER_QR_SETTINGS'))
    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        st.number_input(get_message('UI_BOX_SIZE_LABEL'), min_value=1, max_value=50, value=20, key='box_size_input', on_change=generate_and_store_qr)
    with col4:
        st.number_input(get_message('UI_BORDER_LABEL'), min_value=1, max_value=10, value=2, key='border_input', on_change=generate_and_store_qr)
    with col5:
        st.selectbox(get_message('UI_ERROR_CORRECTION_LABEL'), options=[
            get_message('UI_ERROR_CORRECTION_LEVEL_L'),
            get_message('UI_ERROR_CORRECTION_LEVEL_M'),
            get_message('UI_ERROR_CORRECTION_LEVEL_Q'),
            get_message('UI_ERROR_CORRECTION_LEVEL_H'),
        ], key='error_correction_select', on_change=generate_and_store_qr)
    
    st.selectbox(get_message('UI_MASK_PATTERN_LABEL'), options=list(range(8)), key='mask_pattern_select', on_change=generate_and_store_qr)
    
    st.markdown("---")

    # QR 코드 색상 설정
    st.subheader(get_message('UI_SUBHEADER_COLOR_SETTINGS'))
    if file_format_is_svg:
        st.warning(get_message('UI_WARNING_SVG_COLOR'))
    
    color_options = ["black", "white", "red", "blue", "green", "hotpink", get_message('UI_COLOR_OPTION_DIRECT_INPUT')]
    col_1_1, col_1_2 = st.columns([1, 1])
    with col_1_1:
        st.selectbox(get_message('UI_SELECTBOX_PATTERN_COLOR_LABEL'), options=color_options, key='pattern_color_select', on_change=generate_and_store_qr, disabled=file_format_is_svg)
    with col_1_2:
        st.selectbox(get_message('UI_SELECTBOX_BG_COLOR_LABEL'), options=color_options, key='bg_color_select', on_change=generate_and_store_qr, disabled=file_format_is_svg)

    st.info(get_message('UI_COLOR_INPUT_HELP'))
    st.caption(get_message('UI_COLOR_INPUT_CAPTION'))
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(get_message('UI_TEXT_INPUT_PATTERN_COLOR_LABEL'), placeholder=get_message('UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER'), disabled=(st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or file_format_is_svg, key="custom_pattern_color_input_key", on_change=generate_and_store_qr)
    with col1_6:
        st.text_input(get_message('UI_TEXT_INPUT_BG_COLOR_LABEL'), placeholder=get_message('UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER'), disabled=(st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or file_format_is_svg, key="custom_bg_color_input_key", on_change=generate_and_store_qr)

    st.markdown("---")
    
    # 파일 형식 및 다운로드 설정
    st.subheader(get_message('UI_SUBHEADER_FILE_SETTINGS'))
    col_file_format, col_file_name = st.columns([1, 3])
    with col_file_format:
        st.radio(get_message('UI_RADIO_FILE_FORMAT'), options=[get_message('UI_FILE_FORMAT_PNG'), get_message('UI_FILE_FORMAT_SVG')], key="file_format_select", on_change=generate_and_store_qr)
    with col_file_name:
        col_filename_input, col_filename_delete = st.columns([3, 1.1])
        with col_filename_input:
            st.text_input(get_message('UI_TEXT_INPUT_FILENAME_LABEL'), placeholder=get_message('UI_TEXT_INPUT_FILENAME_PLACEHOLDER'), key="filename_input_key")
        with col_filename_delete:
            is_filename_input_empty = st.session_state.filename_input_key == ""
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) 
            st.button(
                get_message('UI_BUTTON_DELETE_FILENAME_LABEL'),
                use_container_width=True,
                help=get_message('UI_BUTTON_DELETE_FILENAME_HELP'),
                on_click=clear_filename_callback,
                disabled=is_filename_input_empty
            )
            
