# messages.py

import qrcode

def get_messages(lang):
    """지정된 언어에 대한 모든 메시지를 반환합니다."""
    
    # 한국어 메시지
    messages_ko = {
        # 페이지 제목
        "page_title": "QR 코드 생성기",
        # 구분선
        "separator": "---",
        # 메인 제목 및 설명
        "main_title": "QR 코드 생성기",
        # 설정 섹션
        "header_settings": "설정",
        # QR 코드 내용
        "subheader_content": "QR 코드 내용",
        "info_max_chars": "최대 2953자까지 입력 가능합니다. 한글은 약 1000자입니다.",
        "text_area_label": "내용 입력",
        "text_area_placeholder": "웹사이트 주소, 전화번호, 이메일 주소 등을 입력하세요.",
        "char_count_exceeded_error": "최대 문자 수({}자)를 초과했습니다! QR 코드가 생성되지 않습니다.",
        "char_count_warning": "문자 수가 많습니다({}자)! QR 코드 읽기가 불안정할 수 있습니다.",
        "char_count_success": "현재 문자 수: {}자",
        "char_count_caption": "현재 문자 수: 0자",
        "strip_option_label": "내용 앞뒤 공백/줄바꿈 제거",
        "strip_option_help": "QR 코드 데이터의 불필요한 공백과 줄바꿈을 자동으로 제거합니다.",
        "delete_content_button": "내용 삭제",
        "delete_content_help": "입력한 내용을 모두 지웁니다.",
        # 파일 형식
        "subheader_file_format": "파일 형식",
        "file_format_label": "파일 형식 선택",
        "jpg_info_caption": "JPG는 손실 압축으로 품질 저하가 있을 수 있습니다. 품질을 조절하세요.",
        "jpg_quality_label": "JPG 품질 (1-100)",
        "jpg_quality_help": "값이 낮을수록 파일 크기가 작아지지만, QR 코드가 손상될 수 있습니다.",
        "png_info_caption": "PNG는 무손실 압축으로 원본 품질을 유지합니다.",
        "svg_info_caption": "SVG는 벡터 이미지로, 크기를 자유롭게 조절해도 화질 저하가 없습니다.",
        # 패턴 모양
        "subheader_pattern_shape": "패턴 모양",
        "svg_shape_warning": "SVG 형식은 '사각' 패턴만 지원합니다.",
        "pattern_shape_label": "일반 패턴 모양",
        "finder_pattern_shape_label": "파인더 패턴 모양",
        "shape_square": "사각",
        "shape_rounded_square": "둥근사각",
        "shape_circle": "동그라미",
        "shape_diamond": "마름모",
        "shape_star": "별",
        "shape_cross": "십자가",
        "svg_no_rounded_corners_warning": "SVG 형식은 둥근 모서리를 지원하지 않습니다.",
        "rounded_corners_radius_label": "둥근 모서리 반경 (%)",
        "rounded_corners_radius_help": "값이 높을수록 모서리가 더 둥글어집니다.",
        "no_gap_warning": "사각 패턴 및 SVG 형식에서는 패턴 간격 조절이 지원되지 않습니다.",
        "cell_gap_label": "패턴 간격 (%)",
        "cell_gap_help": "값이 높을수록 패턴 사이에 빈 공간이 넓어집니다.",
        # 색상
        "subheader_color_settings": "색상",
        "svg_color_warning": "SVG 형식은 '검은색/흰색'만 지원합니다.",
        "pattern_color_label": "패턴 색상",
        "bg_color_label": "배경 색상",
        "direct_input_color_option": "직접 입력",
        "hex_code_info": "HEX 코드로 직접 색상을 입력할 수 있습니다. (예: #FF5733)",
        "hex_code_caption": "기본 색상 목록은 미리보기에서 확인할 수 있습니다.",
        "pattern_hex_input_label": "패턴 HEX 코드",
        "bg_hex_input_label": "배경 HEX 코드",
        "hex_input_missing_warning": "{}의 HEX 코드를 입력해주세요.",
        "hex_input_invalid_warning": "{}의 HEX 코드가 올바르지 않습니다. 다시 확인해주세요.",
        "same_color_warning": "패턴 색상과 배경 색상이 같으면 QR 코드를 스캔할 수 없습니다.",
        # QR 설정
        "subheader_qr_settings": "QR 코드 설정",
        "box_size_label": "모듈 크기 (픽셀)",
        "border_label": "테두리 크기 (모듈)",
        "error_correction_label": "오류 복원 레벨",
        "error_correction_options_low": "낮음 (7%)",
        "error_correction_options_medium": "보통 (15%)",
        "error_correction_options_quartile": "높음 (25%)",
        "error_correction_options_high": "매우 높음 (30%)",
        "mask_pattern_label": "마스크 패턴 (0-7)",
        "mask_pattern_help": "마스크 패턴은 QR 코드의 밝기 대비를 최적화하여 스캔율을 높입니다.",
        # 파일명
        "subheader_filename": "파일명",
        "filename_input_label": "파일명 입력 (선택 사항)",
        "filename_placeholder": "파일명을 입력하면 날짜가 제외됩니다.",
        "delete_filename_button": "파일명 삭제",
        "delete_filename_help": "입력한 파일명을 지우고 기본 날짜 형식으로 변경합니다.",
        # 미리보기 및 다운로드
        "header_preview_download": "미리보기 & 다운로드",
        "success_message": "QR 코드가 성공적으로 생성되었습니다!",
        "subheader_preview": "미리보기",
        "preview_caption": "QR 코드 이미지",
        "qr_info_title": "QR 코드 상세 정보",
        "qr_version": "버전: {}",
        "qr_cells": "QR 모듈 수: {}x{}",
        "qr_border_cells": "테두리 모듈 수: {}x{}",
        "qr_box_size": "모듈 픽셀: {}px",
        "qr_image_size": "이미지 크기: {}x{}px",
        "qr_calc_method": "💡 크기 계산: (모듈 수 + 테두리 모듈 수) x 모듈 크기",
        "qr_pattern_color": "패턴 색상: {}",
        "qr_bg_color": "배경 색상: {}",
        "download_button_label": "다운로드",
        "download_button_help": "생성된 QR 코드 이미지를 다운로드합니다.",
        "download_filename_display": "다운로드 파일명:",
        "download_error_warning": "QR 코드 생성에 필요한 모든 내용을 입력해주세요.",
        "no_content_info": "내용을 입력하시면 QR 코드가 생성됩니다.",
        # 리셋 버튼
        "reset_button_label": "전체 설정 초기화",
        "reset_button_help": "모든 입력 내용과 설정을 기본값으로 되돌립니다.",
        # 사이드바
        "sidebar_guide_title": "사용 가이드",
        "sidebar_guide_1": "- QR 코드에 넣을 내용을 **'내용 입력'** 칸에 입력하세요.",
        "sidebar_guide_2": "- **'파일 형식'**을 선택하여 PNG, JPG, SVG로 저장할 수 있습니다.",
        "sidebar_guide_3": "- **'패턴 모양'**과 **'색상'**을 커스터마이징하여 나만의 QR 코드를 만들어보세요.",
        "sidebar_guide_4": "- QR 코드의 **'크기'**와 **'테두리'**를 조절하여 사용 환경에 맞게 최적화하세요.",
        "sidebar_guide_5": "- **'오류 복원 레벨'**을 높이면 QR 코드가 손상되어도 더 잘 스캔됩니다. 단, 데이터 용량이 늘어납니다.",
        "sidebar_guide_6": "- **'파일명'**을 입력하면 원하는 이름으로 저장할 수 있습니다. 입력하지 않으면 자동으로 날짜와 시간이 포함됩니다.",
        "sidebar_tips_title": "유용한 팁",
        "tip_text": "- 다음 형식에 맞추어 내용을 입력하면, 스캔 시 자동으로 해당 앱이 실행됩니다.",
        "tip_website": "🌐 **웹사이트**: `https://www.google.com`",
        "tip_email": "📧 **이메일**: `mailto:user@example.com`",
        "tip_email_full": "📧 **이메일 (제목/내용 포함)**: `mailto:user@example.com?subject=Hello&body=Greetings`",
        "tip_phone": "📞 **전화번호**: `tel:01012345678`",
        "tip_sms": "💬 **문자**: `sms:01012345678`",
        "tip_sms_full": "💬 **문자 (내용 포함)**: `sms:01012345678?body=Hello`",
        "tip_wifi": "📶 **와이파이**: `WIFI:T:WPA;S:MyNetwork;P:MyPassword;H:false;`",
        "sidebar_settings_title": "세부 설정 설명",
        "sidebar_file_format_title": "### 파일 형식",
        "sidebar_png_desc": "- **PNG**: 무손실 압축으로 품질 저하가 없으며, 투명 배경을 지원합니다.",
        "sidebar_jpg_desc": "- **JPG**: 손실 압축으로 파일 크기가 작습니다. 사진에 주로 사용됩니다.",
        "sidebar_svg_desc": "- **SVG**: 벡터 형식으로 해상도에 영향을 받지 않아 확대해도 깨지지 않습니다. '사각' 패턴과 '검은색/흰색'만 지원합니다.",
        "sidebar_pattern_shape_title": "### 패턴 모양",
        "sidebar_pattern_shape_desc": "- QR 코드의 작은 점(모듈)들의 모양을 변경할 수 있습니다. '둥근사각'을 선택하면 **'둥근 모서리 반경'** 슬라이더가 나타납니다.",
        "sidebar_pattern_shape_warning": "- '파인더 패턴'은 QR 코드의 세 개의 큰 사각형 패턴을 의미하며, 나머지 부분을 '일반 패턴'으로 커스터마이징할 수 있습니다.",
        "sidebar_cell_gap_title": "### 패턴 간격",
        "sidebar_cell_gap_desc_1": "- 패턴의 크기를 작게 하여 패턴 사이에 간격을 만듭니다.",
        "sidebar_cell_gap_desc_2": "- '사각' 패턴과 **'SVG'** 파일 형식에서는 지원되지 않습니다. 패턴이 너무 작아지면 스캔이 어려울 수 있습니다.",
        "sidebar_color_input_title": "### 색상",
        "sidebar_color_input_desc_1": "- 패턴 색상과 배경 색상을 설정합니다. 대비가 낮으면 스캔이 어려울 수 있습니다.",
        "sidebar_color_input_desc_2": "- **'직접 입력'**을 선택하면 HEX 코드로 원하는 색상을 입력할 수 있습니다. (예: `#FF5733`)",
        "sidebar_color_input_desc_3": "- **'SVG'** 형식은 색상 커스터마이징을 지원하지 않습니다.",
        "sidebar_qr_settings_title": "### QR 코드 설정",
        "sidebar_error_correction_title": "- **오류 복원 레벨**: QR 코드에 손상이 발생했을 때 복구할 수 있는 데이터의 양을 설정합니다. 높을수록 더 많은 데이터가 손상되어도 복원할 수 있지만, 데이터 용량이 커집니다.",
        "sidebar_error_correction_low": "  - **낮음**: 약 7%의 데이터 복원",
        "sidebar_error_correction_medium": "  - **보통**: 약 15%의 데이터 복원",
        "sidebar_error_correction_quartile": "  - **높음**: 약 25%의 데이터 복원",
        "sidebar_error_correction_high": "  - **매우 높음**: 약 30%의 데이터 복원",
        "sidebar_mask_pattern_title": "- **마스크 패턴**: QR 코드의 패턴이 너무 규칙적이어서 스캔이 어려울 때, 패턴의 모양을 미세하게 변경하여 스캔율을 높이는 기술입니다.",
        # 푸터
        "footer_info": "이 웹 앱은 Streamlit과 Python qrcode 라이브러리를 사용하여 개발되었습니다.",
    }
    
    # 영어 메시지
    messages_en = {
        # 페이지 제목
        "page_title": "QR Code Generator",
        # 구분선
        "separator": "---",
        # 메인 제목 및 설명
        "main_title": "QR Code Generator",
        # 설정 섹션
        "header_settings": "Settings",
        # QR 코드 내용
        "subheader_content": "QR Code Content",
        "info_max_chars": "You can enter up to 2953 characters.",
        "text_area_label": "Enter Content",
        "text_area_placeholder": "Enter a website URL, phone number, email address, etc.",
        "char_count_exceeded_error": "Maximum character count ({} characters) exceeded! QR code will not be generated.",
        "char_count_warning": "High character count ({} characters)! QR code readability may be unstable.",
        "char_count_success": "Current character count: {} characters",
        "char_count_caption": "Current character count: 0 characters",
        "strip_option_label": "Strip leading/trailing whitespace/newlines",
        "strip_option_help": "Automatically removes unnecessary spaces and newlines from the QR code data.",
        "delete_content_button": "Clear Content",
        "delete_content_help": "Clears all entered content.",
        # 파일 형식
        "subheader_file_format": "File Format",
        "file_format_label": "Select File Format",
        "jpg_info_caption": "JPG is a lossy format, so quality may be degraded. Adjust the quality.",
        "jpg_quality_label": "JPG Quality (1-100)",
        "jpg_quality_help": "Lower values result in smaller file sizes but may damage the QR code.",
        "png_info_caption": "PNG is a lossless format that maintains original quality.",
        "svg_info_caption": "SVG is a vector image format, which means it won't lose quality when scaled.",
        # 패턴 모양
        "subheader_pattern_shape": "Pattern Shape",
        "svg_shape_warning": "SVG format only supports the 'Square' pattern.",
        "pattern_shape_label": "Data Pattern Shape",
        "finder_pattern_shape_label": "Finder Pattern Shape",
        "shape_square": "Square",
        "shape_rounded_square": "Rounded Square",
        "shape_circle": "Circle",
        "shape_diamond": "Diamond",
        "shape_star": "Star",
        "shape_cross": "Cross",
        "svg_no_rounded_corners_warning": "SVG format does not support rounded corners.",
        "rounded_corners_radius_label": "Rounded Corner Radius (%)",
        "rounded_corners_radius_help": "Higher values result in rounder corners.",
        "no_gap_warning": "Pattern spacing is not supported for 'Square' patterns and SVG format.",
        "cell_gap_label": "Pattern Spacing (%)",
        "cell_gap_help": "Higher values create more empty space between patterns.",
        # 색상
        "subheader_color_settings": "Colors",
        "svg_color_warning": "SVG format only supports 'black/white'.",
        "pattern_color_label": "Pattern Color",
        "bg_color_label": "Background Color",
        "direct_input_color_option": "Direct Input",
        "hex_code_info": "You can enter a color using a HEX code (e.g., #FF5733).",
        "hex_code_caption": "Basic colors are available in the preview.",
        "pattern_hex_input_label": "Pattern HEX Code",
        "bg_hex_input_label": "Background HEX Code",
        "hex_input_missing_warning": "Please enter a HEX code for {}.",
        "hex_input_invalid_warning": "Invalid HEX code for {}. Please check again.",
        "same_color_warning": "The QR code cannot be scanned if the pattern and background colors are the same.",
        # QR 설정
        "subheader_qr_settings": "QR Code Settings",
        "box_size_label": "Module Size (pixels)",
        "border_label": "Border Size (modules)",
        "error_correction_label": "Error Correction Level",
        "error_correction_options_low": "Low (7%)",
        "error_correction_options_medium": "Medium (15%)",
        "error_correction_options_quartile": "Quartile (25%)",
        "error_correction_options_high": "High (30%)",
        "mask_pattern_label": "Mask Pattern (0-7)",
        "mask_pattern_help": "Mask patterns optimize the contrast of the QR code to improve scan rates.",
        # 파일명
        "subheader_filename": "Filename",
        "filename_input_label": "Enter Filename (Optional)",
        "filename_placeholder": "Enter a filename to exclude the date.",
        "delete_filename_button": "Clear Filename",
        "delete_filename_help": "Clears the entered filename and reverts to the default date format.",
        # 미리보기 및 다운로드
        "header_preview_download": "Preview & Download",
        "success_message": "QR code successfully generated!",
        "subheader_preview": "Preview",
        "preview_caption": "QR Code Image",
        "qr_info_title": "QR Code Details",
        "qr_version": "Version: {}",
        "qr_cells": "QR Module Count: {}x{}",
        "qr_border_cells": "Border Module Count: {}x{}",
        "qr_box_size": "Module Pixels: {}px",
        "qr_image_size": "Image Size: {}x{}px",
        "qr_calc_method": "💡 Size Calculation: (Module count + Border modules) x Module size",
        "qr_pattern_color": "Pattern Color: {}",
        "qr_bg_color": "Background Color: {}",
        "download_button_label": "Download",
        "download_button_help": "Download the generated QR code image.",
        "download_filename_display": "Download Filename:",
        "download_error_warning": "Please enter all required content to generate the QR code.",
        "no_content_info": "Enter content to generate the QR code.",
        # 리셋 버튼
        "reset_button_label": "Reset All Settings",
        "reset_button_help": "Resets all inputs and settings to their default values.",
        # 사이드바
        "sidebar_guide_title": "User Guide",
        "sidebar_guide_1": "- Enter the content for the QR code in the **'Enter Content'** box.",
        "sidebar_guide_2": "- Select the **'File Format'** to save as PNG, JPG, or SVG.",
        "sidebar_guide_3": "- Customize the **'Pattern Shape'** and **'Colors'** to create your own unique QR code.",
        "sidebar_guide_4": "- Adjust the **'Size'** and **'Border'** of the QR code to optimize it for your use case.",
        "sidebar_guide_5": "- A higher **'Error Correction Level'** allows the QR code to be scanned even with more damage, but it increases the data capacity.",
        "sidebar_guide_6": "- Enter a **'Filename'** to save with a custom name. If left blank, it will automatically include the date and time.",
        "sidebar_tips_title": "Useful Tips",
        "tip_text": "- If you enter content in the following format, the corresponding app will automatically launch on scan.",
        "tip_website": "🌐 **Website**: `https://www.google.com`",
        "tip_email": "📧 **Email**: `mailto:user@example.com`",
        "tip_email_full": "📧 **Email (with subject/body)**: `mailto:user@example.com?subject=Hello&body=Greetings`",
        "tip_phone": "📞 **Phone**: `tel:01012345678`",
        "tip_sms": "💬 **Text Message**: `sms:01012345678`",
        "tip_sms_full": "💬 **Text Message (with body)**: `sms:01012345678?body=Hello`",
        "tip_wifi": "📶 **Wi-Fi**: `WIFI:T:WPA;S:MyNetwork;P:MyPassword;H:false;`",
        "sidebar_settings_title": "Detailed Settings",
        "sidebar_file_format_title": "### File Format",
        "sidebar_png_desc": "- **PNG**: A lossless format that maintains quality and supports transparent backgrounds.",
        "sidebar_jpg_desc": "- **JPG**: A lossy compressed format with a smaller file size, often used for photos.",
        "sidebar_svg_desc": "- **SVG**: A vector format that won't lose quality when scaled. It only supports 'Square' patterns and 'black/white' colors.",
        "sidebar_pattern_shape_title": "### Pattern Shape",
        "sidebar_pattern_shape_desc": "- You can change the shape of the small dots (modules) of the QR code. Selecting 'Rounded Square' will reveal the **'Rounded Corner Radius'** slider.",
        "sidebar_pattern_shape_warning": "- 'Finder Pattern' refers to the three large square patterns of the QR code, while the remaining parts can be customized as 'Data Pattern'.",
        "sidebar_cell_gap_title": "### Pattern Spacing",
        "sidebar_cell_gap_desc_1": "- Reduces the size of the patterns to create spacing between them.",
        "sidebar_cell_gap_desc_2": "- Not supported for 'Square' patterns and **'SVG'** files. If the patterns become too small, scanning may be difficult.",
        "sidebar_color_input_title": "### Colors",
        "sidebar_color_input_desc_1": "- Set the pattern and background colors. Low contrast can make scanning difficult.",
        "sidebar_color_input_desc_2": "- Select **'Direct Input'** to enter a custom color using a HEX code (e.g., `#FF5733`).",
        "sidebar_color_input_desc_3": "- **'SVG'** format does not support color customization.",
        "sidebar_qr_settings_title": "### QR Code Settings",
        "sidebar_error_correction_title": "- **Error Correction Level**: Sets the amount of data that can be recovered if the QR code is damaged. A higher level allows for more damage to be recovered but increases the data capacity.",
        "sidebar_error_correction_low": "  - **Low**: ~7% data recovery",
        "sidebar_error_correction_medium": "  - **Medium**: ~15% data recovery",
        "sidebar_error_correction_quartile": "  - **Quartile**: ~25% data recovery",
        "sidebar_error_correction_high": "  - **High**: ~30% data recovery",
        "sidebar_mask_pattern_title": "- **마스크 패턴**: QR 코드의 패턴이 너무 규칙적이어서 스캔이 어려울 때, 패턴의 모양을 미세하게 변경하여 스캔율을 높이는 기술입니다.",
        # 푸터
        "footer_info": "This web app was developed using Streamlit and the Python qrcode library.",
    }
    
    # 메시지 딕셔너리 반환
    if lang == 'ko':
        return messages_ko
    elif lang == 'en':
        return messages_en
    else:
        return messages_ko # 기본값은 한국어


def get_language_options():
    """언어 선택 드롭다운에 사용되는 옵션을 반환합니다."""
    return {
        'ko': {'label': '한국어', 'messages': get_messages('ko')},
        'en': {'label': 'English', 'messages': get_messages('en')}
    }

def get_language_codes():
    """언어 코드 리스트를 반환합니다."""
    return list(get_language_options().keys())

def get_language_labels():
    """언어 라벨 리스트를 반환합니다."""
    return [d['label'] for d in get_language_options().values()]

def get_pattern_options(lang_code):
    """패턴 모양 selectbox에 사용되는 옵션을 반환합니다."""
    messages = get_messages(lang_code)
    return {
        'square': messages['shape_square'],
        'rounded_square': messages['shape_rounded_square'],
        'circle': messages['shape_circle'],
        'diamond': messages['shape_diamond'],
        'star': messages['shape_star'],
        'cross': messages['shape_cross'],
    }
    
def get_error_correction_options(lang_code):
    """오류 복원 selectbox에 사용되는 옵션을 반환합니다."""
    messages = get_messages(lang_code)
    return {
        'low': {'label': messages['error_correction_options_low'], 'value': qrcode.constants.ERROR_CORRECT_L},
        'medium': {'label': messages['error_correction_options_medium'], 'value': qrcode.constants.ERROR_CORRECT_M},
        'quartile': {'label': messages['error_correction_options_quartile'], 'value': qrcode.constants.ERROR_CORRECT_Q},
        'high': {'label': messages['error_correction_options_high'], 'value': qrcode.constants.ERROR_CORRECT_H},
    }

def get_message(lang_code, message_key, *args):
    """지정된 언어의 특정 메시지를 반환합니다."""
    messages = get_messages(lang_code)
    message_template = messages.get(message_key, f"Message not found for '{message_key}'")
    
    try:
        if args:
            return message_template.format(*args)
        else:
            return message_template
    except IndexError:
        return f"Formatting error for '{message_key}'"
