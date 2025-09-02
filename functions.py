# 이 파일은 QR 코드 생성과 관련된 핵심적인 로직 함수들을 포함합니다.
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
            version=1,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )

        qr.add_data(data, optimize=0)
        qr.make(fit=True)
        
        # QR 코드 패턴 스타일 적용 (기존 코드와 동일)
        if dot_style != "사각형":
            base_size = qr.modules_count * box_size + 2 * border * box_size
            styled_img = Image.new('RGB', (base_size, base_size), back_color)
            
            for r in range(qr.modules_count):
                for c in range(qr.modules_count):
                    if qr.modules[r][c]:
                        dot_img = Image.new('RGBA', (box_size, box_size), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(dot_img)
                        
                        if dot_style == "둥근 사각":
                            draw.rounded_rectangle((0, 0, box_size, box_size), radius=box_size/4, fill=fill_color)
                        elif dot_style == "원형":
                            draw.ellipse((0, 0, box_size, box_size), fill=fill_color)
                            
                        # --- 💡 다이아몬드(마름모) 모양 추가 ---
                        elif dot_style == "마름모":
                            points = [
                                (box_size/2, 0),        # 상단 꼭짓점
                                (box_size, box_size/2),   # 우측 꼭짓점
                                (box_size/2, box_size),   # 하단 꼭짓점
                                (0, box_size/2)         # 좌측 꼭짓점
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
            version=1,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )

        qr.add_data(data, optimize=0)
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
        
