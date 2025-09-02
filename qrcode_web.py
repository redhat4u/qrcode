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
import messages # 메시지 파일 추가

# 페이지 설정
st.set_page_config(
    page_title=messages.LANGUAGES["한국어"]["page_title"],
    page_icon=messages.LANGUAGES["한국어"]["page_icon"],
    layout="wide",
)

# 세션 상태 초기화
if 'lang' not in st.session_state:
    st.session_state.lang = "한국어"
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
    st.session_state.error_correction_select = "Low (7%)"
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
    st.session_state.pattern_shape_select = "사각"
if 'finder_pattern_shape_select' not in st.session_state:
    st.session_state.finder_pattern_shape_select = "사각"
if 'corner_radius_input' not in st.session_state:
    st.session_state.corner_radius_input = 25
if 'cell_gap_input' not in st.session_state:
    st.session_state.cell_gap_input = 0
if 'jpg_quality_input' not in st.session_state:
    st.session_state.jpg_quality_input = 70

# 현재 언어 메시지 로드
msgs = messages.LANGUAGES[st.session_state.lang]

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
        st.error(msgs["error_gen_data"].format(error=str(e)))
        return None

# 사용자 정의 모양으로 QR 코드 이미지 생성 함수 (PNG)
def draw_custom_shape_image(qr_object, box_size, border, fill_color, back_color, pattern_shape, corner_radius, cell_gap, finder_pattern_shape):
    if not qr_object:
        return None

    img_size = (qr_object.modules_count + 2 * border) * box_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)
    
    # 간격 계산
    gap_pixels = int(box_size * (cell_gap / 100))
    
    def draw_shape(draw, xy, shape, fill, corner_radius):
        x1, y1, x2, y2 = xy
        effective_size = x2 - x1
        if shape == "사각":
            draw.rectangle(xy, fill=fill)
        elif shape == "둥근사각":
            radius = int(effective_size * (corner_radius / 100))
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
            draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
        elif shape == "동그라미":
            draw.ellipse(xy, fill=fill)
        elif shape == "마름모":
            draw.polygon([(x1 + effective_size/2, y1), (x1 + effective_size, y1 + effective_size/2), (x1 + effective_size/2, y1 + effective_size), (x1, y1 + effective_size/2)], fill=fill)
        elif shape == "별":
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
        elif shape == "십자가":
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            cross_width = (x2 - x1) * 0.3
            draw.rectangle([x1, y_center - cross_width/2, x2, y_center + cross_width/2], fill=fill)
            draw.rectangle([x_center - cross_width/2, y1, x_center + cross_width/2, y2], fill=fill)
    
    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            is_finder_pattern = False
            if (r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7):
                is_finder_pattern = True
            
            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size
                
                current_shape = finder_pattern_shape if is_finder_pattern else pattern_shape
                
                if current_shape != msgs["pattern_shape_options"][0]: # '사각'이 아닌 경우
                    new_x = x + gap_pixels // 2
                    new_y = y + gap_pixels // 2
                    new_x_end = x + box_size - (gap_pixels - gap_pixels // 2)
                    new_y_end = y + box_size - (gap_pixels - gap_pixels // 2)
                    draw_coords = [new_x, new_y, new_x_end, new_y_end]
                else:
                    draw_coords = [x, y, x + box_size, y + box_size]

                draw_shape(draw, draw_coords, current_shape, fill_color, corner_radius)

    return img

# QR 코드 SVG 생성 함수
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
        st.error(msgs["error_gen_svg"].format(error=str(e)))
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
    st.session_state.error_correction_select = "Low (7%)"
    st.session_state.mask_pattern_select = 2
    st.session_state.pattern_color_select = "black"
    st.session_state.bg_color_select = "white"
    st.session_state.strip_option = True
    st.session_state.file_format_select = "PNG"
    st.session_state.pattern_shape_select = "사각"
    st.session_state.finder_pattern_shape_select = "사각"
    st.session_state.corner_radius_input = 25
    st.session_state.cell_gap_input = 0
    st.session_state.jpg_quality_input = 70


#[메인]====================================================================================================================================================================

st.title(msgs["main_title"])
st.markdown(msgs["main_separator"])

# 언어 선택
st.selectbox(
    msgs["language_select_label"],
    list(messages.LANGUAGES.keys()),
    index=list(messages.LANGUAGES.keys()).index(st.session_state.lang),
    key='lang'
)

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header(msgs["input_and_settings_header"])

    # QR 코드 입력창
    st.subheader(msgs["content_subheader"])
    st.info(msgs["content_info"])

    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=200,
        placeholder=msgs["content_placeholder"],
        key="qr_input_area",
    )

    # 문자 수 표시
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(msgs["char_count_warning_2"].format(char_count=char_count))
        elif char_count > 2400:
            st.warning(msgs["char_count_warning_1"].format(char_count=char_count))
        else:
            st.success(msgs["char_count_success"].format(char_count=char_count))
    else:
        st.caption(msgs["char_count_caption"])

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        msgs["strip_checkbox_label"],
        value=st.session_state.strip_option,
        key="strip_option",
        help=msgs["strip_checkbox_help"]
    )

    # 입력 내용 삭제 버튼
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            msgs["delete_button_label"],
            help=msgs["delete_button_help"],
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.markdown(msgs["main_separator"])
    
    # 파일 형식 설정
    st.subheader(msgs["file_format_subheader"])
    file_format = st.selectbox(
        msgs["file_format_selectbox"],
        ("PNG", "JPG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else (1 if st.session_state.file_format_select == "JPG" else 2),
        key="file_format_select",
    )
    
    # JPG 품질 설정 슬라이더 (JPG 선택 시에만 표시)
    if file_format == "JPG":
        st.caption(msgs["jpg_caption"])
        jpg_quality = st.slider(
            msgs["jpg_slider_label"],
            min_value=1,
            max_value=100,
            value=st.session_state.jpg_quality_input,
            key="jpg_quality_input",
            help=msgs["jpg_slider_help"]
        )
    else:
        jpg_quality = 70
    
    # 패턴 모양 설정
    st.markdown(msgs["main_separator"])
    st.subheader(msgs["pattern_shape_subheader"])
    pattern_shape_disabled = (file_format == "SVG")
    st.caption(msgs["pattern_shape_warning"])
    
    # 두 개의 패턴 모양 선택 옵션 추가
    col_pattern_shape, col_finder_shape = st.columns(2)
    
    with col_pattern_shape:
        pattern_shape = st.selectbox(
            msgs["pattern_shape_selectbox_label"],
            msgs["pattern_shape_options"],
            key="pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    with col_finder_shape:
        finder_pattern_shape = st.selectbox(
            msgs["finder_shape_selectbox_label"],
            msgs["pattern_shape_options"],
            key="finder_pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    # 둥근사각 전용 슬라이더
    if pattern_shape == msgs["pattern_shape_options"][1] or finder_pattern_shape == msgs["pattern_shape_options"][1]:
        corner_radius_disabled = (file_format == "SVG")
        st.caption(msgs["corner_radius_warning"])
        corner_radius = st.slider(
            msgs["corner_radius_slider_label"], 
            min_value=0, 
            max_value=50, 
            value=st.session_state.corner_radius_input,
            help=msgs["corner_radius_slider_help"],
            key="corner_radius_input",
            disabled=corner_radius_disabled
        )
    else:
        corner_radius = 0
        
    # 패턴 간격 슬라이더 (사각 제외)
    cell_gap_disabled = (pattern_shape == msgs["pattern_shape_options"][0]) or (finder_pattern_shape == msgs["pattern_shape_options"][0]) or (file_format == "SVG")
    st.caption(msgs["cell_gap_warning"])
    cell_gap = st.slider(
        msgs["cell_gap_slider_label"],
        min_value=0,
        max_value=40,
        value=st.session_state.cell_gap_input,
        help=msgs["cell_gap_slider_help"],
        disabled=cell_gap_disabled,
        key="cell_gap_input",
    )
    
#========================================================================================================================================================================

    # 색상 설정
    st.markdown(msgs["main_separator"])
    st.subheader(msgs["color_subheader"])
    
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    if file_format_is_svg:
        st.warning(msgs["svg_color_warning"])

    colors = [
        msgs["color_options_custom"], "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            msgs["pattern_color_selectbox_label"], colors, 
            key="pattern_color_select", 
            disabled=file_format_is_svg
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            msgs["bg_color_selectbox_label"], colors, 
            key="bg_color_select", 
            disabled=file_format_is_svg
        )

    st.markdown(msgs["hex_info_1"])
    st.caption(msgs["hex_info_2"])
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            msgs["pattern_color_input_label"],
            placeholder=msgs["pattern_color_input_placeholder"],
            disabled=(pattern_color_choice != msgs["color_options_custom"]) or file_format_is_svg,
            key="custom_pattern_color_input_key",
        )
    with col1_6:
        st.text_input(
            msgs["bg_color_input_label"],
            placeholder=msgs["bg_color_input_placeholder"],
            disabled=(bg_color_choice != msgs["color_options_custom"]) or file_format_is_svg,
            key="custom_bg_color_input_key",
        )
    
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == msgs["color_options_custom"] else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == msgs["color_options_custom"] else bg_color_choice

#========================================================================================================================================================================

    # QR 코드 설정
    st.markdown(msgs["main_separator"])
    st.subheader(msgs["qr_settings_subheader"])

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input(msgs["box_size_label"], min_value=1, max_value=100, key="box_size_input")
        border = st.number_input(msgs["border_label"], min_value=0, max_value=10, key="border_input")

    with col1_2:
        error_correction_options = {
            "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%)": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox(msgs["error_correction_label"], list(error_correction_options.keys()), key="error_correction_select")
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox(msgs["mask_pattern_label"], options=list(range(8)), key="mask_pattern_select")


#========================================================================================================================================================================

    # 파일명 설정
    st.markdown(msgs["main_separator"])
    st.subheader(msgs["filename_subheader"])
    
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            msgs["filename_input_label"],
            placeholder=msgs["filename_input_placeholder"],
            key="filename_input_key",
        )

    current_filename = filename.strip()

    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button(
            msgs["filename_delete_button_label"],
            help=msgs["filename_delete_button_help"],
            use_container_width=True,
            type="secondary",
            disabled=filename_delete_disabled,
            on_click=clear_filename_callback,
        )


#========================================================================================================================================================================

with col2:
    st.header(msgs["preview_and_download_header"])
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    is_pattern_color_valid_preview = (st.session_state.pattern_color_select != msgs["color_options_custom"]) or (st.session_state.pattern_color_select == msgs["color_options_custom"] and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (st.session_state.bg_color_select != msgs["color_options_custom"]) or (st.session_state.bg_color_select == msgs["color_options_custom"] and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    preview_image_display = None
    preview_qr_object = None
    
    can_generate_preview = current_data and (st.session_state.file_format_select == "SVG" or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview))

    download_data = None
    download_mime = ""
    download_extension = ""
    save_format = ""

    if can_generate_preview:
        try:
            qr = get_qr_data_object(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input),
                messages.LANGUAGES[st.session_state.lang]["error_correction_options"][st.session_state.error_correction_select],
                int(st.session_state.mask_pattern_select)
            )
            if qr:
                preview_qr_object = qr
                if st.session_state.file_format_select in ["PNG", "JPG"]:
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        pattern_color, bg_color, st.session_state.pattern_shape_select,
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        st.session_state.finder_pattern_shape_select
                    )
                    img_buffer = io.BytesIO()
                    if st.session_state.file_format_select == "PNG":
                        preview_image_display.save(img_buffer, format='PNG')
                        download_mime = "image/png"
                        download_extension = ".png"
                    elif st.session_state.file_format_select == "JPG":
                        rgb_image = preview_image_display.convert('RGB')
                        rgb_image.save(img_buffer, format='JPEG', quality=st.session_state.jpg_quality_input)
                        download_mime = "image/jpeg"
                        download_extension = ".jpg"
                        
                    download_data = img_buffer.getvalue()

                else: # SVG
                    svg_data, _ = generate_qr_code_svg(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        messages.LANGUAGES[st.session_state.lang]["error_correction_options"][st.session_state.error_correction_select],
                        int(st.session_state.mask_pattern_select), "black", "white"
                    )
                    download_data = svg_data.encode('utf-8')
                    download_mime = "image/svg+xml"
                    download_extension = ".svg"
                    
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", "사각",
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        "사각",
                    )
        except Exception as e:
            st.error(msgs["error_general"].format(error=str(e)))

    st.markdown(msgs["main_separator"])
    
    if preview_image_display:
        st.success(msgs["preview_success_message"])
        st.subheader(msgs["preview_subheader"])
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=msgs["preview_image_caption"], width=380)
        
        if preview_qr_object:
            st.info(f"""
            {msgs["qr_info_title"]}
            - {msgs["qr_info_version"].format(version=preview_qr_object.version)}
            ** **
            - {msgs["qr_info_cells"].format(count=preview_qr_object.modules_count)}
            - {msgs["qr_info_border"].format(count=2 * int(st.session_state.border_input))}
            - {msgs["qr_info_cell_size"].format(size=int(st.session_state.box_size_input))}
            - {msgs["qr_info_image_size"].format(size=(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input))}
            ** **
            - **{msgs["qr_info_calculation"]}**
            ** **
            - {msgs["qr_info_pattern_color"].format(color="black" if st.session_state.file_format_select == "SVG" else pattern_color)}
            - {msgs["qr_info_bg_color"].format(color="white" if st.session_state.file_format_select == "SVG" else bg_color)}
            """)

        st.markdown(msgs["main_separator"])
        st.subheader(msgs["download_subheader"])
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        final_filename = sanitize_filename(st.session_state.filename_input_key.strip() if st.session_state.filename_input_key.strip() else now.strftime("QR_%Y-%m-%d_%H-%M-%S"))
        download_filename = f"{final_filename}{download_extension}"

        st.download_button(
            label=msgs["download_button_label"],
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=msgs["download_button_help"]
        )
        
        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{msgs["download_filename_label"]} </span> '
            f'<span style="color:dodgerblue;"> {msgs["download_filename_value"].format(filename=download_filename)}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    elif current_data:
        st.warning(msgs["warning_cannot_generate"])
        
        if st.session_state.file_format_select != "SVG":
            if st.session_state.pattern_color_select == msgs["color_options_custom"] and not pattern_color:
                st.warning(msgs["warning_pattern_hex_empty"])
            if st.session_state.bg_color_select == msgs["color_options_custom"] and not bg_color:
                st.warning(msgs["warning_bg_hex_empty"])
            if st.session_state.pattern_color_select == msgs["color_options_custom"] and pattern_color and not is_valid_color(pattern_color):
                st.warning(msgs["warning_pattern_hex_invalid"])
            if st.session_state.bg_color_select == msgs["color_options_custom"] and bg_color and not is_valid_color(bg_color):
                st.warning(msgs["warning_bg_hex_invalid"])
            if is_colors_same_preview:
                st.warning(msgs["warning_same_color"])
    else:
        st.info(msgs["info_initial"])

