# qrcode_web.py

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

import streamlit as st
import qrcode
import io
import re
import math
import hashlib
import base64
import qrcode.image.svg
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

# st.session_state를 초기화하는 함수
if "lang" not in st.session_state:
    st.session_state.lang = "ko"

# 언어 선택 드롭다운의 on_change 콜백 함수
def set_language():
    st.session_state.lang = st.session_state.lang_select

# 마스크 패턴 드롭다운의 on_change 콜백 함수
def set_mask_pattern():
    st.session_state.mask_pattern = st.session_state.mask_pattern_select

# `st.selectbox`의 `format_func`에 사용할 함수
def format_option(option_key):
    return f"{messages[option_key]['native_flag']} {messages[option_key]['native_name']}"

# `error_correction` 드롭다운의 `format_func`에 사용할 함수
def format_ec(option):
    return messages[st.session_state.lang][option]

def reset_language_defaults():
    st.session_state.error_correction_select = messages[st.session_state.lang]['error_correction_low_select']
    st.session_state.error_correction = 'low'
    st.session_state.pattern_shape = 'square'
    st.session_state.border = 4
    st.session_state.gap = 0
    st.session_state.dot_color = 'black'
    st.session_state.background_color = 'white'
    st.session_state.file_format = 'png'
    st.session_state.mask_pattern = 0

# QR 코드 생성 함수
def create_qrcode(content, error_correction, box_size, border, dot_color, background_color, shape, gap, file_format):
    # 선택된 모양에 따라 QR 코드 패턴 모듈을 정의합니다.
    if shape == 'square':
        # 기본 정사각형 모듈을 사용합니다.
        pass
    elif shape == 'rounded':
        # 둥근 모서리 모듈을 사용합니다.
        class RoundedSquareModule(qrcode.image.base.BaseImage):
            def drawrect(self, row, col):
                rounded_square_size = self.box_size * (1 - gap)
                offset = self.box_size * gap / 2
                x = (col * self.box_size) + offset
                y = (row * self.box_size) + offset
                self.draw.rounded_rectangle(
                    (x, y, x + rounded_square_size, y + rounded_square_size),
                    radius=rounded_square_size / 2,
                    fill=self.fill_color
                )
        qr_image_factory = RoundedSquareModule
    elif shape == 'circle':
        # 원형 모듈을 사용합니다.
        class CircleModule(qrcode.image.base.BaseImage):
            def drawrect(self, row, col):
                circle_size = self.box_size * (1 - gap)
                offset = self.box_size * gap / 2
                x = (col * self.box_size) + offset
                y = (row * self.box_size) + offset
                self.draw.ellipse(
                    (x, y, x + circle_size, y + circle_size),
                    fill=self.fill_color
                )
        qr_image_factory = CircleModule
    elif shape == 'diamond':
        # 다이아몬드 모듈을 사용합니다.
        class DiamondModule(qrcode.image.base.BaseImage):
            def drawrect(self, row, col):
                diamond_size = self.box_size * (1 - gap)
                offset = self.box_size * gap / 2
                x = col * self.box_size + offset
                y = row * self.box_size + offset
                half_size = diamond_size / 2
                points = [
                    (x + half_size, y),
                    (x + diamond_size, y + half_size),
                    (x + half_size, y + diamond_size),
                    (x, y + half_size)
                ]
                self.draw.polygon(points, fill=self.fill_color)
        qr_image_factory = DiamondModule
    elif shape == 'star':
        # 별 모양 모듈을 사용합니다.
        class StarModule(qrcode.image.base.BaseImage):
            def drawrect(self, row, col):
                star_size = self.box_size * (1 - gap)
                offset = self.box_size * gap / 2
                x = col * self.box_size + offset
                y = row * self.box_size + offset
                center_x, center_y = x + star_size / 2, y + star_size / 2
                outer_radius = star_size / 2
                inner_radius = outer_radius / 2.5
                points = []
                for i in range(5):
                    outer_x = center_x + outer_radius * math.cos(math.radians(i * 72 - 90))
                    outer_y = center_y + outer_radius * math.sin(math.radians(i * 72 - 90))
                    points.append((outer_x, outer_y))
                    inner_x = center_x + inner_radius * math.cos(math.radians(i * 72 - 90 + 36))
                    inner_y = center_y + inner_radius * math.sin(math.radians(i * 72 - 90 + 36))
                    points.append((inner_x, inner_y))
                self.draw.polygon(points, fill=self.fill_color)
        qr_image_factory = StarModule
    elif shape == 'cross':
        # 십자가 모양 모듈을 사용합니다.
        class CrossModule(qrcode.image.base.BaseImage):
            def drawrect(self, row, col):
                cross_size = self.box_size * (1 - gap)
                offset = self.box_size * gap / 2
                x = col * self.box_size + offset
                y = row * self.box_size + offset
                rect_width = cross_size / 3
                self.draw.rectangle((x, y + rect_width, x + cross_size, y + 2 * rect_width), fill=self.fill_color)
                self.draw.rectangle((x + rect_width, y, x + 2 * rect_width, y + cross_size), fill=self.fill_color)
        qr_image_factory = CrossModule

    # SVG 파일 형식인 경우
    if file_format == 'svg':
        if shape != 'square' or dot_color != 'black' or background_color != 'white':
            st.error(messages[st.session_state.lang]['svg_color_pattern_error'])
            return None
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction_map[error_correction],
            box_size=box_size,
            border=border,
            image_factory=qrcode.image.svg.SvgPathImage
        )
    else:
        # PNG, JPG 파일 형식인 경우
        if shape in ['square', 'rounded', 'circle', 'diamond', 'star', 'cross']:
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_correction_map[error_correction],
                box_size=box_size,
                border=border,
                image_factory=qr_image_factory if shape != 'square' else None
            )
        else:
            st.error(messages[st.session_state.lang]['invalid_pattern_shape'])
            return None

    try:
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color=dot_color, back_color=background_color)
        
        # PIL.ImageDraw.Draw 객체에 둥근 사각형 그리기를 추가합니다.
        if shape == 'rounded':
            ImageDraw.Draw.rounded_rectangle = ImageDraw.rounded_rectangle
        
    except Exception as e:
        st.error(messages[st.session_state.lang]['qr_generation_error'].format(e))
        return None

    return img

