import streamlit as st
from ui_preview_and_download import build_preview_and_download_ui
from functions import get_message, get_error_correction_constant

# 페이지 설정
st.set_page_config(page_title=get_message('UI_APP_TITLE'), layout="wide")

st.title(get_message('UI_APP_TITLE'))
st.write(get_message('UI_APP_DESCRIPTION'))

# 사이드바
with st.sidebar:
    st.header(get_message('UI_OPTIONS_HEADER'))

    qr_data = st.text_area(
        label=get_message('UI_INPUT_LABEL'),
        value="https://www.google.com",
        help=get_message('UI_INPUT_HELP')
    )

    st.subheader(get_message('UI_STYLE_HEADER'))
    dot_style = st.selectbox(
        label=get_message('UI_DOT_STYLE_LABEL'),
        options=[
            get_message('UI_DOT_STYLE_SQUARE'),
            get_message('UI_DOT_STYLE_ROUNDED'),
            get_message('UI_DOT_STYLE_CIRCLE'),
            get_message('UI_DOT_STYLE_DIAMOND')
        ],
        index=0,
    )
    
    fill_color = st.color_picker(
        label=get_message('UI_FILL_COLOR_LABEL'),
        value="#000000"
    )

    back_color = st.color_picker(
        label=get_message('UI_BG_COLOR_LABEL'),
        value="#FFFFFF"
    )

    st.subheader(get_message('UI_ADVANCED_HEADER'))
    error_correction_str = st.selectbox(
        label=get_message('UI_ERROR_CORRECTION_LABEL'),
        options=[
            get_message('UI_ERROR_CORRECTION_LEVEL_L'),
            get_message('UI_ERROR_CORRECTION_LEVEL_M'),
            get_message('UI_ERROR_CORRECTION_LEVEL_Q'),
            get_message('UI_ERROR_CORRECTION_LEVEL_H')
        ],
        index=3,
    )

    box_size = st.slider(
        label=get_message('UI_BOX_SIZE_LABEL'),
        min_value=1,
        max_value=20,
        value=10,
    )

    border = st.slider(
        label=get_message('UI_BORDER_LABEL'),
        min_value=1,
        max_value=10,
        value=4,
    )

    mask_pattern = st.slider(
        label=get_message('UI_MASK_PATTERN_LABEL'),
        min_value=0,
        max_value=7,
        value=0,
    )

    selected_options = {
        "dot_style": dot_style,
        "fill_color": fill_color,
        "back_color": back_color,
        "error_correction": error_correction_str,
        "box_size": box_size,
        "border": border,
        "mask_pattern": mask_pattern,
    }

# 미리보기 UI 호출
build_preview_and_download_ui(qr_data, selected_options)
