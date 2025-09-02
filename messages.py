# This file manages UI text messages by language.
# messages.py

import streamlit as st
import qrcode

# Language-specific message dictionary
MESSAGES = {
    'ko': {
        # UI_main.py
        'APP_TITLE': "QR 코드 생성기",
        'UI_LANG_SELECT_LABEL': "언어 선택",
        'UI_LANG_SELECT_OPTIONS': ["한국어", "English"],

        # ui_input_and_settings.py
        'UI_HEADER_INPUT_AND_SETTINGS': "✍️ 입력 및 설정",
        'UI_SUBHEADER_QR_CONTENT': "QR 코드 내용",
        'UI_INFO_MAX_CHARS': "최대 2,953자까지 입력 가능합니다. (한글, 특수문자 등에 따라 가변적)",
        'UI_TEXT_AREA_LABEL': "내용을 입력하세요.",
        'UI_TEXT_AREA_PLACEHOLDER': "웹사이트 주소, 전화번호, 텍스트 등 QR 코드로 만들 내용을 입력하세요.",
        'UI_ERROR_MAX_CHARS': "⚠️ 입력 가능한 최대 글자수(약 2,953자)를 초과했습니다. 현재 글자수: {char_count}자",
        'UI_INFO_CURRENT_CHARS': "현재 글자수: {char_count}자",
        'UI_BUTTON_CLEAR_TEXT': "내용 지우기",
        'UI_CHECKBOX_STRIP_TEXT': "앞뒤 공백 제거하기",
        'UI_SUBHEADER_QR_SETTINGS': "QR 코드 설정",
        'UI_SELECTBOX_ERROR_CORRECTION': "오류 보정 레벨",
        'UI_ERROR_CORRECTION_LEVEL_L': "Low (7%) - 오류 보정",
        'UI_ERROR_CORRECTION_LEVEL_M': "Medium (15%) - 오류 보정",
        'UI_ERROR_CORRECTION_LEVEL_Q': "Quartile (25%) - 오류 보정",
        'UI_ERROR_CORRECTION_LEVEL_H': "High (30%) - 오류 보정",
        'UI_NUMBER_INPUT_BOX_SIZE': "1개 cell 크기",
        'UI_NUMBER_INPUT_BORDER': "여백 크기",
        'UI_SUBHEADER_COLOR_SETTINGS': "색상 설정",
        'UI_INFO_COLOR_SETTINGS': "PNG 파일 형식에서만 색상 변경이 가능합니다.",
        'UI_COLOR_OPTION_DIRECT_INPUT': "<직접 입력>",
        'UI_SELECTBOX_PATTERN_COLOR': "패턴 색상",
        'UI_SELECTBOX_BG_COLOR': "배경 색상",
        'UI_TEXT_INPUT_PATTERN_COLOR_HEX': "패턴 색상 HEX 값",
        'UI_TEXT_INPUT_BG_COLOR_HEX': "배경 색상 HEX 값",
        'UI_TEXT_INPUT_PLACEHOLDER_HEX': "예: #000000",
        'UI_SUBHEADER_PATTERN_STYLE': "패턴 스타일",
        'UI_SELECTBOX_DOT_STYLE': "패턴 스타일 선택",
        'UI_DOT_STYLE_SQUARE': "사각형",
        'UI_DOT_STYLE_CIRCLE': "원형",
        'UI_DOT_STYLE_ROUNDED': "둥근 사각형",
        'UI_DOT_STYLE_DIAMOND': "다이아몬드",
        'UI_SUBHEADER_FILE_SETTINGS': "파일 설정",
        'UI_TEXT_INPUT_FILENAME': "파일명 입력",
        'UI_TEXT_INPUT_FILENAME_PLACEHOLDER': "파일명 미입력 시 자동 생성",
        'UI_BUTTON_CLEAR_FILENAME': "파일명 지우기",
        'UI_SELECTBOX_FILE_FORMAT': "파일 형식",
        'UI_FILE_FORMAT_PNG': "PNG (색상 변경 가능)",
        'UI_FILE_FORMAT_SVG': "SVG (색상 변경 불가)",

        # ui_preview_and_download.py
        'UI_HEADER_PREVIEW_AND_GENERATE': "👀 미리보기 및 생성",
        'UI_BUTTON_GENERATE_QR': "⚡ QR 코드 생성",
        'UI_ERROR_QR_DATA_MISSING': "⚠️ 생성할 QR 코드 내용을 입력해 주세요.",
        'UI_ERROR_PATTERN_COLOR_HEX_MISSING': "⚠️ 패턴 색의 HEX 값을 입력해 주세요.",
        'UI_ERROR_INVALID_PATTERN_COLOR': "⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
        'UI_ERROR_BG_COLOR_HEX_MISSING': "⚠️ 배경 색의 HEX 값을 입력해 주세요.",
        'UI_ERROR_INVALID_BG_COLOR': "⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
        'UI_ERROR_SAME_COLOR': "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.",
        'UI_WARNING_PATTERN_COLOR_INPUT': "⚠️ 패턴 색을 입력해 주세요.",
        'UI_WARNING_BG_COLOR_INPUT': "⚠️ 배경 색을 입력해 주세요.",
        'UI_WARNING_INVALID_COLOR_HEX': "⚠️ 올바른 색상값이 아닙니다. 다시 확인해 주세요.",
        'UI_WARNING_SAME_COLOR': "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다. 다른 색을 선택해 주세요.",
        'UI_INFO_QR_GENERATION_GUIDE': "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다.",
        'UI_SUBHEADER_QR_PREVIEW': "📱 QR 코드 미리보기",
        'UI_PREVIEW_IMAGE_CAPTION': "생성된 QR 코드",
        'UI_INFO_QR_CODE_INFO_TITLE': "QR 코드 정보",
        'UI_INFO_QR_VERSION': "QR 버전",
        'UI_INFO_QR_CELL_COUNT': "가로/세로 각 cell 개수",
        'UI_INFO_QR_IMAGE_SIZE_REFERENCE': "이미지 크기 (참고)",
        'UI_INFO_QR_PATTERN_COLOR': "패턴 색상",
        'UI_INFO_QR_BG_COLOR': "배경 색상",
        'UI_INFO_QR_IMAGE_SIZE_FORMULA': "이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기",
        'UI_SUBHEADER_DOWNLOAD': "📥 다운로드",
        'UI_DOWNLOAD_LABEL': "💾 QR 코드 다운로드",
        'UI_DOWNLOAD_HELP': "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다.",
        'UI_BUTTON_RESET': "🔄 설정 초기화",
        'UI_DOWNLOAD_FILENAME_LABEL': "다운로드 파일명",
    },
    'en': {
        # UI_main.py
        'APP_TITLE': "QR Code Generator",
        'UI_LANG_SELECT_LABEL': "Language Selection",
        'UI_LANG_SELECT_OPTIONS': ["Korean", "English"],
        
        # ui_input_and_settings.py
        'UI_HEADER_INPUT_AND_SETTINGS': "✍️ Input and Settings",
        'UI_SUBHEADER_QR_CONTENT': "QR Code Content",
        'UI_INFO_MAX_CHARS': "You can enter up to 2,953 characters. (varies depending on language and special characters)",
        'UI_TEXT_AREA_LABEL': "Enter your content.",
        'UI_TEXT_AREA_PLACEHOLDER': "Enter the content to create a QR code, such as a website address, phone number, or text.",
        'UI_ERROR_MAX_CHARS': "⚠️ You have exceeded the maximum number of characters (approx. 2,953). Current characters: {char_count}",
        'UI_INFO_CURRENT_CHARS': "Current characters: {char_count}",
        'UI_BUTTON_CLEAR_TEXT': "Clear Text",
        'UI_CHECKBOX_STRIP_TEXT': "Strip leading/trailing whitespace",
        'UI_SUBHEADER_QR_SETTINGS': "QR Code Settings",
        'UI_SELECTBOX_ERROR_CORRECTION': "Error Correction Level",
        'UI_ERROR_CORRECTION_LEVEL_L': "Low (7%) - Error Correction",
        'UI_ERROR_CORRECTION_LEVEL_M': "Medium (15%) - Error Correction",
        'UI_ERROR_CORRECTION_LEVEL_Q': "Quartile (25%) - Error Correction",
        'UI_ERROR_CORRECTION_LEVEL_H': "High (30%) - Error Correction",
        'UI_NUMBER_INPUT_BOX_SIZE': "Single Cell Size",
        'UI_NUMBER_INPUT_BORDER': "Border Size",
        'UI_SUBHEADER_COLOR_SETTINGS': "Color Settings",
        'UI_INFO_COLOR_SETTINGS': "Color changes are only available for the PNG file format.",
        'UI_COLOR_OPTION_DIRECT_INPUT': "<Enter Directly>",
        'UI_SELECTBOX_PATTERN_COLOR': "Pattern Color",
        'UI_SELECTBOX_BG_COLOR': "Background Color",
        'UI_TEXT_INPUT_PATTERN_COLOR_HEX': "Pattern Color HEX Value",
        'UI_TEXT_INPUT_BG_COLOR_HEX': "Background Color HEX Value",
        'UI_TEXT_INPUT_PLACEHOLDER_HEX': "e.g., #000000",
        'UI_SUBHEADER_PATTERN_STYLE': "Pattern Style",
        'UI_SELECTBOX_DOT_STYLE': "Select Dot Style",
        'UI_DOT_STYLE_SQUARE': "Square",
        'UI_DOT_STYLE_CIRCLE': "Circle",
        'UI_DOT_STYLE_ROUNDED': "Rounded Square",
        'UI_DOT_STYLE_DIAMOND': "Diamond",
        'UI_SUBHEADER_FILE_SETTINGS': "File Settings",
        'UI_TEXT_INPUT_FILENAME': "Enter Filename",
        'UI_TEXT_INPUT_FILENAME_PLACEHOLDER': "Filename will be auto-generated if left blank",
        'UI_BUTTON_CLEAR_FILENAME': "Clear Filename",
        'UI_SELECTBOX_FILE_FORMAT': "File Format",
        'UI_FILE_FORMAT_PNG': "PNG (Color Change Available)",
        'UI_FILE_FORMAT_SVG': "SVG (Color Change Not Available)",

        # ui_preview_and_download.py
        'UI_HEADER_PREVIEW_AND_GENERATE': "👀 Preview and Generate",
        'UI_BUTTON_GENERATE_QR': "⚡ Generate QR Code",
        'UI_ERROR_QR_DATA_MISSING': "⚠️ Please enter content to generate the QR code.",
        'UI_ERROR_PATTERN_COLOR_HEX_MISSING': "⚠️ Please enter the HEX value for the pattern color.",
        'UI_ERROR_INVALID_PATTERN_COLOR': "⚠️ The HEX value entered for the pattern color is not a valid color. Please check again.",
        'UI_ERROR_BG_COLOR_HEX_MISSING': "⚠️ Please enter the HEX value for the background color.",
        'UI_ERROR_INVALID_BG_COLOR': "⚠️ The HEX value entered for the background color is not a valid color. Please check again.",
        'UI_ERROR_SAME_COLOR': "⚠️ The pattern and background cannot be the same color.",
        'UI_WARNING_PATTERN_COLOR_INPUT': "⚠️ Please enter a pattern color.",
        'UI_WARNING_BG_COLOR_INPUT': "⚠️ Please enter a background color.",
        'UI_WARNING_INVALID_COLOR_HEX': "⚠️ This is not a valid color value. Please check again.",
        'UI_WARNING_SAME_COLOR': "⚠️ The pattern and background cannot be the same color. Please choose a different color.",
        'UI_INFO_QR_GENERATION_GUIDE': "Enter your QR code content to see a live preview.",
        'UI_SUBHEADER_QR_PREVIEW': "📱 QR Code Preview",
        'UI_PREVIEW_IMAGE_CAPTION': "Generated QR Code",
        'UI_INFO_QR_CODE_INFO_TITLE': "QR Code Information",
        'UI_INFO_QR_VERSION': "QR Version",
        'UI_INFO_QR_CELL_COUNT': "Cells per side",
        'UI_INFO_QR_IMAGE_SIZE_REFERENCE': "Image Size (approx.)",
        'UI_INFO_QR_PATTERN_COLOR': "Pattern Color",
        'UI_INFO_QR_BG_COLOR': "Background Color",
        'UI_INFO_QR_IMAGE_SIZE_FORMULA': "Image Size = (cells per side + total border cells) × single cell size",
        'UI_SUBHEADER_DOWNLOAD': "📥 Download",
        'UI_DOWNLOAD_LABEL': "💾 Download QR Code",
        'UI_DOWNLOAD_HELP': "Saves to the 'Download' folder on PC and mobile devices.",
        'UI_BUTTON_RESET': "🔄 Reset Settings",
        'UI_DOWNLOAD_FILENAME_LABEL': "Download Filename",
    }
}

def get_current_language():
    """Returns the currently selected language."""
    if 'language_select' not in st.session_state:
        return 'ko'
    
    lang_name = st.session_state.language_select
    if lang_name == "한국어" or lang_name == "Korean":
        return 'ko'
    else:
        return 'en'

def get_message(key):
    """Returns the message for the given key in the current language."""
    lang = get_current_language()
    return MESSAGES[lang].get(key, key)
    
