"""
자.. 지금부터 이 코드가 기준이 되는 코드야...
수정하다 오류나거나 잘못된 방향으로 수정되면 항상 이버전으로
다시 시작하는 거야.. 알겠지??

QR 코드 생성 웹앱 - Streamlit 버전
휴대폰에서도 사용 가능

실행 방법:
1. pip install streamlit qrcode[pil]
2. streamlit run qrcode_web.py

또는 온라인에서 실행:
- Streamlit Cloud, Heroku, Replit 등에 배포 가능
"""

# qrcode_web.py

import streamlit as st
import qrcode
import io
import re
import math
import hashlib
import base64  # SVG 이미지 표시를 위해 추가
import qrcode.image.svg  # SVG 생성을 위해 추가
from datetime import datetime
from zoneinfo import ZoneInfo
from messages import messages
from PIL import Image, ImageDraw


# 오류 복원 수준 옵션과 상수 매핑
error_correction_map = {
    'low': qrcode.constants.ERROR_CORRECT_L,
    'medium': qrcode.constants.ERROR_CORRECT_M,
    'quartile': qrcode.constants.ERROR_CORRECT_Q,
    'high': qrcode.constants.ERROR_CORRECT_H,
}

# 기본 설정값을 초기화하는 함수
def reset_language_defaults():
    st.session_state.error_correction_key = "low"
    st.session_state.pattern_shape_key = "square"
    st.session_state.finder_pattern_shape_key = "square"
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.mask_pattern_select = 2
    st.session_state.corner_radius_input = 25
    st.session_state.finder_corner_radius_input = 25
    st.session_state.cell_gap_input = 0
    st.session_state.finder_cell_gap_input = 0
    st.session_state.jpg_quality_input = 70
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG"

# 세션 상태 초기화
if 'lang' not in st.session_state:
    st.session_state.lang = "ko"
    reset_language_defaults()
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = ""
if 'custom_bg_color_input_key' not in st.session_state:
    st.session_state.custom_bg_color_key = ""
if 'filename_input_key' not in st.session_state:
    st.session_state.filename_input_key = ""
if 'box_size_input' not in st.session_state:
    st.session_state.box_size_input = 20
if 'border_input' not in st.session_state:
    st.session_state.border_input = 2
if 'mask_pattern_select' not in st.session_state:
    st.session_state.mask_pattern_select = 2
if 'pattern_color_select' not in st.session_state:
    st.session_state.pattern_color_select = "black"
if 'bg_color_select' not in st.session_state:
    st.session_state.bg_color_select = "white"
if 'finder_corner_radius_input' not in st.session_state:
    st.session_state.finder_corner_radius_input = 25
if 'finder_cell_gap_input' not in st.session_state:
    st.session_state.finder_cell_gap_input = 0


# 언어에 따른 페이지 제목 매핑
dynamic_page_titles = {
    "ko": "QR 코드 생성기",
    "en": "QR Code Generator"
}

# 페이지 설정
st.set_page_config(
    page_title=dynamic_page_titles[st.session_state.lang],
    page_icon="🔲",
    layout="wide",
)


# 현재 언어 설정 불러오기
lang_messages = messages[st.session_state.lang]

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
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return hex_pattern.match(color_name)


# QR 코드 데이터 생성
def get_qr_data_object(data, box_size, border, error_correction, mask_pattern,):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )
        qr.add_data(data, optimize=0,)
        qr.make(fit=True)
        return qr
    except Exception as e:
        st.error(f"{lang_messages.get('qr_code_data_error', 'QR Code data creation error')}: {str(e)}")
        return None
    

