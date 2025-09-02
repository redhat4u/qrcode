# 이 파일은 QR 코드 생성에 필요한 입력 및 설정 UI를 정의합니다.
# ui_input_and_settings.py

import streamlit as st
import qrcode
from functions import (
    sanitize_filename,
    is_valid_color,
)
from state_manager import (
    clear_text_input,
    clear_filename_callback,
    on_qr_setting_change,
)

def build_input_and_settings_ui():
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
        
    # 새로운 패턴 스타일 선택 드롭다운 메뉴 추가
    st.markdown("---")
    st.subheader("🛠️ 패턴 모양")
    st.selectbox("패턴 모양 선택", options=["사각형", "원형", "둥근 원형"], key="dot_style_select", on_change=on_qr_setting_change, disabled=file_format_is_svg)

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
