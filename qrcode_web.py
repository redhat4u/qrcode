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

# 💡 필요한 라이브러리 및 모듈을 가져옵니다.
import streamlit as st # 웹 앱을 만들기 위한 핵심 라이브러리
import qrcode # QR 코드 생성 라이브러리
import io # 이미지 데이터를 메모리에서 처리하기 위한 모듈
import re # 정규표현식(Regular Expression)을 사용하여 문자열을 처리하는 모듈
import math # 수학 연산을 위한 모듈 (여기서는 별 모양을 그리는 데 사용)
import hashlib # 해시(Hash) 함수를 사용하기 위한 모듈 (현재는 사용되지 않으나 추후 확장성을 위해 남겨둠)
import base64 # 이진 데이터를 텍스트로 변환하는 모듈 (SVG 이미지 표시를 위해 추가됨)
import qrcode.image.svg # SVG 이미지 생성을 위한 모듈
from datetime import datetime
from zoneinfo import ZoneInfo
from messages import messages # 언어별 메시지를 담은 별도의 파일에서 사전(dictionary)을 가져옴
from PIL import Image, ImageDraw # Pillow 라이브러리: 이미지 생성 및 편집을 위한 모듈


# 💡 Streamlit 앱의 페이지 설정을 담당하는 함수입니다.
# 이 함수는 앱이 처음 시작될 때 단 한 번만 호출됩니다.
st.set_page_config(
    page_title="QR 코드 생성기", # 웹 브라우저 탭에 표시될 제목
    page_icon="🔲", # 탭에 표시될 아이콘
    layout="wide", # 전체 화면 너비를 사용하도록 설정
)

# 💡 QR 코드의 오류 복원 수준 옵션과 qrcode 라이브러리의 상수 값을 매핑합니다.
# 사용자가 선택한 텍스트 옵션을 실제 QR 코드 생성에 필요한 상수 값으로 변환합니다.
error_correction_map = {
    'low': qrcode.constants.ERROR_CORRECT_L,
    'medium': qrcode.constants.ERROR_CORRECT_M,
    'quartile': qrcode.constants.ERROR_CORRECT_Q,
    'high': qrcode.constants.ERROR_CORRECT_H,
}

# 💡 언어 변경 시 기본 설정값들을 초기화하는 함수입니다.
# `set_language` 함수에서 언어가 변경될 때 호출되어, 새로운 언어에 맞는 기본값으로 위젯을 초기화합니다.
def reset_language_defaults():
    # Streamlit의 `st.session_state`에 저장된 위젯 상태를 초기화합니다.
    st.session_state.error_correction_select = messages[st.session_state.lang]['error_correction_low_select']
    st.session_state.pattern_shape_select = messages[st.session_state.lang]['pattern_shape_square']
    st.session_state.finder_pattern_shape_select = messages[st.session_state.lang]['pattern_shape_square']
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

# 💡 세션 상태를 초기화하는 부분입니다.
# Streamlit 앱을 처음 실행하거나 새로고침할 때만 실행됩니다.
# `if '키' not in st.session_state:` 구문은 해당 키가 세션 상태에 존재하지 않을 때만 실행되도록 보장합니다.
if 'lang' not in st.session_state:
    st.session_state.lang = "ko" # 기본 언어를 한국어로 설정
    reset_language_defaults()
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


# 💡 현재 세션 상태에 설정된 언어에 따라 메시지 딕셔너리를 불러옵니다.
# 이렇게 하면 모든 텍스트가 동적으로 변경됩니다.
lang_messages = messages[st.session_state.lang]


# 💡 파일명에 특수문자가 포함된 경우 안전하게 '_'로 치환하는 함수입니다.
# 사용자가 입력한 파일명이 시스템에서 오류를 일으키지 않도록 방지합니다.
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()


# 💡 입력된 문자열이 유효한 색상(헥스 코드) 형식인지 확인하는 함수입니다.
def is_valid_color(color_name):
    if not color_name:
        return False
    color_name = color_name.strip()
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$') # #RRGGBB 또는 #RGB 형식의 정규표현식
    return hex_pattern.match(color_name)


