# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from messages import get_message
from functions import create_qr_code, get_qr_info, is_valid_hex_color
from state_manager import set_download_initiated

def build_preview_and_download_ui():
    """QR 코드 미리보기 및 다운로드 섹션을 생성합니다."""
    
    st.header(get_message("UI_HEADER_PREVIEW_AND_GENERATE"))
    
    # QR 코드 생성 버튼
    generate_button_clicked = st.button(
        get_message("UI_BUTTON_GENERATE_QR"), 
        use_container_width=True, 
        key='generate_button'
    )

    if 'qr_generated' not in st.session_state:
        st.session_state.qr_generated = False

    if 'generate_button_clicked' not in st.session_state:
        st.session_state.generate_button_clicked = False
    
    # generate_button_clicked 상태 업데이트
    if generate_button_clicked:
        st.session_state.generate_button_clicked = True
        st.session_state.show_generate_success = False

    if st.session_state.generate_button_clicked:
        # 입력 값 가져오기
        qr_data = st.session_state.qr_input_area
        
        # 유효성 검사
        if not qr_data.strip():
            st.error(get_message("UI_ERROR_QR_DATA_MISSING"))
            st.session_state.qr_generated = False
            return
            
        # Strip whitespace if option is selected
        if st.session_state.strip_option:
            qr_data = qr_data.strip()
            
        # 색상 유효성 검사
        if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
            if not st.session_state.custom_pattern_color_input_key:
                st.warning(get_message("UI_WARNING_PATTERN_COLOR_INPUT"))
                st.session_state.qr_generated = False
                return
            if not is_valid_hex_color(st.session_state.custom_pattern_color_input_key):
                st.warning(get_message("UI_WARNING_INVALID_COLOR_HEX"))
                st.session_state.qr_generated = False
                return

        if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
            if not st.session_state.custom_bg_color_input_key:
                st.warning(get_message("UI_WARNING_BG_COLOR_INPUT"))
                st.session_state.qr_generated = False
                return
            if not is_valid_hex_color(st.session_state.custom_bg_color_input_key):
                st.warning(get_message("UI_WARNING_INVALID_COLOR_HEX"))
                st.session_state.qr_generated = False
                return
        
        # 패턴과 배경 색상이 같은 경우 경고
        if st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT') and st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
            if st.session_state.pattern_color_select == st.session_state.bg_color_select:
                st.warning(get_message('UI_WARNING_SAME_COLOR'))
                st.session_state.qr_generated = False
                return

        # QR 코드 생성
        img_bytes, qr_version = create_qr_code(
            qr_data=qr_data,
            error_correction=st.session_state.error_correction_select,
            box_size=st.session_state.box_size_input,
            border=st.session_state.border_input,
            pattern_color=st.session_state.pattern_color_select,
            bg_color=st.session_state.bg_color_select,
            dot_style=st.session_state.dot_style_select,
            file_format=st.session_state.file_format_select
        )
        
        if img_bytes:
            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_PNG'):
                st.session_state.qr_image_bytes = img_bytes
                st.session_state.qr_svg_bytes = None
            elif st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
                st.session_state.qr_svg_bytes = img_bytes
                st.session_state.qr_image_bytes = None

            st.session_state.qr_generated = True
            st.session_state.qr_version = qr_version
            st.session_state.show_generate_success = True
        else:
            st.session_state.qr_generated = False
            
    # 미리보기 섹션
    st.subheader(get_message("UI_SUBHEADER_QR_PREVIEW"))
    if st.session_state.qr_generated:
        if st.session_state.qr_image_bytes:
            st.image(st.session_state.qr_image_bytes, caption=get_message("UI_PREVIEW_IMAGE_CAPTION"))
        elif st.session_state.qr_svg_bytes:
            st.image(st.session_state.qr_svg_bytes, caption=get_message("UI_PREVIEW_IMAGE_CAPTION"))
            
        st.markdown("---")
        
        # QR 코드 상세 정보
        st.subheader(get_message("UI_INFO_QR_CODE_INFO_TITLE"))
        qr_info = get_qr_info(
            st.session_state.qr_version,
            st.session_state.box_size_input,
            st.session_state.border_input,
            st.session_state.pattern_color_select,
            st.session_state.bg_color_select
        )
        for key, value in qr_info.items():
            st.markdown(f"**{key}**: {value}")

        st.markdown(f"_{get_message('UI_INFO_QR_IMAGE_SIZE_FORMULA')}_")

        # 다운로드 섹션
        st.markdown("---")
        st.subheader(get_message("UI_SUBHEADER_DOWNLOAD"))
        
        file_extension = "png" if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_PNG') else "svg"
        filename = st.session_state.filename_input_key.strip()
        if not filename:
            filename = "qrcode"
        download_filename = f"{filename}.{file_extension}"

        if st.session_state.qr_image_bytes or st.session_state.qr_svg_bytes:
            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_PNG'):
                st.download_button(
                    label=get_message("UI_DOWNLOAD_LABEL"),
                    data=st.session_state.qr_image_bytes,
                    file_name=download_filename,
                    mime="image/png",
                    use_container_width=True,
                    on_click=set_download_initiated
                )
            elif st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
                st.download_button(
                    label=get_message("UI_DOWNLOAD_LABEL"),
                    data=st.session_state.qr_svg_bytes,
                    file_name=download_filename,
                    mime="image/svg+xml",
                    use_container_width=True,
                    on_click=set_download_initiated
                )
    else:
        st.info(get_message("UI_INFO_QR_GENERATION_GUIDE"))
        
