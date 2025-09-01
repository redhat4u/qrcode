# 이 파일은 Streamlit 위젯을 사용하여 앱의 각 UI 섹션을 생성하는 함수들을 정의합니다.
# ui_components.py

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo

from functions import (
   sanitize_filename,
   is_valid_color,
   generate_qr_code_png,
   generate_qr_code_svg,
)

from state_manager import (
   clear_text_input,
   clear_filename_callback,
   on_qr_setting_change,
   set_download_initiated,
)

def build_input_ui():
    """입력 및 설정 섹션을 빌드합니다."""
    st.header("⚙️ 입력 및 설정")
    
    # QR 코드 내용 입력
    st.subheader("📝 QR 코드 내용")
    st.info("최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.")
    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=200,
        placeholder="이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.",
        key="qr_input_area",
        on_change=on_qr_setting_change
    )
    
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(f"⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)")
        elif char_count > 2400:
            st.warning(f"⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 문자 수에 근접)")
        else:
            st.success(f"✅ 현재 입력된 총 문자 수: **{char_count}**")
    else:
        st.caption("현재 입력된 총 문자 수: 0")
        
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            "🗑️ 입력 내용 삭제",
            help="입력한 내용을 전부 삭제합니다 (파일명은 유지)",
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change
    )

    st.markdown("---")
    st.markdown("---")
    
    # QR 코드 설정
    st.subheader("🛠️ QR 코드 설정")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.number_input("QR 코드 1개의 사각 cell 크기 (px)", min_value=1, max_value=100, key="box_size_input", on_change=on_qr_setting_change)
        st.number_input("QR 코드 테두리/여백", min_value=0, max_value=10, key="border_input", on_change=on_qr_setting_change)
    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        st.selectbox("오류 보정 레벨", list(error_correction_options.keys()), key="error_correction_select", on_change=on_qr_setting_change)
        st.selectbox("마스크 패턴 선택 (0~7)", options=list(range(8)), key="mask_pattern_select", on_change=on_qr_setting_change)
        
    st.markdown("---")
    st.subheader("🛠️ 색상 설정")
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    if file_format_is_svg:
        st.warning("⚠️ SVG 파일은 벡터 형식이므로 원하는 색상을 선택할 수 없습니다. 다양한 색상을 원한다면 'PNG' 형식을 선택하세요.")

    colors = [
        "<직접 입력>", "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        st.selectbox("패턴 색상", colors, key="pattern_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)
    with col1_4:
        st.selectbox("배경 색상", colors, key="bg_color_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

    st.markdown("원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.")
    st.caption("예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)")
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input("패턴 색상 HEX 값", placeholder="예: #000000", disabled=(st.session_state.pattern_color_select != "<직접 입력>") or file_format_is_svg, key="custom_pattern_color_input_key", on_change=on_qr_setting_change)
    with col1_6:
        st.text_input("배경 색상 HEX 값", placeholder="예: #FFFFFF", disabled=(st.session_state.bg_color_select != "<직접 입력>") or file_format_is_svg, key="custom_bg_color_input_key", on_change=on_qr_setting_change)

    st.markdown("---")
    st.subheader("🛠️ 파일 설정")
    col_filename_input, col_filename_delete = st.columns([3, 1.1])
    with col_filename_input:
        st.text_input("다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)", placeholder="이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)", key="filename_input_key")
    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button("🗑️ 파일명 삭제", help="입력한 파일명을 삭제합니다", use_container_width=True, type="secondary", disabled=filename_delete_disabled, on_click=clear_filename_callback)

    st.radio("파일 형식 선택", ("PNG", "SVG"), index=0 if st.session_state.file_format_select == "PNG" else 1, key="file_format_select", on_change=on_qr_setting_change)


def build_preview_and_download_ui():
    """미리보기 및 다운로드 섹션을 빌드합니다."""
    st.header("👀 미리보기 및 생성")
    
    qr_data = st.session_state.qr_input_area
    if st.session_state.strip_option:
        current_data = qr_data.strip()
    else:
        current_data = qr_data
    
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    is_pattern_color_valid_preview = (st.session_state.pattern_color_select != "<직접 입력>") or (st.session_state.pattern_color_select == "<직접 입력>" and st.session_state.custom_pattern_color_input_key and is_valid_color(st.session_state.custom_pattern_color_input_key))
    is_bg_color_valid_preview = (st.session_state.bg_color_select != "<직접 입력>") or (st.session_state.bg_color_select == "<직접 입력>" and st.session_state.custom_bg_color_input_key and is_valid_color(st.session_state.custom_bg_color_input_key))
    
    pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == "<직접 입력>" else st.session_state.pattern_color_select
    bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == "<직접 입력>" else st.session_state.bg_color_select
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
        img, qr = generate_qr_code_png(
            current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
            int(st.session_state.mask_pattern_select),
            "black" if file_format_is_svg else pattern_color,
            "white" if file_format_is_svg else bg_color,
        )
        if img and qr:
            preview_image_display = img
            preview_qr_object = qr

    generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True)
    
    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None
        
        errors = []
        final_pattern_color = st.session_state.custom_pattern_color_input_key.strip() if st.session_state.pattern_color_select == "<직접 입력>" else st.session_state.pattern_color_select
        final_bg_color = st.session_state.custom_bg_color_input_key.strip() if st.session_state.bg_color_select == "<직접 입력>" else st.session_state.bg_color_select
        
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
                img, qr = generate_qr_code_png(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), final_pattern_color, final_bg_color,
                )
                if img and qr:
                    img_buffer = io.BytesIO() # st.io.BytesIO() -> io.BytesIO()로 수정
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
        st.success("✅ QR 코드 생성 완료!! 반드시 파일명을 확인하고, 화면 아래의 [💾 QR 코드 다운로드] 버튼을 클릭하세요.")
    elif preview_image_display:
        st.success("현재 입력된 내용으로 생성될 QR 코드를 미리 표현해 보았습니다. 이 QR 코드가 맘에 드신다면, 위의 [⚡ QR 코드 생성] 버튼을 클릭하세요.")
    else:
        st.info("QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다.")

    if preview_image_display:
        st.subheader("📱 QR 코드 미리보기")
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption="생성된 QR 코드", width=380)
        
        if preview_qr_object:
            st.info(f"""
            **QR 코드 정보**
            - QR 버전: {preview_qr_object.version}
            - 가로/세로 각 cell 개수: {preview_qr_object.modules_count}개
            - 이미지 크기 (참고): {(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)} x {(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)} px
            - 패턴 색상: {"black" if file_format_is_svg else pattern_color}
            - 배경 색상: {"white" if file_format_is_svg else bg_color}
            - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
            """)
    
    if st.session_state.get('qr_generated', False) and (st.session_state.get('qr_image_bytes') is not None or st.session_state.get('qr_svg_bytes') is not None):
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
        else: # SVG
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
            st.success("✅ 생성한 QR 코드를 다운로드할 수 있습니다! 휴대폰은 'Download' 폴더에 저장됩니다.")
            st.session_state.download_initiated = False

