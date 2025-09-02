# 이 파일은 생성된 QR 코드의 미리보기와 다운로드 UI를 정의합니다.
# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from functions import generate_qr_code_png, generate_qr_code_svg, is_valid_color, sanitize_filename
from state_manager import set_download_initiated, reset_all_settings
from messages import get_message

def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    # 변수 초기화
    if 'show_generate_success' not in st.session_state:
        st.session_state.show_generate_success = False
    if 'download_initiated' not in st.session_state:
        st.session_state.download_initiated = False
    
    st.header(get_message('UI_HEADER_PREVIEW_AND_GENERATE'))
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data
    
    file_format_is_svg = (st.session_state.file_format_select == get_message('UI_FILE_FORMAT_SVG'))
    
    is_pattern_color_valid_preview = (st.session_state.pattern_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or (st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
    is_bg_color_valid_preview = (st.session_state.bg_color_select != get_message('UI_COLOR_OPTION_DIRECT_INPUT')) or (st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))
    
    pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.pattern_color_select
    bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.bg_color_select
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    error_correction_options = {
        get_message('UI_ERROR_CORRECTION_LEVEL_L'): qrcode.constants.ERROR_CORRECT_L,
        get_message('UI_ERROR_CORRECTION_LEVEL_M'): qrcode.constants.ERROR_CORRECT_M,
        get_message('UI_ERROR_CORRECTION_LEVEL_Q'): qrcode.constants.ERROR_CORRECT_Q,
        get_message('UI_ERROR_CORRECTION_LEVEL_H'): qrcode.constants.ERROR_CORRECT_H,
    }
    error_correction = error_correction_options[st.session_state.error_correction_select]

    preview_image_display = None
    preview_qr_object = None
    
    if current_data and not is_colors_same_preview:
        if file_format_is_svg:
            svg_data, qr = generate_qr_code_svg(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                int(st.session_state.mask_pattern_select), "black", "white"
            )
            if svg_data and qr:
                st.session_state.qr_svg_bytes = svg_data.encode('utf-8')
                preview_image_display = st.session_state.qr_svg_bytes
                preview_qr_object = qr
        else:
            img, qr = generate_qr_code_png(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                int(st.session_state.mask_pattern_select), pattern_color, bg_color, st.session_state.dot_style_select
            )
            if img and qr:
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.session_state.qr_image_bytes = buf.getvalue()
                preview_image_display = st.session_state.qr_image_bytes
                preview_qr_object = qr

    generate_btn = st.button(get_message('UI_BUTTON_GENERATE_QR'), use_container_width=True)
    
    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None
        
        errors = []
        final_pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.pattern_color_select
        final_bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') else st.session_state.bg_color_select
        
        if not current_data:
            errors.append(get_message('UI_ERROR_QR_DATA_MISSING'))
        
        if not file_format_is_svg:
            if st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not final_pattern_color:
                errors.append(get_message('UI_ERROR_PATTERN_COLOR_HEX_MISSING'))
            elif st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not is_valid_color(final_pattern_color):
                errors.append(get_message('UI_ERROR_INVALID_PATTERN_COLOR'))
            
            if st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not final_bg_color:
                errors.append(get_message('UI_ERROR_BG_COLOR_HEX_MISSING'))
            elif st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not is_valid_color(final_bg_color):
                errors.append(get_message('UI_ERROR_INVALID_BG_COLOR'))
                
            if final_pattern_color and final_bg_color and final_pattern_color == final_bg_color:
                errors.append(get_message('UI_ERROR_SAME_COLOR'))

        if errors:
            st.session_state.error_message = errors[0]
            st.session_state.show_generate_success = False
        else:
            st.session_state.error_message = None
            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_PNG'):
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
             """
             <div style='
                 background-color: #0c4145;
                 color: #dffde9;
                 padding: 1rem;
                 border-radius: 0.5rem;
                 border: 1px solid #1a5e31;
                 font-size: 1rem;
                 margin-bottom: 1rem;
                 word-break: keep-all;
             '>
                 ✅ QR 코드 생성 완료!!<br>
                 반드시 파일명을 확인하시고, 화면 아래의 [💾 QR 코드 다운로드] 버튼을 클릭하세요.
             </div>
             """,
             unsafe_allow_html=True,
         )
    elif st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not st.session_state.custom_pattern_color_input_key:
        st.warning(get_message('UI_WARNING_PATTERN_COLOR_INPUT'))
    elif st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not st.session_state.custom_bg_color_input_key:
        st.warning(get_message('UI_WARNING_BG_COLOR_INPUT'))
    elif (st.session_state.pattern_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not is_valid_color(st.session_state.custom_pattern_color_input_key)) or \
         (st.session_state.bg_color_select == get_message('UI_COLOR_OPTION_DIRECT_INPUT') and not is_valid_color(st.session_state.custom_bg_color_input_key)):
        st.warning(get_message('UI_WARNING_INVALID_COLOR_HEX'))
    elif is_colors_same_preview:
        st.warning(get_message('UI_WARNING_SAME_COLOR'))
    elif preview_image_display:
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
                 word-break: keep-all;
             '>
                 ✅ 현재 입력된 내용으로 QR 코드를 미리 표현해 보았습니다.<br>
                 아래의 QR 코드가 맘에 드시면, 위의 [⚡ QR 코드 생성] 버튼을 클릭하세요.
             </div>
             """,
             unsafe_allow_html=True,
         )
    else:
        st.info(get_message('UI_INFO_QR_GENERATION_GUIDE'))

    if preview_image_display and preview_qr_object:
        st.subheader(get_message('UI_SUBHEADER_QR_PREVIEW'))
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=get_message('UI_PREVIEW_IMAGE_CAPTION'), width=380)
        
        st.info(f"""
        **{get_message('UI_INFO_QR_CODE_INFO_TITLE')}**
        - {get_message('UI_INFO_QR_VERSION')}: {preview_qr_object.version}
        - {get_message('UI_INFO_QR_CELL_COUNT')}: {preview_qr_object.modules_count}개
        - {get_message('UI_INFO_QR_IMAGE_SIZE_REFERENCE')}: {(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)} x {(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)} px
        - {get_message('UI_INFO_QR_PATTERN_COLOR')}: {"black" if file_format_is_svg else pattern_color}
        - {get_message('UI_INFO_QR_BG_COLOR')}: {"white" if file_format_is_svg else bg_color}
        - {get_message('UI_INFO_QR_IMAGE_SIZE_FORMULA')}
        """)
    
    if st.session_state.get('qr_generated', False) and (st.session_state.get('qr_image_bytes') is not None or st.session_state.get('qr_svg_bytes') is not None):
        st.markdown("---")
        st.subheader(get_message('UI_SUBHEADER_DOWNLOAD'))

        col_generate, col_reset = st.columns([1, 1])
        
        with col_generate:
            now = datetime.now(ZoneInfo("Asia/Seoul"))
            current_filename = st.session_state.filename_input_key.strip()
            final_filename = current_filename if current_filename else now.strftime("QR_%Y-%m-%d_%H-%M-%S")
            
            download_data = None
            download_mime = ""
            download_extension = ""

            if st.session_state.file_format_select == get_message('UI_FILE_FORMAT_PNG'):
                download_data = st.session_state.qr_image_bytes
                download_mime = "image/png"
                download_extension = ".png"
            else: # SVG
                download_data = st.session_state.qr_svg_bytes
                download_mime = "image/svg+xml"
                download_extension = ".svg"
            
            download_filename = f"{sanitize_filename(final_filename)}{download_extension}"
            
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


        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">📄 {get_message("UI_DOWNLOAD_FILENAME_LABEL")}: </span> '
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
                word-break: keep-all;
            '>
                ✅ QR 코드 다운로드 완료!!<br>
                휴대폰은 'Download' 폴더에 저장됩니다.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.session_state.download_initiated = False
        
