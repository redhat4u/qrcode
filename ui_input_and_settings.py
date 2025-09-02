import streamlit as st

def build_input_and_settings_ui():
    """
    사용자 입력 및 QR 코드 설정 UI를 렌더링합니다.
    """
    st.subheader("입력 및 설정")
    
    st.text_area(
        label="QR 코드로 만들 텍스트/URL",
        key="qr_data",
        value=st.session_state.get("qr_data", ""),
        help="여기에 텍스트나 URL을 입력하세요. 100자까지 지원됩니다."
    )
    
    st.subheader("스타일")
    st.selectbox(
        label="점 스타일",
        options=["사각형", "둥근 사각", "원형", "마름모"],
        key="dot_style",
        index=0,
    )
    
    st.color_picker(
        label="패턴 색상",
        key="fill_color",
        value="#000000"
    )

    st.color_picker(
        label="배경 색상",
        key="back_color",
        value="#FFFFFF"
    )

    st.subheader("고급 옵션")
    st.selectbox(
        label="오류 보정 레벨",
        options=["L (7% 보정)", "M (15% 보정)", "Q (25% 보정)", "H (30% 보정)"],
        key="error_correction",
        index=3,
    )

    st.slider(
        label="상자 크기",
        key="box_size",
        min_value=1,
        max_value=20,
        value=10,
    )

    st.slider(
        label="테두리 너비",
        key="border",
        min_value=1,
        max_value=10,
        value=4,
    )

    st.slider(
        label="마스크 패턴 (고정)",
        key="mask_pattern",
        min_value=0,
        max_value=7,
        value=0,
    )
