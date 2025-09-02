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
    page_title=messages.page_title,
    page_icon=messages.page_icon,
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
        st.error(messages.error_gen_data.format(error=str(e)))
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
    effective_box_size = box_size - gap_pixels

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
    
    # 세 개의 큰 파인더 패턴의 위치를 미리 계산
    finder_pattern_coords = [
        (border * box_size, border * box_size),
        (border * box_size, (qr_object.modules_count - 7 + border) * box_size),
        ((qr_object.modules_count - 7 + border) * box_size, border * box_size)
    ]
    
    for r in range(qr_object.modules_count):
        for c in range(qr_object.modules_count):
            is_finder_pattern = False
            # 세 개의 파인더 패턴 위치에 있는지 확인
            if (r < 7 and c < 7) or (r >= qr_object.modules_count - 7 and c < 7) or (r < 7 and c >= qr_object.modules_count - 7):
                is_finder_pattern = True
            
            if qr_object.modules[r][c]:
                x = (c + border) * box_size
                y = (r + border) * box_size
                
                # 간격을 적용한 새로운 좌표 계산
                current_shape = finder_pattern_shape if is_finder_pattern else pattern_shape
                
                if current_shape != "사각":
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
        st.error(messages.error_gen_svg.format(error=str(e)))
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

st.title(messages.main_title)
st.markdown(messages.main_separator)

