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
import messages  # messages.py 파일을 임포트합니다.

# 언어 선택
lang_options = list(messages.LANGUAGES.keys())
selected_lang = st.sidebar.selectbox("언어", lang_options)
MESSAGES = messages.LANGUAGES[selected_lang]

# 페이지 설정
st.set_page_config(
    page_title=MESSAGES["page_title"],
    page_icon=MESSAGES["page_icon"],
    layout="wide",
)

# 세션 상태 초기화
if 'qr_input_area' not in st.session_state:
    st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
    st.session_state.custom_pattern_color_input_key = ""
if 'custom_bg_color_input_key' not in st.session_state:
    st.session_state.custom_bg_color_input_key = ""
if 'filename_input_key' not in st.session_state:
    st.session_state.filename_input_key = ""
if 'box_size' not in st.session_state:
    st.session_state.box_size = 10
if 'border_size' not in st.session_state:
    st.session_state.border_size = 4
if 'qr_error_correction' not in st.session_state:
    st.session_state.qr_error_correction = "M"
if 'mask_pattern' not in st.session_state:
    st.session_state.mask_pattern = 0
if 'pattern_color' not in st.session_state:
    st.session_state.pattern_color = "#000000"
if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "#FFFFFF"
if 'filename' not in st.session_state:
    st.session_state.filename = ""
if 'jpg_quality' not in st.session_state:
    st.session_state.jpg_quality = 90
if 'pattern_shape_selected' not in st.session_state:
    st.session_state.pattern_shape_selected = MESSAGES["pattern_shape_options"][0]
if 'finder_shape_selected' not in st.session_state:
    st.session_state.finder_shape_selected = MESSAGES["pattern_shape_options"][0]
if 'corner_radius' not in st.session_state:
    st.session_state.corner_radius = 0
if 'cell_gap' not in st.session_state:
    st.session_state.cell_gap = 0
if 'file_format_selected' not in st.session_state:
    st.session_state.file_format_selected = "PNG"


# 헬퍼 함수
def get_qr_image(data, format, **kwargs):
    if format == "SVG":
        return get_svg_image(data, **kwargs)
    else:
        return get_pil_image(data, **kwargs)

def get_pil_image(data, box_size, border, error_correction, mask_pattern,
                  pattern_color, bg_color,
                  pattern_shape, finder_shape, corner_radius, cell_gap):
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        mask_pattern=mask_pattern
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=pattern_color,
        back_color=bg_color,
        pattern_shape=pattern_shape,
        finder_shape=finder_shape,
        corner_radius=corner_radius,
        cell_gap=cell_gap
    )
    return img

def get_svg_image(data, box_size, border, error_correction, mask_pattern,
                  pattern_color, bg_color,
                  pattern_shape, finder_shape, corner_radius, cell_gap):

    # SVG는 오직 사각형 패턴만 지원
    if pattern_shape != MESSAGES["pattern_shape_options"][0] or finder_shape != MESSAGES["pattern_shape_options"][0]:
        st.warning(MESSAGES["pattern_shape_warning"])

    if pattern_color != "#000000" or bg_color != "#FFFFFF":
        st.warning(MESSAGES["svg_color_warning"])

    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        mask_pattern=mask_pattern,
        image_factory=factory
    )
    qr.add_data(data)
    qr.make(fit=True)

    svg_img = qr.make_image(
        fill_color="#000000",
        back_color="#FFFFFF"
    )
    return svg_img.to_string(encoding='utf-8')


def get_image_as_byte_stream(img, format, quality=90):
    buf = io.BytesIO()
    if format == "PNG":
        img.save(buf, format="PNG")
    elif format == "JPG":
        img.save(buf, format="JPEG", quality=quality)
    elif format == "SVG":
        buf = io.BytesIO(img)
    return buf.getvalue()

def generate_filename(data, file_format):
    hash_object = hashlib.sha256(data.encode('utf-8'))
    hex_digest = hash_object.hexdigest()[:8]
    now = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y%m%d_%H%M%S")
    return f"qrcode_{now}_{hex_digest}.{file_format.lower()}"

def is_valid_hex_color(hex_string):
    if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string):
        return True
    return False

# 메인 UI
st.title(MESSAGES["main_title"])
st.markdown(MESSAGES["main_separator"])