def is_valid_hex(color_code):
    """
    유효한 HEX 색상 코드인지 확인하는 함수입니다.
    #RRGGBB 또는 #RGB 형식을 허용합니다.
    """
    return re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color_code)

def download_link(image_data, file_name, lang_messages):
    """
    다운로드 링크를 생성하는 함수입니다.
    """
    b64 = base64.b64encode(image_data).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{file_name}.png">{lang_messages["download_link_text"]}</a>'
    st.markdown(href, unsafe_allow_html=True)

def generate_and_display_qr(lang_messages):
    """
    QR 코드 생성 및 표시를 관리하는 메인 함수입니다.
    """
    st.markdown(f"### **{lang_messages['main_header']}**")
    st.markdown("---")

    # 언어 선택 드롭다운
    selected_lang = st.selectbox(
        label=messages[st.session_state.lang]['language_select_label'],
        options=list(messages.keys()),
        on_change=set_language,
        key="lang_select",
        index=list(messages.keys()).index(st.session_state.lang),
        format_func=format_option
    )

    # 텍스트 입력
    st.markdown(f"#### **{lang_messages['qr_content_subheader']}**")
    st.markdown(f"**{lang_messages['max_char_info']}**")
    qr_content = st.text_area(
        label=lang_messages['text_area_label'],
        placeholder=lang_messages['text_area_placeholder'],
        height=150
    )

    # 설정
    with st.expander(lang_messages['qr_setting_expander'], expanded=False):
        # QR 코드 버전 (box_size)
        col1, col2 = st.columns(2)
        with col1:
            box_size = st.slider(lang_messages['box_size'], 1, 20, 10, help=lang_messages['box_size_help'])
        with col2:
            st.info(f"{lang_messages['box_size_note1']} {box_size}")
            st.info(f"{lang_messages['box_size_note2']} {box_size * 21}x{box_size * 21}")

        # 여백 (border)
        col3, col4 = st.columns(2)
        with col3:
            border = st.slider(lang_messages['border'], 0, 10, 4, help=lang_messages['border_help'])
        with col4:
            st.info(f"{lang_messages['border_note1']} {border}")

        # 오류 보정 레벨
        error_correction_options = {
            messages[st.session_state.lang]['error_correction_low_select']: 'low',
            messages[st.session_state.lang]['error_correction_medium_select']: 'medium',
            messages[st.session_state.lang]['error_correction_quartile_select']: 'quartile',
            messages[st.session_state.lang]['error_correction_high_select']: 'high',
        }
        selected_ec_name = st.selectbox(
            label=lang_messages['error_correction'],
            options=list(error_correction_options.keys()),
            key='error_correction_select',
            index=list(error_correction_options.keys()).index(st.session_state.get('error_correction_select', messages[st.session_state.lang]['error_correction_low_select'])),
            help=lang_messages['error_correction_help']
        )
        error_correction = error_correction_options[selected_ec_name]

        # 마스크 패턴
        mask_pattern = st.slider(
            label=lang_messages['mask_pattern'],
            min_value=0,
            max_value=7,
            step=1,
            value=st.session_state.get('mask_pattern', 0),
            key="mask_pattern_select",
            help=lang_messages['mask_pattern_note'],
            on_change=set_mask_pattern
        )

        # 패턴 모양
        pattern_shape_options = {
            lang_messages['pattern_shape_square']: 'square',
            lang_messages['pattern_shape_rounded']: 'rounded',
            lang_messages['pattern_shape_circle']: 'circle',
            lang_messages['pattern_shape_diamond']: 'diamond',
            lang_messages['pattern_shape_star']: 'star',
            lang_messages['pattern_shape_cross']: 'cross',
        }
        selected_shape_name = st.selectbox(
            label=lang_messages['sidebar_pattern_shape'],
            options=list(pattern_shape_options.keys()),
            key="pattern_shape_select",
            index=list(pattern_shape_options.keys()).index(st.session_state.get('pattern_shape', lang_messages['pattern_shape_square'])),
            help=lang_messages['pattern_shape_help']
        )
        pattern_shape = pattern_shape_options[selected_shape_name]

        # 패턴 간격 (gap)
        gap_value = st.slider(
            label=lang_messages['sidebar_pattern_gap'],
            min_value=0.0,
            max_value=0.5,
            step=0.01,
            value=st.session_state.get('gap', 0.0),
            key="gap_select",
            help=lang_messages['pattern_gap_note']
        )

        # 색상 입력
        col5, col6 = st.columns(2)
        with col5:
            default_dot_color = st.session_state.get('dot_color', 'black')
            dot_color = st.color_picker(
                label=lang_messages['dot_color_picker'],
                value=default_dot_color,
                help=lang_messages['dot_color_picker_help']
            )

        with col6:
            default_bg_color = st.session_state.get('background_color', 'white')
            background_color = st.color_picker(
                label=lang_messages['background_color_picker'],
                value=default_bg_color,
                help=lang_messages['background_color_picker_help']
            )

        # 파일 형식
        file_format_options = {
            lang_messages['file_format_png']: 'png',
            lang_messages['file_format_jpg']: 'jpeg',
            lang_messages['file_format_svg']: 'svg',
        }
        selected_format_name = st.selectbox(
            label=lang_messages['sidebar_file_format'],
            options=list(file_format_options.keys()),
            key='file_format_select',
            index=list(file_format_options.keys()).index(st.session_state.get('file_format', lang_messages['file_format_png'])),
            help=lang_messages['file_format_help']
        )
        file_format = file_format_options[selected_format_name]

    st.markdown("---")

    # QR 코드 생성 및 다운로드
    if st.button(lang_messages['generate_button'], use_container_width=True):
        if not qr_content:
            st.warning(lang_messages['content_required_warning'])
            return

        # QR 코드 생성
        qr_image = create_qrcode(qr_content, error_correction, box_size, border, dot_color, background_color, pattern_shape, gap_value, file_format)
        
        if qr_image:
            st.image(qr_image, caption=lang_messages['generated_qr_caption'], use_column_width=True)

            # 다운로드 버튼
            buf = io.BytesIO()
            if file_format == 'svg':
                qr_image.save(buf)
                file_ext = "svg"
                mime_type = "image/svg+xml"
            elif file_format == 'jpeg':
                qr_image.save(buf, format="JPEG")
                file_ext = "jpg"
                mime_type = "image/jpeg"
            else: # PNG
                qr_image.save(buf, format="PNG")
                file_ext = "png"
                mime_type = "image/png"
            
            buf.seek(0)
            
            # 파일 이름 생성
            file_name_hash = hashlib.sha1(qr_content.encode('utf-8')).hexdigest()[:8]
            seoul_timezone = ZoneInfo('Asia/Seoul')
            current_time = datetime.now(seoul_timezone).strftime('%Y%m%d_%H%M%S')
            file_name = f"QR_{file_name_hash}_{current_time}"

            st.download_button(
                label=lang_messages['download_button'],
                data=buf,
                file_name=f"{file_name}.{file_ext}",
                mime=mime_type,
                use_container_width=True
            )

