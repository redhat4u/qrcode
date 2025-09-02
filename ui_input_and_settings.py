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
from messages import * # <-- 추가

def build_input_and_settings_ui():
    """입력 및 설정 섹션을 빌드합니다."""
    # 파일 형식이 SVG인지 여부를 함수 초반에 정의
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    st.header(UI_HEADER_INPUT_AND_SETTINGS)
    
    # QR 코드 내용 입력
    st.subheader(UI_SUBHEADER_QR_CONTENT)
    st.info(UI_INFO_QR_DATA_LIMIT)
    qr_data = st.text_area(
        UI_TEXT_AREA_LABEL,
        height=200,
        placeholder=UI_TEXT_AREA_PLACEHOLDER,
        key="qr_input_area",
        on_change=on_qr_setting_change
    )
    
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(UI_TEXT_CHAR_COUNT_OVER.format(char_count=char_count))
        elif char_count > 2400:
            st.warning(UI_TEXT_CHAR_COUNT_NEAR.format(char_count=char_count))
        else:
            st.success(UI_TEXT_CHAR_COUNT_OK.format(char_count=char_count))
    else:
        st.caption(UI_CAPTION_CHAR_COUNT_ZERO)
        
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            UI_BUTTON_DELETE_TEXT_LABEL,
            help=UI_BUTTON_DELETE_TEXT_HELP,
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.checkbox(
        UI_CHECKBOX_STRIP_TEXT,
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change
    )

    st.markdown("---")
    
    # 패턴 설정
    st.markdown("---")
    st.subheader(UI_SUBHEADER_DOT_STYLE)
    st.selectbox(UI_SELECTBOX_DOT_STYLE_LABEL, options=[UI_DOT_STYLE_SQUARE, UI_DOT_STYLE_CIRCLE, UI_DOT_STYLE_ROUNDED, UI_DOT_STYLE_DIAMOND], key="dot_style_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    # QR 코드 설정
    st.markdown("---")
    st.subheader(UI_SUBHEADER_QR_SETTINGS)
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.number_input(UI_BOX_SIZE_LABEL, min_value=1, max_value=100, key="box_size_input", on_change=on_qr_setting_change)
        st.number_input(UI_BORDER_LABEL, min_value=0, max_value=10, key="border_input", on_change=on_qr_setting_change)
    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        st.selectbox(UI_ERROR_CORRECTION_LABEL, list(error_correction_options.keys()), key="error_correction_select", on_change=on_qr_setting_change)
        st.selectbox(UI_MASK_PATTERN_LABEL, options=list(range(8)), key="mask_pattern_select", on_change=on_qr_setting_change)

    # 색상 설정
    st.markdown("---")
    st.subheader(UI_SUBHEADER_COLOR_SETTINGS)
    if file_format_is_svg:
        st.warning(UI_WARNING_SVG_COLOR)

    colors = [
        UI_COLOR_OPTION_DIRECT_INPUT, "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        st.selectbox(UI_SELECTBOX_PATTERN_COLOR_LABEL, colors, key="pattern_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)
    with col1_4:
        st.selectbox(UI_SELECTBOX_BG_COLOR_LABEL, colors, key="bg_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    st.markdown(UI_COLOR_INPUT_HELP)
    st.caption(UI_COLOR_INPUT_CAPTION)
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(UI_TEXT_INPUT_PATTERN_COLOR_LABEL, placeholder=UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER, disabled=(st.session_state.pattern_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or file_format_is_svg, key="custom_pattern_color_input_key", on_change=on_qr_setting_change)
    with col1_6:
        st.text_input(UI_TEXT_INPUT_BG_COLOR_LABEL, placeholder=UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER, disabled=(st.session_state.bg_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or file_format_is_svg, key="custom_bg_color_input_key", on_change=on_qr_setting_change)

    # 파일명 설정
    st.markdown("---")
    st.subheader(UI_SUBHEADER_FILE_SETTINGS)
    col_filename_input, col_filename_delete = st.columns([3, 1.1])
    with col_filename_input:
        st.text_input(UI_TEXT_INPUT_FILENAME_LABEL, placeholder=UI_TEXT_INPUT_FILENAME_PLACEHOLDER, key="filename_input_key")
    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button(UI_BUTTON_DELETE_FILENAME_LABEL, help=UI_BUTTON_DELETE_FILENAME_HELP, use_container_width=True, type="secondary", disabled=filename_delete_disabled, on_click=clear_filename_callback)

    # 파일 형식 설정
    st.radio(UI_RADIO_FILE_FORMAT, ("PNG", "SVG"), index=0 if st.session_state.file_format_select == "PNG" else 1, key="file_format_select", on_change=on_file_format_change)
    