# 💡 QR 코드 데이터를 기반으로 `qrcode` 라이브러리의 QR 객체를 생성하는 함수입니다.
# QR 코드의 버전, 오류 복원 수준, 박스 크기, 테두리 등을 설정합니다.
def get_qr_data_object(data, box_size, border, error_correction, mask_pattern,):
    try:
        # qrcode.QRCode 객체를 생성합니다.
        qr = qrcode.QRCode(
            version=1, # QR 코드의 버전 (1-40) - 1로 설정하면 데이터 양에 따라 자동으로 결정
            error_correction=error_correction, # 오류 복원 수준
            box_size=box_size, # QR 코드의 각 "박스"(모듈) 크기 (픽셀 단위)
            border=border, # QR 코드 주변의 테두리 두께 (모듈 단위)
            mask_pattern=mask_pattern, # 마스크 패턴 번호 (0-7)
        )
        qr.add_data(data, optimize=0,) # QR 코드에 데이터를 추가합니다.
        qr.make(fit=True) # 데이터에 맞게 QR 코드의 크기를 최적화합니다.
        return qr
    except Exception as e:
        # 오류 발생 시 사용자에게 에러 메시지를 표시합니다.
        st.error(f"{lang_messages['qr_code_data_error']}: {str(e)}")
        return None
    
# 💡 사용자 정의 모양으로 QR 코드 이미지(PNG/JPG)를 생성하는 핵심 함수입니다.
# `qrcode` 라이브러리 기본 기능 대신, PIL(Pillow)을 사용해 모듈 하나하나를 직접 그려서 다양한 모양을 구현합니다.
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, pattern_shape, finder_pattern_shape, pattern_corner_radius, finder_corner_radius, pattern_cell_gap, finder_cell_gap,):
    if not qr_object:
        return None

    # 전체 이미지 크기를 계산합니다. (QR 모듈 수 + 테두리) * 박스 크기
    img_size = (qr_object.modules_count + 2 * border) * box_size
    # 새로운 이미지 객체를 생성합니다.
    img = Image.new('RGB', (img_size, img_size), back_color,)
    draw = ImageDraw.Draw(img) # 이미지에 그리기 위한 `ImageDraw` 객체를 생성합니다.

    # 💡 다양한 모양을 그리는 내부 함수
    # 이 함수는 각 모듈(점)을 그릴 때 호출됩니다.
    def draw_shape(draw, xy, shape, fill, corner_radius, cell_gap,):
        x1, y1, x2, y2 = xy # 그릴 영역의 좌표를 가져옵니다.
        effective_size = x2 - x1
        
        # 픽셀 단위로 셀 간격(cell_gap)을 계산합니다.
        gap_pixels = int(box_size * (cell_gap / 100))
        # 간격이 적용된 새로운 좌표를 계산합니다.
        new_x = x1 + gap_pixels // 2
        new_y = y1 + gap_pixels // 2
        new_x_end = x2 - (gap_pixels - gap_pixels // 2)
        new_y_end = y2 - (gap_pixels - gap_pixels // 2)
        draw_coords = [new_x, new_y, new_x_end, new_y_end]

        effective_size_after_gap = new_x_end - new_x
        
        # 선택된 모양에 따라 적절한 그리기 함수를 호출합니다.
        if shape == lang_messages['pattern_shape_square']:
            draw.rectangle(draw_coords, fill=fill,)
        elif shape == lang_messages['pattern_shape_rounded']:
            # 둥근 사각형을 그리기 위해 모서리 반지름을 계산합니다.
            radius = int(effective_size_after_gap * (corner_radius / 100))
            # 4개의 모서리를 제외한 부분을 사각형으로 채우고, 4개의 모서리를 원호로 채웁니다.
            draw.rectangle([new_x + radius, new_y, new_x_end - radius, new_y_end], fill=fill,)
            draw.rectangle([new_x, new_y + radius, new_x_end, new_y_end - radius], fill=fill,)
            draw.pieslice([new_x, new_y, new_x + radius * 2, new_y + radius * 2], 180, 270, fill=fill,)
            draw.pieslice([new_x_end - radius * 2, new_y, new_x_end, new_y + radius * 2], 270, 360, fill=fill,)
            draw.pieslice([new_x, new_y_end - radius * 2, new_x + radius * 2, new_y_end], 90, 180, fill=fill,)
            draw.pieslice([new_x_end - radius * 2, new_y_end - radius * 2, new_x_end, new_y_end], 0, 90, fill=fill,)
        elif shape == lang_messages['pattern_shape_circle']:
            draw.ellipse(draw_coords, fill=fill,)
        elif shape == lang_messages['pattern_shape_diamond']:
            # 다이아몬드(마름모) 모양을 그립니다.
            draw.polygon([(new_x + effective_size_after_gap/2, new_y), (new_x + effective_size_after_gap, new_y + effective_size_after_gap/2), (new_x + effective_size_after_gap/2, new_y + effective_size_after_gap), (new_x, new_y + effective_size_after_gap/2)], fill=fill,)
        elif shape == lang_messages['pattern_shape_star']:
            # 별 모양을 그립니다.
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
            # 십자 모양을 그립니다.
            x_center = (new_x + new_x_end) / 2
            y_center = (new_y + new_y_end) / 2
            cross_width = effective_size_after_gap * 0.3
            draw.rectangle([new_x, y_center - cross_width/2, new_x_end, y_center + cross_width/2], fill=fill,)
            draw.rectangle([x_center - cross_width/2, new_y, x_center + cross_width/2, new_y_end], fill=fill,)

    # 💡 QR 코드의 모든 모듈(점)을 순회하며 그립니다.
    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            is_finder_pattern = False
            # 세 개의 파인더 패턴(모서리의 큰 사각형) 위치에 있는지 확인합니다.
            if (r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7):
                is_finder_pattern = True

            # 모듈이 검은색(True)이면 그립니다.
            if qr_object.modules[r][c]:
                # 픽셀 좌표를 계산합니다.
                x = (c + border) * box_size
                y = (r + border) * box_size

                # 파인더 패턴인지 일반 패턴인지에 따라 적용할 모양과 값을 결정합니다.
                current_shape = finder_pattern_shape if is_finder_pattern else pattern_shape
                current_corner_radius = finder_corner_radius if is_finder_pattern else pattern_corner_radius
                current_cell_gap = finder_cell_gap if is_finder_pattern else pattern_cell_gap

                draw_coords = [x, y, x + box_size, y + box_size]
                draw_shape(draw, draw_coords, current_shape, fill_color, current_corner_radius, current_cell_gap,)

    return img


# 💡 QR 코드 SVG를 생성하는 함수입니다.
# SVG는 벡터 기반이므로 모양 및 색상 변경 로직이 PNG/JPG와 다릅니다.
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

        # SVG 이미지 객체를 생성합니다.
        img_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)

        svg_buffer = io.BytesIO()
        img_svg.save(svg_buffer)
        svg_data = svg_buffer.getvalue().decode('utf-8')

        # SVG 파일 내의 기본 색상(black, white)을 사용자가 선택한 색상으로 교체합니다.
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1,)
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1,)

        return svg_data, qr
    except Exception as e:
        st.error(f"{lang_messages['qr_code_svg_error']}: {str(e)}")
        return None, None


