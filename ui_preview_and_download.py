import streamlit as st
import io
from functions import is_valid_color, sanitize_filename, generate_qr_code_png, generate_qr_code_svg, get_error_correction_constant, get_qr_info, get_message

def build_preview_and_download_ui(qr_data, selected_options):
    st.subheader(get_message('UI_PREVIEW_SECTION_TITLE'))

    if not qr_data:
        st.info(get_message('UI_INFO_ENTER_TEXT'))
        return

    # 유효성 검사
    fill_color = selected_options['fill_color']
    back_color = selected_options['back_color']
    
    if not is_valid_color(fill_color) or not is_valid_color(back_color):
        st.error(get_message('UI_ERROR_INVALID_COLOR_FORMAT'))
        return
        
    if fill_color.lower() == back_color.lower():
        st.warning(get_message('UI_WARNING_SAME_COLOR'))
        return

    # QR 코드 생성
    try:
        error_correction = get_error_correction_constant(selected_options['error_correction'])

        qr_image, qr_instance = generate_qr_code_png(
            data=qr_data,
            box_size=selected_options['box_size'],
            border=selected_options['border'],
            error_correction=error_correction,
            mask_pattern=selected_options['mask_pattern'],
            fill_color=fill_color,
            back_color=back_color,
            dot_style=selected_options['dot_style']
        )
        
        svg_data, _ = generate_qr_code_svg(
            data=qr_data,
            box_size=selected_options['box_size'],
            border=selected_options['border'],
            error_correction=error_correction,
            mask_pattern=selected_options['mask_pattern'],
            fill_color=fill_color,
            back_color=back_color,
        )

        if qr_image and svg_data:
            png_buffer = io.BytesIO()
            qr_image.save(png_buffer, format='PNG')
            
            # 미리보기 및 정보 표시
            st.image(png_buffer.getvalue(), caption=get_message('UI_PREVIEW_IMAGE_CAPTION'))
            
            # 파일 다운로드 버튼
            filename = sanitize_filename(qr_data)
            st.download_button(
                label=get_message('UI_DOWNLOAD_PNG_BUTTON'),
                data=png_buffer.getvalue(),
                file_name=f"{filename}.png",
                mime="image/png"
            )
            st.download_button(
                label=get_message('UI_DOWNLOAD_SVG_BUTTON'),
                data=svg_data,
                file_name=f"{filename}.svg",
                mime="image/svg+xml"
            )
            
            # QR 코드 정보 표시
            st.subheader("QR 코드 상세 정보")
            qr_info = get_qr_info(
                qr_instance.version, 
                selected_options['box_size'], 
                selected_options['border'], 
                fill_color, 
                back_color
            )
            for key, value in qr_info.items():
                st.write(f"**{key}:** {value}")

    except Exception as e:
        st.error(f"QR 코드 생성 중 오류가 발생했습니다: {e}")
