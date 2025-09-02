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
    st.header(UI_HEADER_PREVIEW_AND_GENERATE)
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data
    
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    is_pattern_color_valid_preview = (st.session_state.pattern_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or (st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
    is_bg_color_valid_preview = (st.session_state.bg_color_select != UI_COLOR_OPTION_DIRECT_INPUT) or (st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))
    
    pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.pattern_color_select
    bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT else st.session_state.bg_color_select
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
        
        preview_dot_style = UI_DOT_STYLE_SQUARE if file_format_is_svg else st.session_state.dot_style_select
        
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
            if st.session_state.file_format_select == "PNG":
                img, qr = generate_qr_code_png(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), final_pattern_color, final_bg_color,
                    st.session_state.dot_style_select
                )
                if img and qr:
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    st.session_state.qr_image_bytes = img_buffer.getvalue()
                    st.session_state.qr_svg_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
            else: # SVG
                svg_data, qr = generate_qr_code_svg(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), "black", "white",
                )
                if svg_data and qr:
                    st.session_state.qr_svg_bytes = svg_data.encode('utf-8')
                    st.session_state.qr_image_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True

    st.markdown("---")

    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    elif st.session_state.show_generate_success:
         st.markdown(
             f"""
             <div style='
                 background-color: #0c4145;
                 color: #dffde9;
                 padding: 1rem;
                 border-radius: 0.5rem;
                 border: 1px solid #1a5e31;
                 font-size: 1rem;
                 margin-bottom: 1rem;
                 word-break: keep-all;
             '>{UI_SUCCESS_MESSAGE}</div>
             """,
             unsafe_allow_html=True,
         )
    elif st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not st.session_state.custom_pattern_color_input_key:
        st.warning(UI_ERROR_HEX_PATTERN_EMPTY)
    elif st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not st.session_state.custom_bg_color_input_key:
        st.warning(UI_ERROR_HEX_BG_EMPTY)
    elif (st.session_state.pattern_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not is_valid_color(st.session_state.custom_pattern_color_input_key)) or \
         (st.session_state.bg_color_select == UI_COLOR_OPTION_DIRECT_INPUT and not is_valid_color(st.session_state.custom_bg_color_input_key)):
        st.warning(UI_ERROR_HEX_PATTERN_INVALID)
    elif is_colors_same_preview:
        st.warning(UI_ERROR_COLORS_SAME)
    elif preview_image_display:
         st.markdown(
             f"""
             <div style='
                 background-color: #0c4145;
                 color: #dffde9;
                 padding: 1rem;
                 border-radius: 0.5rem;
                 border: 1px solid #1a5e31;
                 font-size: 1rem;
                 margin-bottom: 1rem;
                 word-break: keep-all;
             '>{UI_PREVIEW_READY_MESSAGE}</div>
             """,
             unsafe_allow_html=True,
         )
    else:
        st.info(UI_INFO_ENTER_QR_DATA)

    if preview_image_display:
        st.subheader(UI_SUBHEADER_PREVIEW)
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=UI_IMAGE_CAPTION_PREVIEW, width=380)
        
        if preview_qr_object:
            st.info(UI_INFO_QR_INFO.format(
                version=preview_qr_object.version,
                modules=preview_qr_object.modules_count,
                size=(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input),
                pattern_color="black" if file_format_is_svg else pattern_color,
                bg_color="white" if file_format_is_svg else bg_color
            ))
    
    if st.session_state.get('qr_generated', False) and (st.session_state.get('qr_image_bytes') is not None or st.session_state.get('qr_svg_bytes') is not None):
        st.markdown("---")
        st.subheader(UI_SUBHEADER_DOWNLOAD)
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        current_filename = st.session_state.filename_input_key.strip()
        final_filename = current_filename if current_filename else now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        
        download_data = None
        download_mime = ""
        download_extension = ""

        if st.session_state.file_format_select == "PNG":
            download_data = st.session_state.qr_image_bytes
            download_mime = "image/png"
            download_extension = ".png"
        else: # SVG
            download_data = st.session_state.qr_svg_bytes
            download_mime = "image/svg+xml"
            download_extension = ".svg"
        
        download_filename = f"{sanitize_filename(final_filename)}{download_extension}"
        
        st.download_button(
            label=UI_BUTTON_DOWNLOAD,
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=UI_BUTTON_DOWNLOAD_HELP,
            on_click=set_download_initiated,
        )

        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{UI_DOWNLOAD_FILENAME_LABEL}</span> '
            f'<span style="color:dodgerblue;"> {download_filename}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    if st.session_state.download_initiated:
        st.markdown(
            f"""
            <div style='
                background-color: #0c4145;
                color: #dffde9;
                padding: 1rem;
                border-radius: 0.5rem;
                border: 1px solid #1a5e31;
                font-size: 1rem;
                margin-bottom: 1rem;
                word-break: keep-all;
            '>{UI_SUCCESS_DOWNLOAD_MESSAGE}</div>
            """,
            unsafe_allow_html=True,
        )
        st.session_state.download_initiated = False
        
