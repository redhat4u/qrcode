# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from messages import get_message
from functions import create_qr_code, get_qr_info, is_valid_hex_color, get_error_correction_constant
from state_manager import set_download_initiated

def build_preview_and_download_ui():
    """QR 코드 미리보기 및 다운로드 섹션을 생성합니다."""
    
    st.header(get_message("UI_HEADER_PREVIEW_AND_GENERATE"))
    
    # 세션 상태가 초기화되지 않았을 경우, 기본값 설정
    if 'qr_generated' not in st.session_state:
        st.session_state.qr_generated = False
    if 'qr_input_area' not in st.session_state:
        st.session_state.qr_input_area = ""
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        qr_data = qr_data.strip()

    # 입력창에 내용이 있을 때만 QR 코드 생성 및 미리보기 표시
    if qr_data:
        # 오류 보정 레벨을 문자열에서 상수로 변환
        error_correction_constant = get_error_correction_constant(st.session_state.error_correction_select)
        
        img_bytes, qr_version = create_qr_code(
            qr_data=qr_data,
            error_correction=error_correction_constant, # 변환된 상수 사용
            box_size=st.session_state.box_size_input,
            border=st.session_state.border_input,
            pattern_color=st.session_state.pattern_color_select,
            bg_color=st.session_state.bg_color_select,
            dot_style=st.session_state.dot_style_select,
            file_format=st.session_state.file_format_select
        )
        
        if img_bytes:
            st.session_state.qr_generated = True
            st.session_state.qr_version = qr_version

            # 미리보기 섹션
            st.subheader(get_message("UI_SUBHEADER_QR_PREVIEW"))
            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_PNG'):
                st.image(img_bytes, caption=get_message("UI_PREVIEW_IMAGE_CAPTION"))
                st.session_state.qr_image_bytes = img_bytes
                st.session_state.qr_svg_bytes = None
            elif st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'):
                st.image(img_bytes, caption=get_message("UI_PREVIEW_IMAGE_CAPTION"))
                st.session_state.qr_svg_bytes = img_bytes
                st.session_state.qr_image_bytes = None
            
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
            # QR 코드 생성에 실패하면 오류 메시지 표시
            st.error(st.session_state.error_message)
            st.session_state.qr_generated = False
            st.session_state.qr_image_bytes = None
            st.session_state.qr_svg_bytes = None
            
    else:
        st.info(get_message("UI_INFO_QR_GENERATION_GUIDE"))
        st.session_state.qr_generated = False
        st.session_state.qr_image_bytes = None
        st.session_state.qr_svg_bytes = None
        
