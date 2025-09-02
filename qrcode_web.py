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
import base64  # SVG 이미지 표시를 위해 추가
import qrcode.image.svg  # SVG 생성을 위해 추가
import math

# messages.py 파일에서 메시지 딕셔너리를 가져옵니다.
from messages import MESSAGES

# 페이지 설정
# st.set_page_config는 앱 실행 시 한 번만 설정되므로, 기본 언어(한국어)로 설정합니다.
st.set_page_config(
    page_title=MESSAGES['ko']['page_title'],
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

# 언어 세션 상태 초기화
if 'lang' not in st.session_state:
    st.session_state.lang = 'ko'

# 현재 선택된 언어에 맞는 메시지를 가져옵니다.
messages = MESSAGES[st.session_state.lang]

# 색상 선택 리스트 (사용자 정의 색상 제외)
COLOR_OPTIONS = [
    'black', 'white', 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta',
    'navy', 'lime', 'maroon', 'olive', 'purple', 'teal', 'silver', 'gray'
]

# QR 코드 생성 함수
def create_qr_code(
    text,
    pattern_color_hex,
    background_color_hex,
    transparent_background,
    border,
    error_correction,
    box_size,
    mask_pattern,
    custom_border
):
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        mask_pattern=mask_pattern,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=pattern_color_hex,
        back_color=background_color_hex,
        image_factory=qrcode.image.pil.PilImage,
    )

    if transparent_background:
        # 새로운 RGBA 모드 이미지 생성
        transparent_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
        # 원래 이미지의 패턴만 가져와 투명 이미지에 붙여넣기
        pixels = img.getdata()
        transparent_pixels = []
        for p in pixels:
            if p == img.info.get('back_color'):  # 배경색과 같으면 투명하게
                transparent_pixels.append((255, 255, 255, 0))
            else:  # 패턴색은 그대로
                transparent_pixels.append(p)
        transparent_img.putdata(transparent_pixels)

        # 원래 이미지의 여백을 고려하여 최종 이미지 생성
        if custom_border > 0:
            final_img = Image.new('RGBA', transparent_img.size, (0, 0, 0, 0))
            final_img.paste(transparent_img, (0, 0))
            return final_img
        else:
            return transparent_img
    else:
        return img

# QR 코드에 사용자 정의 패턴 적용 함수
def apply_custom_pattern(qr_image, pattern_type, gap_ratio):
    if pattern_type == 'Square':
        return qr_image

    img_size = qr_image.size
    img_draw = ImageDraw.Draw(qr_image)
    pixels = qr_image.load()

    # 모듈(작은 사각형)의 크기 계산
    box_size = img_size[0] // (qr_image.get_border() * 2 + qr_image.modules.size)

    # QR 코드 데이터의 시작점 계산
    start_x = qr_image.get_border() * box_size
    start_y = qr_image.get_border() * box_size

    # 패턴 간격에 따른 크기 조절
    center_size = box_size * (1 - gap_ratio)
    offset = box_size * gap_ratio / 2

    # QR 코드 데이터 부분을 순회하며 패턴 그리기
    for r in range(qr_image.modules.size):
        for c in range(qr_image.modules.size):
            if qr_image.modules[r, c]:  # True인 모듈만 패턴 적용
                x0 = start_x + c * box_size
                y0 = start_y + r * box_size
                x1 = x0 + box_size
                y1 = y0 + box_size

                # 기존 사각형 지우기 (배경색으로 덮기)
                img_draw.rectangle([x0, y0, x1, y1], fill=pixels[x0, y0])

                # 새로운 패턴 그리기
                pattern_color = pixels[x0, y0]
                center_x = x0 + box_size / 2
                center_y = y0 + box_size / 2
                half_size = center_size / 2

                if pattern_type == 'Rounded Square':
                    img_draw.rounded_rectangle(
                        (x0 + offset, y0 + offset, x1 - offset, y1 - offset),
                        radius=center_size / 4,
                        fill=pattern_color
                    )
                elif pattern_type == 'Circle':
                    img_draw.ellipse(
                        (x0 + offset, y0 + offset, x1 - offset, y1 - offset),
                        fill=pattern_color
                    )
                elif pattern_type == 'Diamond':
                    img_draw.polygon(
                        (
                            (center_x, y0 + offset),
                            (x1 - offset, center_y),
                            (center_x, y1 - offset),
                            (x0 + offset, center_y)
                        ),
                        fill=pattern_color
                    )
                elif pattern_type == 'Star':
                    # 별 그리기 (5개의 점)
                    img_draw.polygon(
                        (
                            (center_x, y0 + offset),
                            (center_x + half_size * 0.95, center_y - half_size * 0.3),
                            (x1 - offset, center_y),
                            (center_x + half_size * 0.3, center_y + half_size * 0.95),
                            (x0 + offset, center_y + half_size * 0.3)
                        ),
                        fill=pattern_color
                    )
                elif pattern_type == 'Cross':
                    img_draw.rectangle((x0 + offset, center_y - half_size * 0.3, x1 - offset, center_y + half_size * 0.3), fill=pattern_color)
                    img_draw.rectangle((center_x - half_size * 0.3, y0 + offset, center_x + half_size * 0.3, y1 - offset), fill=pattern_color)

    return qr_image

