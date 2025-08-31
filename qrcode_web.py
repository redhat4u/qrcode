"""
QR 코드 생성 웹앱 - Streamlit 버전
휴대폰에서도 사용 가능

로컬 실행 방법:
1. pip install streamlit qrcode[pil]
2. streamlit run qrcode_web.py

또는 온라인에서 실행:
- Streamlit Cloud, Heroku, Replit 등에 배포 가능
"""


import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image
import re

# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔲",
    layout="wide"
)

# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    """파일명에서 사용할 수 없는 문자를 '_'로 대체합니다."""
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()

# 색상 유효성 검사 함수
def is_valid_color(color: str) -> bool:
    """입력된 문자열이 유효한 CSS 색상명 또는 HEX 코드인지 확인합니다."""
    # HEX 코드 패턴 (#, rgb, rgba, hsl, hsla 등은 제외)
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    
    # 일반적인 CSS 색상명 목록 (모든 색상명을 포함할 수는 없으므로 일부만 체크)
    basic_colors = {'black', 'white', 'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'gray', 'lightgray', 'brown', 'navy', 'crimson', 'gold'}
    
    return bool(hex_pattern.match(color)) or color.lower() in basic_colors or len(color.strip()) > 0 # 직접입력 시 공백만 아니면 일단 통과

# QR 코드 생성 함수
def generate_qr_code(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
    """주어진 설정으로 QR 코드를 생성하고 PIL Image 객체를 반환합니다."""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )
        qr.add_data(data, optimize=0)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Streamlit과 호환되도록 RGB로 변환 (PIL Image 객체인 경우)
        if hasattr(img, 'convert'):
            img = img.convert('RGB')
        
        return img, qr
    except Exception as e:
        st.error(f"QR 코드 생성 오류: {str(e)}")
        return None, None

# 세션 상태 초기화
if 'qr_image' not in st.session_state:
    st.session_state.qr_image = None
if 'qr_info' not in st.session_state:
    st.session_state.qr_info = None
if 'last_qr_data' not in st.session_state:
    st.session_state.last_qr_data = ""
if 'qr_generated_once' not in st.session_state:
    st.session_state.qr_generated_once = False


# QR 내용 초기화 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""
    st.session_state.qr_image = None
    st.session_state.qr_info = None
    st.session_state.last_qr_data = ""
    st.session_state.qr_generated_once = False


# 모든 입력창 초기화 함수
def clear_all_inputs():
    st.session_state.qr_input_area = ""
    st.session_state.filename_input = ""
    st.session_state.qr_image = None
    st.session_state.qr_info = None
    st.session_state.last_qr_data = ""
    st.session_state.qr_generated_once = False

# 메인 앱 ============================================================================================

st.title("🔲 QR 코드 생성기")
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header("⚙️ 입력 및 설정")
    
    # QR 코드 입력창
    st.subheader("📝 QR 코드 내용")
    st.info("최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.")
    
    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=200,
        placeholder="이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.",
        key="qr_input_area"
    )
    
    # 문자 수 표시
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
        
    # 입력 내용 삭제 버튼 - 입력 내용이 있을 때만 활성화
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        if st.button("🗑️ 입력 내용 삭제", help="입력한 내용을 전부 삭제합니다 (파일명은 유지)", use_container_width=True, type="secondary", disabled=delete_btn_disabled):
            clear_text_input()
            st.rerun()
    
    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=True,
        help="입력된 내용 맨끝에 공백/줄바꿈 문자가 한개라도 포함되면 완전히 다른 QR코드가 생성됩니다. 입력된 마지막 문자 뒤에 공백/줄바꿈이 추가되어도 QR코드에 반영되지 않도록 하고 싶다면, 이 옵션을 켜 두세요."
    )
    
    st.markdown("---")
    
    # QR 코드 설정
    st.subheader("🔧 QR 코드 설정")
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input("QR 코드 1개의 사각 cell 크기 (px)", min_value=1, max_value=100, value=20, key="box_size_input")
        border = st.number_input("QR 코드 테두리/여백", min_value=0, max_value=10, value=2, key="border_input")
    
    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H
        }
        error_correction_choice = st.selectbox("오류 보정 레벨", list(error_correction_options.keys()), index=0, key="error_correction_choice")
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox("마스크 패턴 선택 (0~7)", options=list(range(8)), index=2, key="mask_pattern_choice")
    
    st.markdown("---")
    st.subheader("🔧 색상 설정")
    
    colors = [
        "<직접 선택>", "black", "white", "gray", "lightgray", 
        "lightyellow", "lightgreen", "lightcoral", "lightblue",
        "red", "green", "blue", "purple", "orange", "orangered",
        "darkorange", "maroon", "yellow", "brown", "navy", "mediumblue",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox("패턴 색상", colors, index=1, key="pattern_color_choice")
    with col1_4:
        bg_color_choice = st.selectbox("배경 색상", colors, index=2, key="bg_color_choice")
    
    st.markdown("원하는 색상이 리스트에 없다면, 아래에 직접 색상을 입력하세요.")
    st.caption("색상명 (예: crimson, gold) 또는 HEX 코드 (예: #FF5733, #00FF00)를 입력할 수 있습니다.")
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        custom_pattern_color = st.text_input("패턴 색상 직접 입력", placeholder="예: crimson 또는 #FF0000", disabled=(pattern_color_choice != "<직접 선택>"), key="custom_pattern_color")
    with col1_6:
        custom_bg_color = st.text_input("배경 색상 직접 입력", placeholder="예: lightcyan 또는 #E0FFFF", disabled=(bg_color_choice != "<직접 선택>"), key="custom_bg_color")
    
    pattern_color = custom_pattern_color if pattern_color_choice == "<직접 선택>" and custom_pattern_color else pattern_color_choice
    bg_color = custom_bg_color if bg_color_choice == "<직접 선택>" and custom_bg_color else bg_color_choice
    
    st.markdown("---")

    st.subheader("🔧 파일 설정")
    
    filename = st.text_input(
        "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)",
        placeholder="이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
        key="filename_input"
    )

with col2:
    st.header("👀 미리보기 및 다운로드")

    # 실시간으로 QR 코드 생성 및 미리보기
    current_data = qr_data.strip() if strip_option else qr_data
    
    # 유효성 검사 메시지
    if not current_data:
        st.warning("⚠️ QR 코드에 포함할 내용을 입력해 주세요.")
    elif pattern_color == bg_color:
        st.error("❌ 패턴과 배경은 같은 색을 사용할 수 없습니다.")
    elif pattern_color_choice == "<직접 선택>" and not is_valid_color(custom_pattern_color):
        st.error("❌ 유효한 패턴 색상을 입력해 주세요.")
    elif bg_color_choice == "<직접 선택>" and not is_valid_color(custom_bg_color):
        st.error("❌ 유효한 배경 색상을 입력해 주세요.")
    else:
        # 입력 데이터나 설정이 변경되었을 때만 QR 코드 재생성
        current_settings = (current_data, box_size, border, error_correction, mask_pattern, pattern_color, bg_color)
        if current_settings != st.session_state.get('last_settings'):
            img, qr = generate_qr_code(current_data, int(box_size), int(border), error_correction, int(mask_pattern), pattern_color, bg_color)
            
            if img and qr:
                st.session_state.qr_image = img
                st.session_state.last_qr_data = current_data
                st.session_state.last_settings = current_settings
                
                # QR 코드 정보 텍스트 생성
                st.session_state.qr_info = f"""
                **QR 코드 정보**
                - QR 버전: {qr.version}
                - 가로/세로 각 cell 개수: {qr.modules_count}개
                - 이미지 크기: {img.size[0]} x {img.size[1]} px
                - 패턴 색상: {pattern_color}
                - 배경 색상: {bg_color}
                - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
                """
        
        # QR 코드 이미지가 존재하고 입력 내용이 변경되지 않았을 때만 표시
        if st.session_state.qr_image and current_data == st.session_state.last_qr_data:
            st.subheader("📱 QR 코드 미리보기")
            st.image(st.session_state.qr_image, caption="생성된 QR 코드", use_column_width="auto")
            st.info(st.session_state.qr_info)
            st.session_state.qr_generated_once = True

    st.markdown("---")

    # 다운로드 섹션 - QR 코드가 한 번이라도 성공적으로 생성되었을 때만 표시
    if st.session_state.qr_generated_once:
        st.subheader("📥 다운로드")
        
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        current_filename = filename.strip()
        
        # 파일명이 비어있으면 자동 생성
        if not current_filename:
            final_filename = now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        else:
            final_filename = current_filename
            
        download_filename = f"{sanitize_filename(final_filename)}.png"
        
        # 이미지 객체를 바이트로 변환
        if st.session_state.qr_image:
            img_buffer = io.BytesIO()
            st.session_state.qr_image.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
        
            st.download_button(
                label="💾 QR 코드 다운로드",
                data=img_bytes,
                file_name=download_filename,
                mime="image/png",
                use_container_width=True,
                help="PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다."
            )
            
            # 다운로드 파일명 미리보기
            st.markdown(
                f'<p style="font-size:18px;">'
                f'<span style="color:darkorange; font-weight:bold;">📄 다운로드 파일명: </span> '
                f'<span style="color:dodgerblue;"> {download_filename}</span>'
                f'</p>',
                unsafe_allow_html=True
            )

# 사이드바
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용**에 변환할 텍스트를 입력하세요.
    2. **QR 코드 설정**에서 크기, 여백, 오류 보정 레벨 등을 조정하세요.
    3. **색상 설정**에서 패턴과 배경 색상을 선택하세요.
    4. 입력/설정을 변경하면 **실시간으로 미리보기**가 업데이트됩니다.
    5. 원하는 결과가 나오면 **다운로드** 버튼을 클릭하여 파일을 저장하세요.
    """)
    st.markdown("""---""")
    st.header("💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com` 
    - **전화번호**: `tel:010-1234-5678`
    - **SMS**: `sms:010-1234-5678`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
    """)
    st.markdown("""---""")
    st.header("⚙️ 설정 가이드")
    st.markdown("""
    **오류 보정 레벨:**
    - **Low (7%)**: 손상되지 않는 환경
    - **Medium (15%)**: 일반적인 사용
    - **Quartile (25%)**: 약간의 손상 가능
    - **High (30%)**: 로고 삽입, 손상이 잦은 환경
    
    **마스크 패턴:**
    - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
    
    **색상 입력:**
    - **색상명**: red, blue, green, crimson, gold 등
    - **HEX 코드**: #FF0000, #0000FF, #00FF00 등
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: darkorange; font-weight:bold; font-size: 18px;">© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)</p>',
    unsafe_allow_html=True
)
