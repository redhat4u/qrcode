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
import streamlit.components.v1 as components
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image
import hashlib
import re
import base64 # SVG 이미지 표시를 위해 추가
import qrcode.image.svg # SVG 생성을 위해 추가


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
if 'qr_svg_bytes' not in st.session_state: # SVG 바이트 저장용
    st.session_state.qr_svg_bytes = None
if 'last_qr_params_hash' not in st.session_state:
    st.session_state.last_qr_params_hash = ""
if 'last_filename_state' not in st.session_state:
    st.session_state.last_filename_state = ""
if 'generate_button_clicked' not in st.session_state: # 새로 추가된 상태 변수
    st.session_state.generate_button_clicked = False
if 'error_message' not in st.session_state:
    st.session_state.error_message = None


# 각 입력창에 대한 세션 상태 초기화 (필수)
# None 대신 빈 문자열로 초기화하여 AttributeError 방지
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = ""
if 'custom_bg_color_input_key' not in st.session_state:
    st.session_state.custom_bg_color_input_key = ""
if 'filename_input_key' not in st.session_state:
    st.session_state.filename_input_key = ""
if 'box_size_input' not in st.session_state:
    st.session_state.box_size_input = 20
if 'border_input' not in st.session_state:
    st.session_state.border_input = 2
if 'error_correction_select' not in st.session_state:
    st.session_state.error_correction_select = "Low (7%) - 오류 보정"
if 'mask_pattern_select' not in st.session_state:
    st.session_state.mask_pattern_select = 2
if 'pattern_color_select' not in st.session_state:
    st.session_state.pattern_color_select = "black"
if 'bg_color_select' not in st.session_state:
    st.session_state.bg_color_select = "white"
if 'strip_option' not in st.session_state:  # 상태 변수 이름 통일
    st.session_state.strip_option = True
