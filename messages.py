# 이 파일은 앱 전반에 사용되는 모든 문자열 메시지를 정의합니다.
# messages.py

# =========================================================
# qrcode_web.py
# =========================================================
APP_TITLE = "QR 코드 생성기"

# =========================================================
# ui_input_and_settings.py
# =========================================================
UI_HEADER_INPUT_AND_SETTINGS = "⚙️ 입력 및 설정"
UI_SUBHEADER_QR_CONTENT = "📝 QR 코드 내용"
UI_INFO_QR_DATA_LIMIT = "최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다."
UI_TEXT_AREA_LABEL = "QR 코드로 생성할 내용을 입력해 주세요"
UI_TEXT_AREA_PLACEHOLDER = "이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다."
UI_CAPTION_CHAR_COUNT_ZERO = "현재 입력된 총 문자 수: 0"
UI_BUTTON_DELETE_TEXT_LABEL = "🗑️ 입력 내용 삭제"
UI_BUTTON_DELETE_TEXT_HELP = "입력한 내용을 전부 삭제합니다 (파일명은 유지)"
UI_CHECKBOX_STRIP_TEXT = "마지막 입력문자 이후 모든 공백/줄바꿈 제거"
UI_SUBHEADER_QR_SETTINGS = "🛠️ QR 코드 설정"
UI_BOX_SIZE_LABEL = "QR 코드 1개의 사각 cell 크기 (px)"
UI_BORDER_LABEL = "QR 코드 테두리/여백"
UI_ERROR_CORRECTION_LABEL = "오류 보정 레벨"
UI_MASK_PATTERN_LABEL = "마스크 패턴 선택 (0~7)"
UI_SUBHEADER_COLOR_SETTINGS = "🛠️ 색상 설정"
UI_WARNING_SVG_COLOR = "⚠️ SVG 파일은 벡터 형식이므로 원하는 색상을 선택할 수 없습니다. 다양한 색상을 원한다면 'PNG' 형식을 선택하세요."
UI_SELECTBOX_PATTERN_COLOR_LABEL = "패턴 색상"
UI_SELECTBOX_BG_COLOR_LABEL = "배경 색상"
UI_COLOR_OPTION_DIRECT_INPUT = "<직접 입력>"
UI_COLOR_INPUT_HELP = "원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요."
UI_COLOR_INPUT_CAPTION = "예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)"
UI_TEXT_INPUT_PATTERN_COLOR_LABEL = "패턴 색상 HEX 값"
UI_TEXT_INPUT_PATTERN_COLOR_PLACEHOLDER = "예: #000000"
UI_TEXT_INPUT_BG_COLOR_LABEL = "배경 색상 HEX 값"
UI_TEXT_INPUT_BG_COLOR_PLACEHOLDER = "예: #FFFFFF"
UI_SUBHEADER_DOT_STYLE = "🛠️ 패턴 모양"
UI_SELECTBOX_DOT_STYLE_LABEL = "패턴 모양 선택"
UI_DOT_STYLE_SQUARE = "사각형"
UI_DOT_STYLE_CIRCLE = "원형"
UI_DOT_STYLE_ROUNDED = "둥근 사각"
UI_DOT_STYLE_DIAMOND = "마름모"
UI_SUBHEADER_FILE_SETTINGS = "🛠️ 파일 설정"
UI_TEXT_INPUT_FILENAME_LABEL = "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)"
UI_TEXT_INPUT_FILENAME_PLACEHOLDER = "이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)"
UI_BUTTON_DELETE_FILENAME_LABEL = "🗑️ 파일명 삭제"
UI_BUTTON_DELETE_FILENAME_HELP = "입력한 파일명을 삭제합니다"
UI_RADIO_FILE_FORMAT = "파일 형식 선택"

# =========================================================
# ui_preview_and_download.py
# =========================================================
UI_HEADER_PREVIEW_AND_GENERATE = "👀 미리보기 및 생성"
UI_CAPTION_QR_DATA_EMPTY = "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다."
UI_BUTTON_GENERATE = "⚡ QR 코드 생성"
UI_ERROR_QR_DATA_EMPTY = "⚠️ 생성할 QR 코드 내용을 입력해 주세요."
UI_ERROR_HEX_PATTERN_EMPTY = "⚠️ 패턴 색의 HEX 값을 입력해 주세요."
UI_ERROR_HEX_PATTERN_INVALID = "⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요."
UI_ERROR_HEX_BG_EMPTY = "⚠️ 배경 색의 HEX 값을 입력해 주세요."
UI_ERROR_HEX_BG_INVALID = "⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요."
UI_ERROR_COLORS_SAME = "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다."
UI_SUCCESS_MESSAGE = """
✅ QR 코드 생성 완료!!<br>
반드시 파일명을 확인하시고, 화면 아래의 [💾 QR 코드 다운로드] 버튼을 클릭하세요.
"""
UI_CAPTION_QR_PREVIEW_ERROR = "색상 설정이 유효하지 않습니다. 미리보기를 표시할 수 없습니다."
UI_SUBHEADER_PREVIEW = "📱 QR 코드 미리보기"
UI_IMAGE_CAPTION_PREVIEW = "생성된 QR 코드"
UI_INFO_QR_INFO = """
**QR 코드 정보**
- QR 버전: {version}
- 가로/세로 각 cell 개수: {modules}개
- 이미지 크기 (참고): {size} px
- 패턴 색상: {pattern_color}
- 배경 색상: {bg_color}
- 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
"""
UI_SUBHEADER_DOWNLOAD = "📥 다운로드"
UI_BUTTON_DOWNLOAD = "💾 QR 코드 다운로드"
UI_BUTTON_DOWNLOAD_HELP = "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다."
UI_DOWNLOAD_FILENAME_LABEL = "📄 다운로드 파일명: "
UI_SUCCESS_DOWNLOAD_MESSAGE = """
✅ QR 코드 다운로드 완료!!<br>
휴대폰은 'Download' 폴더에 저장됩니다.
"""
UI_PREVIEW_READY_MESSAGE = """
✅ 현재 입력된 내용으로 QR 코드를 미리 표현해 보았습니다.<br>
아래의 QR 코드가 맘에 드시면, 위의 [⚡ QR 코드 생성] 버튼을 클릭하세요.
"""
UI_INFO_ENTER_QR_DATA = "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 보여드립니다."
UI_TEXT_CHAR_COUNT_OVER = "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)"
UI_TEXT_CHAR_COUNT_NEAR = "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 문자 수에 근접)"
UI_TEXT_CHAR_COUNT_OK = "✅ 현재 입력된 총 문자 수: **{char_count}**"

# =========================================================
# state_manager.py
# =========================================================
UI_DEFAULT_BOX_SIZE = 20
UI_DEFAULT_BORDER = 2
UI_DEFAULT_ERROR_CORRECTION = "Low (7%) - 오류 보정"
UI_DEFAULT_MASK_PATTERN = 2
UI_DEFAULT_PATTERN_COLOR = "black"
UI_DEFAULT_BG_COLOR = "white"
UI_DEFAULT_STRIP_OPTION = True
UI_DEFAULT_DOT_STYLE = "사각형"
UI_FILE_FORMAT_PNG = "PNG"