# 언어 선택
st.sidebar.selectbox("Language", messages.lang_options, key='lang')

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header(messages.input_and_settings_header)

    # QR 코드 입력창
    st.subheader(messages.content_subheader)
    st.info(messages.content_info)

    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요", # 이 부분은 Streamlit API의 레이블이므로 그대로 둠
        height=200,
        placeholder=messages.content_placeholder,
        key="qr_input_area",
    )

    # 문자 수 표시
    char_count = len(qr_data) if qr_data else 0
    if char_count > 0:
        if char_count > 2900:
            st.error(messages.char_count_warning_2.format(char_count=char_count))
        elif char_count > 2400:
            st.warning(messages.char_count_warning_1.format(char_count=char_count))
        else:
            st.success(messages.char_count_success.format(char_count=char_count))
    else:
        st.caption(messages.char_count_caption)

    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        messages.strip_checkbox_label,
        value=st.session_state.strip_option,
        key="strip_option",
        help=messages.strip_checkbox_help
    )

    # 입력 내용 삭제 버튼
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        delete_btn_disabled = (char_count == 0)
        st.button(
            messages.delete_button_label,
            help=messages.delete_button_help,
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
        )

    st.markdown(messages.main_separator)
    
    # 파일 형식 설정
    st.subheader(messages.file_format_subheader)
    file_format = st.selectbox(
        messages.file_format_selectbox,
        ("PNG", "JPG", "SVG"),
        index=0 if st.session_state.file_format_select == "PNG" else (1 if st.session_state.file_format_select == "JPG" else 2),
        key="file_format_select",
    )
    
    # JPG 품질 설정 슬라이더 (JPG 선택 시에만 표시)
    if file_format == "JPG":
        st.caption(messages.jpg_caption)
        jpg_quality = st.slider(
            messages.jpg_slider_label,
            min_value=1,
            max_value=100,
            value=st.session_state.jpg_quality_input,
            key="jpg_quality_input",
            help=messages.jpg_slider_help
        )
    else:
        jpg_quality = 70
    
    # 패턴 모양 설정
    st.markdown(messages.main_separator)
    st.subheader(messages.pattern_shape_subheader)
    pattern_shape_disabled = (file_format == "SVG")
    st.caption(messages.pattern_shape_warning)
    
    # 두 개의 패턴 모양 선택 옵션 추가
    col_pattern_shape, col_finder_shape = st.columns(2)
    
    with col_pattern_shape:
        pattern_shape = st.selectbox(
            messages.pattern_shape_selectbox_label,
            messages.pattern_shape_options,
            key="pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    with col_finder_shape:
        finder_pattern_shape = st.selectbox(
            messages.finder_shape_selectbox_label,
            messages.pattern_shape_options,
            key="finder_pattern_shape_select",
            disabled=pattern_shape_disabled,
        )

    # 둥근사각 전용 슬라이더
    if pattern_shape == "둥근사각" or finder_pattern_shape == "둥근사각":
        corner_radius_disabled = (file_format == "SVG")
        st.caption(messages.corner_radius_warning)
        corner_radius = st.slider(
            messages.corner_radius_slider_label, 
            min_value=0, 
            max_value=50, 
            value=st.session_state.corner_radius_input,
            help=messages.corner_radius_slider_help,
            key="corner_radius_input",
            disabled=corner_radius_disabled
        )
    else:
        corner_radius = 0
        
    # 패턴 간격 슬라이더 (사각 제외)
    cell_gap_disabled = (pattern_shape == "사각") or (finder_pattern_shape == "사각") or (file_format == "SVG")
    st.caption(messages.cell_gap_warning)
    cell_gap = st.slider(
        messages.cell_gap_slider_label,
        min_value=0,
        max_value=40,
        value=st.session_state.cell_gap_input,
        help=messages.cell_gap_slider_help,
        disabled=cell_gap_disabled,
        key="cell_gap_input",
    )
    
#========================================================================================================================================================================

    # 색상 설정 (순서 변경)
    st.markdown(messages.main_separator)
    st.subheader(messages.color_subheader)
    
    file_format_is_svg = (st.session_state.file_format_select == "SVG")
    
    if file_format_is_svg:
        st.warning(messages.svg_color_warning)

    colors = [
        messages.color_options_custom, "black", "white", "gray", "lightgray", "dimgray",
        "red", "green", "blue", "yellow", "cyan", "magenta", "maroon",
        "purple", "navy", "lime", "olive", "teal", "aqua", "fuchsia",
        "silver", "gold", "orange", "orangered", "crimson", "indigo",
    ]
    col1_3, col1_4 = st.columns(2)
    with col1_3:
        pattern_color_choice = st.selectbox(
            messages.pattern_color_selectbox_label, colors, 
            key="pattern_color_select", 
            disabled=file_format_is_svg
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            messages.bg_color_selectbox_label, colors, 
            key="bg_color_select", 
            disabled=file_format_is_svg
        )

    st.markdown(messages.hex_info_1)
    st.caption(messages.hex_info_2)
    col1_5, col1_6 = st.columns(2)
    with col1_5:
        st.text_input(
            messages.pattern_color_input_label,
            placeholder=messages.pattern_color_input_placeholder,
            disabled=(pattern_color_choice != messages.color_options_custom) or file_format_is_svg,
            key="custom_pattern_color_input_key",
        )
    with col1_6:
        st.text_input(
            messages.bg_color_input_label,
            placeholder=messages.bg_color_input_placeholder,
            disabled=(bg_color_choice != messages.color_options_custom) or file_format_is_svg,
            key="custom_bg_color_input_key",
        )
    
    pattern_color = st.session_state.get('custom_pattern_color_input_key', '').strip() if pattern_color_choice == messages.color_options_custom else pattern_color_choice
    bg_color = st.session_state.get('custom_bg_color_input_key', '').strip() if bg_color_choice == messages.color_options_custom else bg_color_choice

#========================================================================================================================================================================

    # QR 코드 설정 (순서 변경)
    st.markdown(messages.main_separator)
    st.subheader(messages.qr_settings_subheader)

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        box_size = st.number_input(messages.box_size_label, min_value=1, max_value=100, key="box_size_input")
        border = st.number_input(messages.border_label, min_value=0, max_value=10, key="border_input")

    with col1_2:
        error_correction_options = {
            "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%)": qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox(messages.error_correction_label, list(error_correction_options.keys()), key="error_correction_select")
        error_correction = error_correction_options[error_correction_choice]
        mask_pattern = st.selectbox(messages.mask_pattern_label, options=list(range(8)), key="mask_pattern_select")


#========================================================================================================================================================================

    # 파일명 설정
    st.markdown(messages.main_separator)
    st.subheader(messages.filename_subheader)
    
    col_filename_input, col_filename_delete = st.columns([3, 1.1])

    with col_filename_input:
        filename = st.text_input(
            messages.filename_input_label,
            placeholder=messages.filename_input_placeholder,
            key="filename_input_key",
        )

    current_filename = filename.strip()

    with col_filename_delete:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
        st.button(
            messages.filename_delete_button_label,
            help=messages.filename_delete_button_help,
            use_container_width=True,
            type="secondary",
            disabled=filename_delete_disabled,
            on_click=clear_filename_callback,
        )


#========================================================================================================================================================================

with col2:
    st.header(messages.preview_and_download_header)
    
    current_data = qr_data.strip() if st.session_state.strip_option else qr_data
    
    is_pattern_color_valid_preview = (pattern_color_choice != messages.color_options_custom) or (pattern_color_choice == messages.color_options_custom and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != messages.color_options_custom) or (bg_color_choice == messages.color_options_custom and bg_color and is_valid_color(bg_color))
    is_colors_same_preview = (is_pattern_color_valid_preview and is_bg_color_valid_preview and pattern_color and bg_color and pattern_color == bg_color)
    
    preview_image_display = None
    preview_qr_object = None
    
    can_generate_preview = current_data and (file_format == "SVG" or (is_pattern_color_valid_preview and is_bg_color_valid_preview and not is_colors_same_preview))

    download_data = None
    download_mime = ""
    download_extension = ""
    save_format = ""

    if can_generate_preview:
        try:
            qr = get_qr_data_object(
                current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                int(st.session_state.mask_pattern_select)
            )
            if qr:
                preview_qr_object = qr
                if file_format in ["PNG", "JPG"]:
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        pattern_color, bg_color, st.session_state.pattern_shape_select,
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        st.session_state.finder_pattern_shape_select
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
                    svg_data, _ = generate_qr_code_svg(
                        current_data, int(st.session_state.box_size_input), int(st.session_state.border_input), error_correction,
                        int(st.session_state.mask_pattern_select), "black", "white"
                    )
                    download_data = svg_data.encode('utf-8')
                    download_mime = "image/svg+xml"
                    download_extension = ".svg"
                    
                    # SVG 미리보기를 위한 이미지 생성
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", "사각",
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        "사각",
                    )
        except Exception as e:
            st.error(messages.error_general.format(error=str(e)))

    st.markdown(messages.main_separator)
    
    if preview_image_display:
        st.success(messages.preview_success_message)
        st.subheader(messages.preview_subheader)
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=messages.preview_image_caption, width=380)
        
        if preview_qr_object:
            st.info(f"""
            {messages.qr_info_title}
            - {messages.qr_info_version.format(version=preview_qr_object.version)}
            ** **
            - {messages.qr_info_cells.format(count=preview_qr_object.modules_count)}
            - {messages.qr_info_border.format(count=2 * int(st.session_state.border_input))}
            - {messages.qr_info_cell_size.format(size=int(st.session_state.box_size_input))}
            - {messages.qr_info_image_size.format(size=(preview_qr_object.modules_count + 2 * int(st.session_state.border_input)) * int(st.session_state.box_size_input))}
            ** **
            - **{messages.qr_info_calculation}**
            ** **
            - {messages.qr_info_pattern_color.format(color="black" if file_format == "SVG" else pattern_color)}
            - {messages.qr_info_bg_color.format(color="white" if file_format == "SVG" else bg_color)}
            """)

        # 다운로드 섹션의 위치를 미리보기 아래로 이동
        st.markdown(messages.main_separator)
        st.subheader(messages.download_subheader)
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        final_filename = sanitize_filename(st.session_state.filename_input_key.strip() if st.session_state.filename_input_key.strip() else now.strftime("QR_%Y-%m-%d_%H-%M-%S"))
        download_filename = f"{final_filename}{download_extension}"

        st.download_button(
            label=messages.download_button_label,
            data=download_data,
            file_name=download_filename,
            mime=download_mime,
            use_container_width=True,
            help=messages.download_button_help
        )
        
        st.markdown(
            f'<p style="font-size:18px;">'
            f'<span style="color:darkorange; font-weight:bold;">{messages.download_filename_label} </span> '
            f'<span style="color:dodgerblue;"> {messages.download_filename_value.format(filename=download_filename)}</span>'
            f'</p>',
            unsafe_allow_html=True,
        )

    elif current_data:
        st.warning(messages.warning_cannot_generate)
        
        if file_format != "SVG":
            if pattern_color_choice == messages.color_options_custom and not pattern_color:
                st.warning(messages.warning_pattern_hex_empty)
            if bg_color_choice == messages.color_options_custom and not bg_color:
                st.warning(messages.warning_bg_hex_empty)
            if pattern_color_choice == messages.color_options_custom and pattern_color and not is_valid_color(pattern_color):
                st.warning(messages.warning_pattern_hex_invalid)
            if bg_color_choice == messages.color_options_custom and bg_color and not is_valid_color(bg_color):
                st.warning(messages.warning_bg_hex_invalid)
            if is_colors_same_preview:
                st.warning(messages.warning_same_color)
    else:
        st.info(messages.info_initial)


