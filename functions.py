# functions.py
import qrcode
import io
import re
from PIL import Image
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


# HEX 축약(#fff) → #ffffff 변환
def normalize_color(color_name: str) -> str:
    if not color_name:
        return "black"
    color_name = color_name.strip()
    # #rgb → #rrggbb 변환
    if re.match(r"^#([A-Fa-f0-9]{3})$", color_name):
        return "#" + "".join([c * 2 for c in color_name[1:]])
    return color_name


# 유효한 색상인지 확인하는 함수 (16진수 및 일반 색상 이름 모두 유효)
def is_valid_color(color_name: str) -> bool:
    if not color_name:
        return False
    color_name = color_name.strip().lower()

    # 16진수 HEX 검사 (#rgb, #rrggbb)
    hex_pattern = re.compile(r"^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$")
    if hex_pattern.match(color_name):
        return True

    # PIL이 인식 가능한 색상명인지 확인
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

        # 모양 선택
        if module_shape == "사각형 (Square)":
            drawer = SquareModuleDrawer()
        elif module_shape == "둥근 사각형 (Rounded)":
            drawer = RoundedModuleDrawer()
        elif module_shape == "원형 (Circle)":
            drawer = CircleModuleDrawer()
        else:
            drawer = SquareModuleDrawer()  # 기본값

        # 색상 정규화
        fill_color = normalize_color(fill_color)
        back_color = normalize_color(back_color)

        # 디버깅 출력 (필요 없으면 제거해도 됨)
        print(f"[DEBUG] 적용된 색상 → fill={fill_color}, back={back_color}")

        # QR 코드 생성
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            fill_color=fill_color,
            back_color=back_color,
        )

        if hasattr(img, "convert"):
            img = img.convert("RGB")
        return img, qr
    except Exception as e:
        print(f"QR 코드 생성 오류: {e}")
        return None, None


# QR 코드 SVG 생성 함수 (색상 고정)
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
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H,
        }
        final_error_correction = error_correction_options.get(
            error_correction, qrcode.constants.ERROR_CORRECT_L
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=final_error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )
        qr.add_data(data, optimize=0)
        qr.make(fit=True)

        img_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        svg_buffer = io.BytesIO()
        img_svg.save(svg_buffer)
        svg_data = svg_buffer.getvalue().decode("utf-8")

        # 색상 강제 적용 (SVG는 black/white 고정)
        svg_data = svg_data.replace('fill="black"', f'fill="{fill_color}"')
        svg_data = svg_data.replace(
            "<path",
            f'<rect width="100%" height="100%" fill="{back_color}"/><path',
        )

        return svg_data, qr
    except Exception as e:
        print(f"SVG QR 코드 생성 오류: {e}")
        return None, None
