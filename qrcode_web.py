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

# messages.py 파일에서 메시지 사전 가져오기
from messages import MESSAGES

# 세션 상태 초기화
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = 0
if 'custom_background_color_input_key' not in st.session_state:
    st.session_state.custom_background_color_input_key = 0
if 'language' not in st.session_state:
    st.session_state.language = 'ko' # 기본 언어 설정

# Streamlit 페이지 설정을 언어에 따라 동적으로 변경
st.set_page_config(
    page_title=MESSAGES[st.session_state.language]['page_title'],
    page_icon=MESSAGES[st.session_state.language]['page_icon'],
    layout="wide",
)

# 메인 UI
st.title(MESSAGES[st.session_state.language]['main_title'])

# --- 언어 선택 드롭다운 ---
# 언어 선택을 위한 드롭다운 메뉴를 타이틀 아래에 배치
lang = st.selectbox(
    MESSAGES[st.session_state.language]['language_select'],
    options=['ko', 'en'],
    format_func=lambda x: {'ko': '한국어', 'en': 'English'}[x],
    key='language_selector_box'
)

# 선택된 언어를 세션 상태에 저장하여 전체 UI를 업데이트
if lang != st.session_state.language:
    st.session_state.language = lang
    st.rerun()

# 선택된 언어에 해당하는 메시지 가져오기
messages = MESSAGES[st.session_state.language]

# --- 메인 섹션: 입력 및 설정 ---
st.header(messages['input_settings_header'])

# QR 코드 내용 입력
st.subheader(messages['qr_content_header'])
st.info(messages['qr_content_info'])

qr_content = st.text_area(
    label=messages['qr_input_label'],
    value=st.session_state.qr_input_area,
    height=200,
    placeholder=messages['qr_input_placeholder'],
    key="qr_content_input_area",
    on_change=lambda: st.session_state.update(qr_input_area=st.session_state.qr_content_input_area)
)

# 문자 수 계산 및 상태 표시
char_count = len(qr_content)
if char_count >= 2400:
    st.warning(messages['char_count_exceeded'].format(char_count))
elif char_count >= 2000:
    st.warning(messages['char_count_warning'].format(char_count))
else:
    st.success(messages['char_count_success'].format(char_count))

# QR 코드 설정
st.subheader(messages['qr_settings_header'])
col1, col2 = st.columns(2)

with col1:
    box_size = st.slider(
        messages['box_size_slider'],
        min_value=5,
        max_value=15,
        value=10
    )
    border = st.slider(
        messages['border_slider'],
        min_value=2,
        max_value=10,
        value=4
    )
    error_correction_options = {
        'L': messages['error_correction_L'],
        'M': messages['error_correction_M'],
        'Q': messages['error_correction_Q'],
        'H': messages['error_correction_H']
    }
    error_correction_level = st.selectbox(
        messages['error_correction_label'],
        options=list(error_correction_options.keys()),
        format_func=lambda x: error_correction_options[x]
    )

with col2:
    fill_color_options = {
        'black': messages['color_black'],
        'navy': messages['color_navy'],
        'dark_green': messages['color_dark_green'],
        'red': messages['color_red'],
        'brown': messages['color_brown'],
        'custom': messages['color_custom']
    }
    fill_color_select = st.selectbox(
        messages['pattern_color_label'],
        options=list(fill_color_options.keys()),
        format_func=lambda x: fill_color_options[x]
    )
    if fill_color_select == 'custom':
        custom_fill_color = st.text_input(
            messages['pattern_color_custom_input'],
            value='#000000',
            key=f'custom_pattern_color_input_{st.session_state.custom_pattern_color_input_key}'
        )
        fill_color = custom_fill_color
    else:
        fill_color = fill_color_select

    back_color_options = {
        'white': messages['color_white'],
        'light_gray': messages['color_light_gray'],
        'light_blue': messages['color_light_blue'],
        'light_yellow': messages['color_light_yellow'],
        'light_green': messages['color_light_green'],
        'custom': messages['color_custom']
    }
    back_color_select = st.selectbox(
        messages['background_color_label'],
        options=list(back_color_options.keys()),
        format_func=lambda x: back_color_options[x]
    )
    if back_color_select == 'custom':
        custom_back_color = st.text_input(
            messages['background_color_custom_input'],
            value='#FFFFFF',
            key=f'custom_background_color_input_{st.session_state.custom_background_color_input_key}'
        )
        back_color = custom_back_color
    else:
        back_color = back_color_select

