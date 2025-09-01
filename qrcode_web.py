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
if 'strip_option' not in st.session_state:  # 상태 변수 이름 통일
    st.session_state.strip_option = True
if 'file_format_select' not in st.session_state: # 파일 형식 선택 상태 추가
    st.session_state.file_format_select = "PNG"


# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip
