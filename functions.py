# 이 파일은 QR 코드 생성과 관련된 핵심적인 로직 함수들을 포함합니다.
# functions.py
import qrcode
import io
import re
from PIL import Image, ImageColor
import qrcode.image.svg
# 모듈 모양 변경을 위한 클래스 임포트
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer

# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()

# 유효한 색상인지 확인하는 함수 (16진수 및 일반 색상 이름 모두 유효)
def is_valid_color(color_name):
    if not color_name:
        return False
    color_name = color_name.strip().lower()
    
    # 1. 16진수 패턴 확인
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if hex_pattern.match(color_name):
        return True
    
    # 2. 일반적인 색상 이름 확인 (PIL 라이브러리가 지원하는 색상 이름 일부)
    try:
        Image.new("RGB", (1, 1), color_name)
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
    module_shape, # 모듈 모양을 인자로 받음
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
        
        # [수정] 모든 패턴 모양에 대해 drawer를 명시적으로 설정
        drawer = None
        if module_shape == "사각형 (Square)":
            drawer = SquareModuleDrawer()
        elif module_shape == "둥근 사각형 (Rounded)":
            drawer = RoundedModuleDrawer()
        elif module_shape == "원형 (Circle)":
            drawer = CircleModuleDrawer()
        else:
            # 기본값으로 사각형 설정
            drawer = SquareModuleDrawer()
        
        # [수정] 모든 경우에 StyledPilImage와 drawer를 사용하여 색상이 확실히 적용되도록 함
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            fill_color=fill_color,
            back_color=back_color
        )
        
        if hasattr(img, 'convert'):
            img = img.convert('RGB')
        return img, qr
    except Exception as e:
        print(f"QR 코드 생성 오류: {e}")
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
        # [추가] 오류 보정 문자열을 QR 코드 상수로 변환
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        final_error_correction = error_correction_options.get(error_correction, qrcode.constants.ERROR_CORRECT_L)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=final_error_correction, # 수정된 변수 사용
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
        
        # SVG 색상 변경 로직을 더 안정적인 방식으로 개선
        # 패턴(기본 검정) 색상을 사용자가 지정한 색으로 변경
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"')
        # 배경색을 채우기 위한 사각형(rect)을 맨 앞에 추가
        svg_data = svg_data.replace('<path', f'<rect width="100%" height="100%" fill="{back_color}"/><path')
        
        return svg_data, qr
    except Exception as e:
        print(f"SVG QR 코드 생성 오류: {e}")
        return None, None