# 사용자 정의 모양으로 QR 코드 이미지 생성 함수 (PNG)
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, pattern_shape, finder_pattern_shape, pattern_corner_radius, finder_corner_radius, pattern_cell_gap, finder_cell_gap,):
    if not qr_object:
        return None

    img_size = (qr_object.modules_count + 2 * border) * box_size
    img = Image.new('RGB', (img_size, img_size), back_color,)
    draw = ImageDraw.Draw(img)

    def draw_shape(draw, xy, shape, fill, corner_radius, cell_gap,):
        x1, y1, x2, y2 = xy
        effective_size = x2 - x1
        
        gap_pixels = int(box_size * (cell_gap / 100))
        new_x = x1 + gap_pixels // 2
        new_y = y1 + gap_pixels // 2
        new_x_end = x2 - (gap_pixels - gap_pixels // 2)
        new_y_end = y2 - (gap_pixels - gap_pixels // 2)
        draw_coords = [new_x, new_y, new_x_end, new_y_end]

        effective_size_after_gap = new_x_end - new_x
        
        if shape == lang_messages['pattern_shape_square']:
            draw.rectangle(draw_coords, fill=fill,)
        elif shape == lang_messages['pattern_shape_rounded']:
            radius = int(effective_size_after_gap * (corner_radius / 100))
            draw.rectangle([new_x + radius, new_y, new_x_end - radius, new_y_end], fill=fill,)
            draw.rectangle([new_x, new_y + radius, new_x_end, new_y_end - radius], fill=fill,)
            draw.pieslice([new_x, new_y, new_x + radius * 2, new_y + radius * 2], 180, 270, fill=fill,)
            draw.pieslice([new_x_end - radius * 2, new_y, new_x_end, new_y + radius * 2], 270, 360, fill=fill,)
            draw.pieslice([new_x, new_y_end - radius * 2, new_x + radius * 2, new_y_end], 90, 180, fill=fill,)
            draw.pieslice([new_x_end - radius * 2, new_y_end - radius * 2, new_x_end, new_y_end], 0, 90, fill=fill,)
        elif shape == lang_messages['pattern_shape_circle']:
            draw.ellipse(draw_coords, fill=fill,)
        elif shape == lang_messages['pattern_shape_diamond']:
            draw.polygon([(new_x + effective_size_after_gap/2, new_y), (new_x + effective_size_after_gap, new_y + effective_size_after_gap/2), (new_x + effective_size_after_gap/2, new_y + effective_size_after_gap), (new_x, new_y + effective_size_after_gap/2)], fill=fill,)
        elif shape == lang_messages['pattern_shape_star']:
            x_center = (new_x + new_x_end) / 2
            y_center = (new_y + new_y_end) / 2
            radius_outer = effective_size_after_gap / 2
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
            draw.polygon(points, fill=fill,)
        elif shape == lang_messages['pattern_shape_cross']:
            x_center = (new_x + new_x_end) / 2
            y_center = (new_y + new_y_end) / 2
            cross_width = effective_size_after_gap * 0.3
            draw.rectangle([new_x, y_center - cross_width/2, new_x_end, y_center + cross_width/2], fill=fill,)
            draw.rectangle([x_center - cross_width/2, new_y, x_center + cross_width/2, new_y_end], fill=fill,)

    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            is_finder_pattern = False
            # 세 개의 파인더 패턴 위치에 있는지 확인
            if (r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7):
                is_finder_pattern = True

            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size

                current_shape = finder_pattern_shape if is_finder_pattern else pattern_shape
                current_corner_radius = finder_corner_radius if is_finder_pattern else pattern_corner_radius
                current_cell_gap = finder_cell_gap if is_finder_pattern else pattern_cell_gap

                draw_coords = [x, y, x + box_size, y + box_size]
                draw_shape(draw, draw_coords, current_shape, fill_color, current_corner_radius, current_cell_gap,)

    return img


# QR 코드 SVG 생성 함수
def generate_qr_code_svg(data, box_size, border, error_correction, mask_pattern, fill_color, back_color,):
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

        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1,)
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1,)

        return svg_data, qr
    except Exception as e:
        st.error(f"{lang_messages.get('qr_code_svg_error', 'QR Code SVG creation error')}: {str(e)}")
        return None, None


# QR 내용만 초기화하는 콜백 함수 (파일명은 유지)
def clear_text_input():
    st.session_state.qr_input_area = ""


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
    st.session_state.error_correction_key = "low"
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG"
    st.session_state.pattern_shape_key = "square"
    st.session_state.finder_pattern_shape_key = "square"
    st.session_state.corner_radius_input = 25
    st.session_state.finder_corner_radius_input = 25
    st.session_state.cell_gap_input = 0
    st.session_state.finder_cell_gap_input = 0
    st.session_state.jpg_quality_input = 70