if 'file_format_select' not in st.session_state: # 파일 형식 선택 상태 추가
    st.session_state.file_format_select = "PNG"


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
def generate_qr_code_png(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
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


# QR 코드 SVG 생성 함수
def generate_qr_code_svg(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
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
        
        img_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        
        svg_buffer = io.BytesIO()
        img_svg.save(svg_buffer)
        svg_data = svg_buffer.getvalue().decode('utf-8')
        
        # 'fill="black"' 문자열 전체를 찾아 원하는 색상값으로 교체
        # replace() 메서드를 사용하여 `fill=` 부분을 포함하여 교체
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1) 
        
        # 'fill="white"' 문자열 전체를 찾아 원하는 색상값으로 교체
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        st.error(f"QR 코드 SVG 생성 오류: {str(e)}")
        return None, None

# 'QR 코드 생성' 버튼 클릭 시, 화면을 자동으로 아래로 스크롤하는
# JavaScript 코드가 포함된 Streamlit 컴포넌트를 호출하는 함수
def scroll_to_element(element_id):
    js_code = f"""
    <script>
        var element = window.parent.document.getElementById("{element_id}");
        if (element) {{
            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }}
    </script>
    """
    components.html(js_code, height=0, width=0)


# QR 내용만 초기화하는 콜백 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.last_qr_params_hash = ""
    st.session_state.generate_button_clicked = False # 상태 초기화
    st.session_state.error_message = None


# 파일명 초기화 콜백 함수
def clear_filename_callback():
    st.session_state.filename_input_key = ""


# 전체 초기화 콜백 함수
def reset_all_settings():
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    
    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.error_correction_select = "Low (7%) - 오류 보정"
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG" # 파일 형식도 초기화

    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False
    st.session_state.error_message = None


# 다운로드 버튼 클릭 시 호출되는 콜백 함수
def set_download_initiated():
    st.session_state.download_initiated = True


# QR 코드 설정값 변경 시 다운로드 관련 상태 초기화
def on_qr_setting_change():
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False # 설정 변경 시 버튼 클릭 상태 초기화
    st.session_state.error_message = None


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
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change # 설정 변경 시 초기화
    )

    st.markdown("---")
    st.markdown("---")

    # QR 코드 설정
    st.subheader("🛠️ QR 코드 설정")

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input("QR 코드 1개의 사각 cell 크기 (px)", min_value=1, max_value=100, key="box_size_input", on_change=on_qr_setting_change)
        border = st.number_input("QR 코드 테두리/여백", min_value=0, max_value=10, key="border_input", on_change=on_qr_setting_change)

    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox("오류 보정 레벨", list(error_correction_options.keys()), key="error_correction_select", on_change=on_qr_setting_change)
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox("마스크 패턴 선택 (0~7)", options=list(range(8)), key="mask_pattern_select", on_change=on_qr_setting_change)

    st.markdown("---")
    st.subheader("🛠️ 색상 설정")
    
    # [수정] 파일 형식에 따라 색상 설정을 활성화/비활성화
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    if file_format_is_svg:
        st.warning("⚠️ SVG 파일은 벡터 형식이므로 원하는 색상을 선택할 수 없습니다. 다양한 색상을 원한다면 'PNG' 형식을 선택하세요.")

    # 색상 선택 옵션을 확장 (약 20개 이상)
    colors = [
        "<직접 입력>", "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            "패턴 색상", colors, 
            key="pattern_color_select", 
            on_change=on_qr_setting_change,
            disabled=file_format_is_svg
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            "배경 색상", colors, 
            key="bg_color_select", 
            on_change=on_qr_setting_change,
            disabled=file_format_is_svg
        )

    st.markdown("원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.")
    st.caption("예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)")
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            "패턴 색상 HEX 값",
            placeholder="예: #000000",
            disabled=(pattern_color_choice != "<직접 입력>") or file_format_is_svg,
            key="custom_pattern_color_input_key",
            on_change=on_qr_setting_change
        )
    with col1_6:
        st.text_input(
            "배경 색상 HEX 값",
            placeholder="예: #FFFFFF",
            disabled=(bg_color_choice != "<직접 입력>") or file_format_is_svg,
            key="custom_bg_color_input_key",
            on_change=on_qr_setting_change
        )
    
    # 이 변수들은 미리보기 용도로만 사용됩니다.
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == "<직접 입력>" else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == "<직접 입력>" else bg_color_choice
    
    st.markdown("---")

    st.subheader("🛠️ 파일 설정")

    # 파일명 입력창과 삭제 버튼을 위한 컬럼
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        # 파일명 입력 시에는 다운로드 초기화가 발생하지 않도록 on_change 콜백 제거
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

    # 파일 형식 선택 라디오 버튼
    file_format = st.radio(
        "파일 형식 선택",
        ("PNG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else 1, # 세션 상태에 따라 초기값 설정
        key="file_format_select",
        on_change=on_qr_setting_change, # 파일 형식 변경시 초기화
    )

    current_filename = filename.strip()

with col2:
    st.header("👀 미리보기 및 생성")
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    # 미리보기를 위한 유효성 검사
    is_pattern_color_valid_preview = (pattern_color_choice != "<직접 입력>") or (pattern_color_choice == "<직접 입력>" and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != "<직접 입력>") or (bg_color_choice == "<직접 입력>" and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    # 미리보기 이미지와 정보 생성 로직을 PNG로 통일
    preview_image_display = None # Streamlit에 표시할 최종 이미지 (PNG)
    preview_qr_object = None # QR 코드 정보 추출을 위한 qr 객체

    if current_data and (file_format_is_svg or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview)):
        img, qr = generate_qr_code_png(
            current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
            int(st.session_state.mask_pattern_select), 
            "black" if file_format_is_svg else pattern_color, # SVG일 경우 검정으로 고정
            "white" if file_format_is_svg else bg_color,      # SVG일 경우 하양으로 고정
        )
        if img and qr:
            preview_image_display = img
            preview_qr_object = qr
    
    # QR 코드 생성 버튼
    generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True,)
    
    # [수정] 생성 버튼 클릭 시 최종 유효성 검사 로직
    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None # 버튼 클릭 시 기존 오류 메시지 초기화
        
        # 유효성 검사 로직을 하나의 리스트로 통합
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
            # 오류 메시지를 세션 상태에 저장하여 다른 곳에서 참조 가능하게 함
            st.session_state.error_message = errors[0] # 첫 번째 오류 메시지만 표시
            st.session_state.show_generate_success = False
        else:
            st.session_state.error_message = None
            # [수정] 모든 유효성 검사를 통과했을 때만 QR 코드 생성 및 저장
            if file_format == "PNG":
                img, qr = generate_qr_code_png(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), final_pattern_color, final_bg_color,
                )
                if img and qr:
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    st.session_state.qr_image_bytes = img_buffer.getvalue()
                    st.session_state.qr_svg_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
                    preview_image_display = img
                    preview_qr_object = qr
                    scroll_to_element("download-anchor")  # 다운로드 섹션으로 강제 스크롤
            else: # SVG
                # SVG 생성 함수는 색상 인자를 무시하므로 검정색과 흰색을 넘겨줌
                svg_data, qr = generate_qr_code_svg(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), "black", "white",
                )
                if svg_data and qr:
                    st.session_state.qr_svg_bytes = svg_data.encode('utf-8')
                    st.session_state.qr_image_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
                    # 미리보기용 PNG도 별도로 생성
                    png_img, png_qr = generate_qr_code_png(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                        int(st.session_state.mask_pattern_select), "black", "white",
                    )
                    preview_image_display = png_img
                    preview_qr_object = png_qr

    st.markdown("---")
    
    # [수정] 메시지 표시 로직 통합
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    elif st.session_state.show_generate_success:
        st.success("✅ QR 코드 생성 완료!!  반드시 파일명을 확인하고, 화면 아래의 [💾 QR 코드 다운로드] 버튼을 클릭하세요.")
    elif preview_image_display:
        st.success("현재 입력된 내용으로 생성될 QR 코드를 미리 표현해 보았습니다.  이 QR 코드가 맘에 드신다면, 위의 [⚡ QR 코드 생성] 버튼을 클릭하세요.")
    else:
        st.info("QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다.")

    # 미리보기 이미지 및 정보는 항상 표시
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
    else:
        # 오류 메시지 표시 로직
        if not current_data:
            # 이 부분은 위의 st.info로 대체되므로 중복 제거
            pass
        else:
            if not file_format_is_svg:
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

    # 다운로드 섹션
    if st.session_state.get('qr_generated', False) and (st.session_state.get('qr_image_bytes') is not None or st.session_state.get('qr_svg_bytes') is not None):

        st.markdown("---")
        # 이 div는 스크롤 목표 지점입니다.
        components.html("""
            <div id="download-anchor"></div>
        """, height=0, width=0)

        st.subheader("📥 다운로드")
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        current_filename = filename.strip()

        if not current_filename:
            final_filename = now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        else:
            final_filename = current_filename

        download_data = None
        download_mime = ""
        download_extension = ""

        if file_format == "PNG":
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

