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
import math

# messages.py에서 다국어 메시지를 불러옵니다.
from messages import MESSAGES

# 세션 상태 초기화
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = 0
if 'custom_bg_color_input_key' not in st.session_state:
    st.session_state.custom_bg_color_input_key = 0
if 'svg_download_key' not in st.session_state:
    st.session_state.svg_download_key = 0
if 'png_download_key' not in st.session_state:
    st.session_state.png_download_key = 0
if 'jpg_download_key' not in st.session_state:
    st.session_state.jpg_download_key = 0
if 'qr_pattern_gap' not in st.session_state:
    st.session_state.qr_pattern_gap = 0
if 'qr_pattern_shape' not in st.session_state:
    st.session_state.qr_pattern_shape = 'square'
if 'qr_dark_color' not in st.session_state:
    st.session_state.qr_dark_color = "#000000"
if 'qr_bg_color' not in st.session_state:
    st.session_state.qr_bg_color = "#ffffff"
if 'lang' not in st.session_state:
    st.session_state.lang = 'ko'

# 언어 선택
lang_option = st.selectbox(
    MESSAGES[st.session_state.lang]['language_select'],
    ('한국어', 'English'),
    key='language_selector',
    on_change=lambda: st.session_state.__setitem__('lang', 'ko' if st.session_state.language_selector == '한국어' else 'en')
)
msgs = MESSAGES[st.session_state.lang]

# 페이지 설정
st.set_page_config(
    page_title=msgs['page_title'],
    page_icon=msgs['page_icon'],
    layout="wide",
)

st.title(msgs['main_title'])

