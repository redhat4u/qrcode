# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from functions import generate_qr_code_png, generate_qr_code_svg, is_valid_color, sanitize_filename
from state_manager import set_download_initiated, reset_all_settings, on_qr_setting_change
from messages import get_message

def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    # 하드코딩된 값으로 유지해야 하는 파일 형식 변수
    FILE_FORMAT_PNG_RAW = "PNG"
    FILE_FORMAT_SVG_RAW = "SVG"

    st.header(get_message('UI_HEADER_PREVIEW_AND_GENERATE'))
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data

    file_format_is_svg = (st.session_state.file_format_select == FILE_FORMAT_SVG_RAW)
    
    is_pattern_color_valid_preview = (st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or (st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
    is_bg_color_valid_preview = (st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or (st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))

    # 입력값 유효성 검사
    if not current_data:
        st.info(get_message('UI_INFO_QR_GENERATION_GUIDE'))
        st.error(get_message('UI_ERROR_EMPTY_DATA'))
    elif not is_pattern_color_valid_preview or not is_bg_color_valid_preview:
        st.error(get_message('UI_ERROR_INVALID_QR_INPUT'))
        st.warning(get_message('UI_ERROR_INVALID_PATTERN_COLOR'))
        st.warning(get_message('UI_ERROR_INVALID_BG_COLOR'))
    else:
        pattern_color_final = st.session_state.custom_pattern_color_input_key if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.pattern_color_select
        bg_color_final = st.session_state.custom_bg_color_input_key if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.bg_color_select

        col_generate, col_reset = st.columns([1, 1])
        with col_generate:
            st.button(get_message('UI_BUTTON_GENERATE'), use_container_width=True, type="primary", key="generate_button", on_click=on_qr_setting_change)
        with col_reset:
            st.button(get_message('UI_BUTTON_RESET'), use_container_width=True, type="secondary", on_click=reset_all_settings) # <-- 이 부분입니다.

        if st.session_state.generate_button_clicked:
            try:
                if file_format_is_svg:
                    qr_img_buffer, _ = generate_qr_code_svg(
                        data=current_data,
                        box_size=st.session_state.box_size_input,
                        border=st.session_state.border_input,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        mask_pattern=st.session_state.mask_pattern_select,
                        fill_color=pattern_color_final,
                        back_color=bg_color_final
                    )
                    st.session_state.qr_svg_bytes = qr_img_buffer.getvalue()
                else:
                    qr_img, _ = generate_qr_code_png(
                        data=current_data,
                        box_size=st.session_state.box_size_input,
                        border=st.session_state.border_input,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        mask_pattern=st.session_state.mask_pattern_select,
                        fill_color=pattern_color_final,
                        back_color=bg_color_final,
                        dot_style=st.session_state.dot_style_select
                    )
                    buf = io.BytesIO()
                    qr_img.save(buf, format="PNG")
                    st.session_state.qr_image_bytes = buf.getvalue()

                st.session_state.qr_generated = True
                st.session_state.show_generate_success = True
            except Exception as e:
                st.session_state.error_message = str(e)

        if st.session_state.qr_generated:
            # 최종 파일명 설정
            now = datetime.now(ZoneInfo('Asia/Seoul'))
            default_filename = now.strftime("QR_%y%m%d_%H%M%S")
            final_filename = st.session_state.filename_input_key if st.session_state.filename_input_key else default_filename

            if file_format_is_svg:
                download_data = st.session_state.qr_svg_bytes
                download_mime = "image/svg+xml"
                download_extension = ".svg"
            else:
                download_data = st.session_state.qr_image_bytes
                download_mime = "image/png"
                download_extension = ".png"

            download_filename = f"{sanitize_filename(final_filename)}{download_extension}"

            st.markdown(get_message('UI_SUCCESS_MESSAGE'))

            col_preview, col_download = st.columns([1, 1])
            with col_preview:
                if file_format_is_svg:
                    st.image(download_data, use_column_width=True)
                else:
                    st.image(download_data, use_column_width=True)

            with col_download:
                st.download_button(
                    label=get_message('UI_DOWNLOAD_LABEL'),
                    data=download_data,
                    file_name=download_filename,
                    mime=download_mime,
                    use_container_width=True,
                    help=get_message('UI_DOWNLOAD_HELP'),
                    on_click=set_download_initiated,
                )
            
            # 파일명 관련 경고 및 정보 메시지
            if not st.session_state.filename_input_key:
                st.warning(get_message('UI_WARNING_EMPTY_FILENAME'))
            elif not sanitize_filename(st.session_state.filename_input_key):
                st.error(get_message('UI_WARNING_INVALID_FILENAME'))
            
            st.info(get_message('UI_DOWNLOAD_INFO').format(download_filename=download_filename))

        if st.session_state.error_message:
            st.error(st.session_state.error_message)
            
