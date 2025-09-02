"""
QR 코드 생성 웹앱 - Streamlit 버전 (다국어 지원)
휴대폰에서도 사용 가능

실행 방법:
1. pip install streamlit qrcode[pil]
2. streamlit run qrcode_web_multilingual.py

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
import math
from messages import MESSAGES

# 다국어 지원 함수
def get_message(key, lang='ko'):
    return MESSAGES.get(lang, MESSAGES['ko']).get(key, key)

# 페이지 설정
st.set_page_config(
    page_title=get_message('page_title'),
    page_icon=get_message('page_icon'),
    layout="wide",
)

# 세션 상태 초기화
if 'language' not in st.session_state:
    st.session_state.language = 'ko'
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
    st.session_state.error_correction_select = get_message('error_low')
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
if 'pattern_shape_select' not in st.session_state:
    st.session_state.pattern_shape_select = get_message('pattern_square')
if 'finder_pattern_shape_select' not in st.session_state:
    st.session_state.finder_pattern_shape_select = get_message('pattern_square')
if 'corner_radius_input' not in st.session_state:
    st.session_state.corner_radius_input = 25
if 'cell_gap_input' not in st.session_state:
    st.session_state.cell_gap_input = 0
if 'jpg_quality_input' not in st.session_state:
    st.session_state.jpg_quality_input = 70


# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()


# 유효한 색상인지 확인하는 함수
def is_valid_color(color_name):
    if not color_name:
        return False
    color_name = color_name.strip()
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})


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
        st.error(get_message('qr_data_error').format(str(e)))
        return None


# 사용자 정의 모양으로 QR 코드 이미지 생성 함수 (PNG)
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, pattern_shape, corner_radius, cell_gap, finder_pattern_shape):
    if not qr_object:
        return None

    img_size = (qr_object.modules_count + 2 * border) * box_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)
    
    # 간격 계산
    gap_pixels = int(box_size * (cell_gap / 100))
    effective_box_size = box_size - gap_pixels

    def draw_shape(draw, xy, shape, fill, corner_radius):
        x1, y1, x2, y2 = xy
        effective_size = x2 - x1
        if shape == get_message('pattern_square') or shape == "Square":
            draw.rectangle(xy, fill=fill)
        elif shape == get_message('pattern_rounded') or shape == "Rounded Square":
            radius = int(effective_size * (corner_radius / 100))
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
            draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
        elif shape == get_message('pattern_circle') or shape == "Circle":
            draw.ellipse(xy, fill=fill)
        elif shape == get_message('pattern_diamond') or shape == "Diamond":
            draw.polygon([(x1 + effective_size/2, y1), (x1 + effective_size, y1 + effective_size/2), (x1 + effective_size/2, y1 + effective_size), (x1, y1 + effective_size/2)], fill=fill)
        elif shape == get_message('pattern_star') or shape == "Star":
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            radius_outer = (x2 - x1) / 2
            radius_inner = radius_outer * 0.4
            points = []
            for i in range(5):
                angle_outer = math.radians(i * 72 + 54)
                x_outer = x_center + radius_outer * math.cos(angle_outer)
                y_outer = y_center + radius_outer * math.sin(angle_outer)
                points.append((x_outer, y_outer))
                angle_inner = math.radians(i * 72 + 90)
                x_inner = x_center + radius_inner * math.cos(angle_inner)
                y_inner = y_center + radius_inner * math.sin(angle_inner)
                points.append((x_inner, y_inner))
            draw.polygon(points, fill=fill)
        elif shape == get_message('pattern_cross') or shape == "Cross":
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            cross_width = (x2 - x1) * 0.3
            draw.rectangle([x1, y_center - cross_width/2, x2, y_center + cross_width/2], fill=fill)
            draw.rectangle([x_center - cross_width/2, y1, x_center + cross_width/2, y2], fill=fill)
    
    # 세 개의 큰 파인더 패턴의 위치를 미리 계산
    finder_pattern_coords = [
        (border * box_size, border * box_size),
        (border * box_size, (qr_object.modules_count - 7 + border) * box_size),
        ((qr_object.modules_count - 7 + border) * box_size, border * box_size)
    ]
    
    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            is_finder_pattern = False
            # 세 개의 파인더 패턴 위치에 있는지 확인
            if (r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7):
                is_finder_pattern = True
            
            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size
                
                # 간격을 적용한 새로운 좌표 계산
                current_shape = finder_pattern_shape if is_finder_pattern else pattern_shape
                
                if current_shape != get_message('pattern_square') and current_shape != "Square":
                    new_x = x + gap_pixels // 2
                    new_y = y + gap_pixels // 2
                    new_x_end = x + box_size - (gap_pixels - gap_pixels // 2)
                    new_y_end = y + box_size - (gap_pixels - gap_pixels // 2)
                    draw_coords = [new_x, new_y, new_x_end, new_y_end]
                else:
                    draw_coords = [x, y, x + box_size, y + box_size]

                draw_shape(draw, draw_coords, current_shape, fill_color, corner_radius)

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
        
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1) 
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        st.error(get_message('qr_svg_error').format(str(e)))
        return None, None


# QR 내용만 초기화하는 콜백 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""

# 파일명 초기화 콜백 함수
def clear_filename_callback():
    st.session_state.filename_input_key = ""

# 전체 초기화 콜백 함수
def reset_all_settings():
    current_lang = st.session_state.language
    
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    
    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.error_correction_select = get_message('error_low', current_lang)
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG"
    st.session_state.pattern_shape_select = get_message('pattern_square', current_lang)
    st.session_state.finder_pattern_shape_select = get_message('pattern_square', current_lang)
    st.session_state.corner_radius_input = 25
    st.session_state.cell_gap_input = 0
    st.session_state.jpg_quality_input = 70


# 언어 변경 콜백 함수
def on_language_change():
    # 언어 변경 시 패턴 모양과 오류 보정 레벨의 현재 값 유지
    pattern_mapping = {
        'ko': {'사각': 'Square', '둥근사각': 'Rounded Square', '동그라미': 'Circle', 
               '마름모': 'Diamond', '별': 'Star', '십자가': 'Cross'},
        'en': {'Square': '사각', 'Rounded Square': '둥근사각', 'Circle': '동그라미',
               'Diamond': '마름모', 'Star': '별', 'Cross': '십자가'}
    }
    
    error_mapping = {
        'ko': {'Low (7%) - 오류 보정': 'Low (7%) - Error Correction',
               'Medium (15%) - 오류 보정': 'Medium (15%) - Error Correction',
               'Quartile (25%) - 오류 보정': 'Quartile (25%) - Error Correction',
               'High (30%) - 오류 보정': 'High (30%) - Error Correction'},
        'en': {'Low (7%) - Error Correction': 'Low (7%) - 오류 보정',
               'Medium (15%) - Error Correction': 'Medium (15%) - 오류 보정',
               'Quartile (25%) - Error Correction': 'Quartile (25%) - 오류 보정',
               'High (30%) - Error Correction': 'High (30%) - 오류 보정'}
    }
    
    current_lang = st.session_state.language
    
    # 패턴 모양 변환
    if current_lang in pattern_mapping:
        old_pattern = st.session_state.pattern_shape_select
        old_finder_pattern = st.session_state.finder_pattern_shape_select
        
        if old_pattern in pattern_mapping[current_lang]:
            st.session_state.pattern_shape_select = pattern_mapping[current_lang][old_pattern]
        if old_finder_pattern in pattern_mapping[current_lang]:
            st.session_state.finder_pattern_shape_select = pattern_mapping[current_lang][old_finder_pattern]
    
    # 오류 보정 레벨 변환
    if current_lang in error_mapping:
        old_error = st.session_state.error_correction_select
        if old_error in error_mapping[current_lang]:
            st.session_state.error_correction_select = error_mapping[current_lang][old_error]


#[메인]====================================================================================================================================================================


st.title(get_message('main_title'))

# 언어 선택 드롭다운
language_options = {'한국어': 'ko', 'English': 'en'}
selected_language_name = st.selectbox(
    get_message('language_select'),
    options=list(language_options.keys()),
    index=0 if st.session_state.language == 'ko' else 1,
    on_change=on_language_change,
)
st.session_state.language = language_options[selected_language_name]

# 현재 언어 설정
current_lang = st.session_state.language

st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header(get_message('input_settings_header', current_lang))

    # QR 코드 입력창
    st.subheader(get_message('qr_content_header', current_lang))
    st.info(get_message('qr_content_info', current_lang))

    qr_data = st.text_area(
        get_message('qr_input_label', current_lang),
        height=200,
        placeholder=get_message('qr_input_placeholder', current_lang),
        key="qr_input_area",
    )

    # 문자 수 표시
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(get_message('char_count_exceeded', current_lang).format(char_count))
        elif char_count > 2400:
            st.warning(get_message('char_count_warning', current_lang).format(char_count))
        else:
            st.success(get_message('char_count_success', current_lang).format(char_count))
    else:
        st.caption(get_message('char_count_zero', current_lang))

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        get_message('strip_option_label', current_lang),
        value=st.session_state.strip_option,
        key="strip_option",
        help=get_message('strip_option_help', current_lang)
    )

    # 입력 내용 삭제 버튼
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            get_message('delete_content_btn', current_lang),
            help=get_message('delete_content_help', current_lang),
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.markdown("---")
    
    # 파일 형식 설정
    st.subheader(get_message('file_format_header', current_lang))
    file_format = st.selectbox(
        get_message('file_format_label', current_lang),
        ("PNG", "JPG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else (1 if st.session_state.file_format_select == "JPG" else 2),
        key="file_format_select",
    )
    
    # JPG 품질 설정 슬라이더 (JPG 선택 시에만 표시)
    if file_format == "JPG":
        st.caption(get_message('jpg_quality_info', current_lang))
        jpg_quality = st.slider(
            get_message('jpg_quality_label', current_lang),
            min_value=1,
            max_value=100,
            value=st.session_state.jpg_quality_input,
            key="jpg_quality_input",
            help=get_message('jpg_quality_help', current_lang)
        )
    else:
        jpg_quality = 70
    
    # 패턴 모양 설정
    st.markdown("---")
    st.subheader(get_message('pattern_shape_header', current_lang))
    pattern_shape_disabled = (file_format == "SVG")
    st.caption(get_message('svg_shape_warning', current_lang))
    
    # 두 개의 패턴 모양 선택 옵션 추가
    col_pattern_shape, col_finder_shape = st.columns(2)
    
    pattern_options = (
        get_message('pattern_square', current_lang), 
        get_message('pattern_rounded', current_lang), 
        get_message('pattern_circle', current_lang), 
        get_message('pattern_diamond', current_lang), 
        get_message('pattern_star', current_lang), 
        get_message('pattern_cross', current_lang)
    )
    
    with col_pattern_shape:
        pattern_shape = st.selectbox(
            get_message('normal_pattern_label', current_lang),
            pattern_options,
            key="pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    with col_finder_shape:
        finder_pattern_shape = st.selectbox(
            get_message('finder_pattern_label', current_lang),
            pattern_options,
            key="finder_pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    # 둥근사각 전용 슬라이더
    rounded_square_ko = get_message('pattern_rounded', 'ko')
    rounded_square_en = get_message('pattern_rounded', 'en')
    
    if pattern_shape in [rounded_square_ko, rounded_square_en] or finder_pattern_shape in [rounded_square_ko, rounded_square_en]:
        corner_radius_disabled = (file_format == "SVG")
        st.caption(get_message('corner_radius_warning', current_lang))
        corner_radius = st.slider(
            get_message('corner_radius_label', current_lang), 
            min_value=0, 
            max_value=50, 
            value=st.session_state.corner_radius_input,
            help=get_message('corner_radius_help', current_lang),
            key="corner_radius_input",
            disabled=corner_radius_disabled
        )
    else:
        corner_radius = 0
        
    # 패턴 간격 슬라이더 (사각 제외)
    square_ko = get_message('pattern_square', 'ko')
    square_en = get_message('pattern_square', 'en')
    
    cell_gap_disabled = (pattern_shape in [square_ko, square_en]) or (finder_pattern_shape in [square_ko, square_en]) or (file_format == "SVG")
    st.caption(get_message('cell_gap_warning', current_lang))
    cell_gap = st.slider(
        get_message('cell_gap_label', current_lang),
        min_value=0,
        max_value=40,
        value=st.session_state.cell_gap_input,
        help=get_message('cell_gap_help', current_lang),
        disabled=cell_gap_disabled,
        key="cell_gap_input",
    )
    
#========================================================================================================================================================================

    # 색상 설정 (순서 변경)
    st.markdown("---")
    st.subheader(get_message('color_settings_header', current_lang))
    
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    if file_format_is_svg:
        st.warning(get_message('svg_color_warning', current_lang))

    colors = [
        get_message('custom_input', current_lang), "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            get_message('pattern_color_label', current_lang), colors, 
            key="pattern_color_select", 
            disabled=file_format_is_svg
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            get_message('bg_color_label', current_lang), colors, 
            key="bg_color_select", 
            disabled=file_format_is_svg
        )

    st.markdown(get_message('custom_color_info', current_lang))
    st.caption(get_message('hex_example', current_lang))
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            get_message('pattern_hex_label', current_lang),
            placeholder=get_message('hex_placeholder', current_lang),
            disabled=(pattern_color_choice != get_message('custom_input', current_lang)) or file_format_is_svg,
            key="custom_pattern_color_input_key",
        )
    with col1_6:
        st.text_input(
            get_message('bg_hex_label', current_lang),
            placeholder=get_message('hex_placeholder_white', current_lang),
            disabled=(bg_color_choice != get_message('custom_input', current_lang)) or file_format_is_svg,
            key="custom_bg_color_input_key",
        )
    
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == get_message('custom_input', current_lang) else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == get_message('custom_input', current_lang) else bg_color_choice

#========================================================================================================================================================================

    # QR 코드 설정
    st.markdown("---")
    st.subheader(get_message('qr_settings_header', current_lang))

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input(get_message('box_size_label', current_lang), min_value=1, max_value=100, key="box_size_input")
        border = st.number_input(get_message('border_label', current_lang), min_value=0, max_value=10, key="border_input")

    with col1_2:
        error_correction_options = {
            get_message('error_low', current_lang): qrcode.constants.ERROR_CORRECT_L,
            get_message('error_medium', current_lang): qrcode.constants.ERROR_CORRECT_M,
            get_message('error_quartile', current_lang): qrcode.constants.ERROR_CORRECT_Q,
            get_message('error_high', current_lang): qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox(get_message('error_correction_label', current_lang), list(error_correction_options.keys()), key="error_correction_select")
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox(get_message('mask_pattern_label', current_lang), options=list(range(8)), key="mask_pattern_select")


#========================================================================================================================================================================

    # 파일명 설정
    st.markdown("---")
    st.subheader(get_message('filename_header', current_lang))
    
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            get_message('filename_input_label', current_lang),
            placeholder=get_message('filename_placeholder', current_lang),
            key="filename_input_key",
        )

    current_filename = filename.strip()

    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button(
            get_message('delete_filename_btn', current_lang),
            help=get_message('delete_filename_help', current_lang),
            use_container_width=True,
            type="secondary",
            disabled=filename_delete_disabled,
            on_click=clear_filename_callback,
        )


#========================================================================================================================================================================

with col2:
    st.header(get_message('preview_download_header', current_lang))
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    is_pattern_color_valid_preview = (pattern_color_choice != get_message('custom_input', current_lang)) or (pattern_color_choice == get_message('custom_input', current_lang) and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != get_message('custom_input', current_lang)) or (bg_color_choice == get_message('custom_input', current_lang) and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    preview_image_display = None
    preview_qr_object = None
    
    can_generate_preview = current_data and (file_format == "SVG" or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview))

    download_data = None
    download_mime = ""
    download_extension = ""
    save_format = ""

    if can_generate_preview:
        try:
            qr = get_qr_data_object(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                int(st.session_state.mask_pattern_select)
            )
            if qr:
                preview_qr_object = qr
                if file_format in ["PNG", "JPG"]:
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        pattern_color, bg_color, st.session_state.pattern_shape_select,
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        st.session_state.finder_pattern_shape_select
                    )
                    img_buffer = io.BytesIO()
                    if file_format == "PNG":
                        preview_image_display.save(img_buffer, format='PNG')
                        download_mime = "image/png"
                        download_extension = ".png"
                    elif file_format == "JPG":
                        # JPG는 투명도를 지원하지 않아, RGB 모드로 변환
                        rgb_image = preview_image_display.convert('RGB')
                        rgb_image.save(img_buffer, format='JPEG', quality=jpg_quality)
                        download_mime = "image/jpeg"
                        download_extension = ".jpg"
                        
                    download_data = img_buffer.getvalue()

                else: # SVG
                    svg_data, _ = generate_qr_code_svg(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                        int(st.session_state.mask_pattern_select), "black", "white"
                    )
                    download_data = svg_data.encode('utf-8')
                    download_mime = "image/svg+xml"
                    download_extension = ".svg"
                    
                    # SVG 미리보기를 위한 이미지 생성
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", get_message('pattern_square', current_lang),
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        get_message('pattern_square', current_lang),
                    )
        except Exception as e:
            st.error(get_message('generation_error', current_lang).format(str(e)))

    st.markdown("---")
    
    if preview_image_display:
        st.success(get_message('qr_preview_success', current_lang))
        st.subheader(get_message('qr_preview_header', current_lang))
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=get_message('qr_caption', current_lang), width=380)
        
        if preview_qr_object:
            image_size = (preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)
            st.info(f"""
            {get_message('qr_info_title', current_lang)}
            - {get_message('qr_version', current_lang).format(preview_qr_object.version)}
            ** **
            - {get_message('modules_count', current_lang).format(preview_qr_object.modules_count)}
            - {get_message('border_count', current_lang).format(2 * int(st.session_state.border_input))}
            - {get_message('cell_size', current_lang).format(int(st.session_state.box_size_input))}
            - {get_message('image_size', current_lang).format(image_size, image_size)}
            ** **
            - {get_message('size_calculation', current_lang)}
            ** **
            - {get_message('pattern_color_info', current_lang).format("black" if file_format == "SVG" else pattern_color)}
            - {get_message('bg_color_info', current_lang).format("white" if file_format == "SVG" else bg_color)}
            """)

        # 다운로드 섹션의 위치를 미리보기 아래로 이동
        st.markdown("---")
        st.subheader(get_message('download_header', current_lang))
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        final_filename = sanitize_filename(st.session_state.filename_input_key.strip() if st.session_state.filename_input_key.strip() else now.strftime("QR_%Y-%m-%d_%H-%M-%S"))
        download_filename = f"{final_filename}{download_extension}"

        st.download_button(
            label=get_message('download_btn', current_lang),
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=get_message('download_help', current_lang)
        )
        
        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{get_message("download_filename", current_lang)}</span> '
            f'<span style="color:dodgerblue;"> {download_filename}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    elif current_data:
        st.warning(get_message('generation_warning', current_lang))
        
        if file_format != "SVG":
            if pattern_color_choice == get_message('custom_input', current_lang) and not pattern_color:
                st.warning(get_message('pattern_hex_empty', current_lang))
            if bg_color_choice == get_message('custom_input', current_lang) and not bg_color:
                st.warning(get_message('bg_hex_empty', current_lang))
            if pattern_color_choice == get_message('custom_input', current_lang) and pattern_color and not is_valid_color(pattern_color):
                st.warning(get_message('pattern_hex_invalid', current_lang))
            if bg_color_choice == get_message('custom_input', current_lang) and bg_color and not is_valid_color(bg_color):
                st.warning(get_message('bg_hex_invalid', current_lang))
            if is_colors_same_preview:
                st.warning(get_message('same_color_warning', current_lang))
    else:
        st.info(get_message('input_content_info', current_lang))


st.markdown("---")

st.button(
    label=get_message('reset_all_btn', current_lang), 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help=get_message('reset_all_help', current_lang),
)

with st.sidebar:
    st.header(get_message('sidebar_usage_title', current_lang))
    st.markdown(get_message('sidebar_usage_content', current_lang))

    st.markdown("---")

    st.header(get_message('sidebar_tips_title', current_lang))
    st.markdown(get_message('sidebar_tips_content', current_lang))

    st.markdown("---")

    st.header(get_message('sidebar_guide_title', current_lang))
    st.markdown(get_message('sidebar_file_format_title', current_lang))
    st.markdown(get_message('sidebar_file_format_content', current_lang))

    st.markdown("---")

    st.markdown(get_message('sidebar_pattern_title', current_lang))
    st.markdown(get_message('sidebar_pattern_content', current_lang))
    
    st.markdown(get_message('sidebar_gap_title', current_lang))
    st.markdown(get_message('sidebar_gap_content', current_lang))

    st.markdown("---")

    st.markdown(get_message('sidebar_color_title', current_lang))
    st.markdown(get_message('sidebar_color_content', current_lang))

    st.markdown("---")
    
    st.markdown(get_message('sidebar_qr_settings_title', current_lang))
    st.markdown(get_message('sidebar_error_correction_title', current_lang))
    st.markdown(get_message('sidebar_error_correction_content', current_lang))

    st.markdown(get_message('sidebar_mask_pattern_title', current_lang))
    st.markdown(get_message('sidebar_mask_pattern_content', current_lang))

# 하단 정보
st.markdown("---")
st.markdown(
    f'<p style="text-align: center; color: mediumslateblue; font-size: 15px;">{get_message("footer", current_lang)}</p>',
    unsafe_allow_html=True
))
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
        st.error(get_message('qr_data_error').format(str(e)))
        return None


# 사용자 정의 모양으로 QR 코드 이미지 생성 함수 (PNG)
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, pattern_shape, corner_radius, cell_gap, finder_pattern_shape):
    if not qr_object:
        return None

    img_size = (qr_object.modules_count + 2 * border) * box_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)
    
    # 간격 계산
    gap_pixels = int(box_size * (cell_gap / 100))
    effective_box_size = box_size - gap_pixels

    def draw_shape(draw, xy, shape, fill, corner_radius):
        x1, y1, x2, y2 = xy
        effective_size = x2 - x1
        if shape == get_message('pattern_square') or shape == "Square":
            draw.rectangle(xy, fill=fill)
        elif shape == get_message('pattern_rounded') or shape == "Rounded Square":
            radius = int(effective_size * (corner_radius / 100))
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
            draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
        elif shape == get_message('pattern_circle') or shape == "Circle":
            draw.ellipse(xy, fill=fill)
        elif shape == get_message('pattern_diamond') or shape == "Diamond":
            draw.polygon([(x1 + effective_size/2, y1), (x1 + effective_size, y1 + effective_size/2), (x1 + effective_size/2, y1 + effective_size), (x1, y1 + effective_size/2)], fill=fill)
        elif shape == get_message('pattern_star') or shape == "Star":
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            radius_outer = (x2 - x1) / 2
            radius_inner = radius_outer * 0.4
            points = []
            for i in range(5):
                angle_outer = math.radians(i * 72 + 54)
                x_outer = x_center + radius_outer * math.cos(angle_outer)
                y_outer = y_center + radius_outer * math.sin(angle_outer)
                points.append((x_outer, y_outer))
                angle_inner = math.radians(i * 72 + 90)
                x_inner = x_center + radius_inner * math.cos(angle_inner)
                y_inner = y_center + radius_inner * math.sin(angle_inner)
                points.append((x_inner, y_inner))
            draw.polygon(points, fill=fill)
        elif shape == get_message('pattern_cross') or shape == "Cross":
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            cross_width = (x2 - x1) * 0.3
            draw.rectangle([x1, y_center - cross_width/2, x2, y_center + cross_width/2], fill=fill)
            draw.rectangle([x_center - cross_width/2, y1, x_center + cross_width/2, y2], fill=fill)
    
    # 세 개의 큰 파인더 패턴의 위치를 미리 계산
    finder_pattern_coords = [
        (border * box_size, border * box_size),
        (border * box_size, (qr_object.modules_count - 7 + border) * box_size),
        ((qr_object.modules_count - 7 + border) * box_size, border * box_size)
    ]
    
    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            is_finder_pattern = False
            # 세 개의 파인더 패턴 위치에 있는지 확인
            if (r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7):
                is_finder_pattern = True
            
            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size
                
                # 간격을 적용한 새로운 좌표 계산
                current_shape = finder_pattern_shape if is_finder_pattern else pattern_shape
                
                if current_shape != get_message('pattern_square') and current_shape != "Square":
                    new_x = x + gap_pixels // 2
                    new_y = y + gap_pixels // 2
                    new_x_end = x + box_size - (gap_pixels - gap_pixels // 2)
                    new_y_end = y + box_size - (gap_pixels - gap_pixels // 2)
                    draw_coords = [new_x, new_y, new_x_end, new_y_end]
                else:
                    draw_coords = [x, y, x + box_size, y + box_size]

                draw_shape(draw, draw_coords, current_shape, fill_color, corner_radius)

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
        
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1) 
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        st.error(get_message('qr_svg_error').format(str(e)))
        return None, None


# QR 내용만 초기화하는 콜백 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""

# 파일명 초기화 콜백 함수
def clear_filename_callback():
    st.session_state.filename_input_key = ""

# 전체 초기화 콜백 함수
def reset_all_settings():
    current_lang = st.session_state.language
    
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    
    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.error_correction_select = get_message('error_low', current_lang)
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG"
    st.session_state.pattern_shape_select = get_message('pattern_square', current_lang)
    st.session_state.finder_pattern_shape_select = get_message('pattern_square', current_lang)
    st.session_state.corner_radius_input = 25
    st.session_state.cell_gap_input = 0
    st.session_state.jpg_quality_input = 70


# 언어 변경 콜백 함수
def on_language_change():
    # 언어 변경 시 패턴 모양과 오류 보정 레벨의 현재 값 유지
    pattern_mapping = {
        'ko': {'사각': 'Square', '둥근사각': 'Rounded Square', '동그라미': 'Circle', 
               '마름모': 'Diamond', '별': 'Star', '십자가': 'Cross'},
        'en': {'Square': '사각', 'Rounded Square': '둥근사각', 'Circle': '동그라미',
               'Diamond': '마름모', 'Star': '별', 'Cross': '십자가'}
    }
    
    error_mapping = {
        'ko': {'Low (7%) - 오류 보정': 'Low (7%) - Error Correction',
               'Medium (15%) - 오류 보정': 'Medium (15%) - Error Correction',
               'Quartile (25%) - 오류 보정': 'Quartile (25%) - Error Correction',
               'High (30%) - 오류 보정': 'High (30%) - Error Correction'},
        'en': {'Low (7%) - Error Correction': 'Low (7%) - 오류 보정',
               'Medium (15%) - Error Correction': 'Medium (15%) - 오류 보정',
               'Quartile (25%) - Error Correction': 'Quartile (25%) - 오류 보정',
               'High (30%) - Error Correction': 'High (30%) - 오류 보정'}
    }
    
    current_lang = st.session_state.language
    
    # 패턴 모양 변환
    if current_lang in pattern_mapping:
        old_pattern = st.session_state.pattern_shape_select
        old_finder_pattern = st.session_state.finder_pattern_shape_select
        
        if old_pattern in pattern_mapping[current_lang]:
            st.session_state.pattern_shape_select = pattern_mapping[current_lang][old_pattern]
        if old_finder_pattern in pattern_mapping[current_lang]:
            st.session_state.finder_pattern_shape_select = pattern_mapping[current_lang][old_finder_pattern]
    
    # 오류 보정 레벨 변환
    if current_lang in error_mapping:
        old_error = st.session_state.error_correction_select
        if old_error in error_mapping[current_lang]:
            st.session_state.error_correction_select = error_mapping[current_lang][old_error]


#[메인]====================================================================================================================================================================


st.title(get_message('main_title'))

# 언어 선택 드롭다운
language_options = {'한국어': 'ko', 'English': 'en'}
selected_language_name = st.selectbox(
    get_message('language_select'),
    options=list(language_options.keys()),
    index=0 if st.session_state.language == 'ko' else 1,
    on_change=on_language_change,
)
st.session_state.language = language_options[selected_language_name]

# 현재 언어 설정
current_lang = st.session_state.language

st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header(get_message('input_settings_header', current_lang))

    # QR 코드 입력창
    st.subheader(get_message('qr_content_header', current_lang))
    st.info(get_message('qr_content_info', current_lang))

    qr_data = st.text_area(
        get_message('qr_input_label', current_lang),
        height=200,
        placeholder=get_message('qr_input_placeholder', current_lang),
        key="qr_input_area",
    )

    # 문자 수 표시
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(get_message('char_count_exceeded', current_lang).format(char_count))
        elif char_count > 2400:
            st.warning(get_message('char_count_warning', current_lang).format(char_count))
        else:
            st.success(get_message('char_count_success', current_lang).format(char_count))
    else:
        st.caption(get_message('char_count_zero', current_lang))

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        get_message('strip_option_label', current_lang),
        value=st.session_state.strip_option,
        key="strip_option",
        help=get_message('strip_option_help', current_lang)
    )

    # 입력 내용 삭제 버튼
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            get_message('delete_content_btn', current_lang),
            help=get_message('delete_content_help', current_lang),
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.markdown("---")
    
    # 파일 형식 설정
    st.subheader(get_message('file_format_header', current_lang))
    file_format = st.selectbox(
        get_message('file_format_label', current_lang),
        ("PNG", "JPG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else (1 if st.session_state.file_format_select == "JPG" else 2),
        key="file_format_select",
    )
    
    # JPG 품질 설정 슬라이더 (JPG 선택 시에만 표시)
    if file_format == "JPG":
        st.caption(get_message('jpg_quality_info', current_lang))
        jpg_quality = st.slider(
            get_message('jpg_quality_label', current_lang),
            min_value=1,
            max_value=100,
            value=st.session_state.jpg_quality_input,
            key="jpg_quality_input",
            help=get_message('jpg_quality_help', current_lang)
        )
    else:
        jpg_quality = 70
    
    # 패턴 모양 설정
    st.markdown("---")
    st.subheader(get_message('pattern_shape_header', current_lang))
    pattern_shape_disabled = (file_format == "SVG")
    st.caption(get_message('svg_shape_warning', current_lang))
    
    # 두 개의 패턴 모양 선택 옵션 추가
    col_pattern_shape, col_finder_shape = st.columns(2)
    
    pattern_options = (
        get_message('pattern_square', current_lang), 
        get_message('pattern_rounded', current_lang), 
        get_message('pattern_circle', current_lang), 
        get_message('pattern_diamond', current_lang), 
        get_message('pattern_star', current_lang), 
        get_message('pattern_cross', current_lang)
    )
    
    with col_pattern_shape:
        pattern_shape = st.selectbox(
            get_message('normal_pattern_label', current_lang),
            pattern_options,
            key="pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    with col_finder_shape:
        finder_pattern_shape = st.selectbox(
            get_message('finder_pattern_label', current_lang),
            pattern_options,
            key="finder_pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    # 둥근사각 전용 슬라이더
    rounded_square_ko = get_message('pattern_rounded', 'ko')
    rounded_square_en = get_message('pattern_rounded', 'en')
    
    if pattern_shape in [rounded_square_ko, rounded_square_en] or finder_pattern_shape in [rounded_square_ko, rounded_square_en]:
        corner_radius_disabled = (file_format == "SVG")
        st.caption(get_message('corner_radius_warning', current_lang))
        corner_radius = st.slider(
            get_message('corner_radius_label', current_lang), 
            min_value=0, 
            max_value=50, 
            value=st.session_state.corner_radius_input,
            help=get_message('corner_radius_help', current_lang),
            key="corner_radius_input",
            disabled=corner_radius_disabled
        )
    else:
        corner_radius = 0
        
    # 패턴 간격 슬라이더 (사각 제외)
    square_ko = get_message('pattern_square', 'ko')
    square_en = get_message('pattern_square', 'en')
    
    cell_gap_disabled = (pattern_shape in [square_ko, square_en]) or (finder_pattern_shape in [square_ko, square_en]) or (file_format == "SVG")
    st.caption(get_message('cell_gap_warning', current_lang))
    cell_gap = st.slider(
        get_message('cell_gap_label', current_lang),
        min_value=0,
        max_value=40,
        value=st.session_state.cell_gap_input,
        help=get_message('cell_gap_help', current_lang),
        disabled=cell_gap_disabled,
        key="cell_gap_input",
    )
    
#========================================================================================================================================================================

    # 색상 설정 (순서 변경)
    st.markdown("---")
    st.subheader(get_message('color_settings_header', current_lang))
    
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    if file_format_is_svg:
        st.warning(get_message('svg_color_warning', current_lang))

    colors = [
        get_message('custom_input', current_lang), "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            get_message('pattern_color_label', current_lang), colors, 
            key="pattern_color_select", 
            disabled=file_format_is_svg
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            get_message('bg_color_label', current_lang), colors, 
            key="bg_color_select", 
            disabled=file_format_is_svg
        )

    st.markdown(get_message('custom_color_info', current_lang))
    st.caption(get_message('hex_example', current_lang))
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            get_message('pattern_hex_label', current_lang),
            placeholder=get_message('hex_placeholder', current_lang),
            disabled=(pattern_color_choice != get_message('custom_input', current_lang)) or file_format_is_svg,
            key="custom_pattern_color_input_key",
        )
    with col1_6:
        st.text_input(
            get_message('bg_hex_label', current_lang),
            placeholder=get_message('hex_placeholder_white', current_lang),
            disabled=(bg_color_choice != get_message('custom_input', current_lang)) or file_format_is_svg,
            key="custom_bg_color_input_key",
        )
    
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == get_message('custom_input', current_lang) else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == get_message('custom_input', current_lang) else bg_color_choice

#========================================================================================================================================================================

    # QR 코드 설정
    st.markdown("---")
    st.subheader(get_message('qr_settings_header', current_lang))

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input(get_message('box_size_label', current_lang), min_value=1, max_value=100, key="box_size_input")
        border = st.number_input(get_message('border_label', current_lang), min_value=0, max_value=10, key="border_input")

    with col1_2:
        error_correction_options = {
            get_message('error_low', current_lang): qrcode.constants.ERROR_CORRECT_L,
            get_message('error_medium', current_lang): qrcode.constants.ERROR_CORRECT_M,
            get_message('error_quartile', current_lang): qrcode.constants.ERROR_CORRECT_Q,
            get_message('error_high', current_lang): qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox(get_message('error_correction_label', current_lang), list(error_correction_options.keys()), key="error_correction_select")
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox(get_message('mask_pattern_label', current_lang), options=list(range(8)), key="mask_pattern_select")


#========================================================================================================================================================================

    # 파일명 설정
    st.markdown("---")
    st.subheader(get_message('filename_header', current_lang))
    
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            get_message('filename_input_label', current_lang),
            placeholder=get_message('filename_placeholder', current_lang),
            key="filename_input_key",
        )

    current_filename = filename.strip()

    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button(
            get_message('delete_filename_btn', current_lang),
            help=get_message('delete_filename_help', current_lang),
            use_container_width=True,
            type="secondary",
            disabled=filename_delete_disabled,
            on_click=clear_filename_callback,
        )


#========================================================================================================================================================================

with col2:
    st.header(get_message('preview_download_header', current_lang))
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    is_pattern_color_valid_preview = (pattern_color_choice != get_message('custom_input', current_lang)) or (pattern_color_choice == get_message('custom_input', current_lang) and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != get_message('custom_input', current_lang)) or (bg_color_choice == get_message('custom_input', current_lang) and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    preview_image_display = None
    preview_qr_object = None
    
    can_generate_preview = current_data and (file_format == "SVG" or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview))

    download_data = None
    download_mime = ""
    download_extension = ""
    save_format = ""

    if can_generate_preview:
        try:
            qr = get_qr_data_object(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                int(st.session_state.mask_pattern_select)
            )
            if qr:
                preview_qr_object = qr
                if file_format in ["PNG", "JPG"]:
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        pattern_color, bg_color, st.session_state.pattern_shape_select,
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        st.session_state.finder_pattern_shape_select
                    )
                    img_buffer = io.BytesIO()
                    if file_format == "PNG":
                        preview_image_display.save(img_buffer, format='PNG')
                        download_mime = "image/png"
                        download_extension = ".png"
                    elif file_format == "JPG":
                        # JPG는 투명도를 지원하지 않아, RGB 모드로 변환
                        rgb_image = preview_image_display.convert('RGB')
                        rgb_image.save(img_buffer, format='JPEG', quality=jpg_quality)
                        download_mime = "image/jpeg"
                        download_extension = ".jpg"
                        
                    download_data = img_buffer.getvalue()

                else: # SVG
                    svg_data, _ = generate_qr_code_svg(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                        int(st.session_state.mask_pattern_select), "black", "white"
                    )
                    download_data = svg_data.encode('utf-8')
                    download_mime = "image/svg+xml"
                    download_extension = ".svg"
                    
                    # SVG 미리보기를 위한 이미지 생성
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", get_message('pattern_square', current_lang),
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        get_message('pattern_square', current_lang),
                    )
        except Exception as e:
            st.error(get_message('generation_error', current_lang).format(str(e)))

    st.markdown("---")
    
    if preview_image_display:
        st.success(get_message('qr_preview_success', current_lang))
        st.subheader(get_message('qr_preview_header', current_lang))
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=get_message('qr_caption', current_lang), width=380)
        
        if preview_qr_object:
            image_size = (preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input)
            st.info(f"""
            {get_message('qr_info_title', current_lang)}
            - {get_message('qr_version', current_lang).format(preview_qr_object.version)}
            ** **
            - {get_message('modules_count', current_lang).format(preview_qr_object.modules_count)}
            - {get_message('border_count', current_lang).format(2 * int(st.session_state.border_input))}
            - {get_message('cell_size', current_lang).format(int(st.session_state.box_size_input))}
            - {get_message('image_size', current_lang).format(image_size, image_size)}
            ** **
            - {get_message('size_calculation', current_lang)}
            ** **
            - {get_message('pattern_color_info', current_lang).format("black" if file_format == "SVG" else pattern_color)}
            - {get_message('bg_color_info', current_lang).format("white" if file_format == "SVG" else bg_color)}
            """)

        # 다운로드 섹션의 위치를 미리보기 아래로 이동
        st.markdown("---")
        st.subheader(get_message('download_header', current_lang))
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        final_filename = sanitize_filename(st.session_state.filename_input_key.strip() if st.session_state.filename_input_key.strip() else now.strftime("QR_%Y-%m-%d_%H-%M-%S"))
        download_filename = f"{final_filename}{download_extension}"

        st.download_button(
            label=get_message('download_btn', current_lang),
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=get_message('download_help', current_lang)
        )
        
        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{get_message("download_filename", current_lang)}</span> '
            f'<span style="color:dodgerblue;"> {download_filename}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    elif current_data:
        st.warning(get_message('generation_warning', current_lang))
        
        if file_format != "SVG":
            if pattern_color_choice == get_message('custom_input', current_lang) and not pattern_color:
                st.warning(get_message('pattern_hex_empty', current_lang))
            if bg_color_choice == get_message('custom_input', current_lang) and not bg_color:
                st.warning(get_message('bg_hex_empty', current_lang))
            if pattern_color_choice == get_message('custom_input', current_lang) and pattern_color and not is_valid_color(pattern_color):
                st.warning(get_message('pattern_hex_invalid', current_lang))
            if bg_color_choice == get_message('custom_input', current_lang) and bg_color and not is_valid_color(bg_color):
                st.warning(get_message('bg_hex_invalid', current_lang))
            if is_colors_same_preview:
                st.warning(get_message('same_color_warning', current_lang))
    else:
        st.info(get_message('input_content_info', current_lang))


st.markdown("---")

st.button(
    label=get_message('reset_all_btn', current_lang), 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help=get_message('reset_all_help', current_lang),
)

with st.sidebar:
    st.header(get_message('sidebar_usage_title', current_lang))
    st.markdown(get_message('sidebar_usage_content', current_lang))

    st.markdown("---")

    st.header(get_message('sidebar_tips_title', current_lang))
    st.markdown(get_message('sidebar_tips_content', current_lang))

    st.markdown("---")

    st.header(get_message('sidebar_guide_title', current_lang))
    st.markdown(get_message('sidebar_file_format_title', current_lang))
    st.markdown(get_message('sidebar_file_format_content', current_lang))

    st.markdown("---")

    st.markdown(get_message('sidebar_pattern_title', current_lang))
    st.markdown(get_message('sidebar_pattern_content', current_lang))
    
    st.markdown(get_message('sidebar_gap_title', current_lang))
    st.markdown(get_message('sidebar_gap_content', current_lang))

    st.markdown("---")

    st.markdown(get_message('sidebar_color_title', current_lang))
    st.markdown(get_message('sidebar_color_content', current_lang))

    st.markdown("---")
    
    st.markdown(get_message('sidebar_qr_settings_title', current_lang))
    st.markdown(get_message('sidebar_error_correction_title', current_lang))
    st.markdown(get_message('sidebar_error_correction_content', current_lang))

    st.markdown(get_message('sidebar_mask_pattern_title', current_lang))
    st.markdown(get_message('sidebar_mask_pattern_content', current_lang))

# 하단 정보
st.markdown("---")
st.markdown(
    f'<p style="text-align: center; color: mediumslateblue; font-size: 15px;">{get_message("footer", current_lang)}</p>',
    unsafe_allow_html=True
)
