# 이 파일은 QR 코드 생성과 관련된 핵심적인 로직 함수들을 포함합니다.
# functions.py

import qrcode
import io
import re
from PIL import Image, ImageColor

# 모듈 모양 변경을 위한 클래스 임포트
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer
import qrcode.image.svg


# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()


# 유효한 색상인지 확인하는 함수 (16진수 및 일반 색상 이름 모두 유효)
def is_valid_color(color_name: str) -> bool:
    if not color_name:
        return False
    color_name = color_name.strip()
    try:
        # PIL이 인식 가능한 색상명인지 확인
        ImageColor.getrgb(color_name)
        return True
    except ValueError:
        return False


# QR 코드 PNG 생성 함수
def generate_qr_code_png(
    data,
    box_size,
    border,
    error_correction,
    mask_pattern,
    fill_color,
    back_color,
    module_shape,
):
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

        # 모양 선택 (새로 추가된 로직)
        if module_shape == "사각형 (Square)":
            drawer = SquareModuleDrawer()
        elif module_shape == "둥근 사각형 (Rounded)":
            drawer = RoundedModuleDrawer()
        elif module_shape == "원형 (Circle)":
            drawer = CircleModuleDrawer()
        else:
            drawer = SquareModuleDrawer()  # 기본값

        # 색상 코드를 (R, G, B) 튜플로 변환하여 안정성을 높입니다.
        try:
            fill_color_rgb = ImageColor.getrgb(fill_color)
            back_color_rgb = ImageColor.getrgb(back_color)
        except ValueError:
            print(f"유효하지 않은 색상 값: fill={fill_color}, back={back_color}")
            fill_color_rgb = (0, 0, 0)
            back_color_rgb = (255, 255, 255)

        # 스타일이 적용된 QR 코드를 생성합니다.
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            fill_color=fill_color_rgb,
            back_color=back_color_rgb,
        )

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
        
        # SVG 색상 강제 적용
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1)
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        return None, None