# 사용자 정의 색상 유효성 검사 함수
def is_valid_hex_color(color_code):
    """6자리 또는 8자리의 유효한 16진수 색상 코드를 확인합니다."""
    return re.fullmatch(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$', color_code)

# QR 코드 생성 함수 (패턴/색상/간격 커스터마이징)
def create_custom_qr(content, file_format, dark_color, bg_color, quality=90, gap_size=0, pattern_shape='square'):
    """커스터마이징된 QR 코드를 생성하고 이미지 파일로 반환합니다."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    if pattern_shape == 'square' or file_format == 'svg':
        # 기본 사각형 패턴
        img = qr.make_image(fill_color=dark_color, back_color=bg_color)
    else:
        # 사용자 정의 패턴
        qr_array = qr.get_matrix()
        box_size = 10
        border = 4
        img_width = (len(qr_array) + border * 2) * box_size
        img = Image.new('RGB', (img_width, img_width), bg_color)
        draw = ImageDraw.Draw(img)

        # 픽셀마다 패턴 그리기
        for y, row in enumerate(qr_array):
            for x, module in enumerate(row):
                if module:
                    center_x = (x + border) * box_size + box_size / 2
                    center_y = (y + border) * box_size + box_size / 2
                    radius = (box_size / 2) - gap_size

                    if pattern_shape == 'rounded_square':
                        draw.rounded_rectangle(
                            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                            radius=radius/4,
                            fill=dark_color
                        )
                    elif pattern_shape == 'circle':
                        draw.ellipse(
                            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                            fill=dark_color
                        )
                    elif pattern_shape == 'diamond':
                        draw.polygon(
                            (
                                (center_x, center_y - radius),
                                (center_x + radius, center_y),
                                (center_x, center_y + radius),
                                (center_x - radius, center_y)
                            ),
                            fill=dark_color
                        )
                    elif pattern_shape == 'star':
                        # 5각형 별 모양
                        points = []
                        for i in range(5):
                            angle_outer = math.pi / 2 + i * 2 * math.pi / 5
                            angle_inner = angle_outer + math.pi / 5
                            points.append((
                                center_x + radius * math.cos(angle_outer),
                                center_y - radius * math.sin(angle_outer)
                            ))
                            points.append((
                                center_x + (radius / 2) * math.cos(angle_inner),
                                center_y - (radius / 2) * math.sin(angle_inner)
                            ))
                        draw.polygon(points, fill=dark_color)
                    elif pattern_shape == 'cross':
                        draw.rectangle(
                            (center_x - radius, center_y - radius/4, center_x + radius, center_y + radius/4),
                            fill=dark_color
                        )
                        draw.rectangle(
                            (center_x - radius/4, center_y - radius, center_x + radius/4, center_y + radius),
                            fill=dark_color
                        )
                        
    # SVG 형식인 경우 PIL Image 대신 SVG 객체 반환
    if file_format == 'svg':
        qr_svg = qrcode.make(
            content,
            image_factory=qrcode.image.svg.SvgPathImage,
        )
        # 색상 적용
        svg_content = qr_svg.to_string(encoding='utf-8').decode('utf-8')
        svg_content = svg_content.replace('fill="#000000"', f'fill="{dark_color}"')
        return svg_content
    
    return img

# 입력 및 설정 섹션
st.header(msgs['input_settings_header'])

# 입력 폼
with st.form("qr_input_form"):
    st.subheader(msgs['qr_content_header'])
    st.info(msgs['qr_content_info'])
    qr_input = st.text_area(
        label=msgs['qr_input_label'],
        placeholder=msgs['qr_input_placeholder'],
        height=200,
        key='qr_input_area'
    )
    
    char_count = len(qr_input)
    # 문자 수에 따라 다른 메시지 표시
    if char_count > 2000:
        st.markdown(msgs['char_count_exceeded'].format(char_count))
    elif char_count > 1000:
        st.markdown(msgs['char_count_warning'].format(char_count))
    else:
        st.markdown(msgs['char_count_success'].format(char_count))

    # 하단 버튼 그룹
    st.form_submit_button(msgs['download_button_label'])

# 미리보기 및 다운로드 섹션
st.header(msgs['preview_download_header'])

if not st.session_state.qr_input_area.strip():
    st.warning(msgs['input_empty_warning'])
else:
    # 사용자에게 선택지를 제공하여 커스텀 QR 코드 생성
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(msgs['sidebar_header'])
        
        # 파일 형식 선택
        st.markdown(msgs['sidebar_file_title'])
        file_format = st.selectbox(
            msgs['file_format_header'],
            ('png', 'jpg', 'svg'),
            key='file_format'
        )
        st.markdown(msgs['sidebar_file_content'])
        
        # JPG 품질 슬라이더
        quality = 90
        if file_format == 'jpg':
            quality = st.slider(msgs['jpg_quality_label'], 10, 100, 90, 10)
        
        st.markdown("---")

        # 패턴 모양 선택
        st.markdown(msgs['sidebar_pattern_title'])
        
        pattern_options = ['square', 'rounded_square', 'circle', 'diamond', 'star', 'cross']
        
        if file_format == 'svg':
            pattern_options = ['square']
            
        st.session_state.qr_pattern_shape = st.selectbox(
            msgs['pattern_shape_header'],
            options=pattern_options,
            key='pattern_shape_selector'
        )
        st.markdown(msgs['sidebar_pattern_content'])

        # 패턴 간격 조절
        st.markdown(msgs['sidebar_gap_title'])
        st.session_state.qr_pattern_gap = st.slider(msgs['pattern_gap_header'], 0, 5, 0)
        st.markdown(msgs['sidebar_gap_content'])
        
        st.markdown("---")

        # 색상 입력
        st.markdown(msgs['sidebar_color_title'])
        st.markdown(msgs['sidebar_color_content'])

        dark_color_input = st.text_input(
            msgs['dark_color_label'],
            value=st.session_state.qr_dark_color,
            max_chars=9,
            key=f'custom_pattern_color_{st.session_state.custom_pattern_color_input_key}'
        )
        bg_color_input = st.text_input(
            msgs['bg_color_label'],
            value=st.session_state.qr_bg_color,
            max_chars=9,
            key=f'custom_bg_color_{st.session_state.custom_bg_color_input_key}'
        )

        # 색상 유효성 검사
        is_dark_color_valid = is_valid_hex_color(dark_color_input)
        is_bg_color_valid = is_valid_hex_color(bg_color_input)
        
        if not dark_color_input or not bg_color_input:
            st.warning(msgs['color_valid_warning_msg'])
        elif not is_dark_color_valid or not is_bg_color_valid:
            st.warning(msgs['color_hex_warning_msg'])
        else:
            st.session_state.qr_dark_color = dark_color_input
            st.session_state.qr_bg_color = bg_color_input

        st.markdown("---")

        st.markdown(msgs['sidebar_qr_settings_title'])
        
        # 에러 수정 레벨
        st.markdown(msgs['sidebar_error_correction_title'])
        error_correction_options = {
            'L (7%)': qrcode.constants.ERROR_CORRECT_L,
            'M (15%)': qrcode.constants.ERROR_CORRECT_M,
            'Q (25%)': qrcode.constants.ERROR_CORRECT_Q,
            'H (30%)': qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_level = st.selectbox(
            msgs['error_correction_label'],
            options=list(error_correction_options.keys()),
        )
        st.markdown(msgs['sidebar_error_correction_content'])
        
        # 마스크 패턴
        st.markdown(msgs['sidebar_mask_pattern_title'])
        mask_pattern = st.slider(msgs['mask_pattern_label'], 0, 7, 0)
        st.markdown(msgs['sidebar_mask_pattern_content'])
        
    with col2:
        st.subheader(msgs['preview_download_header'])

        # 사용자 입력에 따라 QR 코드 생성 및 미리보기
        if st.session_state.qr_input_area:
            try:
                # QR 코드 생성
                qr_image = create_custom_qr(
                    st.session_state.qr_input_area,
                    file_format=file_format,
                    dark_color=st.session_state.qr_dark_color,
                    bg_color=st.session_state.qr_bg_color,
                    quality=quality,
                    gap_size=st.session_state.qr_pattern_gap,
                    pattern_shape=st.session_state.qr_pattern_shape
                )
                
                # SVG와 다른 형식의 다운로드 처리
                if file_format == 'svg':
                    st.image(f"data:image/svg+xml;base64,{base64.b64encode(qr_image.encode('utf-8')).decode('utf-8')}", use_column_width=True)
                    st.download_button(
                        label=msgs['download_svg'],
                        data=qr_image,
                        file_name="qrcode.svg",
                        mime="image/svg+xml"
                    )
                else:
                    # PIL 이미지 객체를 바이트로 변환
                    buf = io.BytesIO()
                    if file_format == 'png':
                        qr_image.save(buf, format='PNG')
                        mime_type = "image/png"
                    elif file_format == 'jpg':
                        qr_image.save(buf, format='JPEG', quality=quality)
                        mime_type = "image/jpeg"
                    
                    st.image(buf, use_column_width=True)
                    st.download_button(
                        label=f"{msgs['download_prefix']} {file_format.upper()}",
                        data=buf.getvalue(),
                        file_name=f"qrcode.{file_format}",
                        mime=mime_type
                    )
                    
            except Exception as e:
                st.error(f"{msgs['generation_error']}: {e}")
                
# 하단 정보
st.markdown("---")
st.markdown(msgs['footer'])
