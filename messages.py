# 이 파일은 앱에서 사용되는 모든 사용자 메시지, 라벨, 힌트 등을 정의합니다.
# messages.py

# qrcode_web.py
APP_TITLE = "🔲 QR 코드 생성기"

# sidebar.py
SIDEBAR_HEADER_HOWTO = "📖 사용 방법"
SIDEBAR_INSTRUCTIONS = """
1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
3. **패턴 모양**에서 QR 코드 점의 모양을 선택하세요 (SVG 형식은 사각형만 가능합니다)
4. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
5. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요
6. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
"""
SIDEBAR_HEADER_TIPS = "💡 용도별 QR 코드 생성 팁"
SIDEBAR_TIPS = """
- **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
- **웹사이트**: `https://www.example.com`
- **이메일**: `mailto:user@example.com`
- **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
- **전화번호**: `tel:type=CELL:+82 10-1234-5678`
- **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
- **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
- **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
"""

# ui_input_and_settings.py
UI_HEADER_INPUT_AND_SETTINGS = "⚙️ 입력 및 설정"
UI_SUBHEADER_CONTENT = "📝 QR 코드 내용"
UI_INFO_CHAR_LIMIT = "최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다."
UI_PLACEHOLDER_CONTENT = "이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다."
UI_ERROR_CHAR_COUNT_OVER = "⚠️ 현재 입력된 총 문자 수: **{}** (권장 최대 문자 수 초과)"
UI_WARNING_CHAR_COUNT_NEAR = "⚠️ 현재 입력된 총 문자 수: **{}** (권장 문자 수에 근접)"
UI_SUCCESS_CHAR_COUNT_OK = "✅ 현재 입력된 총 문자 수: **{}**"
UI_CAPTION_CHAR_COUNT_ZERO = "현재 입력된 총 문자 수: 0"
UI_BUTTON_DELETE = "🗑️ 입력 내용 삭제"
UI_BUTTON_DELETE_HELP = "입력한 내용을 전부 삭제합니다 (파일명은 유지)"
UI_CHECKBOX_STRIP = "마지막 입력문자 이후 모든 공백/줄바꿈 제거"
UI_SUBHEADER_SETTINGS = "🛠️ QR 코드 설정"
UI_LABEL_BOX_SIZE = "QR 코드 1개의 사각 cell 크기 (px)"
UI_LABEL_BORDER = "QR 코드 테두리/여백"
UI_LABEL_EC = "오류 보정 레벨"
UI_LABEL_MP = "마스크 패턴"
UI_SUBHEADER_COLORS = "🎨 색상 설정"
UI_LABEL_PATTERN_COLOR = "패턴 색상 선택"
UI_LABEL_BG_COLOR = "배경 색상 선택"
UI_COLOR_OPTION_DIRECT_INPUT = "<직접 입력>"
UI_INFO_HEX_INPUT = "원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요."
UI_CAPTION_HEX_EXAMPLE = "예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)"
UI_PLACEHOLDER_HEX_PATTERN = "예: #000000"
UI_PLACEHOLDER_HEX_BG = "예: #FFFFFF"
UI_SUBHEADER_DOT_STYLE = "🛠️ 패턴 모양"
UI_LABEL_DOT_STYLE = "패턴 모양 선택"
UI_DOT_STYLE_SQUARE = "사각형"
UI_DOT_STYLE_ROUNDED = "둥근 사각"
UI_DOT_STYLE_CIRCLE = "원형"
UI_DOT_STYLE_RHOMBUS = "마름모"
UI_SUBHEADER_FILE = "🛠️ 파일 설정"
UI_LABEL_FILE_NAME = "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)"
UI_PLACEHOLDER_FILE_NAME = "이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)"
UI_BUTTON_CLEAR_FILE_NAME = "🗑️ 파일명 삭제"
UI_BUTTON_CLEAR_FILE_NAME_HELP = "파일명 삭제"
UI_LABEL_FILE_FORMAT = "다운로드 파일 형식"
UI_FILE_FORMAT_PNG = "PNG (이미지)"
UI_FILE_FORMAT_SVG = "SVG (벡터)"

# ui_preview_and_download.py
UI_HEADER_PREVIEW_AND_GENERATE = "👀 미리보기 및 생성"
UI_BUTTON_GENERATE = "⚡ QR 코드 생성"
UI_ERROR_QR_DATA_EMPTY = "⚠️ 생성할 QR 코드 내용을 입력해 주세요."
UI_ERROR_HEX_PATTERN_EMPTY = "⚠️ 패턴 색의 HEX 값을 입력해 주세요."
UI_ERROR_HEX_PATTERN_INVALID = "⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요."
UI_ERROR_HEX_BG_EMPTY = "⚠️ 배경 색의 HEX 값을 입력해 주세요."
UI_ERROR_HEX_BG_INVALID = "⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요."
UI_ERROR_COLORS_SAME = "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다."
UI_SUCCESS_MESSAGE = "✅ QR 코드 생성에 성공했습니다! 아래 미리보기 이미지를 확인하고 다운로드하세요."
UI_ERROR_MESSAGE = "⚠️ QR 코드 생성에 실패했습니다. 다음 사항을 확인해 주세요."
UI_LIST_INVALID_COLOR_PNG = "- PNG는 16진수(HEX) 색상 코드만 지원합니다. 올바른 HEX 코드를 입력했는지 확인해주세요."
UI_LIST_COLORS_SAME = "- 패턴과 배경 색상이 서로 다르게 설정되었는지 확인해주세요."
UI_LIST_QR_DATA_EMPTY = "- QR 코드에 담을 내용이 올바르게 입력되었는지 확인해주세요."
UI_CAPTION_QR_DATA_EMPTY = "QR 코드를 생성할 내용이 없습니다."
UI_CAPTION_QR_TOO_LARGE = "QR 코드 내용이 너무 많아 미리보기 이미지를 생성할 수 없습니다. 내용을 줄여주세요."
UI_CAPTION_QR_PREVIEW_ERROR = "미리보기를 불러올 수 없습니다. 설정을 확인해 주세요."
UI_BUTTON_DOWNLOAD = "💾 QR 코드 다운로드"
UI_BUTTON_DOWNLOAD_HELP = "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다."
UI_DOWNLOAD_FILENAME = "📄 다운로드 파일명:"
UI_SUCCESS_DOWNLOAD_MESSAGE = "✅ 다운로드에 성공했습니다. 이 파일은 PC의 '다운로드' 폴더에 저장됩니다."
UI_SUCCESS_DOWNLOAD_MOBILE_MESSAGE = "✅ 다운로드에 성공했습니다. 이 파일은 휴대폰의 '다운로드' 폴더에 저장됩니다."

# footer.py
FOOTER_TEXT = "© 2025 QR 코드 생성기 | Streamlit으로 제작 | 제작: 류종훈(redhat4u@gmail.com)"
