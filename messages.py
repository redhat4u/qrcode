# messages.py

MESSAGES = {
    "ko": {
        "APP_TITLE": "QR 코드 생성기",
        "UI_LANG_SELECT_LABEL": "언어 선택",
        "UI_LANG_SELECT_OPTIONS": ["한국어", "English"],

        "UI_SIDEBAR_DESCRIPTION": """
        이 앱은 텍스트를 QR 코드로 변환해주는 웹 애플리케이션입니다. 
        원하는 텍스트를 입력하고, 다양한 옵션을 설정하여 
        나만의 맞춤형 QR 코드를 만들 수 있습니다.
        """,
        "UI_SIDEBAR_INFO_HEADER": "앱 정보",
        "UI_SIDEBAR_INFO_CONTENT": """
        - **버전:** `1.0.0`
        - **프레임워크:** Streamlit
        - **QR 코드 라이브러리:** `qrcode`
        - **특징:**
            - PNG 및 SVG 포맷 지원
            - 다양한 색상 및 패턴 스타일 선택
            - 오류 복원 레벨 설정
        """,
        "UI_SIDEBAR_DEVELOPER_HEADER": "개발자 정보",
        "UI_SIDEBAR_DEVELOPER_INFO": """
        개발자: 홍길동
        이메일: hong.gildong@example.com
        """,
        
        "UI_HEADER_INPUT_AND_SETTINGS": "⚙️ 입력 및 설정",
        "UI_SUBHEADER_QR_CONTENT": "1. QR 코드에 담을 내용",
        "UI_INFO_MAX_CHARS": "**💡 텍스트는 최대 2,953자까지 가능합니다. (영어 기준)**",
        "UI_TEXT_AREA_LABEL": "내용을 입력하세요. (URL, 텍스트, 이메일 등)",
        "UI_TEXT_AREA_PLACEHOLDER": "예시: https://www.google.com",
        "UI_ERROR_MAX_CHARS": "⚠️ 입력 가능한 최대 글자 수를 초과했습니다. (현재: {char_count}자)",
        "UI_INFO_CURRENT_CHARS": "ℹ️ 현재 글자 수: {char_count}자",
        "UI_BUTTON_CLEAR_TEXT": "입력 내용 지우기",
        "UI_CHECKBOX_STRIP_TEXT": "내용의 양쪽 공백 제거하기",

        "UI_SUBHEADER_QR_SETTINGS": "2. QR 코드 설정",
        "UI_SELECTBOX_ERROR_CORRECTION": "오류 보정 레벨",
        "UI_ERROR_CORRECTION_LEVEL_L": "낮음 (7% 복원)",
        "UI_ERROR_CORRECTION_LEVEL_M": "중간 (15% 복원)",
        "UI_ERROR_CORRECTION_LEVEL_Q": "높음 (25% 복원)",
        "UI_ERROR_CORRECTION_LEVEL_H": "매우 높음 (30% 복원)",
        "UI_NUMBER_INPUT_BOX_SIZE": "각 사각형 크기 (픽셀)",
        "UI_NUMBER_INPUT_BORDER": "테두리 두께 (사각형 개수)",

        "UI_SUBHEADER_COLOR_SETTINGS": "3. 색상 설정",
        "UI_INFO_COLOR_SETTINGS": "**⚠️ SVG 포맷은 이 설정을 무시합니다.**",
        "UI_COLOR_OPTION_DIRECT_INPUT": "직접 16진수 입력 (예: #1A5E31)",
        "UI_SELECTBOX_PATTERN_COLOR": "패턴 색상",
        "UI_SELECTBOX_BG_COLOR": "배경 색상",
        "UI_TEXT_INPUT_PATTERN_COLOR_HEX": "패턴 색상 16진수 입력",
        "UI_TEXT_INPUT_BG_COLOR_HEX": "배경 색상 16진수 입력",
        "UI_TEXT_INPUT_PLACEHOLDER_HEX": "#1A5E31",
        
        "UI_SUBHEADER_PATTERN_STYLE": "4. 패턴 스타일",
        "UI_SELECTBOX_DOT_STYLE": "점 스타일",
        "UI_DOT_STYLE_SQUARE": "사각형",
        "UI_DOT_STYLE_CIRCLE": "원형",
        "UI_DOT_STYLE_ROUNDED": "둥근 사각형",
        "UI_DOT_STYLE_DIAMOND": "마름모",
        
        "UI_SUBHEADER_FILE_SETTINGS": "5. 파일 설정",
        "UI_TEXT_INPUT_FILENAME": "파일 이름",
        "UI_TEXT_INPUT_FILENAME_PLACEHOLDER": "예시: my_awesome_qr_code",
        "UI_BUTTON_CLEAR_FILENAME": "파일명 지우기",
        "UI_SELECTBOX_FILE_FORMAT": "파일 형식",
        "UI_FILE_FORMAT_PNG": "PNG",
        "UI_FILE_FORMAT_SVG": "SVG",

        "UI_HEADER_PREVIEW_AND_GENERATE": "✨ 미리보기 & 생성",
        "UI_BUTTON_GENERATE_QR": "⚡ QR 코드 생성",
        "UI_ERROR_QR_DATA_MISSING": "⚠️ QR 코드로 만들 내용이 없습니다.",
        "UI_ERROR_PATTERN_COLOR_HEX_MISSING": "⚠️ 패턴 색상 16진수 값을 입력해주세요.",
        "UI_ERROR_INVALID_PATTERN_COLOR": "⚠️ 패턴 색상 16진수 값이 올바르지 않습니다.",
        "UI_ERROR_BG_COLOR_HEX_MISSING": "⚠️ 배경 색상 16진수 값을 입력해주세요.",
        "UI_ERROR_INVALID_BG_COLOR": "⚠️ 배경 색상 16진수 값이 올바르지 않습니다.",
        "UI_ERROR_SAME_COLOR": "⚠️ 패턴 색상과 배경 색상이 동일합니다. 다른 색상을 선택해주세요.",
        "UI_WARNING_PATTERN_COLOR_INPUT": "⚠️ 패턴 색상 16진수 값을 입력하세요.",
        "UI_WARNING_BG_COLOR_INPUT": "⚠️ 배경 색상 16진수 값을 입력하세요.",
        "UI_WARNING_INVALID_COLOR_HEX": "⚠️ 유효하지 않은 16진수 색상 값입니다.",
        "UI_WARNING_SAME_COLOR": "⚠️ 패턴과 배경 색상이 같으면 QR 코드가 보이지 않습니다.",
        "UI_INFO_QR_GENERATION_GUIDE": "💡 왼쪽에서 내용을 입력하고 '⚡ QR 코드 생성' 버튼을 누르면 여기에 미리보기가 나타납니다.",

        "UI_SUBHEADER_QR_PREVIEW": "QR 코드 미리보기",
        "UI_PREVIEW_IMAGE_CAPTION": "생성된 QR 코드",
        "UI_INFO_QR_CODE_INFO_TITLE": "QR 코드 상세 정보",
        "UI_INFO_QR_VERSION": "버전",
        "UI_INFO_QR_CELL_COUNT": "셀 개수",
        "UI_INFO_QR_IMAGE_SIZE_REFERENCE": "예상 이미지 크기",
        "UI_INFO_QR_PATTERN_COLOR": "패턴 색상",
        "UI_INFO_QR_BG_COLOR": "배경 색상",
        "UI_INFO_QR_IMAGE_SIZE_FORMULA": "(이미지 크기는 QR 버전, 사각형 크기, 테두리 두께에 따라 달라집니다.)",

        "UI_SUBHEADER_DOWNLOAD": "📥 QR 코드 다운로드",
        "UI_DOWNLOAD_LABEL": "💾 QR 코드 다운로드",
        "UI_DOWNLOAD_HELP": "클릭하여 QR 코드를 저장합니다.",
        "UI_BUTTON_RESET": "초기화",
        "UI_DOWNLOAD_FILENAME_LABEL": "생성 파일명",
    },
    "en": {
        "APP_TITLE": "QR Code Generator",
        "UI_LANG_SELECT_LABEL": "Select Language",
        "UI_LANG_SELECT_OPTIONS": ["한국어", "English"],

        "UI_SIDEBAR_DESCRIPTION": """
        This web application allows you to convert text into a QR code.
        On the left panel, you can input your desired text and customize
        various options to create your own unique QR code.
        """,
        "UI_SIDEBAR_INFO_HEADER": "App Info",
        "UI_SIDEBAR_INFO_CONTENT": """
        - **Version:** `1.0.0`
        - **Framework:** Streamlit
        - **QR Code Library:** `qrcode`
        - **Features:**
            - Supports PNG and SVG formats
            - Various color and pattern styles
            - Error correction level settings
        """,
        "UI_SIDEBAR_DEVELOPER_HEADER": "Developer Info",
        "UI_SIDEBAR_DEVELOPER_INFO": """
        Developer: John Doe
        Email: john.doe@example.com
        """,
        
        "UI_HEADER_INPUT_AND_SETTINGS": "⚙️ Input & Settings",
        "UI_SUBHEADER_QR_CONTENT": "1. QR Code Content",
        "UI_INFO_MAX_CHARS": "**💡 Maximum text length is 2,953 characters. (English)**",
        "UI_TEXT_AREA_LABEL": "Enter your content (URL, text, email, etc.)",
        "UI_TEXT_AREA_PLACEHOLDER": "Example: https://www.google.com",
        "UI_ERROR_MAX_CHARS": "⚠️ Maximum character limit exceeded. (Current: {char_count} chars)",
        "UI_INFO_CURRENT_CHARS": "ℹ️ Current character count: {char_count} chars",
        "UI_BUTTON_CLEAR_TEXT": "Clear Text",
        "UI_CHECKBOX_STRIP_TEXT": "Strip whitespace from content",
        
        "UI_SUBHEADER_QR_SETTINGS": "2. QR Code Settings",
        "UI_SELECTBOX_ERROR_CORRECTION": "Error Correction Level",
        "UI_ERROR_CORRECTION_LEVEL_L": "Low (7% restore)",
        "UI_ERROR_CORRECTION_LEVEL_M": "Medium (15% restore)",
        "UI_ERROR_CORRECTION_LEVEL_Q": "High (25% restore)",
        "UI_ERROR_CORRECTION_LEVEL_H": "Very High (30% restore)",
        "UI_NUMBER_INPUT_BOX_SIZE": "Box Size (pixels)",
        "UI_NUMBER_INPUT_BORDER": "Border Thickness (number of boxes)",

        "UI_SUBHEADER_COLOR_SETTINGS": "3. Color Settings",
        "UI_INFO_COLOR_SETTINGS": "**⚠️ This setting is ignored for SVG format.**",
        "UI_COLOR_OPTION_DIRECT_INPUT": "Direct Hex Input (e.g., #1A5E31)",
        "UI_SELECTBOX_PATTERN_COLOR": "Pattern Color",
        "UI_SELECTBOX_BG_COLOR": "Background Color",
        "UI_TEXT_INPUT_PATTERN_COLOR_HEX": "Pattern color hex input",
        "UI_TEXT_INPUT_BG_COLOR_HEX": "Background color hex input",
        "UI_TEXT_INPUT_PLACEHOLDER_HEX": "#1A5E31",
        
        "UI_SUBHEADER_PATTERN_STYLE": "4. Pattern Style",
        "UI_SELECTBOX_DOT_STYLE": "Dot Style",
        "UI_DOT_STYLE_SQUARE": "Square",
        "UI_DOT_STYLE_CIRCLE": "Circle",
        "UI_DOT_STYLE_ROUNDED": "Rounded Square",
        "UI_DOT_STYLE_DIAMOND": "Diamond",
        
        "UI_SUBHEADER_FILE_SETTINGS": "5. File Settings",
        "UI_TEXT_INPUT_FILENAME": "File Name",
        "UI_TEXT_INPUT_FILENAME_PLACEHOLDER": "Example: my_awesome_qr_code",
        "UI_BUTTON_CLEAR_FILENAME": "Clear File Name",
        "UI_SELECTBOX_FILE_FORMAT": "File Format",
        "UI_FILE_FORMAT_PNG": "PNG",
        "UI_FILE_FORMAT_SVG": "SVG",
        
        "UI_HEADER_PREVIEW_AND_GENERATE": "✨ Preview & Generate",
        "UI_BUTTON_GENERATE_QR": "⚡ Generate QR Code",
        "UI_ERROR_QR_DATA_MISSING": "⚠️ QR code content is missing.",
        "UI_ERROR_PATTERN_COLOR_HEX_MISSING": "⚠️ Please enter a hex value for the pattern color.",
        "UI_ERROR_INVALID_PATTERN_COLOR": "⚠️ Invalid hex value for the pattern color.",
        "UI_ERROR_BG_COLOR_HEX_MISSING": "⚠️ Please enter a hex value for the background color.",
        "UI_ERROR_INVALID_BG_COLOR": "⚠️ Invalid hex value for the background color.",
        "UI_ERROR_SAME_COLOR": "⚠️ Pattern and background colors are the same. Please choose different colors.",
        "UI_WARNING_PATTERN_COLOR_INPUT": "⚠️ Please enter a hex value for the pattern color.",
        "UI_WARNING_BG_COLOR_INPUT": "⚠️ Please enter a hex value for the background color.",
        "UI_WARNING_INVALID_COLOR_HEX": "⚠️ Invalid hex color value.",
        "UI_WARNING_SAME_COLOR": "⚠️ QR code will be invisible if pattern and background colors are the same.",
        "UI_INFO_QR_GENERATION_GUIDE": "💡 Enter content on the left and click '⚡ Generate QR Code' to see a preview here.",

        "UI_SUBHEADER_QR_PREVIEW": "QR Code Preview",
        "UI_PREVIEW_IMAGE_CAPTION": "Generated QR Code",
        "UI_INFO_QR_CODE_INFO_TITLE": "QR Code Details",
        "UI_INFO_QR_VERSION": "Version",
        "UI_INFO_QR_CELL_COUNT": "Cell Count",
        "UI_INFO_QR_IMAGE_SIZE_REFERENCE": "Approximate Image Size",
        "UI_INFO_QR_PATTERN_COLOR": "Pattern Color",
        "UI_INFO_QR_BG_COLOR": "Background Color",
        "UI_INFO_QR_IMAGE_SIZE_FORMULA": "(Image size depends on QR version, box size, and border thickness.)",
        
        "UI_SUBHEADER_DOWNLOAD": "📥 Download QR Code",
        "UI_DOWNLOAD_LABEL": "💾 Download QR Code",
        "UI_DOWNLOAD_HELP": "Click to save the QR code.",
        "UI_BUTTON_RESET": "Reset",
        "UI_DOWNLOAD_FILENAME_LABEL": "Generated Filename",
    }
}

def get_message(key):
    # This is a placeholder function, you'll need a way to determine the current language
    # For now, let's assume 'ko' is the default.
    return MESSAGES.get("ko").get(key, "Message not found")

def get_current_language():
    # This function is not used in the final version but kept for consistency
    return "ko"
    