# 💡 QR 코드 내용 입력창을 초기화하는 콜백 함수입니다.
# 버튼 클릭 시 `st.session_state` 값을 변경하여 입력창을 비웁니다.
def clear_text_input():
    st.session_state.qr_input_area = ""

# 💡 파일명 입력창을 초기화하는 콜백 함수입니다.
def clear_filename_callback():
    st.session_state.filename_input_key = ""

# 💡 모든 설정값을 초기화하는 콜백 함수입니다.
def reset_all_settings():
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""

    st.session_state.box_size_input = 20
    st.session_state.border_input = 2
    st.session_state.error_correction_select = messages[st.session_state.lang]['error_correction_low_select']
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG"
    st.session_state.pattern_shape_select = lang_messages['pattern_shape_square']
    st.session_state.finder_pattern_shape_select = lang_messages['pattern_shape_square']
    st.session_state.corner_radius_input = 25
    st.session_state.finder_corner_radius_input = 25
    st.session_state.cell_gap_input = 0
    st.session_state.finder_cell_gap_input = 0
    st.session_state.jpg_quality_input = 70

# 💡 언어 변경을 처리하는 핵심 콜백 함수입니다.
# 사용자가 언어를 변경하면 기존 위젯의 상태를 저장하고, 새로운 언어로 변환한 뒤 복원합니다.
# 이렇게 함으로써 언어를 바꿔도 입력된 내용이나 설정값들이 사라지지 않게 됩니다.
def set_language():
    old_lang = st.session_state.lang

    # 현재 설정값들을 임시 저장합니다.
    current_qr_data = st.session_state.get('qr_input_area', "")
    current_box_size = st.session_state.get('box_size_input', 20)
    current_border = st.session_state.get('border_input', 2)
    current_mask_pattern = st.session_state.get('mask_pattern_select', 2)
    current_error_correction_label = st.session_state.get('error_correction_select', messages[old_lang]['error_correction_low_select'])
    current_pattern_color_choice = st.session_state.get('pattern_color_select', "black")
    current_bg_color_choice = st.session_state.get('bg_color_select', "white")
    current_custom_pattern_color = st.session_state.get('custom_pattern_color_input_key', "")
    current_custom_bg_color = st.session_state.get('custom_bg_color_input_key', "")
    current_filename = st.session_state.get('filename_input_key', "")
    current_strip_option = st.session_state.get('strip_option', True)
    current_file_format = st.session_state.get('file_format_select', "PNG")
    current_pattern_shape = st.session_state.get('pattern_shape_select', messages[old_lang]['pattern_shape_square'])
    current_finder_shape = st.session_state.get('finder_pattern_shape_select', messages[old_lang]['pattern_shape_square'])
    current_corner_radius = st.session_state.get('corner_radius_input', 25)
    current_finder_corner_radius = st.session_state.get('finder_corner_radius_input', 25)
    current_cell_gap = st.session_state.get('cell_gap_input', 0)
    current_finder_cell_gap = st.session_state.get('finder_cell_gap_input', 0)
    current_jpg_quality = st.session_state.get('jpg_quality_input', 70)


    # 선택된 언어 이름을 언어 코드로 변환합니다.
    lang_map = {"한국어": "ko", "English": "en"}
    new_lang = lang_map.get(st.session_state.lang_select, "ko")

    # 언어 변경이 발생했을 때만 상태를 업데이트합니다.
    if new_lang != old_lang:
        st.session_state.lang = new_lang
        # 기존 언어의 오류 복원 레벨 텍스트를 상수값으로 변환합니다.
        error_correction_map_old_lang = {
            messages[old_lang]['error_correction_low_select']: qrcode.constants.ERROR_CORRECT_L,
            messages[old_lang]['error_correction_medium_select']: qrcode.constants.ERROR_CORRECT_M,
            messages[old_lang]['error_correction_quartile_select']: qrcode.constants.ERROR_CORRECT_Q,
            messages[old_lang]['error_correction_high_select']: qrcode.constants.ERROR_CORRECT_H,
        }
        current_error_constant = error_correction_map_old_lang.get(current_error_correction_label, qrcode.constants.ERROR_CORRECT_L)

        # 새로운 언어의 텍스트로 변환합니다.
        error_correction_map_new_lang = {
            qrcode.constants.ERROR_CORRECT_L: messages[new_lang]['error_correction_low_select'],
            qrcode.constants.ERROR_CORRECT_M: messages[new_lang]['error_correction_medium_select'],
            qrcode.constants.ERROR_CORRECT_Q: messages[new_lang]['error_correction_quartile_select'],
            qrcode.constants.ERROR_CORRECT_H: messages[new_lang]['error_correction_high_select'],
        }
        st.session_state.error_correction_select = error_correction_map_new_lang.get(current_error_constant, messages[new_lang]['error_correction_low_select'])

        # 패턴 모양도 동일하게 변환합니다.
        pattern_shape_map_old_lang = {
            messages[old_lang]['pattern_shape_square']: 'square',
            messages[old_lang]['pattern_shape_rounded']: 'rounded',
            messages[old_lang]['pattern_shape_circle']: 'circle',
            messages[old_lang]['pattern_shape_diamond']: 'diamond',
            messages[old_lang]['pattern_shape_star']: 'star',
            messages[old_lang]['pattern_shape_cross']: 'cross',
        }
        
        pattern_shape_map_new_lang = {
            'square': messages[new_lang]['pattern_shape_square'],
            'rounded': messages[new_lang]['pattern_shape_rounded'],
            'circle': messages[new_lang]['pattern_shape_circle'],
            'diamond': messages[new_lang]['pattern_shape_diamond'],
            'star': messages[new_lang]['pattern_shape_star'],
            'cross': messages[new_lang]['pattern_shape_cross'],
        }

        # 기존 선택된 값을 새 언어의 값으로 업데이트합니다.
        old_pattern_shape_key = pattern_shape_map_old_lang.get(current_pattern_shape, 'square')
        st.session_state.pattern_shape_select = pattern_shape_map_new_lang.get(old_pattern_shape_key, messages[new_lang]['pattern_shape_square'])
        
        old_finder_shape_key = pattern_shape_map_old_lang.get(current_finder_shape, 'square')
        st.session_state.finder_pattern_shape_select = pattern_shape_map_new_lang.get(old_finder_shape_key, messages[new_lang]['pattern_shape_square'])

    # 언어 변경 후, 임시 저장했던 값들을 다시 복원합니다.
    st.session_state.qr_input_area = current_qr_data
    st.session_state.box_size_input = current_box_size
    st.session_state.border_input = current_border
    st.session_state.mask_pattern_select = current_mask_pattern
    st.session_state.pattern_color_select = current_pattern_color_choice
    st.session_state.bg_color_select = current_bg_color_choice
    st.session_state.custom_pattern_color_input_key = current_custom_pattern_color
    st.session_state.custom_bg_color_input_key = current_custom_bg_color
    st.session_state.filename_input_key = current_filename
    st.session_state.strip_option = current_strip_option
    st.session_state.file_format_select = current_file_format
    st.session_state.corner_radius_input = current_corner_radius
    st.session_state.finder_corner_radius_input = current_finder_corner_radius
    st.session_state.cell_gap_input = current_cell_gap
    st.session_state.finder_cell_gap_input = current_finder_cell_gap
    st.session_state.jpg_quality_input = current_jpg_quality