# 색상 유효성 검사 함수
def is_valid_hex(hex_str):
    if not isinstance(hex_str, str):
        return False
    hex_str = hex_str.strip()
    return re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_str) is not None

# 페이지 시작 부분
st.title(messages['main_title'])

# 언어 선택 드롭다운
def set_language():
    st.session_state.lang = st.session_state.language_select_box
lang_options = {'한국어': 'ko', 'English': 'en'}
selected_lang_name = st.selectbox(
    messages['language_select'],
    options=list(lang_options.keys()),
    index=list(lang_options.keys()).index('한국어' if st.session_state.lang == 'ko' else 'English'),
    key='language_select_box',
    on_change=set_language
)

st.header(messages['input_settings_header'])

# QR 코드 입력
st.subheader(messages['qr_content_header'])
st.text(messages['qr_content_info'])

# 입력 텍스트 영역
qr_input = st.text_area(
    label=messages['qr_input_label'],
    value=st.session_state.qr_input_area,
    height=200,
    placeholder=messages['qr_input_placeholder'],
    key='qr_input_area',
    on_change=lambda: st.session_state.update(qr_input_area=st.session_state.qr_input_area)
)

char_count = len(qr_input)
# QR 코드 최대 문자 수 표시
max_chars = 2900
if char_count > max_chars:
    st.caption(messages['char_count_exceeded'].format(char_count))
elif char_count >= max_chars * 0.8:
    st.caption(messages['char_count_warning'].format(char_count))
else:
    st.caption(messages['char_count_success'].format(char_count))

# 색상 설정
st.subheader(messages['color_settings_header'])

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("---")
    # 패턴 색상 선택
    pattern_color_choice = st.selectbox(
        label=messages['pattern_color_label'],
        options=COLOR_OPTIONS + [messages['custom_color_picker_label']],
        index=0
    )
    if pattern_color_choice == messages['custom_color_picker_label']:
        pattern_color_hex = st.color_picker(
            label=messages['custom_color_picker_label'],
            value='#000000',
            key='pattern_color_picker'
        )
    else:
        pattern_color_hex = pattern_color_choice
    
    # 색상 HEX 코드 직접 입력
    if st.checkbox(messages['custom_input_hex_label'], key='pattern_hex_input_checkbox'):
        st.session_state.custom_pattern_color_input_key += 1
        pattern_color_input = st.text_input(
            label=messages['custom_hex_input_label'],
            value=pattern_color_hex,
            key=f'pattern_hex_input_{st.session_state.custom_pattern_color_input_key}'
        )
        if not is_valid_hex(pattern_color_input):
            st.warning(messages['color_input_error'])
        else:
            pattern_color_hex = pattern_color_input