# 파일 형식 및 품질 선택
file_format_options = {
    'PNG': 'PNG',
    'JPG': 'JPG',
    'SVG': 'SVG'
}
file_format = st.radio(
    messages['file_format_label'],
    options=list(file_format_options.keys()),
    horizontal=True
)

if file_format == 'JPG':
    jpg_quality = st.slider(
        messages['jpg_quality_slider'],
        min_value=0,
        max_value=100,
        value=95
    )

# --- 미리보기 및 다운로드 섹션 ---
st.header(messages['preview_download_header'])

# QR 코드 생성 함수
def create_qrcode():
    if not qr_content:
        st.warning(messages['qr_content_empty_warning'])
        return None, None

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{error_correction_level}'),
            box_size=box_size,
            border=border
        )
        qr.add_data(qr_content)
        qr.make(fit=True)

        img_buffer = io.BytesIO()

        if file_format == 'SVG':
            qr_svg = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
            qr_svg.save(img_buffer)
            img_buffer.seek(0)
            return "image/svg+xml", img_buffer.getvalue()

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(img_buffer, format=file_format, quality=jpg_quality if file_format == 'JPG' else None)
        img_buffer.seek(0)
        return f"image/{file_format.lower()}", img_buffer.getvalue()

    except Exception as e:
        st.error(messages['qr_generation_error'].format(e))
        return None, None

mimetype, img_data = create_qrcode()

if img_data:
    # 미리보기
    st.subheader(messages['preview_header'])
    if file_format == 'SVG':
        b64_img = base64.b64encode(img_data).decode('utf-8')
        html_code = f'<img src="data:image/svg+xml;base64,{b64_img}" alt="QR Code" style="width:100%; height:auto;">'
        st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.image(img_data, caption=messages['qr_preview_caption'])
    
    # 다운로드 버튼
    st.subheader(messages['download_header'])
    
    # 파일 이름 생성
    # 해시 값을 사용하여 고유한 파일명 생성
    hashed_content = hashlib.sha256(qr_content.encode('utf-8')).hexdigest()[:10]
    now_utc = datetime.now(ZoneInfo('UTC'))
    file_name = f"qrcode_{now_utc.strftime('%Y%m%d%H%M%S')}_{hashed_content}.{file_format.lower()}"
    
    st.download_button(
        label=messages['download_button_label'],
        data=img_data,
        file_name=file_name,
        mime=mimetype
    )

# 사이드바
with st.sidebar:
    st.title(messages['sidebar_title'])
    
    # 섹션 1: 도움말
    st.subheader(messages['sidebar_help_header'])
    
    st.markdown(messages['sidebar_help_content'])
    
    st.markdown("---")
    
    # 섹션 2: 파일 형식
    st.subheader(messages['sidebar_file_format_title'])
    st.markdown(messages['sidebar_file_format_content'])
    
    st.markdown("---")
    
    # 섹션 3: QR 코드 설정
    st.subheader(messages['sidebar_qr_settings_title'])
    
    st.markdown(messages['sidebar_error_correction_title'])
    st.markdown(messages['sidebar_error_correction_content'])
    
    st.markdown("---")
    
    st.markdown(messages['sidebar_mask_pattern_title'])
    st.markdown(messages['sidebar_mask_pattern_content'])
    
    st.markdown("---")
    
    st.markdown(messages['sidebar_color_title'])
    st.markdown(messages['sidebar_color_content'])
    
# 하단 정보
st.markdown(
    messages['footer'],
    unsafe_allow_html=True
)
