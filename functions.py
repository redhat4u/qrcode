# functions.py

import qrcode
import qrcode.image.svg
import io
import streamlit as st
import re
from messages import get_message
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import Rounded, Circle, GappedSquare

def get_error_correction(level):
    """
    사용자가 선택한 오류 보정 레벨에 해당하는 QR 코드 상수를 반환합니다.
    """
    if level == get_message('UI_ERROR_CORRECTION_LEVEL_L'):
        return qrcode.constants.ERROR_CORRECT_L
    elif level == get_message('UI_ERROR_CORRECTION_LEVEL_M'):
        return qrcode.constants.ERROR_CORRECT_M
    elif level == get_message('UI_ERROR_CORRECTION_LEVEL_Q'):
        return qrcode.constants.ERROR_CORRECT_Q
    elif level == get_message('UI_ERROR_CORRECTION_LEVEL_H'):
        return qrcode.constants.ERROR_CORRECT_H
    else:
        # 기본값은 H로 설정
        return qrcode.constants.ERROR_CORRECT_H

def get_dot_style(style_name):
    """
    사용자가 선택한 점 스타일 이름에 해당하는 qrcode-with-dots 클래스를 반환합니다.
    """
    if style_name == get_message('UI_DOT_STYLE_SQUARE'):
        return qrcode.image.styles.moduledrawers.Square
    elif style_name == get_message('UI_DOT_STYLE_ROUNDED'):
        return qrcode.image.styles.moduledrawers.Rounded
    elif style_name == get_message('UI_DOT_STYLE_CIRCLE'):
        return qrcode.image.styles.moduledrawers.Circle
    elif style_name == get_message('UI_DOT_STYLE_DIAMOND'):
        return qrcode.image.styles.moduledrawers.GappedSquare
    else:
        # 기본값은 Square
        return qrcode.image.styles.moduledrawers.Square

def is_valid_hex_color(hex_code):
    """
    입력된 문자열이 유효한 16진수 색상 코드인지 확인합니다.
    """
    if not isinstance(hex_code, str) or not hex_code.startswith('#'):
        return False
    # # 뒤에 3자리 또는 6자리의 16진수 문자가 있는지 확인
    hex_chars = hex_code[1:]
    return len(hex_chars) in (3, 6) and all(c in '0123456789abcdefABCDEF' for c in hex_chars)

def create_qr_code(qr_data, error_correction, box_size, border, pattern_color, bg_color, dot_style, file_format):
    """
    사용자 설정에 따라 QR 코드를 생성하고 이미지 바이트를 반환합니다.
    """
    # 색상 유효성 검사
    if pattern_color == get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
        pattern_color_hex = st.session_state.custom_pattern_color_input_key
        if not is_valid_hex_color(pattern_color_hex):
            st.session_state.error_message = get_message('UI_ERROR_INVALID_PATTERN_COLOR')
            return None, None
        dot_color = pattern_color_hex
    else:
        dot_color = pattern_color
        
    if bg_color == get_message('UI_COLOR_OPTION_DIRECT_INPUT'):
        bg_color_hex = st.session_state.custom_bg_color_input_key
        if not is_valid_hex_color(bg_color_hex):
            st.session_state.error_message = get_message('UI_ERROR_INVALID_BG_COLOR')
            return None, None
        background_color = bg_color_hex
    else:
        background_color = bg_color

    # 패턴 색상과 배경 색상이 같으면 경고 메시지 표시
    if dot_color == background_color:
        st.session_state.error_message = get_message('UI_ERROR_SAME_COLOR')
        return None, None
        
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=box_size,
            border=border
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # PNG 생성 로직
        if file_format == get_message('UI_FILE_FORMAT_PNG'):
            # DotStyle 객체 생성
            dot_style_class = get_dot_style(dot_style)
            # make_image 호출 시 fill_color와 back_color를 명시적으로 전달
            img = qr.make_image(
                image_factory=qrcode.image.StyledPilImage,
                module_drawer=dot_style_class(),
                color_mask=SolidFillColorMask(
                    front_color=dot_color,
                    back_color=background_color
                )
            )
            # 이미지 바이트로 변환
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format='PNG')
            img_bytes = img_bytes_io.getvalue()
            return img_bytes, qr.version

        # SVG 생성 로직
        elif file_format == get_message('UI_FILE_FORMAT_SVG'):
            # SVG는 기본 사각형과 색상만 지원
            factory = qrcode.image.svg.SvgPathImage
            svg_img = qr.make_image(image_factory=factory)
            svg_bytes_io = io.BytesIO()
            svg_img.save(svg_bytes_io)
            return svg_bytes_io.getvalue(), qr.version
        
    except Exception as e:
        st.session_state.error_message = f"QR 코드 생성 중 오류가 발생했습니다: {e}"
        return None, None
    
    return None, None

def get_qr_info(qr_version, qr_size, border, pattern_color, bg_color):
    """QR 코드의 상세 정보를 딕셔너리로 반환합니다."""
    # QR 코드 버전 정보
    if qr_version <= 0:
        version_text = "자동 생성 (Auto)"
    else:
        version_text = f"버전 {qr_version}"
        
    # 셀 개수
    cells_per_side = 21 + (qr_version - 1) * 4 if qr_version > 0 else "자동 계산"
    
    # 이미지 크기
    image_size = (cells_per_side + border * 2) * qr_size if isinstance(cells_per_side, int) else "자동 계산"
    
    return {
        get_message('UI_INFO_QR_VERSION'): version_text,
        get_message('UI_INFO_QR_CELL_COUNT'): cells_per_side,
        get_message('UI_INFO_QR_IMAGE_SIZE_REFERENCE'): f"{image_size}px x {image_size}px" if isinstance(image_size, int) else image_size,
        get_message('UI_INFO_QR_PATTERN_COLOR'): pattern_color,
        get_message('UI_INFO_QR_BG_COLOR'): bg_color,
    }
    
