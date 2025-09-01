"""
QR 코드 생성 웹앱 - Streamlit 버전
휴대폰에서도 사용 가능

실행 방법:
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
import hashlib
import re

# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔲",
    layout="wide",
)

# 세션 상태 초기화
if 'download_initiated' not in st.session_state:
    st.session_state.download_initiated = False
if 'show_generate_success' not in st.session_state:
    st.session_state.show_generate_success = False
if 'qr_generated' not in st.session_state:
    st.session_state.qr_generated = False
if 'qr_image_bytes' not in st.session_state:
    st.session_state.qr_image_bytes = None
if 'last_qr_params_hash' not in st.session_state:
    st.session_state.last_qr_params_hash = ""
if 'last_filename_state' not in st.session_state:
    st.session_state.last_filename_state = ""

# 각 입력창에 대한 세션 상태 초기화 (필수)
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = ""
if 'custom_bg_color_input_key' not in st.session_state:
    st.session_state.custom_bg_color_input_key = ""
if 'filename_input_key' not in st.session_state:
    st.session_state.filename_input_key = ""


# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()

# 유효한 색상인지 확인하는 함수 (16진수 값만 유효하며, 공백을 자동으로 제거)
def is_valid_color(color_name):
    if not color_name:
        return False
    color_name = color_name.strip()
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return hex_pattern.match(color_name)

# QR 코드 생성 함수 (업데이트된 qrcode 라이브러리 문법 적용)
def generate_qr_code(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
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

        if hasattr(img, 'convert'):
            img = img.convert('RGB')
        
        return img, qr
    except Exception as e:
        st.error(f"QR 코드 생성 오류: {str(e)}")
        return None, None

# QR 내용만 초기화하는 콜백 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.last_qr_params_hash = ""


# 파일명 초기화 콜백 함수
def clear_filename_callback():
    st.session_state.filename_input_key = ""
    # 파일명만 변경되었으므로 다운로드 정보는 그대로 유지

# 다운로드 버튼 클릭 시 호출되는 콜백 함수
def set_download_initiated():
    st.session_state.download_initiated = True

# QR 코드 설정값 변경 시 다운로드 관련 상태 초기화
def on_qr_setting_change():
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False


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
        key="qr_input_area",
        on_change=on_qr_setting_change
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

    # 입력 내용 삭제 버튼 - on_click 콜백을 사용하도록 수정
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

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=True,
        help="입력된 내용 맨끝에 공백/줄바꿈 문자가 한개라도 포함되면 완전히 다른 QR코드가 생성됩니다. 입력된 마지막 문자 뒤에 공백/줄바꿈이 추가되어도 QR코드에 반영되지 않도록 하고 싶다면, 이 옵션을 켜 두세요.",
        on_change=on_qr_setting_change
    )

    st.markdown("---")
    st.markdown("---")

    # QR 코드 설정
    st.subheader("🔧 QR 코드 설정")

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input("QR 코드 1개의 사각 cell 크기 (px)", min_value=1, max_value=100, value=20, key="box_size_input", on_change=on_qr_setting_change)
        border = st.number_input("QR 코드 테두리/여백", min_value=0, max_value=10, value=2, key="border_input", on_change=on_qr_setting_change)

    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox("오류 보정 레벨", list(error_correction_options.keys()), index=0, key="error_correction_select", on_change=on_qr_setting_change)
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox("마스크 패턴 선택 (0~7)", options=list(range(8)), index=2, key="mask_pattern_select", on_change=on_qr_setting_change)

    st.markdown("---")
    st.subheader("🔧 색상 설정")

    # 색상 선택 옵션을 확장 (약 20개 이상)
    colors = [
        "<직접 입력>", "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox("패턴 색상", colors, index=1, key="pattern_color_select", on_change=on_qr_setting_change)
    with col1_4:
        bg_color_choice = st.selectbox("배경 색상", colors, index=2, key="bg_color_select", on_change=on_qr_setting_change)

    st.markdown("원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.")
    st.caption("예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)")
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            "패턴 색상 HEX 값",
            placeholder="예: #000000",
            disabled=(pattern_color_choice != "<직접 입력>"),
            key="custom_pattern_color_input_key",
            on_change=on_qr_setting_change,
        )
    with col1_6:
        st.text_input(
            "배경 색상 HEX 값",
            placeholder="예: #FFFFFF",
            disabled=(bg_color_choice != "<직접 입력>"),
            key="custom_bg_color_input_key",
            on_change=on_qr_setting_change,
        )

    # 사용될 최종 색상 값 결정 (공백 제거)
    pattern_color = st.session_state.custom_pattern_color_input_key.strip() if pattern_color_choice == "<직접 입력>" else pattern_color_choice
    bg_color = st.session_state.custom_bg_color_input_key.strip() if bg_color_choice == "<직접 입력>" else bg_color_choice
    
    st.markdown("---")

    st.subheader("🔧 파일 설정")

    # 파일명 입력창과 삭제 버튼을 위한 컬럼
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)",
            placeholder="이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
            key="filename_input_key",
        )

    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button(
            "🗑️ 파일명 삭제",
            help="입력한 파일명을 삭제합니다",
            use_container_width=True,
            type="secondary",
            disabled=filename_delete_disabled,
            on_click=clear_filename_callback,
        )

    current_filename = filename.strip()

with col2:
    st.header("👀 미리보기 및 생성")
    
    current_data = qr_data.strip() if strip_option else qr_data
    
    # 미리보기를 위한 유효성 검사
    is_pattern_color_valid_preview = (pattern_color_choice != "<직접 입력>") or (pattern_color_choice == "<직접 입력>" and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != "<직접 입력>") or (bg_color_choice == "<직접 입력>" and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    # 미리보기 이미지와 정보 생성 로직
    preview_image = None
    preview_info_text = ""
    
    if current_data and is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview:
        img, qr = generate_qr_code(
            current_data, int(box_size), int(border), error_correction,
            int(mask_pattern), pattern_color, bg_color,
        )
        if img and qr:
            preview_image = img
            preview_info_text = f"""
            **QR 코드 정보**
            - QR 버전: {qr.version}
            - 가로/세로 각 cell 개수: {qr.modules_count}개
            - 이미지 크기: {img.size[0]} x {img.size[1]} px
            - 패턴 색상: {pattern_color}
            - 배경 색상: {bg_color}
            - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
            """

    # QR 코드 생성 버튼
    generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True,)
    
    # 생성 버튼 클릭 시 최종 유효성 검사 로직
    if generate_btn:
        errors = []
        if not current_data:
            errors.append("생성할 QR 코드 내용을 입력해 주세요.")
        
        is_pattern_ok = True
        if pattern_color_choice == "<직접 입력>":
            if not pattern_color:
                errors.append("QR 코드 **패턴 색**의 HEX 값을 입력해 주세요.")
                is_pattern_ok = False
            elif not is_valid_color(pattern_color):
                errors.append("패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.")
                is_pattern_ok = False
        
        is_bg_ok = True
        if bg_color_choice == "<직접 입력>":
            if not bg_color:
                errors.append("QR 코드 **배경 색**의 HEX 값을 입력해 주세요.")
                is_bg_ok = False
            elif not is_valid_color(bg_color):
                errors.append("배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.")
                is_bg_ok = False
            
        if is_pattern_ok and is_bg_ok and is_valid_color(pattern_color) and is_valid_color(bg_color) and pattern_color == bg_color:
            errors.append("패턴과 배경은 같은 색을 사용할 수 없습니다.")

        if errors:
            for error_msg in errors:
                st.error(f"⚠️ {error_msg}")
            # 에러 발생 시 다운로드 기능 비활성화
            st.session_state.qr_generated = False
        else:
            # 모든 유효성 검사를 통과했을 때만 QR 코드 생성
            img, qr = generate_qr_code(
                current_data, int(box_size), int(border), error_correction,
                int(mask_pattern), pattern_color, bg_color,
            )
            
            if img and qr:
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                st.session_state.qr_image_bytes = img_buffer.getvalue()
                st.session_state.qr_generated = True
                st.session_state.show_generate_success = True

    st.markdown("---")
    
    # 미리보기 이미지 및 정보 표시
    if preview_image:
        st.subheader("📱 QR 코드 미리보기")
        st.image(preview_image, caption="생성된 QR 코드", width=380)
        st.info(preview_info_text)
    else:
        # 오류 메시지 표시 로직
        if not current_data:
            st.info("QR 코드 내용을 입력하시면 미리보기가 자동으로 나타납니다.")
        else:
            if pattern_color_choice == "<직접 입력>" and not pattern_color:
                st.warning("⚠️ 패턴 색의 HEX 값을 입력해 주세요. 미리보기를 위해 유효한 색상 값이 필요합니다.")
            if bg_color_choice == "<직접 입력>" and not bg_color:
                st.warning("⚠️ 배경 색의 HEX 값을 입력해 주세요. 미리보기를 위해 유효한 색상 값이 필요합니다.")
            if pattern_color_choice == "<직접 입력>" and pattern_color and not is_valid_color(pattern_color):
                st.warning("⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.")
            if bg_color_choice == "<직접 입력>" and bg_color and not is_valid_color(bg_color):
                st.warning("⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.")
            if is_colors_same_preview:
                st.warning("⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.")

    # 생성 성공 메시지 (고정)
    if st.session_state.show_generate_success:
        st.success("✅ QR 코드 생성 완료! 반드시 파일명을 확인하고 다운로드하세요.")

    # 다운로드 섹션
    if st.session_state.get('qr_generated', False) and st.session_state.get('qr_image_bytes', None) is not None:
        st.markdown("---")
        st.subheader("📥 다운로드")
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        current_filename = filename.strip()

        if not current_filename:
            final_filename = now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        else:
            final_filename = current_filename

        download_filename = f"{sanitize_filename(final_filename)}.png"

        st.download_button(
            label="💾 QR 코드 다운로드",
            data=st.session_state.qr_image_bytes,
            file_name=download_filename,
            mime="image/png",
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
            st.success("✅ 다운로드 준비 완료! 휴대폰의 경우 'Download' 폴더에 저장됩니다.")
            st.session_state.download_initiated = False

# 사이드바
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
    2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
    3. **색상 설정**에서 패턴과 배경 색상을 선택하세요
    4. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
    """)
    st.markdown("---")
    st.header("💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com`
    - **전화번호**: `tel:010-1234-5678`
    - **SMS**: `sms:010-1234-5678`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
    """)
    st.markdown("---")
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
    - **HEX 코드**: #FF0000, #0000FF, #00FF00 등
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: hotpink; font-size: 15px;">© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)</p>',
    unsafe_allow_html=True
)
# final 버전 - 모든 기능 정상 작동함..