st.markdown("---")

# 전체 초기화 버튼
st.button(
    label="🔄 전체 초기화", 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help="모든 내용을 초기화 합니다.",
)


# 사이드바
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
    2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
    3. **색상 설정**에서 패턴과 배경 색상을 선택하세요
    4. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요.
    5. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
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
# 최신버전(25/09/01-22:59)..

import base64 # SVG 이미지 표시를 위해 추가
import qrcode.image.svg # SVG 생성을 위해 추가

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
if 'qr_svg_bytes' not in st.session_state: # SVG 바이트 저장용
    st.session_state.qr_svg_bytes = None
if 'last_qr_params_hash' not in st.session_state:
    st.session_state.last_qr_params_hash = ""
if 'last_filename_state' not in st.session_state:
    st.session_state.last_filename_state = ""
if 'generate_button_clicked' not in st.session_state: # 새로 추가된 상태 변수
    st.session_state.generate_button_clicked = False
if 'error_message' not in st.session_state:
    st.session_state.error_message = None


# 각 입력창에 대한 세션 상태 초기화 (필수)
# None 대신 빈 문자열로 초기화하여 AttributeError 방지
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = ""
if 'custom_bg_color_input_key' not in st.session_state:
    st.session_state.custom_bg_color_input_key = ""
if 'filename_input_key' not in st.session_state:
    st.session_state.filename_input_key = ""
if 'box_size_input' not in st.session_state:
    st.session_state.box_size_input = 20
if 'border_input' not in st.session_state:
    st.session_state.border_input = 2
if 'error_correction_select' not in st.session_state:
    st.session_state.error_correction_select = "Low (7%) - 오류 보정"
if 'mask_pattern_select' not in st.session_state:
    st.session_state.mask_pattern_select = 2
if 'pattern_color_select' not in st.session_state:
    st.session_state.pattern_color_select = "black"
if 'bg_color_select' not in st.session_state:
    st.session_state.bg_color_select = "white"
if 'strip_option' not in st.session_state:  # 상태 변수 이름 통일
    st.session_state.strip_option = True