# 언어 변경 콜백 함수
def set_language():
    new_lang = st.session_state.language_select
    st.session_state.lang = new_lang
    reset_language_defaults()


# --- 사이드바 ---
with st.sidebar:
    st.header(lang_messages['sidebar_title'])
    st.markdown(f"**{lang_messages['sidebar_tip_title']}**")
    st.markdown(f"""
    - **{lang_messages['text_example']}**
    - **{lang_messages['website_example']}**
    - **{lang_messages['email_example']}**
    - **{lang_messages['email_full_example']}**
    - **{lang_messages['phone_example']}**
    - **{lang_messages['sms_example']}**
    - **{lang_messages['sms_full_example']}**
    - **{lang_messages['wifi_example']}**
    """)
    st.markdown("---\n" * 1)
    st.header(lang_messages['sidebar_setting_guide_title'])
    st.markdown(f"**{lang_messages['sidebar_file_format']}**")
    st.markdown(f"""
    {lang_messages['file_format_png']}
    {lang_messages['file_format_jpg']}
    {lang_messages['file_format_svg']}
    """)
    st.markdown(f"**{lang_messages['sidebar_pattern_shape']}**")
    st.markdown(f"""
    - {lang_messages['pattern_shape_square']}, {lang_messages['pattern_shape_rounded']}, {lang_messages['pattern_shape_circle']}, {lang_messages['pattern_shape_diamond']}, {lang_messages['pattern_shape_star']}, {lang_messages['pattern_shape_cross']} {lang_messages['pattern_shape_svg_note']}
    """)
    st.markdown(f"**{lang_messages['sidebar_pattern_gap']}**")
    st.markdown(f"""
    {lang_messages['pattern_gap_note1']}
    {lang_messages['pattern_gap_note2']}
    """)
    st.markdown("---\n" * 1)
    st.markdown(f"**{lang_messages['sidebar_color_input']}**")
    st.markdown(f"""
    {lang_messages['color_input_note1']}
    {lang_messages['color_input_note2']}
    {lang_messages['color_input_note3']}
    """)
    st.markdown("---\n" * 1)
    st.markdown(f"**{lang_messages['sidebar_qr_setting']}**")
    st.markdown(f"**{lang_messages['sidebar_error_correction']}**")
    st.markdown(f"""
    {lang_messages['error_correction_low']}
    {lang_messages['error_correction_medium']}
    {lang_messages['error_correction_quartile']}
    {lang_messages['error_correction_high']}
    """)
    st.markdown("---\n" * 1)
    st.markdown(f"**{lang_messages['sidebar_mask_pattern']}**")
    st.markdown(f"{lang_messages['mask_pattern_note']}")
    st.markdown("---\n" * 1)
    st.info(lang_messages['author_info'], icon="ℹ️")


# --- 메인 컨텐츠 ---
st.title(lang_messages['title'])
st.caption(lang_messages['description'])

# 언어 선택
lang_options = {
    "ko": "한국어",
    "en": "English",
    "ja": "日本語"
}
st.selectbox(
    lang_messages['language_select_label'],
    options=list(lang_options.keys()),
    format_func=lambda x: lang_options[x],
    key="language_select",
    on_change=set_language
)

st.markdown("---")

# 전체 초기화 버튼
st.button(lang_messages['reset_button'], help=lang_messages['reset_button_help'], on_click=reset_all_settings,)
st.markdown("---")

# 1. QR 코드 내용
st.header(lang_messages['main_header'])
st.subheader(lang_messages['qr_content_subheader'])
qr_text_input = st.text_area(
    lang_messages['text_area_label'],
    placeholder=lang_messages['text_area_placeholder'],
    value=st.session_state.qr_input_area,
    height=200,
    key='qr_input_area',
)

strip_option = st.checkbox(
    lang_messages['strip_option'],
    value=st.session_state.strip_option,
    help=lang_messages['strip_option_help'],
    key='strip_option'
)

if st.button(lang_messages['delete_button'], help=lang_messages['delete_button_help'], on_click=clear_text_input,):
    st.rerun()

st.markdown("---")

if strip_option:
    qr_data = qr_text_input.strip()
