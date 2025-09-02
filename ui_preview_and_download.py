# 이 파일은 생성된 QR 코드의 미리보기와 다운로드 UI를 정의합니다.
# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from functions import generate_qr_code_png, generate_qr_code_svg, is_valid_color, sanitize_filename
from state_manager import set_download_initiated
from messages import * # <-- 추가

def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    st.header(UI_HEADER_PREVIEW_AND_GENERATE) # <-- 수정
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data
    
    file_format_is_svg = (st.session_state.file_format_select == UI_FILE_FORMAT_SVG) # <-- 수정
    
    is_pattern_color_valid_preview = (st.session_state.pattern_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or (st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key)) # <-- 수정
    is_bg_color_valid_preview = (st.session_state.bg_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or (st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key)) # <-- 수정
    
    pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.pattern_color_select # <-- 수정
    bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.bg_color_select # <-- 수정
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    error_correction_options = {
        "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
        "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
        "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
        "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
    }
    error_correction = error_correction_options[st.session_state.error_correction_select]

    preview_image_display = None
    preview_qr_object = None
    
    if current_data and (file_format_is_svg or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview)):
        
        preview_dot_style = UI_DOT_STYLE_SQUARE if file_format_is_svg else st.session_state.dot_style_select # <-- 수정
        
        img, qr = generate_qr_code_png(
            current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
            int(st.session_state.mask_pattern_select),
            "black" if file_format_is_svg else pattern_color,
            "white" if file_format_is_svg else bg_color,
            preview_dot_style
        )
        if img and qr:
            preview_image_display = img
            preview_qr_object = qr

    generate_btn = st.button(UI_BUTTON_GENERATE, use_container_width=True) # <-- 수정
    
    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None
        
        errors = []
        final_pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.pattern_color_select # <-- 수정
        final_bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.bg_color_select # <-- 수정
        
        if not current_data:
            errors.append(UI_ERROR_QR_DATA_EMPTY) # <-- 수정
        
        if not file_format_is_svg:
            if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not final_pattern_color: # <-- 수정
                errors.append(UI_ERROR_HEX_PATTERN_EMPTY) # <-- 수정
            elif st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not is_valid_color(final_pattern_color): # <-- 수정
                errors.append(UI_ERROR_HEX_PATTERN_INVALID) # <-- 수정
            
            if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not final_bg_color: # <-- 수정
                errors.append(UI_ERROR_HEX_BG_EMPTY) # <-- 수정
            elif st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not is_valid_color(final_bg_color): # <-- 수정
                errors.append(UI_ERROR_HEX_BG_INVALID) # <-- 수정
            
            if final_pattern_color and final_bg_color and final_pattern_color == final_bg_color:
                errors.append(UI_ERROR_COLORS_SAME) # <-- 수정

        if errors:
            st.session_state.error_message = errors[0]
            st.session_state.show_generate_success = False
        else:
            st.session_state.error_message = None
            if st.session_state.file_format_select == UI_FILE_FORMAT_PNG: # <-- 수정
                img, qr = generate_qr_code_png(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select),
                    final_pattern_color,
                    final_bg_color,
                    st.session_state.dot_style_select
                )
                if img and qr:
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    st.session_state.qr_image_bytes = img_buffer.getvalue()
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
                else:
                    st.session_state.error_message = "알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                    st.session_state.show_generate_success = False

            elif st.session_state.file_format_select == UI_FILE_FORMAT_SVG: # <-- 수정
                img_svg, qr = generate_qr_code_svg(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select),
                    "black", # SVG에서는 fill_color, back_color를 아직 처리하지 않음
                    "white"
                )
                if img_svg and qr:
                    st.session_state.qr_svg_bytes = img_svg
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
                else:
                    st.session_state.error_message = "알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                    st.session_state.show_generate_success = False
    
    # 미리보기 및 다운로드
    st.markdown("---")
    if st.session_state.generate_button_clicked and st.session_state.show_generate_success:
        st.success(UI_SUCCESS_MESSAGE) # <-- 수정
        st.markdown(
            f'<div style="text-align: center; border: 1px solid #ddd; padding: 10px; margin-bottom: 20px;">'
            f'{st.image(st.session_state.qr_image_bytes, use_column_width=True) if st.session_state.file_format_select == UI_FILE_FORMAT_PNG else st.image(st.session_state.qr_svg_bytes, use_column_width=True)}' # <-- 수정
            f'</div>',
            unsafe_allow_html=True
        )

        final_filename = st.session_state.filename_input_key.strip()
        if not final_filename:
            korean_tz = ZoneInfo("Asia/Seoul")
            timestamp = datetime.now(korean_tz).strftime("%Y%m%d_%H%M%S")
            final_filename = f"qrcode_{timestamp}"

        if st.session_state.file_format_select == UI_FILE_FORMAT_PNG: # <-- 수정
            download_data = st.session_state.qr_image_bytes
            download_mime = "image/png"
            download_extension = ".png"
        else:
            download_data = st.session_state.qr_svg_bytes
            download_mime = "image/svg+xml"
            download_extension = ".svg"
        
        download_filename = f"{sanitize_filename(final_filename)}{download_extension}"
        
        st.download_button(
            label=UI_BUTTON_DOWNLOAD, # <-- 수정
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=UI_BUTTON_DOWNLOAD_HELP, # <-- 수정
            on_click=set_download_initiated,
        )

        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{UI_DOWNLOAD_FILENAME} </span> ' # <-- 수정
            f'<span style="color:dodgerblue;"> {download_filename}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    if st.session_state.download_initiated:
        st.markdown(
            """
            <div style='
                background-color: #0c4145;
                color: #dffde9;
                padding: 1rem;
                border-radius: 0.5rem;
                border: 1px solid #1a5e31;
                font-size: 1rem;
                margin-bottom: 1rem;
            '>
            """, unsafe_allow_html=True
        )
        st.markdown(UI_SUCCESS_DOWNLOAD_MESSAGE)
        st.markdown("</div>", unsafe_allow_html=True)
        st.session_state.download_initiated = False
    
    if not current_data:
        if st.session_state.error_message:
            st.error(st.session_state.error_message)
        else:
            st.caption(UI_CAPTION_QR_DATA_EMPTY) # <-- 수정
            
    if st.session_state.generate_button_clicked and st.session_state.error_message:
        st.error(st.session_state.error_message)
        if st.session_state.file_format_select == UI_FILE_FORMAT_PNG: # <-- 수정
            st.markdown("- PNG는 16진수(HEX) 색상 코드만 지원합니다. 올바른 HEX 코드를 입력했는지 확인해주세요.")
            st.markdown("- 패턴과 배경 색상이 서로 다르게 설정되었는지 확인해주세요.")
            st.markdown("- QR 코드에 담을 내용이 올바르게 입력되었는지 확인해주세요.")
            
