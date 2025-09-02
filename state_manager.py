# state_manager.py

import streamlit as st
import qrcode
from messages import get_message, MESSAGES

def initialize_session_state_with_language():
    """Initializes session state variables with language-specific defaults."""
    # Ensure the language dropdown is always set
    if 'language_select' not in st.session_state:
        st.session_state.language_select = MESSAGES['ko']['UI_LANG_SELECT_OPTIONS'][0] # Default to '한국어'
    
    # Set default values if not already in session state
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
    if 'mask_pattern_select' not in st.session_state:
        st.session_state.mask_pattern_select = 0


def on_qr_setting_change():
    """Resets flags to trigger preview update."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False

def on_file_format_change():
    """Updates state when file format changes."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.download_initiated = False
    
def clear_text_input():
    """Clears the QR content input."""
    st.session_state.qr_input_area = ""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False

def clear_filename_callback():
    """Clears the filename input."""
    st.session_state.filename_input_key = ""
    st.session_state.qr_generated = False

def set_download_initiated():
    """Sets a flag when the download button is clicked."""
    st.session_state.download_initiated = True

def reset_all_settings():
    """Resets all settings to their initial state, preserving only language."""
    # Keep the language selection and clear the rest
    lang_select = st.session_state.get('language_select', MESSAGES['ko']['UI_LANG_SELECT_OPTIONS'][0])
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.session_state.language_select = lang_select
    # Re-initialize with the new language setting
    initialize_session_state_with_language()
    