else:
    qr_data = qr_text_input

# 2. 파일 형식 선택
st.subheader(lang_messages['file_format_subheader'])
file_format_select = st.selectbox(
    lang_messages['file_format_select_label'],
    options=["PNG", "JPG", "SVG"],
    key='file_format_select'
)

if file_format_select == "JPG":
    st.info(lang_messages['jpg_quality_info'])
    jpg_quality_input = st.slider(
        lang_messages['jpg_quality_label'],
        min_value=1, max_value=100,
        value=st.session_state.jpg_quality_input,
        help=lang_messages['jpg_quality_help'],
        key='jpg_quality_input'
    )
else:
    jpg_quality_input = 100

st.markdown("---")


# 3. 패턴 모양 설정
st.subheader(lang_messages['pattern_shape_subheader'])
pattern_shape_options = {
    "square": lang_messages['pattern_shape_square'],
    "rounded": lang_messages['pattern_shape_rounded'],
    "circle": lang_messages['pattern_shape_circle'],
    "diamond": lang_messages['pattern_shape_diamond'],
    "star": lang_messages['pattern_shape_star'],
    "cross": lang_messages['pattern_shape_cross']
}
finder_pattern_shape_options = {
    "square": lang_messages['pattern_shape_square'],
    "rounded": lang_messages['pattern_shape_rounded'],
    "circle": lang_messages['pattern_shape_circle']
}

pattern_shape_select = st.selectbox(
    lang_messages['pattern_select_label'],
    options=list(pattern_shape_options.keys()),
    format_func=lambda x: pattern_shape_options[x],
    key='pattern_shape_key',
)

finder_pattern_shape_select = st.selectbox(
    lang_messages['finder_pattern_select_label'],
    options=list(finder_pattern_shape_options.keys()),
    format_func=lambda x: finder_pattern_shape_options[x],
    key='finder_pattern_shape_key',
)


# SVG 형식은 사각만 지원
if file_format_select == "SVG":
    st.warning(lang_messages['pattern_shape_warning'])

# 둥근 모서리 반경 설정
if pattern_shape_select == 'rounded':
    if file_format_select == "SVG":
        st.warning(lang_messages['corner_radius_warning'])
    corner_radius_input = st.slider(
        lang_messages['corner_radius_label'],
        min_value=0, max_value=50,
        value=st.session_state.corner_radius_input,
        help=lang_messages['corner_radius_help'],
        key='corner_radius_input'
    )
else:
    corner_radius_input = 0


# 파인더 패턴 둥근 모서리 반경
if finder_pattern_shape_select == 'rounded':
    finder_corner_radius_input = st.slider(
        lang_messages['finder_corner_radius_label'],
        min_value=0, max_value=50,
        value=st.session_state.finder_corner_radius_input,
        help=lang_messages['finder_corner_radius_help'],
        key='finder_corner_radius_input'
    )
    st.warning(lang_messages['finder_corner_radius_warning'])
else:
    finder_corner_radius_input = 0


# 패턴 간격
if file_format_select == "SVG":
    st.warning(lang_messages['cell_gap_warning'])
    cell_gap_input = 0
else:
    cell_gap_input = st.slider(
        lang_messages['cell_gap_label'],
        min_value=0, max_value=100,
        value=st.session_state.cell_gap_input,
        help=lang_messages['cell_gap_help'],
        key='cell_gap_input'
    )

finder_cell_gap_input = st.slider(
    lang_messages['finder_cell_gap_label'],
    min_value=0, max_value=100,
    value=st.session_state.finder_cell_gap_input,
    help=lang_messages['finder_cell_gap_help'],
    key='finder_cell_gap_input'
)
st.warning(lang_messages['finder_cell_gap_warning'])

st.markdown("---")


# 4. 색상 설정
st.subheader(lang_messages['color_subheader'])

# SVG 경고 메시지
if file_format_select == "SVG":
    st.warning(lang_messages['svg_color_warning'])
    pattern_color = "black"
    bg_color = "white"

