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
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = 'ko'
if 'selected_lang_name' not in st.session_state:
    st.session_state.selected_lang_name = '한국어'

# 현재 언어 설정
current_lang = st.session_state.current_lang

# 페이지 설정
# page_title과 page_icon을 메시지 파일에서 가져오도록 수정
st.set_page_config(
    page_title=MESSAGES[current_lang]['page_title'],
    page_icon=MESSAGES[current_lang]['page_icon'],
    layout="wide",
)


def update_lang():
    """언어 선택 드롭다운의 콜백 함수."""
    # 드롭다운에서 선택된 언어 이름을 기반으로 언어 코드(ko, en)를 업데이트합니다.
    if st.session_state.lang_select_box == '한국어':
        st.session_state.current_lang = 'ko'
    else:
        st.session_state.current_lang = 'en'
    st.session_state.selected_lang_name = st.session_state.lang_select_box
    # 언어 변경 후 페이지를 새로고침하여 UI를 업데이트합니다.
    st.experimental_rerun()


# 메인 타이틀 및 언어 선택 드롭다운
# 타이틀과 언어 선택을 같은 라인에 정렬하기 위해 컬럼을 사용합니다.
title_col, lang_col = st.columns([0.8, 0.2])

with title_col:
    # 타이틀을 메시지 파일에서 가져오도록 수정
    st.title(MESSAGES[current_lang]['main_title'])

with lang_col:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)  # 타이틀과의 간격 조정
    # 언어 선택 드롭다운을 추가하고, 메시지 파일에서 레이블을 가져오도록 수정
    st.selectbox(
        label=MESSAGES[current_lang]['language_select'],
        options=['한국어', 'English'],
        index=['한국어', 'English'].index(st.session_state.selected_lang_name),
        key='lang_select_box',
        on_change=update_lang
    )

# ---
# 섹션1: 입력 및 설정
# 헤더를 메시지 파일에서 가져오도록 수정
st.header(MESSAGES[current_lang]['input_settings_header'])
st.markdown("---")

# QR 코드 내용 입력
# 헤더와 정보를 메시지 파일에서 가져오도록 수정
st.subheader(MESSAGES[current_lang]['qr_content_header'])
st.info(MESSAGES[current_lang]['qr_content_info'])

qr_content = st.text_area(
    # 레이블과 플레이스홀더를 메시지 파일에서 가져오도록 수정
    label=MESSAGES[current_lang]['qr_input_label'],
    value=st.session_state.qr_input_area,
    height=200,
    placeholder=MESSAGES[current_lang]['qr_input_placeholder']
)

# 문자 수 표시
qr_content_length = len(qr_content.encode('utf-8'))
if qr_content_length > 2000:
    # 메시지를 메시지 파일에서 가져오도록 수정
    st.warning(MESSAGES[current_lang]['char_count_exceeded'].format(qr_content_length))
elif qr_content_length > 1500:
    # 메시지를 메시지 파일에서 가져오도록 수정
    st.warning(MESSAGES[current_lang]['char_count_warning'].format(qr_content_length))
else:
    # 메시지를 메시지 파일에서 가져오도록 수정
    st.success(MESSAGES[current_lang]['char_count_success'].format(qr_content_length))

st.session_state.qr_input_area = qr_content

# ---
# 섹션2: 미리보기 및 다운로드
# 헤더를 메시지 파일에서 가져오도록 수정
st.header(MESSAGES[current_lang]['preview_download_header'])
st.markdown("---")

# 레이아웃을 위한 두 개의 컬럼 생성
preview_col, download_col = st.columns([0.7, 0.3])

