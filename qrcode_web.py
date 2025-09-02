"""
화면에 표시되는 언어를 한국어와 영어로 선택할 수 있도록 하려고해..
언어선택은 타이틀바 밑에 드롭다운으로 할거야..
따옴표로 묶인 모든 메시지, 설정과 사이드바에서 보이는 모든 한글은
messages.py 파일로 만들었어.. 메인 파일만 수정해줘..

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
import math

from messages import MESSAGES

# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔲",
    layout="wide",
)

# 세션 상태 초기화
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = 0
if 'custom_background_color_input_key' not in st.session_state:
    st.session_state.custom_background_color_input_key = 0
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = 'ko'

# --- 언어 선택 ---
LANG_OPTIONS = {
    '한국어': 'ko',
    'English': 'en'
}
lang_label = '언어 선택' if st.session_state.current_lang == 'ko' else 'Language Selection'
selected_lang_display = st.sidebar.selectbox(lang_label, list(LANG_OPTIONS.keys()))
st.session_state.current_lang = LANG_OPTIONS[selected_lang_display]

M = MESSAGES[st.session_state.current_lang]

# 페이지 설정
st.set_page_config(
    page_title=M['page_title'],
    page_icon=M['page_icon'],
    layout="wide",
)

st.title(M['main_title'])
st.markdown("<hr/>", unsafe_allow_html=True)

# 문자열을 SHA256 해시로 변환
def generate_sha256(text):
    if text:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    return ""

def generate_svg(qr_data, gap, error_correction_level, box_size):
    factory = qrcode.image.svg.SvgPathImage
    qr_code = qrcode.QRCode(
        error_correction=error_correction_level,
        box_size=box_size,
        border=4,
        image_factory=factory
    )
    qr_code.add_data(qr_data)
    qr_code.make(fit=True)

    # SVG 객체를 바로 반환
    return qr_code.make_image(fill_color="black", back_color="white")._svg_string

def generate_qr(qr_data, file_format, box_size, border, pattern_shape, pattern_gap, pattern_color, background_color, error_correction_level):
    if file_format == 'SVG':
        return generate_svg(qr_data, pattern_gap, error_correction_level, box_size)
    
    # SVG가 아닌 경우 PIL을 사용하여 QR 코드를 생성합니다.
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction_level,
        box_size=box_size,
        border=border,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=pattern_color,
        back_color=background_color,
    ).convert("RGBA")

    # 패턴 모양에 따라 이미지 처리
    if pattern_shape == "Round":
        img = round_corners(img)
    elif pattern_shape == "Circle":
        img = circle_mask(img)
    elif pattern_shape == "Diamond":
        img = diamond_mask(img)
    elif pattern_shape == "Star":
        img = star_mask(img)
    elif pattern_shape == "Cross":
        img = cross_mask(img)

    # 패턴 간격 조절
    if pattern_gap > 0 and pattern_shape != 'Square':
        img = apply_gap(img, pattern_gap, background_color)
    
    return img

def apply_gap(img, gap, bg_color):
    """Adds a gap between QR code modules."""
    
    pixel_data = img.getdata()
    original_size = img.size[0]
    module_size = original_size // 21  # Assuming version 1 for simplicity
    
    if module_size <= 1:
        return img
    
    # Calculate new module size with gap
    new_module_size = module_size - gap
    if new_module_size <= 0:
        new_module_size = 1
        
    new_size = new_module_size * (original_size // module_size)
    new_img = Image.new("RGBA", (new_size, new_size), bg_color)
    
    draw = ImageDraw.Draw(new_img)
    
    for y in range(original_size // module_size):
        for x in range(original_size // module_size):
            pixel = pixel_data[y * original_size + x * module_size]
            
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:  # Assuming black
                draw.rectangle(
                    [
                        x * new_module_size, 
                        y * new_module_size, 
                        (x + 1) * new_module_size - gap, 
                        (y + 1) * new_module_size - gap
                    ],
                    fill=img.getpixel((x * module_size, y * module_size))
                )
                
    return new_img

def circle_mask(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    img.putalpha(mask)
    return img

def round_corners(img, radius=20):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + img.size, radius, fill=255)
    img.putalpha(mask)
    return img

def diamond_mask(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon([
        (img.width / 2, 0),
        (img.width, img.height / 2),
        (img.width / 2, img.height),
        (0, img.height / 2)
    ], fill=255)
    img.putalpha(mask)
    return img

def star_mask(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    points = []
    num_points = 5
    center_x, center_y = img.width / 2, img.height / 2
    inner_radius = center_x / 2
    outer_radius = center_x
    
    for i in range(num_points * 2):
        angle = math.pi / num_points * i
        r = outer_radius if i % 2 == 0 else inner_radius
        x = center_x + r * math.cos(angle - math.pi / 2)
        y = center_y + r * math.sin(angle - math.pi / 2)
        points.append((x, y))
    
    draw.polygon(points, fill=255)
    img.putalpha(mask)
    return img

def cross_mask(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    # 가로 막대
    draw.rectangle([(0, img.height * 0.4), (img.width, img.height * 0.6)], fill=255)
    # 세로 막대
    draw.rectangle([(img.width * 0.4, 0), (img.width * 0.6, img.height)], fill=255)
    img.putalpha(mask)
    return img

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_valid_hex(hex_color):
    if not isinstance(hex_color, str):
        return False
    hex_color = hex_color.lstrip('#')
    return re.match(r'^[0-9a-fA-F]{6}$', hex_color)

# 사이드바
st.sidebar.markdown(f"## {M['sidebar_title']}")
st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

# 섹션 1: 입력 및 설정
st.sidebar.header(M['input_settings_header'])
st.sidebar.markdown(f"### {M['qr_content_header']}")
qr_content = st.sidebar.text_area(
    M['qr_input_label'], 
    value=st.session_state.qr_input_area,
    height=200, 
    placeholder=M['qr_input_placeholder']
)

# 문자 수 표시
char_count = len(qr_content)
if char_count > 2900:
    st.sidebar.warning(M['char_count_exceeded'].format(char_count))
elif char_count > 2400:
    st.sidebar.info(M['char_count_warning'].format(char_count))
else:
    st.sidebar.success(M['char_count_success'].format(char_count))

st.sidebar.markdown("---")

# 파일 형식 선택
st.sidebar.markdown(f"### {M['file_format_header']}")
st.sidebar.markdown(M['file_format_content'], unsafe_allow_html=True)
file_format = st.sidebar.radio(
    M['file_format_label'], 
    ('PNG', 'JPG', 'SVG'),
    index=0
)

# JPG 품질 슬라이더 (JPG 선택 시에만 표시)
if file_format == 'JPG':
    jpg_quality = st.sidebar.slider(
        M['jpg_quality_label'],
        1, 100, 95
    )

st.sidebar.markdown("---")

# 패턴 모양 선택
st.sidebar.markdown(f"### {M['pattern_shape_title']}")
st.sidebar.markdown(M['pattern_shape_content'], unsafe_allow_html=True)
pattern_shape = st.sidebar.radio(
    M['pattern_shape_label'],
    ('Square', 'Round', 'Circle', 'Diamond', 'Star', 'Cross'),
    index=0
)
if file_format == 'SVG' and pattern_shape != 'Square':
    st.sidebar.warning(M['svg_pattern_warning'])
    st.sidebar.info(M['svg_pattern_info'])
    pattern_shape = 'Square'

st.sidebar.markdown("---")

# 패턴 간격
st.sidebar.markdown(f"### {M['sidebar_gap_title']}")
st.sidebar.markdown(M['sidebar_gap_content'], unsafe_allow_html=True)
pattern_gap = st.sidebar.slider(
    M['sidebar_gap_label'],
    0, 10, 0
)
if pattern_shape == 'Square' or file_format == 'SVG':
    st.sidebar.info(M['square_gap_info'])
    pattern_gap = 0
st.sidebar.markdown("---")

# 색상 선택
st.sidebar.markdown(f"### {M['sidebar_color_title']}")
st.sidebar.markdown(M['sidebar_color_content'], unsafe_allow_html=True)
color_options = {
    'Black': '#000000',
    'White': '#FFFFFF',
    'Red': '#FF0000',
    'Green': '#008000',
    'Blue': '#0000FF',
    'Custom': 'custom'
}
pattern_color_option = st.sidebar.radio(
    M['pattern_color_label'],
    list(color_options.keys())
)
background_color_option = st.sidebar.radio(
    M['background_color_label'],
    list(color_options.keys()),
    index=1
)

# 커스텀 색상 입력
pattern_color = color_options.get(pattern_color_option)
if pattern_color_option == 'Custom':
    pattern_color = st.sidebar.text_input(
        M['custom_pattern_color_label'], 
        '#000000',
        key=f'custom_pattern_color_input_key_{st.session_state.custom_pattern_color_input_key}'
    )
    if not is_valid_hex(pattern_color):
        st.sidebar.warning(M['invalid_color_warning'])
        pattern_color = '#000000'
    
background_color = color_options.get(background_color_option)
if background_color_option == 'Custom':
    background_color = st.sidebar.text_input(
        M['custom_background_color_label'], 
        '#FFFFFF',
        key=f'custom_background_color_input_key_{st.session_state.custom_background_color_input_key}'
    )
    if not is_valid_hex(background_color):
        st.sidebar.warning(M['invalid_color_warning'])
        background_color = '#FFFFFF'

if file_format == 'SVG':
    pattern_color = "#000000"
    background_color = "#FFFFFF"
    st.sidebar.info(M['svg_color_info'])

st.sidebar.markdown("---")

# QR 코드 설정
st.sidebar.markdown(f"### {M['sidebar_qr_settings_title']}")

# 오류 보정 레벨 선택
st.sidebar.markdown(f"**{M['sidebar_error_correction_title']}**")
st.sidebar.markdown(M['sidebar_error_correction_content'], unsafe_allow_html=True)
error_correction_level_map = {
    M['error_correction_L']: qrcode.constants.ERROR_CORRECT_L,
    M['error_correction_M']: qrcode.constants.ERROR_CORRECT_M,
    M['error_correction_Q']: qrcode.constants.ERROR_CORRECT_Q,
    M['error_correction_H']: qrcode.constants.ERROR_CORRECT_H
}
error_correction_level_label = st.sidebar.radio(
    M['error_correction_level_label'],
    list(error_correction_level_map.keys())
)
error_correction_level = error_correction_level_map[error_correction_level_label]
st.sidebar.markdown("---")

# 마스크 패턴 선택
st.sidebar.markdown(f"**{M['sidebar_mask_pattern_title']}**")
st.sidebar.markdown(M['sidebar_mask_pattern_content'], unsafe_allow_html=True)
mask_pattern = st.sidebar.slider(M['mask_pattern_label'], 0, 7, 0)
st.sidebar.markdown("---")

# 메인 화면
st.header(M['preview_download_header'])

if not qr_content:
    st.info(M['no_qr_content_warning'])
else:
    # QR 코드 생성
    try:
        if file_format == 'SVG':
            qr_image = generate_qr(
                qr_content, 
                file_format, 
                box_size=10, 
                border=4,
                pattern_shape=pattern_shape,
                pattern_gap=pattern_gap,
                pattern_color=pattern_color,
                background_color=background_color,
                error_correction_level=error_correction_level
            )
            # SVG를 HTML로 직접 렌더링
            svg_html = qr_image.decode('utf-8')
            st.markdown(
                f'<div style="width: 100%; text-align: center;">{svg_html}</div>', 
                unsafe_allow_html=True
            )
            
            # 다운로드 버튼
            download_name = f'qrcode_{generate_sha256(qr_content)}.svg'
            st.download_button(
                label=M['download_button_label'].format(file_format),
                data=qr_image,
                file_name=download_name,
                mime="image/svg+xml"
            )
        else:
            qr_image = generate_qr(
                qr_content, 
                file_format, 
                box_size=10, 
                border=4,
                pattern_shape=pattern_shape,
                pattern_gap=pattern_gap,
                pattern_color=pattern_color,
                background_color=background_color,
                error_correction_level=error_correction_level
            )
            
            # 이미지 표시
            st.image(qr_image, use_column_width=True)
            
            # 다운로드 버튼
            buf = io.BytesIO()
            if file_format == 'JPG':
                rgb_image = qr_image.convert('RGB')
                rgb_image.save(buf, format='JPEG', quality=jpg_quality)
            else:
                qr_image.save(buf, format=file_format)
            
            download_name = f'qrcode_{generate_sha256(qr_content)}.{file_format.lower()}'
            st.download_button(
                label=M['download_button_label'].format(file_format),
                data=buf.getvalue(),
                file_name=download_name,
                mime=f'image/{file_format.lower()}'
            )

    except Exception as e:
        st.error(f"{M['error_message']} {e}")
        st.info(M['error_info'])
    
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown(f"<footer>{M['footer']}</footer>", unsafe_allow_html=True)
