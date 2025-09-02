# 이 파일은 QR 코드 생성과 관련된 핵심적인 로직 함수들을 포함합니다.
# functions.py

import qrcode
import io
import re
from PIL import Image, ImageDraw
import qrcode.image.svg
import streamlit as st 

def get_message(key):
    """
    이 함수는 UI에 사용되는 텍스트 메시지를 관리합니다.
    """
    messages = {
        'UI_ERROR_CORRECTION_LEVEL_L': 'L (7% 보정)',
        'UI_ERROR_CORRECTION_LEVEL_M': 'M (15% 보정)',
        'UI_ERROR_CORRECTION_LEVEL_Q': 'Q (25% 보정)',
        'UI_ERROR_CORRECTION_LEVEL_H': 'H (30% 보정)',
        'UI_DOT_STYLE_SQUARE': '사각형',
        'UI_DOT_STYLE_ROUNDED': '둥근 사각',
        'UI_DOT_STYLE_CIRCLE': '원형',
        'UI_DOT_STYLE_DIAMOND': '마름모',
        "UI_ERROR_INVALID_COLOR_FORMAT": "유효한 16진수 색상 코드를 입력해주세요. 예: #000000 또는 #FFF",
        "UI_WARNING_SAME_COLOR": "패턴 색상과 배경 색상이 동일합니다. QR 코드를 인식할 수 없게 됩니다.",
        "UI_PREVIEW_IMAGE_CAPTION": "QR 코드 미리보기",
        "UI_DOWNLOAD_PNG_BUTTON": "PNG 다운로드",
        "UI_DOWNLOAD_SVG_BUTTON": "SVG 다운로드",
    }
    return messages.get(key, key)

# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()

# 유효한 색상인지 확인하는 함수 (16진수 값만 유효)
def is_valid_color(color_name):
    if not color_name:
        return False
    color_name = color_name.strip()
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return hex_pattern.match(color_name)

def get_error_correction_constant(level_str):
    """
    사용자가 선택한 오류 보정 레벨 문자열에 해당하는 QR 코드 상수를 반환합니다.
    """
    if level_str == get_message('UI_ERROR_CORRECTION_LEVEL_L'):
        return qrcode.constants.ERROR_CORRECT_L
    elif level_str == get_message('UI_ERROR_CORRECTION_LEVEL_M'):
        return qrcode.constants.ERROR_CORRECT_M
    elif level_str == get_message('UI_ERROR_CORRECTION_LEVEL_Q'):
        return qrcode.constants.ERROR_CORRECT_Q
    elif level_str == get_message('UI_ERROR_CORRECTION_LEVEL_H'):
        return qrcode.constants.ERROR_CORRECT_H
    else:
        return qrcode.constants.ERROR_CORRECT_H

# QR 코드 PNG 생성 함수 (패턴 스타일 추가)
def generate_qr_code_png(
    data,
    box_size,
    border,
    error_correction,
    mask_pattern,
    fill_color,
    back_color,
    dot_style,
):
    try:
        qr = qrcode.QRCode(
            version=None, # auto version
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )

        qr.add_data(data)
        qr.make(fit=True)
        
        # QR 코드 패턴 스타일 적용 (기존 코드와 동일)
        if dot_style != get_message('UI_DOT_STYLE_SQUARE'):
            base_size = qr.modules_count * box_size + 2 * border * box_size
            styled_img = Image.new('RGB', (base_size, base_size), back_color)
            
            for r in range(qr.modules_count):
                for c in range(qr.modules_count):
                    if qr.modules[r][c]:
                        dot_img = Image.new('RGBA', (box_size, box_size), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(dot_img)
                        
                        if dot_style == get_message('UI_DOT_STYLE_ROUNDED'):
                            draw.rounded_rectangle((0, 0, box_size, box_size), radius=box_size/4, fill=fill_color)
                        elif dot_style == get_message('UI_DOT_STYLE_CIRCLE'):
                            draw.ellipse((0, 0, box_size, box_size), fill=fill_color)
                            
                        # --- 💡 다이아몬드(마름모) 모양 추가 ---
                        elif dot_style == get_message('UI_DOT_STYLE_DIAMOND'):
                            points = [
                                (box_size/2, 0),         # 상단 꼭짓점
                                (box_size, box_size/2),  # 우측 꼭짓점
                                (box_size/2, box_size),  # 하단 꼭짓점
                                (0, box_size/2)          # 좌측 꼭짓점
                            ]
                            draw.polygon(points, fill=fill_color)
                        # ------------------------------------
                            
                        pos_x = (c + border) * box_size
                        pos_y = (r + border) * box_size
                        styled_img.paste(dot_img, (pos_x, pos_y), dot_img)

            img = styled_img
        else: # 사각형 패턴인 경우
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            if hasattr(img, 'convert'):
                img = img.convert('RGB')

        return img, qr
    except Exception as e:
        return None, None

# QR 코드 SVG 생성 함수
def generate_qr_code_svg(
    data,
    box_size,
    border,
    error_correction,
    mask_pattern,
    fill_color,
    back_color,
):
    try:
        # SVG는 자체적으로 fill_color, back_color를 지원
        factory = qrcode.image.svg.SvgPathImage
        
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )

        qr.add_data(data)
        qr.make(fit=True)
        
        img_svg = qr.make_image(image_factory=factory)
        
        svg_buffer = io.BytesIO()
        img_svg.save(svg_buffer)
        svg_data = svg_buffer.getvalue().decode('utf-8')
        
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1)
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        return None, None
