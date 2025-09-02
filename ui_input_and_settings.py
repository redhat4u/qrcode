# ui_input_and_settings.py

import streamlit as st
import qrcode
from state_manager import on_qr_setting_change, on_file_format_change, clear_text_input, clear_filename_callback
from messages import get_message

def build_input_and_settings_ui():
    """사용자 입력 및 QR 코드 설정 UI를 생성합니다."""
    
    st.header(get_message("UI_HEADER_INPUT_AND_SETTINGS"))
    
    # 1. QR 코드 내용 입력 섹션
    st.subheader(get_message("UI_SUBHEADER_QR_CONTENT"))
    st.info(get_message("UI_INFO_MAX_CHARS"))
    
    qr_data = st.text_area(
        get_message('UI_TEXT_AREA_LABEL'),
        value=st.session_state.qr_input_area,
        placeholder=get_message('UI_TEXT_AREA_PLACEHOLDER'),
        height=150,
        key='qr_input_area',
        on_change=on_qr_setting_change
    )
    
    char_count = len(qr_data)
    st.markdown(get_message('UI_INFO_CURRENT_CHARS').format(char_count=char_count))
    if char_count > 2953:
        st.warning(get_message('UI_ERROR_MAX_CHARS').format(char_count=char_count))

    col1_1, col1_2 = st.columns([1, 1])
    with col1_1:
        st.button(get_message('UI_BUTTON_CLEAR_TEXT'), on_click=clear_text_input, use_container_width=True)

    with col1_2:
        st.checkbox(get_message('UI_CHECKBOX_STRIP_TEXT'), key='strip_option', on_change=on_qr_setting_change)
        
    st.markdown("---")
    
    # 2. QR 코드 설정 섹션
    st.subheader(get_message("UI_SUBHEADER_QR_SETTINGS"))
    
    col2_1, col2_2, col2_3 = st.columns(3)
    with col2_1:
        st.selectbox(
            get_message("UI_SELECTBOX_ERROR_CORRECTION"),
            (get_message('UI_ERROR_CORRECTION_LEVEL_H'),
             get_message('UI_ERROR_CORRECTION_LEVEL_Q'),
             get_message('UI_ERROR_CORRECTION_LEVEL_M'),
             get_message('UI_ERROR_CORRECTION_LEVEL_L')),
            key='error_correction_select',
            on_change=on_qr_setting_change
        )
    with col2_2:
        st.number_input(
            get_message('UI_NUMBER_INPUT_BOX_SIZE'),
            min_value=1,
            max_value=100,
            step=1,
            key='box_size_input',
            on_change=on_qr_setting_change
        )
    with col2_3:
        st.number_input(
            get_message('UI_NUMBER_INPUT_BORDER'),
            min_value=1,
            max_value=10,
            step=1,
            key='border_input',
            on_change=on_qr_setting_change
        )
    st.markdown("---")
    
    # 3. 색상 설정 섹션
    st.subheader(get_message("UI_SUBHEADER_COLOR_SETTINGS"))
    st.info(get_message("UI_INFO_COLOR_SETTINGS"))
    
    col3_1, col3_2 = st.columns(2)
    with col3_1:
        st.selectbox(
            get_message('UI_SELECTBOX_PATTERN_COLOR'),
            options=['black', 'white', 'red', 'green', 'blue', 'orange', get_message('UI_COLOR_OPTION_DIRECT_INPUT')],
            key='pattern_color_select',
            on_change=on_qr_setting_change
        )
    with col3_2:
        st.selectbox(
            get_message('UI_SELECTBOX_BG_COLOR'),
            options=['white', 'black', 'red', 'green', 'blue', 'orange', get_message('UI_COLOR_OPTION_DIRECT_INPUT')],
            key='bg_color_select',
            on_change=on_qr_setting_change
        )
        
    if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
        st.text_input(
            get_message('UI_TEXT_INPUT_PATTERN_COLOR_HEX'),
            placeholder=get_message('UI_TEXT_INPUT_PLACEHOLDER_HEX'),
            key='custom_pattern_color_input_key',
            on_change=on_qr_setting_change
        )
        
    if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
        st.text_input(
            get_message('UI_TEXT_INPUT_BG_COLOR_HEX'),
            placeholder=get_message('UI_TEXT_INPUT_PLACEHOLDER_HEX'),
            key='custom_bg_color_input_key',
            on_change=on_qr_setting_change
        )

    st.markdown("---")
    
    # 4. 패턴 스타일 설정
    st.subheader(get_message("UI_SUBHEADER_PATTERN_STYLE"))
    st.selectbox(
        get_message('UI_SELECTBOX_DOT_STYLE'),
        options=[get_message('UI_DOT_STYLE_SQUARE'), 
                 get_message('UI_DOT_STYLE_ROUNDED'),
                 get_message('UI_DOT_STYLE_CIRCLE'),
                 get_message('UI_DOT_STYLE_DIAMOND')],
        key='dot_style_select',
        on_change=on_qr_setting_change
    )

    st.markdown("---")
    
    # 5. 파일 설정 섹션
    st.subheader(get_message("UI_SUBHEADER_FILE_SETTINGS"))
    
    col5_1, col5_2 = st.columns([1,1])
    with col5_1:
        st.text_input(
            get_message('UI_TEXT_INPUT_FILENAME'),
            placeholder=get_message('UI_TEXT_INPUT_FILENAME_PLACEHOLDER'),
            key='filename_input_key'
        )
    with col5_2:
        st.button(get_message('UI_BUTTON_CLEAR_FILENAME'), on_click=clear_filename_callback, use_container_width=True)
        
    st.selectbox(
        get_message('UI_SELECTBOX_FILE_FORMAT'),
        options=[get_message('UI_FILE_FORMAT_PNG'), get_message('UI_FILE_FORMAT_SVG')],
        key='file_format_select',
        on_change=on_file_format_change
    )
    