if 'file_format_select' not in st.session_state: # 파일 형식 선택 상태 추가
    st.session_state.file_format_select = "PNG"


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
def generate_qr_code_png(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
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

# QR 코드 SVG 생성 함수
def generate_qr_code_svg(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
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
        
        img_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        
        svg_buffer = io.BytesIO()
        img_svg.save(svg_buffer)
        svg_data = svg_buffer.getvalue().decode('utf-8')
        
        # 'fill="black"' 문자열 전체를 찾아 원하는 색상값으로 교체
        # replace() 메서드를 사용하여 `fill=` 부분을 포함하여 교체
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1) 
        
        # 'fill="white"' 문자열 전체를 찾아 원하는 색상값으로 교체
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        st.error(f"QR 코드 SVG 생성 오류: {str(e)}")
        return None, None


# QR 내용만 초기화하는 콜백 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.last_qr_params_hash = ""
    st.session_state.generate_button_clicked = False # 상태 초기화
    st.session_state.error_message = None

# 파일명 초기화 콜백 함수
def clear_filename_callback():
    st.session_state.filename_input_key = ""
    
# 전체 초기화 콜백 함수
def reset_all_settings():
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    
    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.error_correction_select = "Low (7%) - 오류 보정"
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG" # 파일 형식도 초기화

    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False
    st.session_state.error_message = None


# 다운로드 버튼 클릭 시 호출되는 콜백 함수
def set_download_initiated():
    st.session_state.download_initiated = True

# QR 코드 설정값 변경 시 다운로드 관련 상태 초기화
def on_qr_setting_change():
    st.session_state.qr_generated = False
    st.session_state.show_generate_success = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_svg_bytes = None
    st.session_state.generate_button_clicked = False # 설정 변경 시 버튼 클릭 상태 초기화
    st.session_state.error_message = None


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
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change # 설정 변경 시 초기화
    )

    st.markdown("---")
    st.markdown("---")

    # QR 코드 설정
    st.subheader("🛠️ QR 코드 설정")

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input("QR 코드 1개의 사각 cell 크기 (px)", min_value=1, max_value=100, key="box_size_input", on_change=on_qr_setting_change)
        border = st.number_input("QR 코드 테두리/여백", min_value=0, max_value=10, key="border_input", on_change=on_qr_setting_change)

    with col1_2:
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox("오류 보정 레벨", list(error_correction_options.keys()), key="error_correction_select", on_change=on_qr_setting_change)
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox("마스크 패턴 선택 (0~7)", options=list(range(8)), key="mask_pattern_select", on_change=on_qr_setting_change)

    st.markdown("---")
    st.subheader("🛠️ 색상 설정")
    
    # [수정] 파일 형식에 따라 색상 설정을 활성화/비활성화
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    if file_format_is_svg:
        st.warning("⚠️ SVG 파일은 벡터 형식이므로 원하는 색상을 선택할 수 없습니다. 다양한 색상을 원한다면 'PNG' 형식을 선택하세요.")

    # 색상 선택 옵션을 확장 (약 20개 이상)
    colors = [
        "<직접 입력>", "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            "패턴 색상", colors, 
            key="pattern_color_select", 
            on_change=on_qr_setting_change,
            disabled=file_format_is_svg
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            "배경 색상", colors, 
            key="bg_color_select", 
            on_change=on_qr_setting_change,
            disabled=file_format_is_svg
        )

    st.markdown("원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.")
    st.caption("예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)")
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            "패턴 색상 HEX 값",
            placeholder="예: #000000",
            disabled=(pattern_color_choice != "<직접 입력>") or file_format_is_svg,
            key="custom_pattern_color_input_key",
            on_change=on_qr_setting_change
        )
    with col1_6:
        st.text_input(
            "배경 색상 HEX 값",
            placeholder="예: #FFFFFF",
            disabled=(bg_color_choice != "<직접 입력>") or file_format_is_svg,
            key="custom_bg_color_input_key",
            on_change=on_qr_setting_change
        )
    
    # 이 변수들은 미리보기 용도로만 사용됩니다.
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == "<직접 입력>" else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == "<직접 입력>" else bg_color_choice
    
    st.markdown("---")

    st.subheader("🛠️ 파일 설정")

    # 파일명 입력창과 삭제 버튼을 위한 컬럼
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        # 파일명 입력 시에는 다운로드 초기화가 발생하지 않도록 on_change 콜백 제거
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

    # 파일 형식 선택 라디오 버튼
    file_format = st.radio(
        "파일 형식 선택",
        ("PNG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else 1, # 세션 상태에 따라 초기값 설정
        key="file_format_select",
        on_change=on_qr_setting_change, # 파일 형식 변경시 초기화
    )

    current_filename = filename.strip()

with col2:
    st.header("👀 미리보기 및 생성")
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    # 미리보기를 위한 유효성 검사
    is_pattern_color_valid_preview = (pattern_color_choice != "<직접 입력>") or (pattern_color_choice == "<직접 입력>" and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != "<직접 입력>") or (bg_color_choice == "<직접 입력>" and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    # 미리보기 이미지와 정보 생성 로직을 PNG로 통일
    preview_image_display = None # Streamlit에 표시할 최종 이미지 (PNG)
    preview_qr_object = None # QR 코드 정보 추출을 위한 qr 객체

    if current_data and (file_format_is_svg or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview)):
        img, qr = generate_qr_code_png(
            current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
            int(st.session_state.mask_pattern_select), 
            "black" if file_format_is_svg else pattern_color, # SVG일 경우 검정으로 고정
            "white" if file_format_is_svg else bg_color,      # SVG일 경우 하양으로 고정
        )
        if img and qr:
            preview_image_display = img
            preview_qr_object = qr
    
    # QR 코드 생성 버튼
    generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True,)
    
    # [수정] 생성 버튼 클릭 시 최종 유효성 검사 로직
    if generate_btn:
        st.session_state.generate_button_clicked = True
        st.session_state.error_message = None # 버튼 클릭 시 기존 오류 메시지 초기화
        
        # 유효성 검사 로직을 하나의 리스트로 통합
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
            # 오류 메시지를 세션 상태에 저장하여 다른 곳에서 참조 가능하게 함
            st.session_state.error_message = errors[0] # 첫 번째 오류 메시지만 표시
            st.session_state.show_generate_success = False
        else:
            st.session_state.error_message = None
            # [수정] 모든 유효성 검사를 통과했을 때만 QR 코드 생성 및 저장
            if file_format == "PNG":
                img, qr = generate_qr_code_png(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), final_pattern_color, final_bg_color,
                )
                if img and qr:
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    st.session_state.qr_image_bytes = img_buffer.getvalue()
                    st.session_state.qr_svg_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
                    preview_image_display = img
                    preview_qr_object = qr
            else: # SVG
                # SVG 생성 함수는 색상 인자를 무시하므로 검정색과 흰색을 넘겨줌
                svg_data, qr = generate_qr_code_svg(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select), "black", "white",
                )
                if svg_data and qr:
                    st.session_state.qr_svg_bytes = svg_data.encode('utf-8')
                    st.session_state.qr_image_bytes = None
                    st.session_state.qr_generated = True
                    st.session_state.show_generate_success = True
                    # 미리보기용 PNG도 별도로 생성
                    png_img, png_qr = generate_qr_code_png(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                        int(st.session_state.mask_pattern_select), "black", "white",
                    )
                    preview_image_display = png_img
                    preview_qr_object = png_qr

    st.markdown("---")
    
    # [수정] 메시지 표시 로직 통합
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    elif st.session_state.show_generate_success:
        st.success("✅ QR 코드 생성 완료! 반드시 파일명을 확인하고 다운로드하세요.")
    elif preview_image_display:
        st.success("현재 입력된 내용으로 생성될 QR 코드를 미리 표현해 보았습니다.")
    else:
        st.info("QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다.")

    # 미리보기 이미지 및 정보는 항상 표시
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
    else:
        # 오류 메시지 표시 로직
        if not current_data:
            # 이 부분은 위의 st.info로 대체되므로 중복 제거
            pass
        else:
            if not file_format_is_svg:
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

    # 다운로드 섹션
    if st.session_state.get('qr_generated', False) and (st.session_state.get('qr_image_bytes') is not None or st.session_state.get('qr_svg_bytes') is not None):
        st.markdown("---")
        st.subheader("📥 다운로드")
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        current_filename = filename.strip()

        if not current_filename:
            final_filename = now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        else:
            final_filename = current_filename

        download_data = None
        download_mime = ""
        download_extension = ""

        if file_format == "PNG":
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

st.markdown("---")

# 전체 초기화 버튼
st.button(
    label="🔄 전체 초기화", 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help="모든 내용을 초기화 합니다.",
)


# 사이드바
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
    2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
    3. **색상 설정**에서 패턴과 배경 색상을 선택하세요
    4. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요.
    5. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
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
# 최신버전(25/09/01-23:00)