st.markdown(messages.main_separator)

st.button(
    label=messages.reset_button_label, 
    use_container_width=True,
    type="secondary",
    on_click=reset_all_settings,
    help=messages.reset_button_help,
)

with st.sidebar:
    st.header(messages.sidebar_title)
    st.markdown(f"""
    1. {messages.sidebar_usage_1}
    2. {messages.sidebar_usage_2}
    3. {messages.sidebar_usage_3}
    4. {messages.sidebar_usage_4}
    5. {messages.sidebar_usage_5}
    6. {messages.sidebar_usage_6}
    """)

    st.markdown(messages.main_separator)

    st.header(messages.sidebar_tips_title)
    st.markdown(f"""
    - {messages.sidebar_tip_text}
    - {messages.sidebar_tip_website}
    - {messages.sidebar_tip_email}
    - {messages.sidebar_tip_email_full}
    - {messages.sidebar_tip_tel}
    - {messages.sidebar_tip_sms}
    - {messages.sidebar_tip_sms_full}
    - {messages.sidebar_tip_wifi}
    """)

    st.markdown(messages.main_separator)

    st.header(messages.sidebar_guide_title)
    st.markdown(messages.sidebar_guide_file_format)
    st.markdown(f"""
    - {messages.sidebar_guide_png}
    - {messages.sidebar_guide_jpg}
    - {messages.sidebar_guide_svg}
    """)

    st.markdown(messages.main_separator)

    st.markdown(messages.sidebar_guide_pattern_shape)
    st.markdown(f"""
    - {messages.sidebar_guide_pattern_shape_desc_1}
    - {messages.sidebar_guide_pattern_shape_desc_2}
    """)
    
    st.markdown(messages.sidebar_guide_cell_gap)
    st.markdown(f"""
    - {messages.sidebar_guide_cell_gap_desc_1}
    - {messages.sidebar_guide_cell_gap_desc_2}
    """)

    st.markdown(messages.main_separator)

    st.markdown(messages.sidebar_guide_color)
    st.markdown(f"""
    - {messages.sidebar_guide_color_desc_1}
    - {messages.sidebar_guide_color_desc_2}
    - {messages.sidebar_guide_color_desc_3}
    """)

    st.markdown(messages.main_separator)
    
    st.markdown(messages.sidebar_guide_qr_settings)
    st.markdown(messages.sidebar_guide_error_correction)
    st.markdown(f"""
    - {messages.sidebar_guide_ec_L}
    - {messages.sidebar_guide_ec_M}
    - {messages.sidebar_guide_ec_Q}
    - {messages.sidebar_guide_ec_H}
    """)

    st.markdown(messages.sidebar_guide_mask_pattern)
    st.markdown(f"""
    - {messages.sidebar_guide_mask_pattern_desc}
    """)

# 하단 정보
st.markdown(messages.main_separator)
st.markdown(
    f'<p style="text-align: center; color: mediumslateblue; font-size: 15px;">{messages.footer_text}</p>',
    unsafe_allow_html=True
)