with col2:
    st.markdown("---")
    # 배경 색상 선택
    background_color_choice = st.selectbox(
        label=messages['background_color_label'],
        options=COLOR_OPTIONS + [messages['custom_color_picker_label']],
        index=1
    )
    if background_color_choice == messages['custom_color_picker_label']:
        background_color_hex = st.color_picker(
            label=messages['custom_color_picker_label'],
            value='#FFFFFF',
            key='background_color_picker'
        )
    else:
        background_color_hex = background_color_choice
    
    # 색상 HEX 코드 직접 입력
    if st.checkbox(messages['custom_input_hex_label'], key='background_hex_input_checkbox'):
        st.session_state.custom_background_color_input_key += 1
        background_color_input = st.text_input(
            label=messages['custom_hex_input_label'],
            value=background_color_hex,
            key=f'background_hex_input_{st.session_state.custom_background_color_input_key}'
        )
        if not is_valid_hex(background_color_input):
            st.warning(messages['color_input_error'])
        else:
            background_color_hex = background_color_input

st.subheader(messages['other_settings_header'])

# 기타 설정
col3, col4, col5 = st.columns([1, 1, 1])
with col3:
    # 에러 보정 레벨
    error_correction_level = st.selectbox(
        messages['error_correction_label'],
        options=['L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'],
        index=1
    )
    error_correction_map = {
        'L (7%)': qrcode.constants.ERROR_CORRECT_L,
        'M (15%)': qrcode.constants.ERROR_CORRECT_M,
        'Q (25%)': qrcode.constants.ERROR_CORRECT_Q,
        'H (30%)': qrcode.constants.ERROR_CORRECT_H
    }
    error_correction = error_correction_map[error_correction_level]
    
with col4:
    # 마스크 패턴
    mask_pattern = st.slider(messages['mask_pattern_label'], 0, 7, 0)

with col5:
    # 여백
    border = st.slider(messages['border_slider_label'], 0, 20, 4)
    custom_border = border
    transparent_background = st.checkbox(messages['transparent_background_label'])

# 패턴 모양, 패턴 간격
pattern_type = st.selectbox(
    messages['pattern_type_label'],
    options=['Square', 'Rounded Square', 'Circle', 'Diamond', 'Star', 'Cross']
)
gap_ratio = st.slider(messages['gap_slider_label'], 0.0, 0.5, 0.0, disabled=(pattern_type == 'Square'))

# SVG 파일 형식은 패턴 및 색상 제한이 있음
if pattern_type != 'Square' and st.session_state.file_format == 'SVG':
    st.warning(messages['svg_pattern_warning'])
    pattern_type = 'Square'

if gap_ratio > 0 and pattern_type == 'Square':
    st.warning(messages['gap_pattern_warning'])
    gap_ratio = 0.0

st.markdown("---")

# 다운로드 파일 형식
st.subheader(messages['download_settings_header'])
st.session_state.file_format = st.selectbox(messages['file_format_label'], options=['PNG', 'JPG', 'SVG'])
if st.session_state.file_format == 'JPG':
    jpeg_quality = st.slider(messages['jpeg_quality_label'], 0, 100, 95)
else:
    jpeg_quality = 95

# 사이드바
with st.sidebar:
    st.title(messages['sidebar_title'])
    st.markdown(messages['sidebar_content'])

    st.markdown("---")

    st.markdown(messages['sidebar_file_format_title'])
    st.markdown(messages['sidebar_file_format_content'])

    st.markdown("---")

    st.markdown(messages['sidebar_pattern_title'])
    st.markdown(messages['sidebar_pattern_content'])

    st.markdown(messages['sidebar_gap_title'])
    st.markdown(messages['sidebar_gap_content'])

    st.markdown("---")

    st.markdown(messages['sidebar_color_title'])
    st.markdown(messages['sidebar_color_content'])

    st.markdown("---")

    st.markdown(messages['sidebar_qr_settings_title'])
    st.markdown(messages['sidebar_error_correction_title'])
    st.markdown(messages['sidebar_error_correction_content'])

    st.markdown(messages['sidebar_mask_pattern_title'])
    st.markdown(messages['sidebar_mask_pattern_content'])

