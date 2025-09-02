# 이 파일은 앱 전반에 사용되는 모든 문자열 메시지를 정의합니다.
# messages.py

# =========================================================
# 다국어 지원을 위한 딕셔너리
# =========================================================

import streamlit as st

# 언어별 메시지 딕셔너리
MESSAGES = {
    'ko': {
        # qrcode_web.py
        'APP_TITLE': "QR 코드 생성기",
        'APP_MAIN_HEADER': "🔲 QR 코드 생성기",
        'APP_RESET_BUTTON_LABEL': "🔄 전체 초기화",
        'APP_RESET_BUTTON_HELP': "모든 내용을 초기화 합니다.",
        # ui_input_and_settings.py
        'UI_HEADER_INPUT_AND_SETTINGS': "⚙️ 입력 및 설정",
        'UI_SUBHEADER_QR_CONTENT': "📝 QR 코드 내용",
        'UI_INFO_QR_DATA_LIMIT': "최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.",
        'UI_TEXT_AREA_LABEL': "QR 코드로 생성할 내용을 입력해 주세요",
        'UI_TEXT_AREA_PLACEHOLDER': "이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.",
        'UI_CAPTION_CHAR_COUNT_ZERO': "현재 입력된 총 문자 수: 0",
        'UI_BUTTON_DELETE_TEXT_LABEL': "🗑️ 입력 내용 삭제",
        'UI_BUTTON_DELETE_TEXT_HELP': "입력한 내용을 전부 삭제합니다 (파일명은 유지)",
        'UI_CHECKBOX_STRIP_TEXT': "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        'UI_SUBHEADER_QR_SETTINGS': "🛠️ QR 코드 설정",
        'UI_BOX_SIZE_LABEL': "QR 코드 1개의 사각 cell 크기 (px)",
        'UI_BORDER_LABEL': "QR 코드 테두리/여백",
        'UI_ERROR_CORRECTION_LABEL': "오류 보정 레벨",
        'UI_MASK_PATTERN_LABEL': "마스크 패턴 선택 (0~7)",
        'UI_SUBHEADER_COLOR_SETTINGS': "🛠️ 색상 설정",
        'UI_WARNING_SVG_COLOR': "⚠️ SVG 파일은 벡터 형식이므로 원하는 색상을 선택할 수 없습니다. 다양한 색상을 원한다면 'PNG' 형식을 선택하세요.",
        'UI_SELECTBOX_PATTERN_COLOR_LABEL': "패턴 색상",
        'UI_SELECTBOX_BG_COLOR_LABEL': "배경 색상",
        'UI_COLOR_OPTION_DIRECT_INPUT': "<직접 입력>",
        'UI_COLOR_INPUT_HELP': "원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.",
        'UI_COLOR_INPUT_CAPTION': "예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)",
        'UI_TEXT_INPUT_PATTERN_COLOR_LABEL': "패턴 색상 HEX 값",
        'UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER': "예: #000000",
        'UI_TEXT_INPUT_BG_COLOR_LABEL': "배경 색상 HEX 값",
        'UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER': "예: #FFFFFF",
        'UI_SUBHEADER_DOT_STYLE': "🛠️ 패턴 모양",
        'UI_SELECTBOX_DOT_STYLE_LABEL': "패턴 모양 선택",
        'UI_DOT_STYLE_SQUARE': "사각형",
        'UI_DOT_STYLE_CIRCLE': "원형",
        'UI_DOT_STYLE_ROUNDED': "둥근 사각",
        'UI_DOT_STYLE_DIAMOND': "마름모",
        'UI_SUBHEADER_FILE_SETTINGS': "🛠️ 파일 설정",
        'UI_TEXT_INPUT_FILENAME_LABEL': "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)",
        'UI_TEXT_INPUT_FILENAME_PLACEHOLDER': "이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
        'UI_BUTTON_DELETE_FILENAME_LABEL': "🗑️ 파일명 삭제",
        'UI_BUTTON_DELETE_FILENAME_HELP': "입력한 파일명을 삭제합니다",
        'UI_RADIO_FILE_FORMAT': "파일 형식 선택",
        'UI_TEXT_CHAR_COUNT_OVER': "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)",
        'UI_TEXT_CHAR_COUNT_NEAR': "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 문자 수에 근접)",
        'UI_TEXT_CHAR_COUNT_OK': "✅ 현재 입력된 총 문자 수: **{char_count}**",
        # ui_preview_and_download.py
        'UI_HEADER_PREVIEW_AND_GENERATE': "👀 미리보기 및 생성",
        'UI_CAPTION_QR_DATA_EMPTY': "QR 코드 내용을 입력하면 아래에 생성될 QR 코드가 나타납니다.",
        'UI_BUTTON_GENERATE': "⚡ QR 코드 생성",
        'UI_ERROR_QR_DATA_EMPTY': "⚠️ 생성할 QR 코드 내용을 입력해 주세요.",
        'UI_ERROR_HEX_PATTERN_EMPTY': "⚠️ 패턴 색의 HEX 값을 입력해 주세요.",
        'UI_ERROR_HEX_PATTERN_INVALID': "⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
        'UI_ERROR_HEX_BG_EMPTY': "⚠️ 배경 색의 HEX 값을 입력해 주세요.",
        'UI_ERROR_HEX_BG_INVALID': "⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
        'UI_ERROR_COLORS_SAME': "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.",
        'UI_SUCCESS_MESSAGE': """
            ✅ QR 코드 생성 완료!!<br>
            반드시 파일명을 확인하시고, 화면 아래의 [💾 QR 코드 다운로드] 버튼을 클릭하세요.
            """,
        'UI_CAPTION_QR_PREVIEW_ERROR': "색상 설정이 유효하지 않습니다. 미리보기를 표시할 수 없습니다.",
        'UI_SUBHEADER_PREVIEW': "📱 QR 코드 미리보기",
        'UI_IMAGE_CAPTION_PREVIEW': "생성된 QR 코드",
        'UI_INFO_QR_INFO': """
            **QR 코드 정보**
            - QR 버전: {version}
            - 가로/세로 각 cell 개수: {modules}개
            - 이미지 크기 (참고): {size} px
            - 패턴 색상: {pattern_color}
            - 배경 색상: {bg_color}
            - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
            """,
        'UI_SUBHEADER_DOWNLOAD': "📥 다운로드",
        'UI_BUTTON_DOWNLOAD': "💾 QR 코드 다운로드",
        'UI_BUTTON_DOWNLOAD_HELP': "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다.",
        'UI_DOWNLOAD_FILENAME_LABEL': "📄 다운로드 파일명: ",
        'UI_SUCCESS_DOWNLOAD_MESSAGE': """
            ✅ QR 코드 다운로드 완료!!<br>
            휴대폰은 'Download' 폴더에 저장됩니다.
            """,
        'UI_PREVIEW_READY_MESSAGE': """
            ✅ 현재 입력된 내용으로 QR 코드를 미리 표현해 보았습니다.<br>
            아래의 QR 코드가 맘에 드시면, 위의 [⚡ QR 코드 생성] 버튼을 클릭하세요.
            """,
        'UI_INFO_ENTER_QR_DATA': "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다.",
        # sidebar.py
        'SIDEBAR_HEADER_HOWTO': "📖 사용 방법",
        'SIDEBAR_GUIDE_HOWTO': """
            1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
            2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
            3. **패턴 모양**에서 QR 코드 점의 모양을 선택하세요 (SVG 형식은 사각형만 가능합니다)
            4. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
            5. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요
            6. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
            """,
        'SIDEBAR_HEADER_USAGE_TIPS': "💡 용도별 QR 코드 생성 팁",
        'SIDEBAR_GUIDE_USAGE_TIPS': """
            - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
            - **웹사이트**: `https://www.example.com`
            - **이메일**: `mailto:user@example.com`
            - **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
            - **전화번호**: `tel:type=CELL:+82 10-1234-5678`
            - **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
            - **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
            - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
            """,
        'SIDEBAR_HEADER_SETTINGS_GUIDE': "⚙️ 설정 가이드",
        'SIDEBAR_GUIDE_ERROR_CORRECTION': "**오류 보정 레벨:**",
        'SIDEBAR_GUIDE_ERROR_CORRECTION_DESC': """
            - **Low (7%)**: 손상되지 않는 환경
            - **Medium (15%)**: 일반적인 사용
            - **Quartile (25%)**: 약간의 손상 가능
            - **High (30%)**: 로고 삽입, 손상이 잦은 환경
            """,
        'SIDEBAR_GUIDE_MASK_PATTERN': "**마스크 패턴:**",
        'SIDEBAR_GUIDE_MASK_PATTERN_DESC': """
            - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
            """,
        'SIDEBAR_GUIDE_DOT_STYLE': "**패턴 모양:**",
        'SIDEBAR_GUIDE_DOT_STYLE_DESC': """
            - 사각형, 둥근 사각, 원형, 마름모 중 선택
            - **SVG** 파일 형식 선택 시에는 **사각형**만 지원합니다.
            """,
        'SIDEBAR_GUIDE_COLOR_INPUT': "**색상 입력:**",
        'SIDEBAR_GUIDE_COLOR_INPUT_DESC': """
            - **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
            - **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
            - **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.
            """,
        # footer.py
        'FOOTER_MESSAGE': "© 2025 QR 코드 생성기 | Streamlit으로 제작 | 제작: 류종훈(redhat4u@gmail.com)"
    },
    'en': {
        # qrcode_web.py
        'APP_TITLE': "QR Code Generator",
        'APP_MAIN_HEADER': "🔲 QR Code Generator",
        'APP_RESET_BUTTON_LABEL': "🔄 Reset All",
        'APP_RESET_BUTTON_HELP': "Resets all inputs and settings.",
        # ui_input_and_settings.py
        'UI_HEADER_INPUT_AND_SETTINGS': "⚙️ Input and Settings",
        'UI_SUBHEADER_QR_CONTENT': "📝 QR Code Content",
        'UI_INFO_QR_DATA_LIMIT': "The maximum number of characters that can be entered is approximately 2,400 to 2,900, depending on the type.",
        'UI_TEXT_AREA_LABEL': "Enter the content to be generated into a QR code",
        'UI_TEXT_AREA_PLACEHOLDER': "Enter the content to be generated into a QR code here.\nCopy/paste is available.",
        'UI_CAPTION_CHAR_COUNT_ZERO': "Total characters entered: 0",
        'UI_BUTTON_DELETE_TEXT_LABEL': "🗑️ Clear Content",
        'UI_BUTTON_DELETE_TEXT_HELP': "Clears all entered content (filename is preserved)",
        'UI_CHECKBOX_STRIP_TEXT': "Remove all spaces/newlines after the last character",
        'UI_SUBHEADER_QR_SETTINGS': "🛠️ QR Code Settings",
        'UI_BOX_SIZE_LABEL': "QR code single square cell size (px)",
        'UI_BORDER_LABEL': "QR code border/margin",
        'UI_ERROR_CORRECTION_LABEL': "Error Correction Level",
        'UI_MASK_PATTERN_LABEL': "Mask Pattern (0~7)",
        'UI_SUBHEADER_COLOR_SETTINGS': "🛠️ Color Settings",
        'UI_WARNING_SVG_COLOR': "⚠️ SVG files are vector graphics and do not support custom colors. Choose 'PNG' for various colors.",
        'UI_SELECTBOX_PATTERN_COLOR_LABEL': "Pattern Color",
        'UI_SELECTBOX_BG_COLOR_LABEL': "Background Color",
        'UI_COLOR_OPTION_DIRECT_INPUT': "<Direct Input>",
        'UI_COLOR_INPUT_HELP': "If your desired color is not in the list, enter the **HEX code** below.",
        'UI_COLOR_INPUT_CAPTION': "Ex: #FF0000 (Red), #00FF00 (Green), #0000FF (Blue)",
        'UI_TEXT_INPUT_PATTERN_COLOR_LABEL': "Pattern Color HEX Value",
        'UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER': "Ex: #000000",
        'UI_TEXT_INPUT_BG_COLOR_LABEL': "Background Color HEX Value",
        'UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER': "Ex: #FFFFFF",
        'UI_SUBHEADER_DOT_STYLE': "🛠️ Pattern Shape",
        'UI_SELECTBOX_DOT_STYLE_LABEL': "Select Pattern Shape",
        'UI_DOT_STYLE_SQUARE': "Square",
        'UI_DOT_STYLE_CIRCLE': "Circle",
        'UI_DOT_STYLE_ROUNDED': "Rounded Square",
        'UI_DOT_STYLE_DIAMOND': "Diamond",
        'UI_SUBHEADER_FILE_SETTINGS': "🛠️ File Settings",
        'UI_TEXT_INPUT_FILENAME_LABEL': "Download Filename (without extension)",
        'UI_TEXT_INPUT_FILENAME_PLACEHOLDER': "Enter the filename here (auto-generated if empty)",
        'UI_BUTTON_DELETE_FILENAME_LABEL': "🗑️ Clear Filename",
        'UI_BUTTON_DELETE_FILENAME_HELP': "Clears the entered filename",
        'UI_RADIO_FILE_FORMAT': "File Format",
        'UI_TEXT_CHAR_COUNT_OVER': "⚠️ Total characters entered: **{char_count}** (Exceeds recommended limit)",
        'UI_TEXT_CHAR_COUNT_NEAR': "⚠️ Total characters entered: **{char_count}** (Approaching recommended limit)",
        'UI_TEXT_CHAR_COUNT_OK': "✅ Total characters entered: **{char_count}**",
        # ui_preview_and_download.py
        'UI_HEADER_PREVIEW_AND_GENERATE': "👀 Preview and Generate",
        'UI_CAPTION_QR_DATA_EMPTY': "Enter QR code content to see a preview of the generated QR code.",
        'UI_BUTTON_GENERATE': "⚡ Generate QR Code",
        'UI_ERROR_QR_DATA_EMPTY': "⚠️ Please enter the content for the QR code.",
        'UI_ERROR_HEX_PATTERN_EMPTY': "⚠️ Please enter a HEX value for the pattern color.",
        'UI_ERROR_HEX_PATTERN_INVALID': "⚠️ The entered HEX value for the pattern color is not a valid color. Please check again.",
        'UI_ERROR_HEX_BG_EMPTY': "⚠️ Please enter a HEX value for the background color.",
        'UI_ERROR_HEX_BG_INVALID': "⚠️ The entered HEX value for the background color is not a valid color. Please check again.",
        'UI_ERROR_COLORS_SAME': "⚠️ Pattern and background colors cannot be the same.",
        'UI_SUCCESS_MESSAGE': """
            ✅ QR Code generated successfully!!<br>
            Please confirm the filename and click the [💾 Download QR Code] button below.
            """,
        'UI_CAPTION_QR_PREVIEW_ERROR': "Color settings are invalid. Cannot display preview.",
        'UI_SUBHEADER_PREVIEW': "📱 QR Code Preview",
        'UI_IMAGE_CAPTION_PREVIEW': "Generated QR Code",
        'UI_INFO_QR_INFO': """
            **QR Code Information**
            - QR Version: {version}
            - Grid Cells (W/H): {modules} cells
            - Image Size (approx.): {size} px
            - Pattern Color: {pattern_color}
            - Background Color: {bg_color}
            - Image Size = (Grid Cells + Total Border) × Cell Size
            """,
        'UI_SUBHEADER_DOWNLOAD': "📥 Download",
        'UI_BUTTON_DOWNLOAD': "💾 Download QR Code",
        'UI_BUTTON_DOWNLOAD_HELP': "Files will be saved in your 'Download' folder.",
        'UI_DOWNLOAD_FILENAME_LABEL': "📄 Download Filename: ",
        'UI_SUCCESS_DOWNLOAD_MESSAGE': """
            ✅ QR Code downloaded successfully!!<br>
            The file is saved in your 'Download' folder.
            """,
        'UI_PREVIEW_READY_MESSAGE': """
            ✅ A preview of the QR code has been generated with the current input.<br>
            If you like the QR code below, click the [⚡ Generate QR Code] button above.
            """,
        'UI_INFO_ENTER_QR_DATA': "Enter QR code content to see a preview of the generated QR code.",
        # sidebar.py
        'SIDEBAR_HEADER_HOWTO': "📖 How to Use",
        'SIDEBAR_GUIDE_HOWTO': """
            1. Enter text in the **QR Code Content** area.
            2. Adjust the size and error correction level in **QR Code Settings**.
            3. Select the pattern shape in **Pattern Shape** (SVG format only supports square).
            4. Choose pattern and background colors in **Color Settings** (SVG only supports default colors).
            5. Select the file format (PNG/SVG) and specify a filename in **File Settings**.
            6. Click the **Generate QR Code** button to download the final file.
            """,
        'SIDEBAR_HEADER_USAGE_TIPS': "💡 Usage Tips",
        'SIDEBAR_GUIDE_USAGE_TIPS': """
            - **Text**: `Enter your text here`
            - **Website**: `https://www.example.com`
            - **Email**: `mailto:user@example.com`
            - **Email (with subject/body)**: `mailto:user1@example.com,user2@example.com?subject=Subject&body=Message`
            - **Phone**: `tel:type=CELL:+82 10-1234-5678`
            - **SMS (number only)**: `sms:type=CELL:+82 10-1234-5678`
            - **SMS (with message)**: `sms:type=CELL:+82 10-1234-5678?body=Message`
            - **WiFi**: `WIFI:T:WPA;S:Network_Name(SSID);P:Password;H:false;;`
            """,
        'SIDEBAR_HEADER_SETTINGS_GUIDE': "⚙️ Settings Guide",
        'SIDEBAR_GUIDE_ERROR_CORRECTION': "**Error Correction Level:**",
        'SIDEBAR_GUIDE_ERROR_CORRECTION_DESC': """
            - **Low (7%)**: For non-damaging environments.
            - **Medium (15%)**: For general use.
            - **Quartile (25%)**: For environments with minor damage.
            - **High (30%)**: For environments with frequent damage or for inserting a logo.
            """,
        'SIDEBAR_GUIDE_MASK_PATTERN': "**Mask Pattern:**",
        'SIDEBAR_GUIDE_MASK_PATTERN_DESC': """
            - Select from 0-7 (the pattern changes with the number, even for the same content).
            """,
        'SIDEBAR_GUIDE_DOT_STYLE': "**Pattern Shape:**",
        'SIDEBAR_GUIDE_DOT_STYLE_DESC': """
            - Choose from Square, Rounded Square, Circle, Diamond.
            - Only **Square** is supported for **SVG** file format.
            """,
        'SIDEBAR_GUIDE_COLOR_INPUT': "**Color Input:**",
        'SIDEBAR_GUIDE_COLOR_INPUT_DESC': """
            - **Direct Input**: You can enter a HEX code for colors not in the list.
            - **Error Messages**: Color input is validated to show a warning if the field is empty or the value is invalid.
            - **SVG** format only supports black patterns on a white background.
            """,
        # footer.py
        'FOOTER_MESSAGE': "© 2025 QR Code Generator | Built with Streamlit | Developer: Ryu Jong-hun (redhat4u@gmail.com)"
    }
}

# 언어 선택 함수
def get_message(key):
    """현재 언어에 맞는 메시지를 반환합니다."""
    # 세션 상태에 current_lang이 없으면 기본값 'ko'를 사용
    lang = st.session_state.get('current_lang', 'ko')
    return MESSAGES[lang].get(key, 'Key Not Found')
  