# 미리보기 컬럼
with preview_col:
    # 헤더를 메시지 파일에서 가져오도록 수정
    st.subheader(MESSAGES[current_lang]['preview_header'])
    
    # QR 코드 생성
    if qr_content:
        # QR 코드 설정
        qr_settings = qrcode.QRCode(
            version=1,
            error_correction=getattr(qrcode.constants, 'ERROR_CORRECT_' + st.session_state.selected_error_correction),
            box_size=10,
            border=st.session_state.selected_border_size
        )
        qr_settings.add_data(qr_content)
        qr_settings.make(fit=True)

        img = qr_settings.make_image(
            # 패턴과 배경 색상을 메시지 파일에서 가져오거나 직접 입력하도록 수정
            image_factory=qrcode.image.svg.SvgPathImage if st.session_state.selected_file_format == 'SVG' else None,
            fill_color=st.session_state.selected_pattern_color if not st.session_state.custom_pattern_color_input else st.session_state.custom_pattern_color_input,
            back_color=st.session_state.selected_background_color if not st.session_state.custom_background_color_input else st.session_state.custom_background_color_input
        )

        # 이미지 표시
        img_buffer = io.BytesIO()
        if st.session_state.selected_file_format == 'SVG':
            img.save(img_buffer)
            # Streamlit이 SVG를 직접 지원하지 않으므로 base64로 인코딩하여 표시
            b64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
            st.markdown(
                f'<img src="data:image/svg+xml;base64,{b64}" alt="QR Code" style="width:100%; height:auto;">',
                unsafe_allow_html=True
            )
        else:
            img.save(img_buffer, st.session_state.selected_file_format, quality=st.session_state.jpg_quality)
            st.image(img_buffer, use_column_width=True)
    else:
        # 입력 내용이 없을 때 메시지를 메시지 파일에서 가져오도록 수정
        st.info(MESSAGES[current_lang]['no_content_message'])

# 다운로드 컬럼
with download_col:
    # 헤더를 메시지 파일에서 가져오도록 수정
    st.subheader(MESSAGES[current_lang]['download_header'])
    
    # QR 코드 생성 함수 (다운로드 버튼에 사용)
    def generate_qr_for_download():
        if not qr_content:
            st.error(MESSAGES[current_lang]['empty_qr_content_error'])
            return None, None
        
        qr_settings = qrcode.QRCode(
            version=1,
            error_correction=getattr(qrcode.constants, 'ERROR_CORRECT_' + st.session_state.selected_error_correction),
            box_size=10,
            border=st.session_state.selected_border_size
        )
        qr_settings.add_data(qr_content)
        qr_settings.make(fit=True)

        if st.session_state.selected_file_format == 'SVG':
            img = qr_settings.make_image(
                image_factory=qrcode.image.svg.SvgPathImage,
                # 색상 입력을 메시지 파일에서 가져오도록 수정
                fill_color=MESSAGES[current_lang]['default_svg_pattern_color'],
                back_color=MESSAGES[current_lang]['default_svg_background_color']
            )
        else:
            img = qr_settings.make_image(
                # 색상 입력을 메시지 파일에서 가져오도록 수정
                fill_color=st.session_state.selected_pattern_color if not st.session_state.custom_pattern_color_input else st.session_state.custom_pattern_color_input,
                back_color=st.session_state.selected_background_color if not st.session_state.custom_background_color_input else st.session_state.custom_background_color_input
            )

        # 파일 이름 생성
        timestamp = datetime.now(ZoneInfo('Asia/Seoul')).strftime("%Y%m%d_%H%M%S")
        content_hash = hashlib.sha256(qr_content.encode('utf-8')).hexdigest()[:8]
        file_name = f"qrcode_{content_hash}_{timestamp}.{st.session_state.selected_file_format.lower()}"

        img_buffer = io.BytesIO()
        if st.session_state.selected_file_format == 'SVG':
            img.save(img_buffer)
        else:
            img.save(img_buffer, st.session_state.selected_file_format, quality=st.session_state.jpg_quality)
        
        return img_buffer.getvalue(), file_name

    # 다운로드 버튼
    download_btn_text = MESSAGES[current_lang]['download_button_text']
    if st.button(download_btn_text, use_container_width=True):
        binary_data, file_name = generate_qr_for_download()
        if binary_data:
            st.download_button(
                label=download_btn_text,
                data=binary_data,
                file_name=file_name,
                mime=f"image/{st.session_state.selected_file_format.lower()}",
                use_container_width=True
            )
            # 다운로드 버튼을 누르면 상태가 변경되므로 페이지를 새로고침하여 다운로드 버튼이 활성화되도록 합니다.
            st.experimental_rerun()

