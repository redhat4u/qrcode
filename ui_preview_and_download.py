# 이 파일은 생성된 QR 코드의 미리보기와 다운로드 UI를 정의합니다.
# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from functions import generate_qr_code_png, generate_qr_code_svg, is_valid_color, sanitize_filename
from state_manager import set_download_initiated
from messages import *

def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    st.header(UI_HEADER_PREVIEW_AND_GENERATE)
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data
    
    file_format_is_svg = (st.session_state.file_format_select == UI_FILE_FORMAT_SVG)
    
    is_pattern_color_valid = (st.session_state.pattern_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or (st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
    is_bg_color_valid = (st.session_state.bg_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or (st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))
    
    pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.pattern_color_select
    bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.bg_color_select
    is_colors_same = (is_pattern_color_valid and is_bg_color_valid and pattern_color and bg_color and pattern_color == bg_color)
    
    error_correction_options = {
        "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
        "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
        "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
        "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
    }
    error_correction = error_correction_options[st.session_state.error_correction_select]

    # 미리보기 이미지 생성 및 표시
    if current_data:
        # 색상 유효성 검사 (SVG는 제외)
        if not file_format_is_svg and (not is_pattern_color_valid or not is_bg_color_valid or is_colors_same):
            if not is_pattern_color_valid:
                st.error(UI_ERROR_HEX_PATTERN_INVALID)
            elif not is_bg_color_valid:
                st.error(UI_ERROR_HEX_BG_INVALID)
            elif is_colors_same:
                st.error(UI_ERROR_COLORS_SAME)
            st.caption(UI_CAPTION_QR_PREVIEW_ERROR)
        else:
            if st.session_state.file_format_select == UI_FILE_FORMAT_PNG:
                img, qr = generate_qr_code_png(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select),
                    "black" if file_format_is_svg else pattern_color,
                    "white" if file_format_is_svg else bg_color,
                    st.session_state.dot_style_select
                )
                if img:
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    st.session_state.qr_image_bytes = img_buffer.getvalue()
                    st.image(st.session_state.qr_image_bytes, use_column_width=True)
            elif st.session_state.file_format_select == UI_FILE_FORMAT_SVG:
                img_svg, qr = generate_qr_code_svg(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select),
                    "black",
                    "white"
                )
                if img_svg:
                    st.session_state.qr_svg_bytes = img_svg
                    st.image(st.session_state.qr_svg_bytes, use_column_width=True)
    else:
        st.caption(UI_CAPTION_QR_DATA_EMPTY)

    st.markdown("---")

    # QR 코드 생성 버튼 및 다운로드 로직 (기존 로직 유지)
    generate_btn = st.button(UI_BUTTON_GENERATE, use_container_width=True)
    
    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None
        
        errors = []
        final_pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.pattern_color_select
        final_bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.bg_color_select
        
        if not current_data:
            errors.append(UI_ERROR_QR_DATA_EMPTY)
        
        if not file_format_is_svg:
            if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not final_pattern_color:
                errors.append(UI_ERROR_HEX_PATTERN_EMPTY)
            elif st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not is_valid_color(final_pattern_color):
                errors.append(UI_ERROR_HEX_PATTERN_INVALID)
            
            if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not final_bg_color:
                errors.append(UI_ERROR_HEX_BG_EMPTY)
            elif st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not is_valid_color(final_bg_color):
                errors.append(UI_ERROR_HEX_BG_INVALID)
            
            if final_pattern_color and final_bg_color and final_pattern_color == final_bg_color:
                errors.append(UI_ERROR_COLORS_SAME)

        if errors:
            st.session_state.error_message = errors[0]
            st.session_state.show_generate_success = False
        else:
            st.session_state.error_message = None
            st.session_state.show_generate_success = True
            
    if st.session_state.generate_button_clicked:
        if st.session_state.error_message:
            st.error(st.session_state.error_message)
        elif st.session_state.show_generate_success:
            st.success(UI_SUCCESS_MESSAGE)
            
            # 다운로드 버튼 표시
            if current_data:
                final_filename = st.session_state.filename_input_key.strip()
                if not final_filename:
                    korean_tz = ZoneInfo("Asia/Seoul")
                    timestamp = datetime.now(korean_tz).strftime("%Y%m%d_%H%M%S")
                    final_filename = f"qrcode_{timestamp}"
                
                if st.session_state.file_format_select == UI_FILE_FORMAT_PNG:
                    download_data = st
                    
