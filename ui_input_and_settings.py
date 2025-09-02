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
)
from messages import *

def build_input_and_settings_ui():
    """입력 및 설정 섹션을 빌드합니다."""
    file_format_is_svg = (st.session_state.file_format_select == UI_FILE_FORMAT_SVG)

    st.header(UI_HEADER_INPUT_AND_SETTINGS)
    
    # QR 코드 내용 입력
    st.subheader(UI_SUBHEADER_CONTENT)
    st.info(UI_INFO_CHAR_LIMIT)
    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=200,
        placeholder=UI_PLACEHOLDER_CONTENT,
        key="qr_input_area",
        on_change=on_qr_setting_change
    )
    
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(UI_ERROR_CHAR_COUNT_OVER.format(char_count))
        elif char_count > 2400:
            st.warning(UI_WARNING_CHAR_COUNT_NEAR.format(char_count))
        else:
            st.success(UI_SUCCESS_CHAR_COUNT_OK.format(char_count))
    else:
        st.caption(UI_CAPTION_CHAR_COUNT_ZERO)
        
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            UI_BUTTON_DELETE,
            help=UI_BUTTON_DELETE_HELP,
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.checkbox(
        UI_CHECKBOX_STRIP,
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change
    )

    st.markdown("---")
    st.markdown("---")
    
    # QR 코드 설정
    st.subheader(UI_SUBHEADER_SETTINGS)
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.number_input(UI_LABEL_BOX_SIZE, min_value=1, max_value=100, key="box_size_input", on_change=on_qr_setting_change)
        st.number_input(UI_LABEL_BORDER, min_value=0, max_value=10, key="border_input", on_change=on_qr_setting_change)
    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        st.selectbox(
            UI_LABEL_EC,
            options=list(error_correction_options.keys()),
            key="error_correction_select",
            on_change=on_qr_setting_change,
        )
        st.selectbox(
            UI_LABEL_MP,
            options=[0, 1, 2, 3, 4, 5, 6, 7],
            key="mask_pattern_select",
            on_change=on_qr_setting_change,
        )

    st.markdown("---")
    st.subheader(UI_SUBHEADER_COLORS)
    if file_format_is_svg:
        st.warning("⚠️ SVG 파일은 벡터 형식이므로 원하는 색상을 선택할 수 없습니다. 다양한 색상을 원한다면 'PNG' 형식을 선택하세요.")

    colors = [
        "<직접 입력>", "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        st.selectbox(UI_LABEL_PATTERN_COLOR, options=colors, key="pattern_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)
    with col1_4:
        st.selectbox(UI_LABEL_BG_COLOR, options=colors, key="bg_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    st.markdown(UI_INFO_HEX_INPUT)
    st.caption(UI_CAPTION_HEX_EXAMPLE)
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input("패턴 색상 HEX 값", placeholder=UI_PLACEHOLDER_HEX_PATTERN, disabled=(st.session_state.pattern_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or file_format_is_svg, key="custom_pattern_color_input_key", on_change=on_qr_setting_change)
    with col1_6:
        st.text_input("배경 색상 HEX 값", placeholder=UI_PLACEHOLDER_HEX_BG, disabled=(st.session_state.bg_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or file_format_is_svg, key="custom_bg_color_input_key", on_change=on_qr_setting_change)
        
    # 새로운 패턴 스타일 선택 드롭다운 메뉴 추가
    st.markdown("---")
    st.subheader(UI_SUBHEADER_DOT_STYLE)
    st.selectbox(UI_LABEL_DOT_STYLE, options=[UI_DOT_STYLE_SQUARE, UI_DOT_STYLE_CIRCLE, UI_DOT_STYLE_ROUNDED, UI_DOT_STYLE_RHOMBUS], key="dot_style_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    st.markdown("---")
    st.subheader(UI_SUBHEADER_FILE)
    col_filename_input, col_filename_delete = st.columns([3, 1.1])
    with col_filename_input:
        st.text_input(UI_LABEL_FILE_NAME, placeholder=UI_PLACEHOLDER_FILE_NAME, key="filename_input_key")
    with col_filename_delete:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(
            UI_BUTTON_CLEAR_FILE_NAME,
            help=UI_BUTTON_CLEAR_FILE_NAME_HELP,
            use_container_width=True,
            on_click=clear_filename_callback,
        )

    st.selectbox(
        UI_LABEL_FILE_FORMAT,
        options=[UI_FILE_FORMAT_PNG, UI_FILE_FORMAT_SVG],
        key="file_format_select",
        on_change=on_file_format_change,
    )
    
