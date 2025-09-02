# 이 파일은 생성된 QR 코드의 미리보기와 다운로드 UI를 정의합니다.
# ui_preview_and_download.py

import streamlit as st
import qrcode
import io
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from functions import (
    generate_qr_code_png,
    generate_qr_code_svg,
    is_valid_color,
    sanitize_filename,
)
from state_manager import set_download_initiated


def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    st.header("👀 미리보기 및 생성")

    # --- 실시간 미리보기 로직 시작 ---
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data

    file_format_is_svg = st.session_state.file_format_select == "SVG"

    # 유효성 검사 및 색상값 가져오기
    # 미리보기를 위한 색상 유효성 검사
    pattern_color_for_preview = (
        st.session_state.custom_pattern_color_input_key.strip()
        if st.session_state.pattern_color_select == "<직접 입력>"
        else st.session_state.pattern_color_select
    )
    bg_color_for_preview = (
        st.session_state.custom_bg_color_input_key.strip()
        if st.session_state.bg_color_select == "<직접 입력>"
        else st.session_state.bg_color_select
    )
    
    # 미리보기 이미지 생성
    preview_image_display = None
    preview_qr_object = None

    # 모든 조건이 충족될 때만 미리보기 이미지를 생성
    if (
        current_data
        and is_valid_color(pattern_color_for_preview)
        and is_valid_color(bg_color_for_preview)
        and pattern_color_for_preview != bg_color_for_preview
    ):
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction = error_correction_options[st.session_state.error_correction_select]

        # [수정] SVG 선택 시 미리보기 패턴과 색상을 강제로 기본값으로 변경
        if file_format_is_svg:
            preview_module_shape = "기본 사각형 (Square)"
            preview_pattern_color = "black"
            preview_bg_color = "white"
        else:
            preview_module_shape = st.session_state.module_shape_select
            preview_pattern_color = pattern_color_for_preview
            preview_bg_color = bg_color_for_preview

        img, qr = generate_qr_code_png(
            current_data,
            int(st.session_state.box_size_input),
            int(st.session_state.border_input),
            error_correction,
            int(st.session_state.mask_pattern_select),
            preview_pattern_color, # 수정된 미리보기 패턴 색상 사용
            preview_bg_color, # 수정된 미리보기 배경 색상 사용
            preview_module_shape, # 수정된 미리보기 모듈 모양 사용
        )
        if img and qr:
            preview_image_display = img
            preview_qr_object = qr

    # --- 실시간 미리보기 로직 끝 ---

    generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True)

    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None

        errors = []
        final_pattern_color = (
            st.session_state.custom_pattern_color_input_key.strip()
            if st.session_state.pattern_color_select == "<직접 입력>"
            else st.session_state.pattern_color_select
        )
        final_bg_color = (
            st.session_state.custom_bg_color_input_key.strip()
            if st.session_state.bg_color_select == "<직접 입력>"
            else st.session_state.bg_color_select
        )

        if not current_data:
            errors.append("⚠️ 생성할 QR 코드 내용을 입력해 주세요.")
            
        if not file_format_is_svg:
            if st.session_state.pattern_color_select == "<직접 입력>" and not final_pattern_color:
                errors.append("⚠️ 패턴 색의 HEX 값을 입력해 주세요.")
            elif st.session_state.pattern_color_select == "<직접 입력>" and not is_valid_color(final_pattern_color):
                errors.append("⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.")

            if st.session_state.bg_color_select == "<직접 입력>" and not final_bg_color:
                errors.append("⚠️ 배경 색의 HEX 값을 입력해 주세요.")
            elif st.session_state.bg_color_select == "<직접 입력>" and not is_valid_color(final_bg_color):
                errors.append("⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.")

            if final_pattern_color and final_bg_color and final_pattern_color == final_bg_color:
                errors.append("⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.")

        if errors:
            st.session_state.error_message = errors[0]
            st.session_state.show_generate_success = False
        else:
            st.session_state.error_message = None
            if st.session_state.file_format_select == "PNG":
                error_correction_options = {
                    "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
                    "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
                    "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
                    "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
                }
                error_correction = error_correction_options[st.session_state.error_correction_select]

                img, qr = generate_qr_code_png(
                    current_data,
                    int(st.session_state.box_size_input),
                    int(st.session_state.border_input),
                    error_correction,
                    int(st.session_state.mask_pattern_select),
                    final_pattern_color,
                    final_bg_color,
                    st.session_state.module_shape_select,
                )
                if img and qr:
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format="PNG")
                    st.session_state.qr_image_bytes = img_buffer.getvalue()
                    st.session_state.qr_svg_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
            else:  # SVG
                # [수정] SVG 다운로드 시에도 색상을 기본값으로 통일
                svg_data, qr = generate_qr_code_svg(
                    current_data,
                    int(st.session_state.box_size_input),
                    int(st.session_state.border_input),
                    st.session_state.error_correction_select,
                    int(st.session_state.mask_pattern_select),
                    "black", # SVG 색상 기본값으로 고정
                    "white", # SVG 색상 기본값으로 고정
                )
                if svg_data and qr:
                    st.session_state.qr_svg_bytes = svg_data.encode("utf-8")
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
    elif file_format_is_svg:
        st.info("💡 아래 미리보기는 SVG 형식의 한계로 인해 기본 사각형 패턴만 표시됩니다. [⚡ QR 코드 생성] 버튼을 클릭하면 SVG 파일이 생성됩니다.")
    elif pattern_color_for_preview == bg_color_for_preview and is_valid_color(pattern_color_for_preview) and is_valid_color(bg_color_for_preview):
        st.warning("⚠️ 미리보기를 위해 패턴과 배경 색상을 다르게 설정해 주세요.")
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
        st.info("QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다.")

    if preview_image_display:
        st.subheader("📱 QR 코드 미리보기")
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption="생성된 QR 코드", width=380)

        if preview_qr_object:
            st.info(
                f"""
            **QR 코드 정보**
            - QR 버전: {preview_qr_object.version}
            - 가로/세로 각 cell 개수: {preview_qr_object.modules_count}개
            - 이미지 크기 (참고): {(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)} x {(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)} px
            - 패턴 색상: {"black" if file_format_is_svg else pattern_color_for_preview}
            - 배경 색상: {"white" if file_format_is_svg else bg_color_for_preview}
            - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
            """
            )

    if st.session_state.get("qr_generated", False) and (
        st.session_state.get("qr_image_bytes") is not None
        or st.session_state.get("qr_svg_bytes") is not None
    ):
        st.markdown("---")
        st.subheader("📥 다운로드")
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
        else:  # SVG
            download_data = st.session_state.qr_svg_bytes
            download_mime = "image/svg+xml"
            download_extension = ".svg"

        download_filename = f"{sanitize_filename(final_filename)}{download_extension}"

        st.download_button(
            label="💾 QR 코드 다운로드",
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help="PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다.",
            on_click=set_download_initiated,
        )

        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">📄 다운로드 파일명: </span> '
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
