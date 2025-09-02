# functions.py
import qrcode
import io
import re
from PIL import Image, ImageDraw
import qrcode.image.svg

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

# --- 새로 추가된 코드 시작 ---
# 원형 및 둥근 사각형 모듈을 그리는 커스텀 이미지 팩토리
class CustomPilImage(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, fill_color, back_color, module_shape='square'):
        self.border = border
        self.width = width
        self.box_size = box_size
        self.fill_color = fill_color
        self.back_color = back_color
        self.module_shape = module_shape
        self.pixel_size = (self.width + self.border*2) * self.box_size
        self.img = Image.new("RGB", (self.pixel_size, self.pixel_size), self.back_color)
        self.draw = ImageDraw.Draw(self.img)

    def drawrect(self, row, col):
        left, top = (col + self.border) * self.box_size, (row + self.border) * self.box_size
        right, bottom = left + self.box_size, top + self.box_size

        if self.module_shape == 'circular':
            self.draw.ellipse((left, top, right, bottom), fill=self.fill_color)
        elif self.module_shape == 'rounded':
            radius = int(self.box_size / 3)
            self.draw.rounded_rectangle((left, top, right, bottom), radius=radius, fill=self.fill_color)
        else: # 기본 사각형
            self.draw.rectangle((left, top, right, bottom), fill=self.fill_color)

    def save(self, stream, format):
        self.img.save(stream, format)

# --- 새로 추가된 코드 끝 ---

# QR 코드 PNG 생성 함수
def generate_qr_code_png(
    data,
    box_size,
    border,
    error_correction,
    mask_pattern,
    fill_color,
    back_color,
    module_shape='square' # module_shape 인자 추가
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
        
        # module_shape 인자를 사용하여 make_image에 커스텀 팩토리 전달
        if module_shape != 'square':
            img = qr.make_image(
                image_factory=lambda **kwargs: CustomPilImage(
                    fill_color=fill_color, back_color=back_color, module_shape=module_shape, **kwargs
                )
            )
        else:
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
    module_shape='square' # module_shape 인자 추가
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
        
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"', 1)
        svg_data = svg_data.replace('fill="white"', f'fill="{back_color}"', 1)
        
        # SVG는 모듈 모양 변경이 더 복잡하므로, 이 부분은 현재 사각형만 지원
        # TODO: SVG 모듈 모양 변경 로직 추가
        
        return svg_data, qr
    except Exception as e:
        return None, None