# 미리보기 및 다운로드
st.header(messages['preview_download_header'])

# 유효성 검사
if not qr_input:
    st.info(messages['input_info'])
else:
    # SVG 파일일 경우
    if st.session_state.file_format == 'SVG':
        # SVG는 색상 및 패턴 제한
        if not (pattern_color_hex == 'black' and background_color_hex == 'white' and pattern_type == 'Square'):
            st.warning(messages['svg_limitation_warning'])
            st.info(messages['svg_limitation_info'])
            
            # SVG를 생성하지 않고 미리보기 부분에 메시지 표시
            st.image('data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==', width=250)
            st.warning(messages['svg_display_warning'])
            
        else:
            try:
                # SVG 객체 생성 및 미리보기
                qr_svg = qrcode.QRCode(
                    version=None,
                    error_correction=error_correction,
                    box_size=10, # SVG는 고정된 크기
                    border=border,
                    mask_pattern=mask_pattern,
                )
                qr_svg.add_data(qr_input)
                qr_svg.make(fit=True)

                svg_image = qr_svg.make_image(
                    image_factory=qrcode.image.svg.SvgPathImage
                )
                
                # Streamlit에 SVG 표시를 위해 base64 인코딩
                svg_string = svg_image.to_string(encoding='utf-8')
                b64_svg = base64.b64encode(svg_string).decode('utf-8')
                st.image(f'data:image/svg+xml;base64,{b64_svg}', use_column_width=True)

                # 다운로드 버튼
                svg_bytes = svg_image.to_string(encoding='utf-8')
                st.download_button(
                    label=messages['download_svg_button'],
                    data=svg_bytes,
                    file_name="qrcode.svg",
                    mime="image/svg+xml"
                )
            except Exception as e:
                st.error(f"{messages['error_generating_qr']}: {e}")
                st.info(messages['check_input_size_info'])
                st.image('data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==', width=250)

    # PNG 또는 JPG 파일일 경우
    else:
        try:
            # QR 코드 생성
            qr_image = create_qr_code(
                qr_input,
                pattern_color_hex,
                background_color_hex,
                transparent_background,
                border,
                error_correction,
                box_size=10,
                mask_pattern=mask_pattern,
                custom_border=border
            )
            # 사용자 정의 패턴 적용
            qr_image = apply_custom_pattern(qr_image, pattern_type, gap_ratio)

            # 미리보기 표시
            st.image(qr_image, use_column_width=True)

            # 다운로드 버튼
            # PNG 다운로드
            if st.session_state.file_format == 'PNG':
                buf = io.BytesIO()
                qr_image.save(buf, format='PNG')
                byte_im = buf.getvalue()
                st.download_button(
                    label=messages['download_png_button'],
                    data=byte_im,
                    file_name="qrcode.png",
                    mime="image/png"
                )
            
            # JPG 다운로드
            elif st.session_state.file_format == 'JPG':
                buf = io.BytesIO()
                if transparent_background:
                    # JPG는 투명 배경을 지원하지 않으므로 흰색 배경으로 변환
                    rgb_image = Image.new("RGB", qr_image.size, (255, 255, 255))
                    rgb_image.paste(qr_image, (0, 0), qr_image)
                    rgb_image.save(buf, format='JPEG', quality=jpeg_quality)
                else:
                    qr_image.save(buf, format='JPEG', quality=jpeg_quality)
                byte_im = buf.getvalue()
                st.download_button(
                    label=messages['download_jpg_button'],
                    data=byte_im,
                    file_name="qrcode.jpg",
                    mime="image/jpeg"
                )

        except Exception as e:
            st.error(f"{messages['error_generating_qr']}: {e}")
            st.info(messages['check_input_size_info'])
            st.image('data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==', width=250)
            
# 푸터
st.markdown("---")
st.markdown(messages['footer'])
