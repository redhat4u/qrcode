"""
자.. 지금부터 이 코드가 기준이 되는 코드야...
수정하다 오류나거나 잘못된 방향으로 수정되면 항상 이버전으로
다시 시작하는 거야.. 알겠지??


한국어로 사용하다가 영어로 바뀌면 입력창 내용및 모든 설정이 초기화돼..
모든걸 그대로 유지하면서 언어만 바뀌게 해줘..


QR 코드 생성 웹앱 - Streamlit 버전
휴대폰에서도 사용 가능


실행 방법:
1. pip install streamlit qrcode[pil]
2. streamlit run qrcode_web.py


또는 온라인에서 실행:
- Streamlit Cloud, Heroku, Replit 등에 배포 가능
"""


# qrcode_web.py


import streamlit as st
import qrcode
import io
import re
import math
import hashlib
import base64 # SVG 이미지 표시를 위해 추가
import qrcode.image.svg # SVG 생성을 위해 추가
from datetime import datetime
from zoneinfo import ZoneInfo
from messages import messages
from PIL import Image, ImageDraw




# 페이지 설정
st.set_page_config(
page_title="QR 코드 생성기",
page_icon="🔲",
layout="wide",
)


# 언어 의존적인 UI 라벨/옵션만 갱신하는 함수
def update_language_labels():
st.session_state.error_correction_select = messages[st.session_state.lang]['error_correction_low_select']
st.session_state.pattern_shape_select = messages[st.session_state.lang]['pattern_shape_square']
st.session_state.finder_pattern_shape_select = messages[st.session_state.lang]['pattern_shape_square']


# 세션 상태 초기화
if 'lang' not in st.session_state:
st.session_state.lang = "ko"
# 기본 UI 라벨만 설정
update_language_labels()
if 'qr_input_area' not in st.session_state:
st.session_state.qr_input_area = ""
if 'custom_pattern_color_input_key' not in st.session_state:
st.session_state.custom_pattern_color_input_key = ""
if 'custom_bg_color_input_key' not in st.session_state:
st.session_state.custom_bg_color_input_key = ""
if 'filename_input_key' not in st.session_state:
st.session_state.filename_input_key = ""
if 'pattern_color_select' not in st.session_state:
st.session_state.pattern_color_select = "black"
if 'bg_color_select' not in st.session_state:
st.session_state.bg_color_select = "white"
if 'box_size_input' not in st.session_state:
st.session_state.box_size_input = 20
if 'border_input' not in st.session_state:
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
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
        key="qr_input_area",
    )

    # 문자 수 표시
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
        delete_btn_disabled = (char_count == 0)
        st.button(
            lang_messages['delete_button'],
            help=lang_messages['delete_button_help'],
            use_container_width=True,
            type="secondary",
            disabled=delete_btn_disabled,
            on_click=clear_text_input,
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

    # 둥근사각 전용 슬라이더
    if pattern_shape == lang_messages['pattern_shape_rounded'] or finder_pattern_shape == lang_messages['pattern_shape_rounded']:
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

    # 패턴 간격 슬라이더 (사각 제외)
    cell_gap_disabled = (pattern_shape == lang_messages['pattern_shape_square']) or (finder_pattern_shape == lang_messages['pattern_shape_square']) or (file_format == "SVG")
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

#========================================================================================================================================================================

    # 색상 설정 (순서 변경)
    st.markdown("---")
    st.subheader(lang_messages['color_subheader'])

    file_format_is_svg = (st.session_state.file_format_select == "SVG")

    if file_format_is_svg:
        st.warning(lang_messages['svg_color_warning'])

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
            key="pattern_color_select",
            disabled=file_format_is_svg,
        )
    with col1_4:
        bg_color_choice = st.selectbox(
            lang_messages['bg_color_label'], colors,
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
        error_correction_options = {
            lang_messages['error_correction_low_select']: qrcode.constants.ERROR_CORRECT_L,
            lang_messages['error_correction_medium_select']: qrcode.constants.ERROR_CORRECT_M,
            lang_messages['error_correction_quartile_select']: qrcode.constants.ERROR_CORRECT_Q,
            lang_messages['error_correction_high_select']: qrcode.constants.ERROR_CORRECT_H,
        }
        error_correction_choice = st.selectbox(lang_messages['error_correction_label'], list(error_correction_options.keys()), key="error_correction_select",)
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
        filename_delete_disabled = not st.session_state.get("filename_input_key", "")
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

    is_pattern_color_valid_preview = (pattern_color_choice != lang_messages['custom_color_select']) or (pattern_color_choice == lang_messages['custom_color_select'] and pattern_color and is_valid_color(pattern_color))
    is_bg_color_valid_preview = (bg_color_choice != lang_messages['custom_color_select']) or (bg_color_choice == lang_messages['custom_color_select'] and bg_color and is_valid_color(bg_color))
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
                        st.session_state.finder_pattern_shape_select,
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
                        int(st.session_state.mask_pattern_select), "black", "white",
                    )
                    download_data = svg_data.encode('utf-8')
                    download_mime = "image/svg+xml"
                    download_extension = ".svg"

                    # SVG 미리보기를 위한 이미지 생성
                    preview_image_display = draw_custom_shape_image(
                        qr, int(st.session_state.box_size_input), int(st.session_state.border_input),
                        "black", "white", lang_messages['pattern_shape_square'],
                        st.session_state.corner_radius_input,
                        st.session_state.cell_gap_input,
                        lang_messages['pattern_shape_square'],
                    )
        except Exception as e:
            st.error(f"{lang_messages['error_occurred']}: {str(e)}")

    st.markdown("---")

    if preview_image_display:
        st.success(lang_messages['preview_success'])
        st.subheader(lang_messages['preview_subheader'])
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(preview_image_display, caption=lang_messages['preview_subheader'], width=380)

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
#  최종버전(다중 언어 지원 통함 파일 버전)