# 전체 초기화 버튼
if st.button(MESSAGES["reset_button_label"], help=MESSAGES["reset_button_help"]):
    st.session_state.qr_input_area = ""
    st.session_state.custom_pattern_color_input_key = ""
    st.session_state.custom_bg_color_input_key = ""
    st.session_state.filename_input_key = ""
    st.session_state.box_size = 10
    st.session_state.border_size = 4
    st.session_state.qr_error_correction = "M"
    st.session_state.mask_pattern = 0
    st.session_state.pattern_color = "#000000"
    st.session_state.bg_color = "#FFFFFF"
    st.session_state.filename = ""
    st.session_state.jpg_quality = 90
    st.session_state.pattern_shape_selected = MESSAGES["pattern_shape_options"][0]
    st.session_state.finder_shape_selected = MESSAGES["pattern_shape_options"][0]
    st.session_state.corner_radius = 0
    st.session_state.cell_gap = 0
    st.session_state.file_format_selected = "PNG"
    st.rerun()

st.header(MESSAGES["input_and_settings_header"])
st.markdown(MESSAGES["main_separator"])

# 입력 및 설정 섹션
col1, col2 = st.columns(2)

with col1:
    st.subheader(MESSAGES["content_subheader"])
    st.info(MESSAGES["content_info"])
    
    # QR 코드 내용 입력
    qr_content = st.text_area(
        label=MESSAGES["content_subheader"],
        value=st.session_state.qr_input_area,
        placeholder=MESSAGES["content_placeholder"],
        height=150,
        key="qr_input_area_key"
    )

    # 입력 내용 지우기
    if st.button(MESSAGES["delete_button_label"], help=MESSAGES["delete_button_help"]):
        st.session_state.qr_input_area = ""
        st.rerun()

    char_count = len(qr_content)
    if char_count > 200:
        st.warning(MESSAGES["char_count_warning_2"].format(char_count=char_count))
    elif char_count > 50:
        st.warning(MESSAGES["char_count_warning_1"].format(char_count=char_count))
    else:
        st.success(MESSAGES["char_count_success"].format(char_count=char_count))
    
    st.caption(MESSAGES["char_count_caption"])

    st.checkbox(
        label=MESSAGES["strip_checkbox_label"],
        help=MESSAGES["strip_checkbox_help"],
        value=False,
        key="strip_content"
    )

    if st.session_state.strip_content:
        qr_content = qr_content.strip()

    st.markdown(MESSAGES["main_separator"])

    st.subheader(MESSAGES["file_format_subheader"])
    file_format = st.selectbox(
        MESSAGES["file_format_selectbox"],
        ("PNG", "JPG", "SVG"),
        key="file_format_selected"
    )

    if file_format == "JPG":
        st.caption(MESSAGES["jpg_caption"])
        st.session_state.jpg_quality = st.slider(
            MESSAGES["jpg_slider_label"], 1, 100, st.session_state.jpg_quality,
            help=MESSAGES["jpg_slider_help"]
        )

    st.markdown(MESSAGES["main_separator"])

    st.subheader(MESSAGES["pattern_shape_subheader"])
    
    pattern_shape_options = MESSAGES["pattern_shape_options"]
    
    if file_format == "SVG":
        st.warning(MESSAGES["pattern_shape_warning"])
        st.session_state.pattern_shape_selected = st.selectbox(
            MESSAGES["pattern_shape_selectbox_label"],
            [pattern_shape_options[0]],
            key="pattern_shape_selected_key"
        )
        st.session_state.finder_shape_selected = st.selectbox(
            MESSAGES["finder_shape_selectbox_label"],
            [pattern_shape_options[0]],
            key="finder_shape_selected_key"
        )
    else:
        st.session_state.pattern_shape_selected = st.selectbox(
            MESSAGES["pattern_shape_selectbox_label"],
            pattern_shape_options,
            key="pattern_shape_selected_key"
        )
        st.session_state.finder_shape_selected = st.selectbox(
            MESSAGES["finder_shape_selectbox_label"],
            pattern_shape_options,
            key="finder_shape_selected_key"
        )

    if st.session_state.pattern_shape_selected == pattern_shape_options[1]: # 둥근 사각
        st.caption(MESSAGES["corner_radius_warning"])
        st.session_state.corner_radius = st.slider(
            MESSAGES["corner_radius_slider_label"], 0, 50, st.session_state.corner_radius,
            help=MESSAGES["corner_radius_slider_help"]
        )
    else:
        st.session_state.corner_radius = 0

    if st.session_state.pattern_shape_selected != pattern_shape_options[0] and file_format != "SVG":
        st.caption(MESSAGES["cell_gap_warning"])
        st.session_state.cell_gap = st.slider(
            MESSAGES["cell_gap_slider_label"], 0, 40, st.session_state.cell_gap,
            help=MESSAGES["cell_gap_slider_help"]
        )
    else:
        st.session_state.cell_gap = 0
        

    st.markdown(MESSAGES["main_separator"])

    st.subheader(MESSAGES["color_subheader"])
    if file_format == "SVG":
        st.warning(MESSAGES["svg_color_warning"])
    
    color_options = ["Black", "White", "Blue", "Red", "Green", "Yellow", "Cyan", "Magenta"]
    pattern_color_default = "Black" if st.session_state.pattern_color == "#000000" else MESSAGES["color_options_custom"]
    bg_color_default = "White" if st.session_state.bg_color == "#FFFFFF" else MESSAGES["color_options_custom"]
    
    pattern_color_selected = st.selectbox(
        MESSAGES["pattern_color_selectbox_label"],
        color_options + [MESSAGES["color_options_custom"]],
        index=color_options.index(pattern_color_default) if pattern_color_default in color_options else len(color_options),
        key="pattern_color_key"
    )
    bg_color_selected = st.selectbox(
        MESSAGES["bg_color_selectbox_label"],
        color_options + [MESSAGES["color_options_custom"]],
        index=color_options.index(bg_color_default) if bg_color_default in color_options else len(color_options),
        key="bg_color_key"
    )

    if pattern_color_selected == MESSAGES["color_options_custom"]:
        st.caption(MESSAGES["hex_info_1"])
        st.caption(MESSAGES["hex_info_2"])
        st.session_state.pattern_color = st.text_input(
            MESSAGES["pattern_color_input_label"], value=st.session_state.pattern_color,
            placeholder=MESSAGES["pattern_color_input_placeholder"],
            key="custom_pattern_color_input_key"
        )
    else:
        color_hex_map = {
            "Black": "#000000", "White": "#FFFFFF", "Blue": "#0000FF", "Red": "#FF0000",
            "Green": "#008000", "Yellow": "#FFFF00", "Cyan": "#00FFFF", "Magenta": "#FF00FF"
        }
        st.session_state.pattern_color = color_hex_map[pattern_color_selected]
    
    if bg_color_selected == MESSAGES["color_options_custom"]:
        st.session_state.bg_color = st.text_input(
            MESSAGES["bg_color_input_label"], value=st.session_state.bg_color,
            placeholder=MESSAGES["bg_color_input_placeholder"],
            key="custom_bg_color_input_key"
        )
    else:
        color_hex_map = {
            "Black": "#000000", "White": "#FFFFFF", "Blue": "#0000FF", "Red": "#FF0000",
            "Green": "#008000", "Yellow": "#FFFF00", "Cyan": "#00FFFF", "Magenta": "#FF00FF"
        }
        st.session_state.bg_color = color_hex_map[bg_color_selected]

    st.markdown(MESSAGES["main_separator"])

    st.subheader(MESSAGES["qr_settings_subheader"])
    st.session_state.box_size = st.slider(MESSAGES["box_size_label"], 1, 20, st.session_state.box_size)
    st.session_state.border_size = st.slider(MESSAGES["border_label"], 1, 10, st.session_state.border_size)

    error_correction_options = {
        "L (7%)": qrcode.constants.ERROR_CORRECT_L,
        "M (15%)": qrcode.constants.ERROR_CORRECT_M,
        "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
        "H (30%)": qrcode.constants.ERROR_CORRECT_H,
    }
    st.session_state.qr_error_correction = st.selectbox(
        MESSAGES["error_correction_label"],
        list(error_correction_options.keys()),
        index=list(error_correction_options.keys()).index(st.session_state.qr_error_correction),
        help=f"{MESSAGES['sidebar_guide_ec_L']}\n{MESSAGES['sidebar_guide_ec_M']}\n{MESSAGES['sidebar_guide_ec_Q']}\n{MESSAGES['sidebar_guide_ec_H']}"
    )

    st.session_state.mask_pattern = st.slider(MESSAGES["mask_pattern_label"], 0, 7, st.session_state.mask_pattern)

    st.markdown(MESSAGES["main_separator"])

    st.subheader(MESSAGES["filename_subheader"])
    st.session_state.filename = st.text_input(
        MESSAGES["filename_input_label"],
        value=st.session_state.filename,
        placeholder=MESSAGES["filename_input_placeholder"],
        key="filename_input_key"
    )
    if st.button(MESSAGES["filename_delete_button_label"], help=MESSAGES["filename_delete_button_help"]):
        st.session_state.filename = ""
        st.rerun()

    # QR 코드 생성 로직 및 미리보기
    if not qr_content:
        with col2:
            st.info(MESSAGES["info_initial"])
    else:
        is_valid = True
        if not is_valid_hex_color(st.session_state.pattern_color):
            st.warning(MESSAGES["warning_pattern_hex_invalid"])
            is_valid = False
        if not is_valid_hex_color(st.session_state.bg_color):
            st.warning(MESSAGES["warning_bg_hex_invalid"])
            is_valid = False
        if st.session_state.pattern_color == st.session_state.bg_color:
            st.warning(MESSAGES["warning_same_color"])
            is_valid = False

        if not is_valid:
            with col2:
                st.warning(MESSAGES["warning_cannot_generate"])
        else:
            try:
                # QR 코드 데이터 생성
                version = qrcode.util.get_version(qr_content, error_correction_options[st.session_state.qr_error_correction])
                cells_count = version * 4 + 17
                border_cells = st.session_state.border_size
                img_size = (cells_count + 2 * border_cells) * st.session_state.box_size

                # QR 코드 이미지 생성
                if file_format == "SVG":
                    img_data = get_qr_image(
                        data=qr_content,
                        format=file_format,
                        box_size=st.session_state.box_size,
                        border=st.session_state.border_size,
                        error_correction=error_correction_options[st.session_state.qr_error_correction],
                        mask_pattern=st.session_state.mask_pattern,
                        pattern_color=st.session_state.pattern_color,
                        bg_color=st.session_state.bg_color,
                        pattern_shape=st.session_state.pattern_shape_selected,
                        finder_shape=st.session_state.finder_shape_selected,
                        corner_radius=st.session_state.corner_radius,
                        cell_gap=st.session_state.cell_gap
                    )
                else:
                    img = get_qr_image(
                        data=qr_content,
                        format=file_format,
                        box_size=st.session_state.box_size,
                        border=st.session_state.border_size,
                        error_correction=error_correction_options[st.session_state.qr_error_correction],
                        mask_pattern=st.session_state.mask_pattern,
                        pattern_color=st.session_state.pattern_color,
                        bg_color=st.session_state.bg_color,
                        pattern_shape=st.session_state.pattern_shape_selected,
                        finder_shape=st.session_state.finder_shape_selected,
                        corner_radius=st.session_state.corner_radius,
                        cell_gap=st.session_state.cell_gap
                    )
                
                with col2:
                    st.header(MESSAGES["preview_and_download_header"])
                    st.success(MESSAGES["preview_success_message"])
                    st.markdown(MESSAGES["main_separator"])
                    st.subheader(MESSAGES["preview_subheader"])

                    if file_format == "SVG":
                        b64 = base64.b64encode(img_data).decode("utf-8")
                        html_code = f'<img src="data:image/svg+xml;base64,{b64}" width="100%">'
                        st.markdown(html_code, unsafe_allow_html=True)
                        st.caption(MESSAGES["preview_image_caption"])
                    else:
                        st.image(img, caption=MESSAGES["preview_image_caption"], use_column_width=True)

                    # QR 코드 정보 표시
                    st.subheader(MESSAGES["qr_info_title"])
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.markdown(MESSAGES["qr_info_version"].format(version=version))
                        st.markdown(MESSAGES["qr_info_cells"].format(count=cells_count))
                        st.markdown(MESSAGES["qr_info_border"].format(count=border_cells))
                    with info_col2:
                        st.markdown(MESSAGES["qr_info_cell_size"].format(size=st.session_state.box_size))
                        st.markdown(MESSAGES["qr_info_image_size"].format(size=img_size))
                        st.markdown(MESSAGES["qr_info_calculation"])

                    st.markdown(MESSAGES["qr_info_pattern_color"].format(color=st.session_state.pattern_color))
                    st.markdown(MESSAGES["qr_info_bg_color"].format(color=st.session_state.bg_color))
                    
                    st.markdown(MESSAGES["main_separator"])

                    st.subheader(MESSAGES["download_subheader"])
                    
                    # 파일명 자동 생성
                    filename_to_use = st.session_state.filename or generate_filename(qr_content, file_format)
                    st.markdown(MESSAGES["download_filename_label"] + " " + MESSAGES["download_filename_value"].format(filename=filename_to_use))

                    if file_format == "SVG":
                        st.download_button(
                            label=MESSAGES["download_button_label"],
                            data=img_data,
                            file_name=filename_to_use,
                            mime="image/svg+xml",
                            help=MESSAGES["download_button_help"]
                        )
                    else:
                        img_bytes = get_image_as_byte_stream(img, file_format, st.session_state.jpg_quality)
                        st.download_button(
                            label=MESSAGES["download_button_label"],
                            data=img_bytes,
                            file_name=filename_to_use,
                            mime=f"image/{file_format.lower()}",
                            help=MESSAGES["download_button_help"]
                        )
            except Exception as e:
                with col2:
                    st.error(MESSAGES["error_general"].format(error=e))

