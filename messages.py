# messages.py

import streamlit as st

MESSAGES = {
    "ko": {
        "APP_TITLE": "QR 코드 생성기",
        "UI_LANG_SELECT_LABEL": "언어 선택(Select Language)",
        "UI_LANG_SELECT_OPTIONS": ["한국어", "English"],

        "UI_SIDEBAR_HEADER_GUIDE": "📖 사용 방법",
        "UI_SIDEBAR_GUIDE_CONTENT": """
        1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
        2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
        3. **패턴 모양**에서 QR 코드 점의 모양을 선택하세요 (SVG 형식은 사각형만 가능합니다)
        4. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
        5. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요
        6. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
        """,
        "UI_SIDEBAR_HEADER_TIPS": "💡 용도별 QR 코드 생성 팁",
        "UI_SIDEBAR_TIPS_CONTENT": """
        - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
        - **웹사이트**: `https://www.example.com`
        - **이메일**: `mailto:user@example.com`
        - **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
        - **전화번호**: `tel:type=CELL:+82 10-1234-5678`
        - **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
        - **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
        - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
        """,
        "UI_SIDEBAR_HEADER_SETTINGS_GUIDE": "⚙️ 설정 가이드",
        "UI_SIDEBAR_SETTINGS_GUIDE_CONTENT": """
        **오류 보정 레벨:**
        - **Low (7%)**: 손상되지 않는 환경
        - **Medium (15%)**: 일반적인 사용
        - **Quartile (25%)**: 약간의 손상 가능
        - **High (30%)**: 로고 삽입, 손상이 잦은 환경
        
        **마스크 패턴:**
        - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
        
        **패턴 모양:**
        - 사각형, 둥근 사각, 원형, 마름모 중 선택
        - **SVG** 파일 형식 선택 시에는 **사각형**만 지원합니다.
        
        **색상 입력:**
        - **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
        - **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
        - **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.
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
        "UI_INFO_QR_GENERATION_GUIDE": "💡 QR 코드 내용을 입력하고 위의 [⚡ QR 코드 생성] 버튼을 누르면, 아래에 미리보기가 나타납니다.",

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
        "UI_FOOTER": "© 2025 QR 코드 생성기 | Streamlit으로 제작 | 제작: 류종훈(redhat4u@gmail.com)"
    },
    "en": {
        "APP_TITLE": "QR Code Generator",
        "UI_LANG_SELECT_LABEL": "Select Language",
        "UI_LANG_SELECT_OPTIONS": ["한국어", "English"],

        "UI_SIDEBAR_HEADER_GUIDE": "📖 How to Use",
        "UI_SIDEBAR_GUIDE_CONTENT": """
        1. In the **QR Code Content** area, enter the text you want to convert.
        2. In **QR Code Settings**, adjust the size and error correction level.
        3. In **Pattern Shape**, select the shape of the QR code dots (SVG format only supports squares).
        4. In **Color Settings**, select the pattern and background colors (SVG format only supports default colors).
        5. In **File Settings**, choose the desired file format (PNG/SVG) and specify a filename.
        6. Click the **Generate QR Code** button to download the final file.
        """,
        "UI_SIDEBAR_HEADER_TIPS": "💡 Tips for Creating QR Codes",
        "UI_SIDEBAR_TIPS_CONTENT": """
        - **Text**: `Enter text you want to generate a QR code for`
        - **Website**: `https://www.google.com`
        - **Email**: `mailto:user@example.com`
        - **Email (with subject, body, multiple recipients)**: `mailto:user1@example.com,user2@example.com?subject=Subject&body=Message content`
        - **Phone Number**: `tel:type=CELL:+82 10-1234-5678`
        - **SMS (number only)**: `sms:type=CELL:+82 10-1234-5678`
        - **SMS (with message)**: `sms:type=CELL:+82 10-1234-5678?body=Message content`
        - **WiFi**: `WIFI:T:WPA;S:Network Name(SSID);P:Password;H:false;;`
        """,
        "UI_SIDEBAR_HEADER_SETTINGS_GUIDE": "⚙️ Settings Guide",
        "UI_SIDEBAR_SETTINGS_GUIDE_CONTENT": """
        **Error Correction Level:**
        - **Low (7%)**: For environments with no damage
        - **Medium (15%)**: For general use
        - **Quartile (25%)**: For slight damage
        - **High (30%)**: For inserting a logo or in environments with frequent damage
        
        **Mask Pattern:**
        - Select between 0-7 (the pattern changes for the same content depending on the number)
        
        **Pattern Shape:**
        - Select from Square, Rounded Square, Circle, or Diamond
        - **SVG** file format only supports **squares**.
        
        **Color Input:**
        - **Direct Input**: You can directly enter HEX codes for colors not on the list.
        - **Error Message**: When you enter a color, a validation check will show a warning if the input field is empty or if the color value is incorrect.
        - **SVG** file format only supports black for the pattern and white for the background.
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
        "UI_BUTTON_RESET": "초기화",
        "UI_DOWNLOAD_FILENAME_LABEL": "생성 파일명",
        "UI_FOOTER": "© 2025 QR Code Generator | Built with Streamlit | Developed by JongHoon Ryu (redhat4u@gmail.com)"
    }
}

def get_message(key):
    """
    Retrieves the correct message based on the current language selected in the session state.
    """
    if 'language_select' not in st.session_state:
        # Initial setup if not already in session state
        st.session_state.language_select = MESSAGES['ko']['UI_LANG_SELECT_OPTIONS'][0]
    
    current_lang_code = 'ko' if st.session_state.language_select == '한국어' else 'en'
    
    return MESSAGES.get(current_lang_code, {}).get(key, f"Missing message for key: {key}")