else:
    # 색상 선택 드롭다운
    color_options = {
        "black": "검정",
        "white": "하양",
        "red": "빨강",
        "blue": "파랑",
        "green": "초록",
        "yellow": "노랑",
        "custom_color": lang_messages['custom_color_select']
    }
    
    st.session_state.pattern_color_select = st.selectbox(
        lang_messages['pattern_color_label'],
        options=list(color_options.keys()),
        format_func=lambda x: color_options[x] if x != 'custom_color' else messages[st.session_state.lang]['custom_color_select'],
        key='pattern_color_select'
    )

    st.session_state.bg_color_select = st.selectbox(
        lang_messages['bg_color_label'],
        options=list(color_options.keys()),
        format_func=lambda x: color_options[x] if x != 'custom_color' else messages[st.session_state.lang]['custom_color_select'],
        key='bg_color_select'
    )

    pattern_color_choice = st.session_state.pattern_color_select
    bg_color_choice = st.session_state.bg_color_select

    # 사용자 정의 색상 입력
    if pattern_color_choice == "custom_color" or bg_color_choice == "custom_color":
        st.info(lang_messages['custom_color_info'])
        st.caption(lang_messages['custom_color_example'])

        # 패턴 색상 HEX 입력
        if pattern_color_choice == "custom_color":
            custom_pattern_color_input = st.text_input(
                lang_messages['pattern_hex_label'],
                placeholder=lang_messages['custom_color_placeholder'],
                key='custom_pattern_color_input_key',
                max_chars=7
            ).strip()
            if not is_valid_color(custom_pattern_color_input):
                st.warning(lang_messages.get('pattern_hex_invalid_warning', "Invalid HEX value for pattern color."), icon="⚠️")
                pattern_color = None
            else:
                pattern_color = custom_pattern_color_input
        else:
            pattern_color = pattern_color_choice
        
        # 배경 색상 HEX 입력
        if bg_color_choice == "custom_color":
            custom_bg_color_input = st.text_input(
                lang_messages['bg_hex_label'],
                placeholder=lang_messages['custom_color_placeholder'],
                key='custom_bg_color_input_key',
                max_chars=7
            ).strip()
            if not is_valid_color(custom_bg_color_input):
                st.warning(lang_messages.get('bg_hex_invalid_warning', "Invalid HEX value for background color."), icon="⚠️")
                bg_color = None
            else:
                bg_color = custom_bg_color_input
        else:
            bg_color = bg_color_choice

    else:
        pattern_color = pattern_color_choice
        bg_color = bg_color_choice
    
    # 패턴과 배경 색상이 같을 때 경고
    if pattern_color == bg_color and qr_data:
        st.warning(lang_messages['same_color_warning'], icon="⚠️")
        pattern_color = None
        bg_color = None

st.markdown("---")


# 5. QR 코드 설정
st.subheader(lang_messages['qr_setting_subheader'])

# 오류 보정 레벨
error_correction_options = {
    "low": lang_messages['error_correction_low_select'],
    "medium": lang_messages['error_correction_medium_select'],
    "quartile": lang_messages['error_correction_quartile_select'],
    "high": lang_messages['error_correction_high_select'],
}
error_correction_key = st.selectbox(
    lang_messages['error_correction_label'],
    options=list(error_correction_options.keys()),
    format_func=lambda x: error_correction_options[x],
    key='error_correction_key'
)
error_correction_level = error_correction_map[error_correction_key]


# 박스 사이즈 & 테두리
box_size_input = st.number_input(
    lang_messages['box_size_label'],
    min_value=1, max_value=50,
    value=st.session_state.box_size_input,
    key='box_size_input'
)

border_input = st.number_input(
    lang_messages['border_label'],
    min_value=0, max_value=10,
    value=st.session_state.border_input,
    key='border_input'
)

mask_pattern_select = st.radio(
    lang_messages['mask_pattern_label'],
    options=list(range(8)),
    index=st.session_state.mask_pattern_select,
    key='mask_pattern_select'
)

st.markdown("---")

# 6. 파일명 설정
st.subheader(lang_messages['filename_subheader'])
filename_input = st.text_input(
    lang_messages['filename_input_label'],
    placeholder=lang_messages['filename_placeholder'],
    value=st.session_state.filename_input_key,
    key='filename_input_key'
)
if st.button(lang_messages['filename_delete_button'], help=lang_messages['filename_delete_help'], on_click=clear_filename_callback,):
    st.rerun()