# 사이드바
st.sidebar.title(MESSAGES["sidebar_title_usage"])
st.sidebar.markdown(MESSAGES["sidebar_usage_1"])
st.sidebar.markdown(MESSAGES["sidebar_usage_2"])
st.sidebar.markdown(MESSAGES["sidebar_usage_3"])
st.sidebar.markdown(MESSAGES["sidebar_usage_4"])
st.sidebar.markdown(MESSAGES["sidebar_usage_5"])
st.sidebar.markdown(MESSAGES["sidebar_usage_6"])
st.sidebar.markdown("---")

st.sidebar.title(MESSAGES["sidebar_title_tips"])
st.sidebar.markdown(MESSAGES["sidebar_tip_text"])
st.sidebar.markdown(MESSAGES["sidebar_tip_website"])
st.sidebar.markdown(MESSAGES["sidebar_tip_email"])
st.sidebar.markdown(MESSAGES["sidebar_tip_email_full"])
st.sidebar.markdown(MESSAGES["sidebar_tip_tel"])
st.sidebar.markdown(MESSAGES["sidebar_tip_sms"])
st.sidebar.markdown(MESSAGES["sidebar_tip_sms_full"])
st.sidebar.markdown(MESSAGES["sidebar_tip_wifi"])
st.sidebar.markdown("---")