# ---
# 사이드바
with st.sidebar:
    # 사이드바 제목을 메시지 파일에서 가져오도록 수정
    st.header(MESSAGES[current_lang]['sidebar_header'])
    st.markdown("---")
    
    # QR 코드 설정
    # 사이드바 헤더를 메시지 파일에서 가져오도록 수정
    st.subheader(MESSAGES[current_lang]['sidebar_qr_settings_title'])
    
    # 파일 형식 선택
    # 레이블과 옵션을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['file_format_title'])
    st.session_state.selected_file_format = st.radio(
        label="",
        options=['PNG', 'JPG', 'SVG'],
        index=0,
        key='file_format_radio'
    )
    st.markdown(MESSAGES[current_lang]['file_format_content'], unsafe_allow_html=True)
    
    # JPG 품질 슬라이더 (JPG 선택 시에만 표시)
    if st.session_state.selected_file_format == 'JPG':
        # 레이블을 메시지 파일에서 가져오도록 수정
        st.markdown(MESSAGES[current_lang]['jpg_quality_title'])
        st.session_state.jpg_quality = st.slider(
            label="",
            min_value=0,
            max_value=100,
            value=95,
            step=1,
            key='jpg_quality_slider'
        )

    # 에러 보정 레벨
    # 레이블과 옵션을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['sidebar_error_correction_title'])
    st.session_state.selected_error_correction = st.radio(
        label="",
        options=['L', 'M', 'Q', 'H'],
        index=1,
        key='error_correction_radio'
    )
    st.markdown(MESSAGES[current_lang]['sidebar_error_correction_content'])
    
    # 마스크 패턴
    # 레이블을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['sidebar_mask_pattern_title'])
    st.slider(
        label="",
        min_value=0,
        max_value=7,
        value=0,
        step=1,
        key='mask_pattern_slider'
    )
    st.markdown(MESSAGES[current_lang]['sidebar_mask_pattern_content'])
    
    st.markdown("---")
    
    # 모양 설정
    # 사이드바 헤더를 메시지 파일에서 가져오도록 수정
    st.subheader(MESSAGES[current_lang]['sidebar_shape_settings_title'])
    
    # 패턴 모양
    # 레이블과 옵션을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['sidebar_pattern_shape_title'])
    st.session_state.selected_pattern_shape = st.radio(
        label="",
        options=['Square', 'Rounded', 'Circle', 'Diamond', 'Star', 'Cross'],
        index=0,
        disabled=st.session_state.selected_file_format == 'SVG',
        key='pattern_shape_radio'
    )
    st.markdown(MESSAGES[current_lang]['sidebar_pattern_shape_content'])

    # 패턴 간격
    # 레이블을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['sidebar_gap_title'])
    st.slider(
        label="",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05,
        disabled=st.session_state.selected_pattern_shape == 'Square' or st.session_state.selected_file_format == 'SVG',
        key='pattern_gap_slider'
    )
    st.markdown(MESSAGES[current_lang]['sidebar_gap_content'])
    
    st.markdown("---")

    # 색상 설정
    # 사이드바 헤더를 메시지 파일에서 가져오도록 수정
    st.subheader(MESSAGES[current_lang]['sidebar_color_title'])
    
    # 패턴 색상
    # 레이블과 옵션을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['pattern_color_title'])
    st.session_state.selected_pattern_color = st.selectbox(
        label="",
        options=['black', 'red', 'green', 'blue', 'orange'],
        key='pattern_color_select',
        disabled=st.session_state.selected_file_format == 'SVG'
    )
    
    # 커스텀 패턴 색상 입력
    # 레이블을 메시지 파일에서 가져오도록 수정
    st.session_state.custom_pattern_color_input = st.text_input(
        label=MESSAGES[current_lang]['custom_pattern_color_input_label'],
        placeholder="#000000",
        disabled=st.session_state.selected_file_format == 'SVG'
    )
    
    # 배경 색상
    # 레이블과 옵션을 메시지 파일에서 가져오도록 수정
    st.markdown(MESSAGES[current_lang]['background_color_title'])
    st.session_state.selected_background_color = st.selectbox(
        label="",
        options=['white', 'yellow', 'cyan', 'magenta'],
        key='background_color_select',
        disabled=st.session_state.selected_file_format == 'SVG'
    )
    
    # 커스텀 배경 색상 입력
    # 레이블을 메시지 파일에서 가져오도록 수정
    st.session_state.custom_background_color_input = st.text_input(
        label=MESSAGES[current_lang]['custom_background_color_input_label'],
        placeholder="#FFFFFF",
        disabled=st.session_state.selected_file_format == 'SVG'
    )
    
    st.markdown(MESSAGES[current_lang]['sidebar_color_content'])

    # 하단 정보
    # 푸터를 메시지 파일에서 가져오도록 수정
    st.markdown("---")
    st.markdown(MESSAGES[current_lang]['footer'], unsafe_allow_html=True)
    