#[메인]====================================================================================================================================================================

st.title(lang_messages['title'])
st.markdown("---")

# 💡 언어 선택 드롭다운
lang_options = {"한국어": "ko", "English": "en"}
lang_selected_name = st.selectbox(
    "Select Language" if st.session_state.lang == "en" else "언어 선택(Select Language)",
    options=list(lang_options.keys()),
    on_change=set_language, # ❗ 드롭다운 선택 시 `set_language` 함수를 호출하여 언어를 변경합니다.
    key="lang_select",
    index=list(lang_options.values()).index(st.session_state.lang),
)

st.markdown("---")

# 💡 메인 레이아웃을 두 개의 컬럼으로 나눕니다.
# col1: 입력 및 설정 영역, col2: 미리보기 및 다운로드 영역
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header(lang_messages['main_header'])

    # QR 코드 입력창
    st.subheader(lang_messages['qr_content_subheader'])
    st.info(lang_messages['max_char_info'])

    qr_data = st.text_area(
        lang_messages['text_area_label'],
        height=200,
        placeholder=lang_messages['text_area_placeholder'],
        key="qr_input_area", # ❗ 사용자의 입력값을 세션 상태에 저장합니다.
    )

    # 입력된 문자 수에 따라 경고/정보 메시지를 표시합니다.
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(lang_messages['char_count_exceeded'].format(char_count=char_count))
        elif char_count > 2400:
            st.warning(lang_messages['char_count_near_limit'].format(char_count=char_count))
        else:
            st.success(lang_messages['char_count_ok'].format(char_count=char_count))
    else:
        st.caption(lang_messages['char_count_zero'])

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        lang_messages['strip_option'],
        value=st.session_state.strip_option,
        key="strip_option",
        help=lang_messages['strip_option_help'],
    )

    # 입력 내용 삭제 버튼
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0) # 입력 내용이 없으면 버튼 비활성화
        st.button(
            lang_messages['delete_button'],
            help=lang_messages['delete_button_help'],
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input, # ❗ 버튼 클릭 시 `clear_text_input` 함수 호출
        )

    st.markdown("---")

    # 파일 형식 설정
    st.subheader(lang_messages['file_format_subheader'])
    file_format = st.selectbox(
        lang_messages['file_format_select_label'],
        ("PNG", "JPG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else (1 if st.session_state.file_format_select == "JPG" else 2),
        key="file_format_select",
    )

    # JPG 품질 설정 슬라이더 (JPG 선택 시에만 표시)
    if file_format == "JPG":
        st.caption(lang_messages['jpg_quality_info'])
        jpg_quality = st.slider(
            lang_messages['jpg_quality_label'],
            min_value=1,
            max_value=100,
            value=st.session_state.jpg_quality_input,
            key="jpg_quality_input",
            help=lang_messages['jpg_quality_help'],
        )
    else:
        jpg_quality = 70

    # 패턴 모양 설정
    st.markdown("---")
    st.subheader(lang_messages['pattern_shape_subheader'])
    # SVG 형식은 커스텀 모양을 지원하지 않으므로, SVG 선택 시 위젯을 비활성화합니다.
    pattern_shape_disabled = (file_format == "SVG")
    st.caption(lang_messages['pattern_shape_warning'])

    # 두 개의 패턴 모양 선택 옵션 추가
    col_pattern_shape, col_finder_shape = st.columns(2)

    pattern_options = (lang_messages['pattern_shape_square'], lang_messages['pattern_shape_rounded'], lang_messages['pattern_shape_circle'], lang_messages['pattern_shape_diamond'], lang_messages['pattern_shape_star'], lang_messages['pattern_shape_cross'],)

    with col_pattern_shape:
        pattern_shape = st.selectbox(
            lang_messages['pattern_select_label'],
            pattern_options,
            key="pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    with col_finder_shape:
        finder_pattern_shape = st.selectbox(
            lang_messages['finder_pattern_select_label'],
            pattern_options,
            key="finder_pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    # 둥근사각 전용 슬라이더 (일반 패턴)
    if pattern_shape == lang_messages['pattern_shape_rounded']:
        corner_radius_disabled = (file_format == "SVG")
        st.caption(lang_messages['corner_radius_warning'])
        corner_radius = st.slider(
            lang_messages['corner_radius_label'],
            min_value=0,
            max_value=50,
            value=st.session_state.corner_radius_input,
            help=lang_messages['corner_radius_help'],
            key="corner_radius_input",
            disabled=corner_radius_disabled,
        )
    else:
        corner_radius = 0

    # 둥근사각 전용 슬라이더 (파인더 패턴)
    if finder_pattern_shape == lang_messages['pattern_shape_rounded']:
        finder_corner_radius_disabled = (file_format == "SVG")
        st.caption(lang_messages['finder_corner_radius_warning'])
        finder_corner_radius = st.slider(
            lang_messages['finder_corner_radius_label'],
            min_value=0,
            max_value=50,
            value=st.session_state.finder_corner_radius_input,
            help=lang_messages['finder_corner_radius_help'],
            key="finder_corner_radius_input",
            disabled=finder_corner_radius_disabled,
        )
    else:
        finder_corner_radius = 0

    # 패턴 간격 슬라이더 (일반 패턴)
    cell_gap_disabled = (file_format == "SVG")
    st.caption(lang_messages['cell_gap_warning'])
    cell_gap = st.slider(
        lang_messages['cell_gap_label'],
        min_value=0,
        max_value=40,
        value=st.session_state.cell_gap_input,
        help=lang_messages['cell_gap_help'],
        disabled=cell_gap_disabled,
        key="cell_gap_input",
    )

    # 패턴 간격 슬라이더 (파인더 패턴)
    finder_cell_gap_disabled = (file_format == "SVG")
    st.caption(lang_messages['finder_cell_gap_warning'])
    finder_cell_gap = st.slider(
        lang_messages['finder_cell_gap_label'],
        min_value=0,
        max_value=40,
        value=st.session_state.finder_cell_gap_input,
        help=lang_messages['finder_cell_gap_help'],
        disabled=finder_cell_gap_disabled,
        key="finder_cell_gap_input",
    )
    
#========================================================================================================================================================================

    # 색상 설정
    st.markdown("---")
    st.subheader(lang_messages['color_subheader'])

    file_format_is_svg = (st.session_state.file_format_select == "SVG")

    if file_format_is_svg:
        st.warning(lang_messages['svg_color_warning'])

    # 색상 선택 드롭다운 리스트
    colors = [
        lang_messages['custom_color_select'], "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            lang_messages['pattern_color_label'], colors,
            index=colors.index(st.session_state.pattern_color_select),
            key="pattern_color_select",
            disabled=file_format_is_svg,
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            lang_messages['bg_color_label'], colors,
            index=colors.index(st.session_state.bg_color_select),
            key="bg_color_select",
            disabled=file_format_is_svg,
        )

    st.markdown(lang_messages['custom_color_info'])
    st.caption(lang_messages['custom_color_example'])
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            lang_messages['pattern_hex_label'],
            placeholder=lang_messages['custom_color_placeholder'],
            # "직접 입력"을 선택하거나 SVG 형식이면 비활성화
            disabled=(pattern_color_choice != lang_messages['custom_color_select']) or file_format_is_svg,
            key="custom_pattern_color_input_key",
        )
    with col1_6:
        st.text_input(
            lang_messages['bg_hex_label'],
            placeholder=lang_messages['custom_color_placeholder'],
            disabled=(bg_color_choice != lang_messages['custom_color_select']) or file_format_is_svg,
            key="custom_bg_color_input_key",
        )

    # 최종 색상 값을 결정합니다.
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '',).strip() if pattern_color_choice == lang_messages['custom_color_select'] else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '',).strip() if bg_color_choice == lang_messages['custom_color_select'] else bg_color_choice