st.sidebar.title(MESSAGES["sidebar_title_guide"])

st.sidebar.markdown(MESSAGES["sidebar_guide_file_format"])
st.sidebar.markdown(MESSAGES["sidebar_guide_png"])
st.sidebar.markdown(MESSAGES["sidebar_guide_jpg"])
st.sidebar.markdown(MESSAGES["sidebar_guide_svg"])

st.sidebar.markdown(MESSAGES["main_separator"])
st.sidebar.markdown(MESSAGES["sidebar_guide_pattern_shape"])
st.sidebar.markdown(MESSAGES["sidebar_guide_pattern_shape_desc_1"])
st.sidebar.markdown(MESSAGES["sidebar_guide_pattern_shape_desc_2"])

st.sidebar.markdown(MESSAGES["main_separator"])
st.sidebar.markdown(MESSAGES["sidebar_guide_cell_gap"])
st.sidebar.markdown(MESSAGES["sidebar_guide_cell_gap_desc_1"])
st.sidebar.markdown(MESSAGES["sidebar_guide_cell_gap_desc_2"])

st.sidebar.markdown(MESSAGES["main_separator"])
st.sidebar.markdown(MESSAGES["sidebar_guide_color"])
st.sidebar.markdown(MESSAGES["sidebar_guide_color_desc_1"])
st.sidebar.markdown(MESSAGES["sidebar_guide_color_desc_2"])
st.sidebar.markdown(MESSAGES["sidebar_guide_color_desc_3"])

st.sidebar.markdown(MESSAGES["main_separator"])
st.sidebar.markdown(MESSAGES["sidebar_guide_qr_settings"])
st.sidebar.markdown(MESSAGES["sidebar_guide_error_correction"])
st.sidebar.markdown(MESSAGES["sidebar_guide_ec_L"])
st.sidebar.markdown(MESSAGES["sidebar_guide_ec_M"])
st.sidebar.markdown(MESSAGES["sidebar_guide_ec_Q"])
st.sidebar.markdown(MESSAGES["sidebar_guide_ec_H"])

st.sidebar.markdown(MESSAGES["main_separator"])
st.sidebar.markdown(MESSAGES["sidebar_guide_mask_pattern"])
st.sidebar.markdown(MESSAGES["sidebar_guide_mask_pattern_desc"])

# 푸터
st.sidebar.markdown("---")
st.sidebar.markdown(f'<div style="text-align: center; color: gray;">{MESSAGES["footer_text"]}</div>', unsafe_allow_html=True)
