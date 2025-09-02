# 이 파일은 QR 코드 생성과 관련된 핵심적인 로직 함수들을 포함합니다.
# functions.py

import qrcode
import io
import re
from PIL import Image, ImageDraw
import qrcode.image.svg
import qrcode.image.styles

# SVG를 위한 둥근 사각형 및 원형 이미지 팩토리 클래스 정의
class SvgRoundedImage(qrcode.image.svg.SvgFragmentImage):
    """SVG에서 둥근 사각형 모듈을 그리는 이미지 팩토리."""
    def drawrect(self, row, col):
        return self._svg.element('rect',
                                 x=self.box_size * col, y=self.box_size * row,
                                 width=self.box_size, height=self.box_size,
                                 rx=self.box_size * 0.25, ry=self.box_size * 0.25,
                                 fill=self.fill_color)

class SvgCircleImage(qrcode.image.svg.SvgFragmentImage):
    """SVG에서 원형 모듈을 그리는 이미지 팩토리."""
    def drawrect(self, row, col):
        cx = self.box_size * (col + 0.5)
        cy = self.box_size * (row + 0.5)
        r = self.box_size * 0.5
        return self._svg.element('circle', cx=cx, cy=cy, r=r, fill=self.fill_color)

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

# QR 코드 PNG 생성 함수
def generate_qr_code_png(
    data,
    box_size,
    border,
    error_correction,
    mask_pattern,
    fill_color,
    back_color,
    pattern_shape,  # 새로운 파라미터 추가
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
        
        # 선택된 모양에 따라 이미지 팩토리를 선택
        if pattern_shape == "Square":
            img_factory = None  # 기본 값
        elif pattern_shape == "Rounded":
            img_factory = qrcode.image.styles.Rounded
        elif pattern_shape == "Circle":
            img_factory = qrcode.image.styles.Circle

        img = qr.make_image(
            fill_color=fill_color,
            back_color=back_color,
            image_factory=img_factory
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
    pattern_shape,  # 새로운 파라미터 추가
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
        
        # 선택된 모양에 따라 이미지 팩토리를 선택
        if pattern_shape == "Square":
            img_factory = qrcode.image.svg.SvgPathImage
        elif pattern_shape == "Rounded":
            img_factory = SvgRoundedImage
        elif pattern_shape == "Circle":
            img_factory = SvgCircleImage

        img_svg = qr.make_image(image_factory=img_factory)
        
        svg_buffer = io.BytesIO()
        img_svg.save(svg_buffer)
        svg_data = svg_buffer.getvalue().decode('utf-8')
        
        # SVG 색상 변경 (SVGPathImage의 경우 필요)
        if pattern_shape == "Square":
            svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1)
            svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        return svg_data, qr
    except Exception as e:
        return None, None
        