#========================================================================================================================================================================

    # QR 코드 설정
    st.markdown("---")
    st.subheader(lang_messages['qr_setting_subheader'])

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input(lang_messages['box_size_label'], min_value=1, max_value=100, key="box_size_input",)
        border = st.number_input(lang_messages['border_label'], min_value=0, max_value=10, key="border_input",)

    with col1_2:
        # 오류 복원 수준 옵션과 상수 매핑
        error_correction_options = {
            lang_messages['error_correction_low_select']: qrcode.constants.ERROR_CORRECT_L,
            lang_messages['error_correction_medium_select']: qrcode.constants.ERROR_CORRECT_M,
            lang_messages['error_correction_quartile_select']: qrcode.constants.ERROR_CORRECT_Q,
            lang_messages['error_correction_high_select']: qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_options_list = list(error_correction_options.keys())

        try:
            current_error_index = error_correction_options_list.index(st.session_state.error_correction_select)
        except ValueError:
            current_error_index = 0 # 만약 세션 상태 값이 없으면 기본값으로

        error_correction_choice = st.selectbox(
            lang_messages['error_correction_label'],
            options=error_correction_options_list,
            index=current_error_index,
            key="error_correction_select",
        )
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox(lang_messages['mask_pattern_label'], options=list(range(8)), key="mask_pattern_select",)


#========================================================================================================================================================================

    # 파일명 설정
    st.markdown("---")
    st.subheader(lang_messages['filename_subheader'])

    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            lang_messages['filename_input_label'],
            placeholder=lang_messages['filename_placeholder'],
            key="filename_input_key",
        )

    current_filename = filename.strip()

    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "") # 파일명이 없으면 버튼 비활성화
        st.button(
            lang_messages['filename_delete_button'],
            help=lang_messages['filename_delete_help'],
            use_container_width=True,
            type="secondary",
            disabled=filename_delete_disabled,
            on_click=clear_filename_callback,
        )