st.markdown(msgs["main_separator"])

st.button(
    label=msgs["reset_button_label"], 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help=msgs["reset_button_help"],
)

with st.sidebar:
    st.header(msgs["sidebar_title"])
    st.markdown(f"""
    1. {msgs["sidebar_usage_1"]}
    2. {msgs["sidebar_usage_2"]}
    3. {msgs["sidebar_usage_3"]}
    4. {msgs["sidebar_usage_4"]}
    5. {msgs["sidebar_usage_5"]}
    6. {msgs["sidebar_usage_6"]}
    """)

    st.markdown(msgs["main_separator"])

    st.header(msgs["sidebar_tips_title"])
    st.markdown(f"""
    - {msgs["sidebar_tip_text"]}
    - {msgs["sidebar_tip_website"]}
    - {msgs["sidebar_tip_email"]}
    - {msgs["sidebar_tip_email_full"]}
    - {msgs["sidebar_tip_tel"]}
    - {msgs["sidebar_tip_sms"]}
    - {msgs["sidebar_tip_sms_full"]}
    - {msgs["sidebar_tip_wifi"]}
    """)

    st.markdown(msgs["main_separator"])

    st.header(msgs["sidebar_guide_title"])
    st.markdown(msgs["sidebar_guide_file_format"])
    st.markdown(f"""
    - {msgs["sidebar_guide_png"]}
    - {msgs["sidebar_guide_jpg"]}
    - {msgs["sidebar_guide_svg"]}
    """)

    st.markdown(msgs["main_separator"])

    st.markdown(msgs["sidebar_guide_pattern_shape"])
    st.markdown(f"""
    - {msgs["sidebar_guide_pattern_shape_desc_1"]}
    - {msgs["sidebar_guide_pattern_shape_desc_2"]}
    """)
    
    st.markdown(msgs["sidebar_guide_cell_gap"])
    st.markdown(f"""
    - {msgs["sidebar_guide_cell_gap_desc_1"]}
    - {msgs["sidebar_guide_cell_gap_desc_2"]}
    """)

    st.markdown(msgs["main_separator"])

    st.markdown(msgs["sidebar_guide_color"])
    st.markdown(f"""
    - {msgs["sidebar_guide_color_desc_1"]}
    - {msgs["sidebar_guide_color_desc_2"]}
    - {msgs["sidebar_guide_color_desc_3"]}
    """)

    st.markdown(msgs["main_separator"])
    
    st.markdown(msgs["sidebar_guide_qr_settings"])
    st.markdown(msgs["sidebar_guide_error_correction"])
    st.markdown(f"""
    - {msgs["sidebar_guide_ec_L"]}
    - {msgs["sidebar_guide_ec_M"]}
    - {msgs["sidebar_guide_ec_Q"]}
    - {msgs["sidebar_guide_ec_H"]}
    """)

    st.markdown(msgs["sidebar_guide_mask_pattern"])
    st.markdown(f"""
    - {msgs["sidebar_guide_mask_pattern_desc"]}
    """)

# 하단 정보
st.markdown(msgs["main_separator"])
st.markdown(
    f'<p style="text-align: center; color: mediumslateblue; font-size: 15px;">{msgs["footer_text"]}</p>',
    unsafe_allow_html=True
)
