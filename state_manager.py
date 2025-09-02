# This file manages the Streamlit session_state to control the app's state.
# state_manager.py

import streamlit as st
import qrcode
from messages import get_message, get_current_language

def initialize_session_state_with_language():
    """Initializes the session state, considering language settings."""
    # Use default value before session_state is initialized
    current_lang = get_current_language()
    
    if "is_initialized" not in st.session_state or st.session_state.current_language != current_lang:
        st.session_state.is_initialized = True
        st.session_state.current_language = current_lang
        
        # QR code input and settings
        st.session_state.qr_input_area = ""
        st.session_state.strip_option = True
        st.session_state.box_size_input = 20
        st.session_state.border_input = 2
        st.session_state.mask_pattern_select = 7
        st.session_state.pattern_color_select = "black"
        st.session_state.bg_color_select = "white"
        st.session_state.custom_pattern_color_input_key = ""
        st.session_state.custom_bg_color_input_key = ""
        st.session_state.dot_style_select = get_message('UI_DOT_STYLE_SQUARE')
        st.session_state.file_format_select = get_message('UI_FILE_FORMAT_PNG')
        st.session_state.filename_input_key = ""
        st.session_state.error_correction_select = get_message('UI_ERROR_CORRECTION_LEVEL_M')
        
        # UI state
        st.session_state.qr_image_bytes = None
        st.session_state.qr_svg_bytes = None
        st.session_state.qr_generated = False
        st.session_state.error_message = None
        st.session_state.generate_button_clicked = False
        st.session_state.show_generate_success = False
        st.session_state.download_initiated = False

def clear_text_input():
    """Resets the QR code content input area."""
    st.session_state.qr_input_area = ""

def clear_filename_callback():
    """Resets the filename input area."""
    st.session_state.filename_input_key = ""

def on_qr_setting_change():
    """Refreshes the preview when a QR setting is changed."""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False

def on_file_format_change():
    """Resets state when the file format is changed."""
    on_qr_setting_change()
    if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
        st.session_state.pattern_color_select = "black"
        st.session_state.bg_color_select = "white"

def set_download_initiated():
    """Sets the state to show the download complete message."""
    st.session_state.download_initiated = True

def reset_all_settings():
    """Resets all settings to their initial state."""
    st.session_state.is_initialized = False
    # Call the initialization function again to reset
    initialize_session_state_with_language()
    