#========================================================================================================================================================================
with col2:
    st.header(lang_messages['preview_header'])

    current_data = qr_data.strip() if st.session_state.strip_option else qr_data

    # 미리보기 생성 가능 여부 검사
    is_pattern_color_valid_preview = (pattern_color_choice != lang_messages['custom_color_select']) or (pattern_color_choice == lang_messages['custom_color_select'] and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != lang_messages['custom_color_select']) or (bg_color_choice == lang_messages['custom_color_select'] and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)

    preview_image_display = None
    preview_qr_object = None

    # 미리보기를 생성할 수 있는 조건을 확인합니다.
    can_generate_preview = current_data and (file_format == "SVG" or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview))

    download_data = None
    download_mime = ""
    download_extension = ""
    save_format = ""

    if can_generate_preview:
        try:
            # QR 코드 데이터 객체를 생성합니다.
            qr = get_qr_data_object(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                int(st.session_state.mask_pattern_select)
            )
            if qr:
                preview_qr_object = qr
                if file_format in ["PNG", "JPG"]:
                    # PNG/JPG 형식일 경우 커스텀 모양 이미지 생성 함수 호출
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        pattern_color, bg_color, st.session_state.pattern_shape_select,
                        st.session_state.finder_pattern_shape_select,
                        st.session_state.corner_radius_input,
                        st.session_state.finder_corner_radius_input,
                        st.session_state.cell_gap_input,
                        st.session_state.finder_cell_gap_input,
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
                    # SVG 형식일 경우 SVG 생성 함수 호출
                    svg_data, _ = generate_qr_code_svg(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                        int(st.session_state.mask_pattern_select), "black", "white",
                    )
                    download_data = svg_data.encode('utf-8')
                    download_mime = "image/svg+xml"
                    download_extension = ".svg"

                    # SVG는 색상 미리보기가 불가능하여, PNG용으로 변환된 기본 미리보기 이미지 생성
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", lang_messages['pattern_shape_square'],
                        lang_messages['pattern_shape_square'],
                        st.session_state.corner_radius_input,
                        st.session_state.finder_corner_radius_input,
                        st.session_state.cell_gap_input,
                        st.session_state.finder_cell_gap_input,
                    )
        except Exception as e:
            st.error(f"{lang_messages['error_occurred']}: {str(e)}")

    st.markdown("---")

    # 미리보기 이미지 표시 및 정보 출력
    if preview_image_display:
        st.success(lang_messages['preview_success'])
        st.subheader(lang_messages['preview_subheader'])
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=lang_messages['preview_subheader'], width=378)

        if preview_qr_object:
            st.subheader(lang_messages['qr_info_header'])
            st.info(f"""
- **{lang_messages['qr_version'].format(version=preview_qr_object.version)}**
- **{lang_messages['qr_modules_count'].format(modules_count=preview_qr_object.modules_count)}**
- **{lang_messages['qr_border_count'].format(border_count=2 * int(st.session_state.border_input))}**
- **{lang_messages['qr_box_size'].format(box_size=int(st.session_state.box_size_input))}**
- **{lang_messages['qr_image_size'].format(width=(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input), height=(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input))}**
---
- **{lang_messages['qr_size_formula']}**
---
- **{lang_messages['qr_pattern_color'].format(color='black' if file_format == 'SVG' else pattern_color)}**
- **{lang_messages['qr_bg_color'].format(color='white' if file_format == 'SVG' else bg_color)}**
            """)

        # 다운로드 섹션의 위치를 미리보기 아래로 이동
        st.markdown("---")
        st.subheader(lang_messages['download_subheader'])
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        # 파일명이 비어 있으면 현재 시각을 기반으로 자동 생성합니다.
        final_filename = sanitize_filename(st.session_state.filename_input_key.strip() if st.session_state.filename_input_key.strip() else now.strftime("QR_%Y-%m-%d_%H-%M-%S"))
        download_filename = f"{final_filename}{download_extension}"

        st.download_button(
            label=lang_messages['download_button'],
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=lang_messages['download_help'],
        )

        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{lang_messages["download_filename_display"]} </span> '
            f'<span style="color:dodgerblue;"> {download_filename}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    # 미리보기 생성 불가능 시 경고 메시지 표시
    elif current_data:
        st.warning(lang_messages['preview_warning'])

        if file_format != "SVG":
            if pattern_color_choice == lang_messages['custom_color_select'] and not pattern_color:
                st.warning(lang_messages['pattern_hex_empty_warning'])
            if bg_color_choice == lang_messages['custom_color_select'] and not bg_color:
                st.warning(lang_messages['bg_hex_empty_warning'])
            if pattern_color_choice == lang_messages['custom_color_select'] and pattern_color and not is_valid_color(pattern_color):
                st.warning(lang_messages['pattern_hex_invalid_warning'])
            if bg_color_choice == lang_messages['custom_color_select'] and bg_color and not is_valid_color(bg_color):
                st.warning(lang_messages['bg_hex_invalid_warning'])
            if is_colors_same_preview:
                st.warning(lang_messages['same_color_warning'])
    else:
        st.info(lang_messages['no_input_info'])


