import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw
import re
import base64
import qrcode.image.svg
import math

from messages import MESSAGES   # ✅ 다국어 메시지 불러오기

# 세션 상태 초기화
if 'language' not in st.session_state:
    st.session_state.language = 'ko'   # 기본 언어: 한국어

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
    st.session_state.error_correction_select = 'error_low'
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
    st.session_state.pattern_shape_select = 'pattern_square'
if 'finder_pattern_shape_select' not in st.session_state:
    st.session_state.finder_pattern_shape_select = 'pattern_square'
if 'corner_radius_input' not in st.session_state:
    st.session_state.corner_radius_input = 25
if 'cell_gap_input' not in st.session_state:
    st.session_state.cell_gap_input = 0
if 'jpg_quality_input' not in st.session_state:
    st.session_state.jpg_quality_input = 70

# 현재 언어 설정
lang = st.session_state.language
t = MESSAGES[lang]

# 페이지 설정
st.set_page_config(
    page_title=t['page_title'],
    page_icon=t['page_icon'],
    layout="wide",
)

# 언어 선택 드롭다운
lang_choice = st.selectbox(
    t['language_select'],
    options=[('ko', '한국어'), ('en', 'English')],
    format_func=lambda x: x[1],
    index=0 if lang == 'ko' else 1,
)
st.session_state.language = lang_choice[0]
lang = st.session_state.language
t = MESSAGES[lang]

# ---------------------------- 유틸 함수 ---------------------------- #

def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()

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
        st.error(t['qr_data_error'].format(str(e)))
        return None

# 사용자 정의 모양 QR 이미지 생성 (PNG/JPG)
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, pattern_shape, corner_radius, cell_gap, finder_pattern_shape):
    if not qr_object:
        return None

    img_size = (qr_object.modules_count + 2 * border) * box_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)

    gap_pixels = int(box_size * (cell_gap / 100))
    effective_box_size = box_size - gap_pixels

    def draw_shape(draw, xy, shape, fill, corner_radius):
        x1, y1, x2, y2 = xy
        effective_size = x2 - x1
        if shape == t['pattern_square']:
            draw.rectangle(xy, fill=fill)
        elif shape == t['pattern_rounded']:
            radius = int(effective_size * (corner_radius / 100))
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
            draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
        elif shape == t['pattern_circle']:
            draw.ellipse(xy, fill=fill)
        elif shape == t['pattern_diamond']:
            draw.polygon([(x1 + effective_size/2, y1), (x1 + effective_size, y1 + effective_size/2), (x1 + effective_size/2, y1 + effective_size), (x1, y1 + effective_size/2)], fill=fill)
        elif shape == t['pattern_star']:
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
        elif shape == t['pattern_cross']:
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            cross_width = (x2 - x1) * 0.3
            draw.rectangle([x1, y_center - cross_width/2, x2, y_center + cross_width/2], fill=fill)
            draw.rectangle([x_center - cross_width/2, y1, x_center + cross_width/2, y2], fill=fill)

    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size
                current_shape = finder_pattern_shape if ((r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7)) else pattern_shape
                new_x = x + gap_pixels // 2
                new_y = y + gap_pixels // 2
                new_x_end = x + box_size - (gap_pixels - gap_pixels // 2)
                new_y_end = y + box_size - (gap_pixels - gap_pixels // 2)
                draw_coords = [new_x, new_y, new_x_end, new_y_end]
                draw_shape(draw, draw_coords, current_shape, fill_color, corner_radius)

    return img

# SVG 생성
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
        st.error(t['qr_svg_error'].format(str(e)))
        return None, None

# ---------------------------- UI ---------------------------- #

st.title(t['main_title'])
st.markdown("---")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.header(t['input_settings_header'])
    st.subheader(t['qr_content_header'])
    st.info(t['qr_content_info'])

    qr_data = st.text_area(
        t['qr_input_label'],
        height=200,
        placeholder=t['qr_input_placeholder'],
        key="qr_input_area",
    )

    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(t['char_count_exceeded'].format(char_count))
        elif char_count > 2400:
            st.warning(t['char_count_warning'].format(char_count))
        else:
            st.success(t['char_count_success'].format(char_count))
    else:
        st.caption(t['char_count_zero'])

    strip_option = st.checkbox(
        t['strip_option_label'],
        value=st.session_state.strip_option,
        key="strip_option",
        help=t['strip_option_help']
    )

    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        st.button(
            t['delete_content_btn'],
            help=t['delete_content_help'],
            use_container_width=True,
            type="secondary",
            disabled=(char_count == 0),
            on_click=lambda: st.session_state.update(qr_input_area=""),
        )

    st.markdown("---")

    st.subheader(t['file_format_header'])
    file_format = st.selectbox(
        t['file_format_label'],
        ("PNG", "JPG", "SVG"),
        index=(0 if st.session_state.file_format_select == "PNG" else (1 if st.session_state.file_format_select == "JPG" else 2)),
        key="file_format_select",
    )
    if file_format == "JPG":
        st.caption(t['jpg_quality_info'])
        jpg_quality = st.slider(
            t['jpg_quality_label'],
            min_value=1, max_value=100,
            value=st.session_state.jpg_quality_input,
            key="jpg_quality_input",
            help=t['jpg_quality_help']
        )
    else:
        jpg_quality = 70

# ... (이후 모든 텍스트 출력 부분은 동일하게 t[...] 사용)

# 사이드바
with st.sidebar:
    st.header(t['sidebar_usage_title'])
    st.markdown(t['sidebar_usage_content'])
    st.markdown("---")
    st.header(t['sidebar_tips_title'])
    st.markdown(t['sidebar_tips_content'])
    st.markdown("---")
    st.header(t['sidebar_guide_title'])
    st.markdown(t['sidebar_file_format_title'])
    st.markdown(t['sidebar_file_format_content'])
    st.markdown("---")
    st.markdown(t['sidebar_pattern_title'])
    st.markdown(t['sidebar_pattern_content'])
    st.markdown("---")
    st.markdown(t['sidebar_gap_title'])
    st.markdown(t['sidebar_gap_content'])
    st.markdown("---")
    st.markdown(t['sidebar_color_title'])
    st.markdown(t['sidebar_color_content'])
    st.markdown("---")
    st.markdown(t['sidebar_qr_settings_title'])
    st.markdown(t['sidebar_error_correction_title'])
    st.markdown(t['sidebar_error_correction_content'])
    st.markdown("---")
    st.markdown(t['sidebar_mask_pattern_title'])
    st.markdown(t['sidebar_mask_pattern_content'])

# 푸터
st.markdown("---")
st.markdown(
    f'<p style="text-align: center; color: mediumslateblue; font-size: 15px;">{t["footer"]}</p>',
    unsafe_allow_html=True
)
