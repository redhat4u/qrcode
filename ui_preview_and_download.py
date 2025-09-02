# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from functions import sanitize_filename
from state_manager import reset_all_settings, set_download_initiated
from messages import get_message

def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    st.header(get_message('UI_HEADER_PREVIEW_AND_GENERATE'))
    
    qr_data = st.session_state.qr_input_area
    
    if st.session_state.qr_generated:
        # QR 코드 이미지를 중앙에 정렬하고 크기를 380px로 고정
        col_left, col_center, col_right = st.columns([1, 1, 1])
        
        with col_center:
            # QR 코드 이미지 표시
            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
                if st.session_state.qr_svg_bytes:
                    st.image(st.session_state.qr_svg_bytes, width=380, use_container_width=False)
            else:
                if st.session_state.qr_image_bytes:
                    st.image(st.session_state.qr_image_bytes, width=600, use_container_width=False)
                    
        st.success(get_message('UI_SUCCESS_MESSAGE'))

        # 다운로드 버튼 및 기타 정보 표시
        col_generate, col_reset = st.columns([1, 1])
        with col_generate:
            # 최종 파일명 설정
            now = datetime.now(ZoneInfo('Asia/Seoul'))
            default_filename = now.strftime("QR_%y%m%d_%H%M%S")
            final_filename = st.session_state.filename_input_key if st.session_state.filename_input_key else default_filename
            download_filename = f"{sanitize_filename(final_filename)}.{st.session_state.file_format_select.lower()}"
            
            # 다운로드 버튼
            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
                download_data = st.session_state.qr_svg_bytes
                download_mime = "image/svg+xml"
            else:
                download_data = st.session_state.qr_image_bytes
                download_mime = "image/png"

            st.download_button(
                label=get_message('UI_DOWNLOAD_LABEL'),
                data=download_data,
                file_name=download_filename,
                mime=download_mime,
                use_container_width=True,
                help=get_message('UI_DOWNLOAD_HELP'),
                on_click=set_download_initiated,
            )
            
        with col_reset:
            st.button(get_message('UI_BUTTON_RESET'), use_container_width=True, type="secondary", on_click=reset_all_settings)
        
        # 파일명 관련 경고 및 정보 메시지
        if not st.session_state.filename_input_key:
            st.warning(get_message('UI_WARNING_EMPTY_FILENAME'))
        elif not sanitize_filename(st.session_state.filename_input_key):
            st.error(get_message('UI_WARNING_INVALID_FILENAME'))
        
        st.info(get_message('UI_DOWNLOAD_INFO').format(download_filename=download_filename))
            
    elif st.session_state.error_message:
        st.error(st.session_state.error_message)
    elif not qr_data:
        st.info(get_message('UI_INFO_QR_GENERATION_GUIDE'))
    else:
        # 유효성 검사 실패 시
        is_pattern_color_valid_preview = (st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or (st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
        is_bg_color_valid_preview = (st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or (st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))
        
        if not is_pattern_color_valid_preview or not is_bg_color_valid_preview:
            st.error(get_message('UI_ERROR_INVALID_QR_INPUT'))
            if not is_pattern_color_valid_preview:
                st.warning(get_message('UI_ERROR_INVALID_PATTERN_COLOR'))
            if not is_bg_color_valid_preview:
                st.warning(get_message('UI_ERROR_INVALID_BG_COLOR'))
                