st.markdown("---")

st.button(
    label=lang_messages['reset_button'],
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help=lang_messages['reset_button_help'],
)

# 사이드바 내용
with st.sidebar:
    st.header(lang_messages['sidebar_title'])
    st.markdown(f"""
    {lang_messages['how_to_use_step1']}
    {lang_messages['how_to_use_step2']}
    {lang_messages['how_to_use_step3']}
    {lang_messages['how_to_use_step4']}
    {lang_messages['how_to_use_step5']}
    {lang_messages['how_to_use_step6']}
    """)

    st.markdown("---")

    st.header(lang_messages['sidebar_tip_title'])
    st.markdown(f"""
    - {lang_messages['text_example']}
    - {lang_messages['website_example']}
    - {lang_messages['email_example']}
    - {lang_messages['email_full_example']}
    - {lang_messages['phone_example']}
    - {lang_messages['sms_example']}
    - {lang_messages['sms_full_example']}
    - {lang_messages['wifi_example']}
    """)

    st.markdown("---")

    st.header(lang_messages['sidebar_setting_guide_title'])
    st.markdown(f"**{lang_messages['sidebar_file_format']}**")
    st.markdown(f"""
    {lang_messages['file_format_png']}
    {lang_messages['file_format_jpg']}
    {lang_messages['file_format_svg']}
    """)

    st.markdown("---")

    st.markdown(f"**{lang_messages['sidebar_pattern_shape']}**")
    st.markdown(f"""
    - {lang_messages['pattern_shape_square']}, {lang_messages['pattern_shape_rounded']}, {lang_messages['pattern_shape_circle']}, {lang_messages['pattern_shape_diamond']}, {lang_messages['pattern_shape_star']}, {lang_messages['pattern_shape_cross']} {lang_messages['pattern_shape_svg_note']}
    """)

    st.markdown(f"**{lang_messages['sidebar_pattern_gap']}**")
    st.markdown(f"""
    {lang_messages['pattern_gap_note1']}
    {lang_messages['pattern_gap_note2']}
    """)

    st.markdown("---")

    st.markdown(f"**{lang_messages['sidebar_color_input']}**")
    st.markdown(f"""
    {lang_messages['color_input_note1']}
    {lang_messages['color_input_note2']}
    {lang_messages['color_input_note3']}
    """)

    st.markdown("---")

    st.markdown(f"**{lang_messages['sidebar_qr_setting']}**")
    st.markdown(f"**{lang_messages['sidebar_error_correction']}**")
    st.markdown(f"""
    {lang_messages['error_correction_low']}
    {lang_messages['error_correction_medium']}
    {lang_messages['error_correction_quartile']}
    {lang_messages['error_correction_high']}
    """)

    st.markdown(f"**{lang_messages['sidebar_mask_pattern']}**")
    st.markdown(f"""
    {lang_messages['mask_pattern_note']}
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    f'<p style="text-align: center; color: mediumslateblue; font-size: 15px;">{lang_messages["author_info"]}</p>',
    unsafe_allow_html=True
)
# 최종버전(다중 언어 지원 통함 파일 버전)