def main():
    lang = st.session_state.lang
    lang_messages = messages[lang]

    st.title(lang_messages['title'])
    st.markdown(f"**{lang_messages['description']}**")
    
    with st.sidebar:
        st.title(lang_messages['sidebar_title'])
        st.markdown(f"**{lang_messages['sidebar_tip_title']}**")
        st.info(lang_messages['sidebar_tip_1'])
        st.info(lang_messages['sidebar_tip_2'])
        st.info(lang_messages['sidebar_tip_3'])

        st.markdown("---")
        st.markdown(f"**{lang_messages['sidebar_setting_guide_title']}**")
        
        st.markdown(f"**{lang_messages['sidebar_file_format']}**")
        st.markdown(f"\"\"\"\n{lang_messages['file_format_png']}\n{lang_messages['file_format_jpg']}\n{lang_messages['file_format_svg']}\n\"\"\"")

        st.markdown(f"**{lang_messages['sidebar_pattern_shape']}**")
        st.markdown(f"\"\"\"\n{lang_messages['pattern_shape_square']}\n{lang_messages['pattern_shape_rounded']}\n{lang_messages['pattern_shape_circle']}\n{lang_messages['pattern_shape_diamond']}\n{lang_messages['pattern_shape_star']}\n{lang_messages['pattern_shape_cross']}\n\"\"\"")
        st.markdown(f"**{lang_messages['pattern_shape_note1']}**")
        
        st.markdown(f"**{lang_messages['sidebar_pattern_gap']}**")
        st.markdown(f"\"\"\"\n{lang_messages['pattern_gap_note1']}\n{lang_messages['pattern_gap_note2']}\n\"\"\"")

        st.markdown(f"**{lang_messages['sidebar_color_input']}**")
        st.markdown(f"\"\"\"\n{lang_messages['color_input_note1']}\n{lang_messages['color_input_note2']}\n{lang_messages['color_input_note3']}\n\"\"\"")

        st.markdown(f"**{lang_messages['sidebar_qr_setting']}**")
        st.markdown(f"**{lang_messages['sidebar_error_correction']}**")
        st.markdown(f"\"\"\"\n{lang_messages['error_correction_low']}\n{lang_messages['error_correction_medium']}\n{lang_messages['error_correction_quartile']}\n{lang_messages['error_correction_high']}\n\"\"\"")
        
        st.markdown(f"**{lang_messages['sidebar_mask_pattern']}**")
        st.markdown(f"\"\"\"\n{lang_messages['mask_pattern_note']}\n\"\"\"")

        st.markdown("---")
        st.markdown(f"*{lang_messages['author_info']}*", unsafe_allow_html=True)

    generate_and_display_qr(lang_messages)

if __name__ == "__main__":
    main()
