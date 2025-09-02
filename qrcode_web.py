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
from PIL import Image, ImageDraw
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
if 'strip_option' not in st.session_state:
    st.session_state.strip_option = True
if 'file_format_select' not in st.session_state:
    st.session_state.file_format_select = "PNG"
if 'pattern_shape_select' not in st.session_state: # 패턴 모양 선택 상태 추가
    st.session_state.pattern_shape_select = "사각"


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


# QR 코드 데이터 생성
def get_qr_data_object(data, box_size, border, error_correction, mask_pattern):
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
        return qr
    except Exception as e:
        st.error(f"QR 코드 데이터 생성 오류: {str(e)}")
        return None


# 사용자 정의 모양으로 QR 코드 이미지 생성 함수 (PNG)
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, shape):
    if not qr_object:
        return None

    img_size = (qr_object.modules_count + 2 * border) * box_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)

    # 둥근 사각형을 위한 함수 (직접 구현)
    def draw_rounded_rectangle(draw, xy, radius, fill):
        x1, y1, x2, y2 = xy
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
        draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)

    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size
                
                if shape == "사각" or shape == "사각형":
                    draw.rectangle([x, y, x + box_size, y + box_size], fill=fill_color)
                elif shape == "둥근사각":
                    radius = box_size // 4 # 둥근 정도
                    draw_rounded_rectangle(draw, [x, y, x + box_size, y + box_size], radius, fill=fill_color)
                elif shape == "동그라미":
                    draw.ellipse([x, y, x + box_size, y + box_size], fill=fill_color)
                elif shape == "마름모":
                    draw.polygon([(x + box_size/2, y), (x + box_size, y + box_size/2), (x + box_size/2, y + box_size), (x, y + box_size/2)], fill=fill_color)
    return img


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
    st.session_state.generate_button_clicked = False
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
    st.session_state.file_format_select = "PNG"
    st.session_state.pattern_shape_select = "사각"

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
    st.session_state.generate_button_clicked = False
    st.session_state.error_message = None


#[메인]====================================================================================================================================================================


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

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=st.session_state.strip_option,
        key="strip_option",
        on_change=on_qr_setting_change
    )

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

    st.markdown("---")


#========================================================================================================================================================================

    # QR 코드 설정
    st.markdown("---")
    st.subheader("🔨 QR 코드 설정")

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


#========================================================================================================================================================================

    # 색상 설정
    st.markdown("---")
    st.subheader("🎨 색상 설정")
    
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
    
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == "<직접 입력>" else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == "<직접 입력>" else bg_color_choice


#========================================================================================================================================================================

    # 파일 설정
    st.markdown("---")
    st.subheader("💾 파일 설정")
    
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)",
            placeholder="이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
            key="filename_input_key",
        )

    current_filename = filename.strip()

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

    file_format = st.radio(
        "파일 형식 선택",
        ("PNG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else 1,
        key="file_format_select",
        on_change=on_qr_setting_change,
    )
    
    # 패턴 모양 선택
    pattern_shape_disabled = (file_format == "SVG")
    st.markdown("---")
    st.subheader("🖼️ 패턴 모양 설정")
    st.caption("⚠️ SVG 형식은 사각만 지원합니다.")
    pattern_shape = st.selectbox(
        "패턴 모양 선택",
        ("사각", "둥근사각", "동그라미", "마름모"),
        key="pattern_shape_select",
        on_change=on_qr_setting_change,
        disabled=pattern_shape_disabled,
    )


#========================================================================================================================================================================

with col2:
    st.header("👀 미리보기 및 생성")
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    is_pattern_color_valid_preview = (pattern_color_choice != "<직접 입력>") or (pattern_color_choice == "<직접 입력>" and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != "<직접 입력>") or (bg_color_choice == "<직접 입력>" and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    preview_image_display = None
    preview_qr_object = None

    if current_data and (file_format_is_svg or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview)):
        qr = get_qr_data_object(
            current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
            int(st.session_state.mask_pattern_select)
        )
        if qr:
            # 미리보기는 항상 PNG로 생성 (SVG 색상 고정)
            preview_image_display = draw_custom_shape_image(
                qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                "black" if file_format_is_svg else pattern_color,
                "white" if file_format_is_svg else bg_color,
                "사각" if file_format_is_svg else st.session_state.pattern_shape_select
            )
            preview_qr_object = qr
    
    generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True,)
    
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
            if file_format == "PNG":
                qr = get_qr_data_object(
                    current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                    int(st.session_state.mask_pattern_select)
                )
                if qr:
                    img = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        final_pattern_color, final_bg_color, st.session_state.pattern_shape_select
                    )
                    if img:
                        img_buffer = io.BytesIO()
                        img.save(img_buffer, format='PNG')
                        st.session_state.qr_image_bytes = img_buffer.getvalue()
                        st.session_state.qr_svg_bytes = None
                        st.session_state.qr_generated = True
                        st.session_state.show_generate_success = True
                        preview_image_display = img
                        preview_qr_object = qr
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
                    
                    # [수정된 부분] SVG 미리보기를 위해 draw_custom_shape_image 함수를 사용합니다.
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", "사각"
                    )
                    preview_qr_object = qr

    st.markdown("---")
    
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    elif st.session_state.show_generate_success:
        st.success("✅ QR 코드 생성 완료!!  반드시 파일명을 확인하고, 화면 아래의 [💾 QR 코드 다운로드] 버튼을 클릭하세요.")
    elif preview_image_display:
        st.success("현재 입력된 내용으로 생성될 QR 코드를 미리 표현해 보았습니다.  이 QR 코드가 맘에 드신다면, 위의 [⚡ QR 코드 생성] 버튼을 클릭하세요.")
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
    else:
        if not current_data:
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
        else:
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

st.button(
    label="🔄 전체 초기화", 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help="모든 내용을 초기화 합니다.",
)

with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
    2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
    3. **패턴 모양**에서 QR 코드 점의 모양을 선택하세요 (SVG 형식은 사각형만 가능합니다)
    4. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
    5. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요
    6. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
    """)

    st.markdown("---")

    st.header("💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com`
    - **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
    - **전화번호**: `tel:type=CELL:+82 10-1234-5678`
    - **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
    - **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
    """)

    st.markdown("---")

    st.header("⚙️ 설정 가이드")
    st.markdown("**오류 보정 레벨:**")
    st.markdown("""
    - **Low (7%)**: 손상되지 않는 환경
    - **Medium (15%)**: 일반적인 사용
    - **Quartile (25%)**: 약간의 손상 가능
    - **High (30%)**: 로고 삽입, 손상이 잦은 환경
    """)

    st.markdown("**마스크 패턴:**")
    st.markdown("""
    - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
    """)

    st.markdown("**패턴 모양:**")
    st.markdown("""
    - 사각, 둥근사각, 동그라미, 마름모 중 선택
    - **SVG** 파일 형식 선택 시에는 **사각**만 지원합니다.
    """)

    st.markdown("**색상 입력:**")
    st.markdown("""
    - **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
    - **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
    - **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: hotpink; font-size: 15px;">© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)</p>',
    unsafe_allow_html=True
)
