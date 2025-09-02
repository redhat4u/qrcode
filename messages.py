# 이 파일은 앱에서 사용되는 모든 사용자 인터페이스(UI) 메시지를 정의합니다.
# messages.py

import streamlit as st
import qrcode

# 모든 언어의 메시지를 포함하는 사전
MESSAGES = {
    'ko': {
        # 앱 전체
        'APP_TITLE': 'QR 코드 생성기',
        'FOOTER_MESSAGE': '© 2025 QR 코드 생성기 | Streamlit으로 제작 | 제작: 류종훈(redhat4u@gmail.com)',
        
        # 사이드바
        'SIDEBAR_HEADER_LANG': '🌐 언어 선택',
        'LANG_KO': '한국어',
        'LANG_EN': '영어',
        'SELECTBOX_LANG_LABEL': '언어를 선택하세요',
        'SIDEBAR_HEADER_HOWTO': '📖 사용 방법',
        'SIDEBAR_HOWTO_CONTENT': '''
        1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
        2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
        3. **패턴 모양**에서 QR 코드 점의 모양을 선택하세요 (SVG 형식은 사각형만 가능합니다)
        4. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
        5. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요
        6. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
        ''',
        'SIDEBAR_HEADER_TIPS': '💡 용도별 QR 코드 생성 팁',
        'SIDEBAR_TIPS_CONTENT': '''
        - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
        - **웹사이트**: `https://www.example.com`
        - **이메일**: `mailto:user@example.com`
        - **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
        - **전화번호**: `tel:type=CELL:+82 10-1234-5678`
        - **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
        - **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
        - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
        ''',
        'SIDEBAR_HEADER_TECH_INFO': '⚙️ 기술 정보',
        'SIDEBAR_TECH_INFO_CONTENT': '''
        - **제작**: 류종훈
        - **라이브러리**: Streamlit, qrcode, pillow
        - **호스팅**: Streamlit Community Cloud
        - **버전**: 1.0.0
        ''',

        # 입력 및 설정 UI
        'UI_HEADER_INPUT_AND_SETTINGS': '⚙️ 입력 및 설정',
        'UI_SUBHEADER_QR_CONTENT': '📝 QR 코드 내용',
        'UI_INFO_QR_DATA_LIMIT': '최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.',
        'UI_TEXT_AREA_LABEL': 'QR 코드로 생성할 내용을 입력해 주세요',
        'UI_TEXT_AREA_PLACEHOLDER': '이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.',
        'UI_TEXT_CHAR_COUNT_OVER': '⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)',
        'UI_TEXT_CHAR_COUNT_NEAR': '⚠️ 현재 입력된 총 문자 수: **{char_count}** (문자 수가 많아질수록 오류 보정률이 떨어집니다)',
        'UI_TEXT_CHAR_COUNT_OK': '✅ 현재 입력된 총 문자 수: **{char_count}**',
        'UI_CAPTION_CHAR_COUNT_ZERO': '내용을 입력해주세요',
        'UI_BUTTON_DELETE_TEXT_LABEL': '내용 지우기',
        'UI_BUTTON_DELETE_TEXT_HELP': 'QR 코드 입력 내용을 모두 지웁니다.',
        'UI_CHECKBOX_STRIP_TEXT': '입력 내용 앞뒤 공백 제거하기',

        'UI_SUBHEADER_DOT_STYLE': '🛠️ 패턴 모양',
        'UI_SELECTBOX_DOT_STYLE_LABEL': '패턴 모양 선택',
        'UI_DOT_STYLE_SQUARE': '사각형',
        'UI_DOT_STYLE_CIRCLE': '원형',
        'UI_DOT_STYLE_ROUNDED': '둥근 사각',
        'UI_DOT_STYLE_DIAMOND': '마름모',

        'UI_SUBHEADER_QR_SETTINGS': '🛠️ QR 코드 설정',
        'UI_BOX_SIZE_LABEL': '점 크기 (px)',
        'UI_BORDER_LABEL': '테두리 두께 (점의 개수)',
        'UI_ERROR_CORRECTION_LABEL': '오류 보정 레벨',
        'UI_ERROR_CORRECTION_LEVEL_L': 'Low (7%) - 오류 보정',
        'UI_ERROR_CORRECTION_LEVEL_M': 'Medium (15%) - 오류 보정',
        'UI_ERROR_CORRECTION_LEVEL_Q': 'Quartile (25%) - 오류 보정',
        'UI_ERROR_CORRECTION_LEVEL_H': 'High (30%) - 오류 보정',
        'UI_MASK_PATTERN_LABEL': '마스크 패턴',

        'UI_SUBHEADER_COLOR_SETTINGS': '🎨 색상 설정',
        'UI_WARNING_SVG_COLOR': '⚠️ SVG 형식은 색상 커스텀이 불가능합니다.',
        'UI_COLOR_OPTION_DIRECT_INPUT': '<직접 입력>',
        'UI_SELECTBOX_PATTERN_COLOR_LABEL': '패턴 색상',
        'UI_SELECTBOX_BG_COLOR_LABEL': '배경 색상',
        'UI_COLOR_INPUT_HELP': '원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.',
        'UI_COLOR_INPUT_CAPTION': '예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)',
        'UI_TEXT_INPUT_PATTERN_COLOR_LABEL': '패턴 색상 HEX 값',
        'UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER': '예: #000000',
        'UI_TEXT_INPUT_BG_COLOR_LABEL': '배경 색상 HEX 값',
        'UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER': '예: #FFFFFF',

        'UI_SUBHEADER_FILE_SETTINGS': '🛠️ 파일 설정',
        'UI_TEXT_INPUT_FILENAME_LABEL': '다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)',
        'UI_TEXT_INPUT_FILENAME_PLACEHOLDER': '이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)',
        'UI_BUTTON_DELETE_FILENAME_LABEL': '파일명 지우기',
        'UI_BUTTON_DELETE_FILENAME_HELP': '입력한 파일명을 지웁니다.',
        'UI_RADIO_FILE_FORMAT': '파일 형식',
        'UI_FILE_FORMAT_PNG': 'PNG',
        'UI_FILE_FORMAT_SVG': 'SVG',

        # 미리보기 및 다운로드 UI
        'UI_HEADER_PREVIEW_AND_GENERATE': '👀 미리보기 및 생성',
        'UI_INFO_QR_GENERATION_GUIDE': 'QR 코드를 생성하려면 내용을 입력해 주세요.',
        'UI_ERROR_EMPTY_DATA': '⚠️ QR 코드 내용을 입력해 주세요.',
        'UI_ERROR_INVALID_QR_INPUT': '⚠️ 유효하지 않은 입력값이 있습니다. 색상 코드 형식을 확인해 주세요.',
        'UI_ERROR_INVALID_PATTERN_COLOR': '⚠️ 패턴 색상 HEX 코드가 유효하지 않습니다.',
        'UI_ERROR_INVALID_BG_COLOR': '⚠️ 배경 색상 HEX 코드가 유효하지 않습니다.',
        'UI_BUTTON_GENERATE': 'QR 코드 생성',
        'UI_BUTTON_RESET': '모두 초기화',
        'UI_SUCCESS_MESSAGE': '✅ QR 코드가 성공적으로 생성되었습니다!',
        'UI_DOWNLOAD_LABEL': '💾 QR 코드 다운로드',
        'UI_DOWNLOAD_HELP': 'PC는 "Download" 폴더, 휴대폰은 "Download" 폴더에 저장됩니다.',
        'UI_WARNING_EMPTY_FILENAME': '⚠️ 파일명이 비어있으므로 자동으로 생성됩니다.',
        'UI_WARNING_INVALID_FILENAME': '⚠️ 입력한 파일명에 유효하지 않은 문자가 포함되어 있습니다.',
        'UI_DOWNLOAD_INFO': '📄 다운로드 파일명: {download_filename}'
    },
    'en': {
        # 앱 전체
        'APP_TITLE': 'QR Code Generator',
        'FOOTER_MESSAGE': '© 2025 QR Code Generator | Built with Streamlit | By Jonghun Ryu (redhat4u@gmail.com)',
        
        # 사이드바
        'SIDEBAR_HEADER_LANG': '🌐 Language Selection',
        'LANG_KO': 'Korean',
        'LANG_EN': 'English',
        'SELECTBOX_LANG_LABEL': 'Select a language',
        'SIDEBAR_HEADER_HOWTO': '📖 How to Use',
        'SIDEBAR_HOWTO_CONTENT': '''
        1. Enter the text you want to convert in the **QR Code Content** area.
        2. Adjust the size and error correction level in **QR Code Settings**.
        3. Select the shape of the QR code dots in **Pattern Shape** (only square is available for SVG format).
        4. Choose the pattern and background colors in **Color Settings** (only default colors are available for SVG format).
        5. Select your desired file format (PNG/SVG) and specify a filename in **File Settings**.
        6. Download the final file with the **Generate QR Code** button.
        ''',
        'SIDEBAR_HEADER_TIPS': '💡 QR Code Generation Tips',
        'SIDEBAR_TIPS_CONTENT': '''
        - **Text**: `Enter text to generate a QR code`
        - **Website**: `https://www.example.com`
        - **Email**: `mailto:user@example.com`
        - **Email (with Subject/Body)**: `mailto:user1@example.com,user2@example.com?subject=Subject&body=Message content`
        - **Phone Number**: `tel:type=CELL:+82 10-1234-5678`
        - **SMS (Number Only)**: `sms:type=CELL:+82 10-1234-5678`
        - **SMS (with Message)**: `sms:type=CELL:+82 10-1234-5678?body=Message content`
        - **WiFi**: `WIFI:T:WPA;S:NetworkName(SSID);P:Password;H:false;;`
        ''',
        'SIDEBAR_HEADER_TECH_INFO': '⚙️ Technical Information',
        'SIDEBAR_TECH_INFO_CONTENT': '''
        - **Creator**: Jonghun Ryu
        - **Libraries**: Streamlit, qrcode, pillow
        - **Hosting**: Streamlit Community Cloud
        - **Version**: 1.0.0
        ''',

        # Input and Settings UI
        'UI_HEADER_INPUT_AND_SETTINGS': '⚙️ Input & Settings',
        'UI_SUBHEADER_QR_CONTENT': '📝 QR Code Content',
        'UI_INFO_QR_DATA_LIMIT': 'The maximum number of characters you can enter is about 2,400 to 2,900 depending on the type.',
        'UI_TEXT_AREA_LABEL': 'Enter content to generate a QR code',
        'UI_TEXT_AREA_PLACEHOLDER': 'Enter the content for the QR code here.\nCopy/paste is available.',
        'UI_TEXT_CHAR_COUNT_OVER': '⚠️ Current character count: **{char_count}** (Exceeded recommended max)',
        'UI_TEXT_CHAR_COUNT_NEAR': '⚠️ Current character count: **{char_count}** (Error correction decreases as character count increases)',
        'UI_TEXT_CHAR_COUNT_OK': '✅ Current character count: **{char_count}**',
        'UI_CAPTION_CHAR_COUNT_ZERO': 'Please enter some content.',
        'UI_BUTTON_DELETE_TEXT_LABEL': 'Clear Content',
        'UI_BUTTON_DELETE_TEXT_HELP': 'Clears all QR code input content.',
        'UI_CHECKBOX_STRIP_TEXT': 'Strip leading/trailing whitespace from input',

        'UI_SUBHEADER_DOT_STYLE': '🛠️ Pattern Shape',
        'UI_SELECTBOX_DOT_STYLE_LABEL': 'Select pattern shape',
        'UI_DOT_STYLE_SQUARE': 'Square',
        'UI_DOT_STYLE_CIRCLE': 'Circle',
        'UI_DOT_STYLE_ROUNDED': 'Rounded',
        'UI_DOT_STYLE_DIAMOND': 'Diamond',
        
        'UI_SUBHEADER_QR_SETTINGS': '🛠️ QR Code Settings',
        'UI_BOX_SIZE_LABEL': 'Dot Size (px)',
        'UI_BORDER_LABEL': 'Border Thickness (number of dots)',
        'UI_ERROR_CORRECTION_LABEL': 'Error Correction Level',
        'UI_ERROR_CORRECTION_LEVEL_L': 'Low (7%) - Error Correction',
        'UI_ERROR_CORRECTION_LEVEL_M': 'Medium (15%) - Error Correction',
        'UI_ERROR_CORRECTION_LEVEL_Q': 'Quartile (25%) - Error Correction',
        'UI_ERROR_CORRECTION_LEVEL_H': 'High (30%) - Error Correction',
        'UI_MASK_PATTERN_LABEL': 'Mask Pattern',

        'UI_SUBHEADER_COLOR_SETTINGS': '🎨 Color Settings',
        'UI_WARNING_SVG_COLOR': '⚠️ Color customization is not available for SVG format.',
        'UI_COLOR_OPTION_DIRECT_INPUT': '<Direct Input>',
        'UI_SELECTBOX_PATTERN_COLOR_LABEL': 'Pattern Color',
        'UI_SELECTBOX_BG_COLOR_LABEL': 'Background Color',
        'UI_COLOR_INPUT_HELP': 'If your desired color is not in the list, enter the **HEX code** below.',
        'UI_COLOR_INPUT_CAPTION': 'e.g., #FF0000 (Red), #00FF00 (Green), #0000FF (Blue)',
        'UI_TEXT_INPUT_PATTERN_COLOR_LABEL': 'Pattern Color HEX Value',
        'UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER': 'e.g., #000000',
        'UI_TEXT_INPUT_BG_COLOR_LABEL': 'Background Color HEX Value',
        'UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER': 'e.g., #FFFFFF',

        'UI_SUBHEADER_FILE_SETTINGS': '🛠️ File Settings',
        'UI_TEXT_INPUT_FILENAME_LABEL': 'Download Filename (no extension)',
        'UI_TEXT_INPUT_FILENAME_PLACEHOLDER': 'Enter filename here (auto-generated if empty)',
        'UI_BUTTON_DELETE_FILENAME_LABEL': 'Clear Filename',
        'UI_BUTTON_DELETE_FILENAME_HELP': 'Clears the entered filename.',
        'UI_RADIO_FILE_FORMAT': 'File Format',
        'UI_FILE_FORMAT_PNG': 'PNG',
        'UI_FILE_FORMAT_SVG': 'SVG',

        # Preview and Download UI
        'UI_HEADER_PREVIEW_AND_GENERATE': '👀 Preview & Generate',
        'UI_INFO_QR_GENERATION_GUIDE': 'Enter content to generate a QR code.',
        'UI_ERROR_EMPTY_DATA': '⚠️ Please enter QR code content.',
        'UI_ERROR_INVALID_QR_INPUT': '⚠️ There is an invalid input. Please check the color code format.',
        'UI_ERROR_INVALID_PATTERN_COLOR': '⚠️ Invalid pattern color HEX code.',
        'UI_ERROR_INVALID_BG_COLOR': '⚠️ Invalid background color HEX code.',
        'UI_BUTTON_GENERATE': 'Generate QR Code',
        'UI_BUTTON_RESET': 'Reset All Settings',
        'UI_SUCCESS_MESSAGE': '✅ QR code has been successfully generated!',
        'UI_DOWNLOAD_LABEL': '💾 Download QR Code',
        'UI_DOWNLOAD_HELP': 'Saved to the "Download" folder on PC and mobile.',
        'UI_WARNING_EMPTY_FILENAME': '⚠️ Filename is empty, it will be automatically generated.',
        'UI_WARNING_INVALID_FILENAME': '⚠️ The entered filename contains invalid characters.',
        'UI_DOWNLOAD_INFO': '📄 Download Filename: {download_filename}'
    }
}

def get_message(key):
    """현재 언어에 맞는 메시지를 반환합니다."""
    # 세션 상태에 current_lang이 없으면 기본값 'ko'를 사용
    lang = st.session_state.get('current_lang', 'ko')
    return MESSAGES[lang].get(key, 'Key Not Found')
    