# 파일명 자동 생성 (입력된 내용의 해시값 사용)
if not filename_input:
    file_extension = file_format_select.lower()
    # 해시 값을 파일명으로 사용
    hashed_name = hashlib.md5(qr_data.encode()).hexdigest()
    filename = f"qr-code-{hashed_name}.{file_extension}"
else:
    file_extension = file_format_select.lower()
    filename = f"{sanitize_filename(filename_input)}.{file_extension}"

st.markdown(f"{lang_messages['download_filename_display']} `{filename}`")
st.markdown("---")


# 7. 미리보기 및 다운로드
st.header(lang_messages['preview_header'])

if qr_data:
    if pattern_color is not None and bg_color is not None:
        try:
            # QR 코드 생성
            qr_object = get_qr_data_object(
                data=qr_data,
                box_size=box_size_input,
                border=border_input,
                error_correction=error_correction_level,
                mask_pattern=mask_pattern_select
            )

            if qr_object:
                # 미리보기
                st.subheader(lang_messages['preview_subheader'])
                st.info(lang_messages['preview_success'])

                # 이미지 생성
                if file_format_select == "SVG":
                    svg_data, _ = generate_qr_code_svg(
                        data=qr_data,
                        box_size=box_size_input,
                        border=border_input,
                        error_correction=error_correction_level,
                        mask_pattern=mask_pattern_select,
                        fill_color="black",
                        back_color="white",
                    )
                    st.image(f"data:image/svg+xml;base64,{base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')}")
                    img_bytes = svg_data.encode('utf-8')
                else:
                    img = draw_custom_shape_image(
                        qr_object,
                        box_size_input,
                        border_input,
                        pattern_color,
                        bg_color,
                        pattern_shape_options[pattern_shape_select],
                        finder_pattern_shape_options[finder_pattern_shape_select],
                        corner_radius_input,
                        finder_corner_radius_input,
                        cell_gap_input,
                        finder_cell_gap_input,
                    )

                    # 바이트 스트림에 이미지 저장
                    img_bytes_io = io.BytesIO()
                    if file_format_select == "PNG":
                        img.save(img_bytes_io, format='PNG')
                    elif file_format_select == "JPG":
                        img.save(img_bytes_io, format='JPEG', quality=jpg_quality_input, optimize=True)
                    img_bytes = img_bytes_io.getvalue()

                    st.image(img)

                # QR 정보 표시
                qr_version = qr_object.version
                qr_modules_count = qr_object.modules_count
                qr_border_count = qr_object.border
                qr_box_size = qr_object.box_size
                qr_width = (qr_modules_count + qr_border_count * 2) * qr_box_size
                qr_height = qr_width

                st.markdown(f"**{lang_messages['qr_info_header']}**")
                st.markdown(lang_messages['qr_version'].format(version=qr_version))
                st.markdown(lang_messages['qr_modules_count'].format(modules_count=qr_modules_count))
                st.markdown(lang_messages['qr_border_count'].format(border_count=qr_border_count))
                st.markdown(lang_messages['qr_box_size'].format(box_size=qr_box_size))
                st.markdown(lang_messages['qr_image_size'].format(width=qr_width, height=qr_height))
                st.markdown(lang_messages['qr_size_formula'])
                st.markdown(lang_messages['qr_pattern_color'].format(color=pattern_color))
                st.markdown(lang_messages['qr_bg_color'].format(color=bg_color))

                # 다운로드
                st.subheader(lang_messages['download_subheader'])
                st.download_button(
                    label=lang_messages['download_button'],
                    data=img_bytes,
                    file_name=filename,
                    help=lang_messages['download_help']
                )

        except Exception as e:
            st.error(f"Error creating QR code: {str(e)}")
            st.warning(lang_messages['preview_warning'])

    else:
        st.warning(lang_messages['preview_warning'])
else:
    st.info(lang_messages['no_input_info'])

st.markdown("---")
kst_zone = ZoneInfo('Asia/Seoul')
current_time_kst = datetime.now(kst_zone).strftime('%Y-%m-%d %H:%M:%S')
st.caption(f"최종 업데이트: {current_time_kst} KST")
