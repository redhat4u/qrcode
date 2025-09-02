# app.py configuration strings
PAGE_TITLE = "QR 코드 생성기"
PAGE_ICON = "🔲"

# Header and subheader
HEADER_INPUT_SETTINGS = "⚙️ 입력 및 설정"
HEADER_PREVIEW_DOWNLOAD = "👀 미리보기 및 다운로드"
SUBHEADER_CONTENT = "📝 QR 코드 내용"
SUBHEADER_FILE_FORMAT = "💾 파일 형식 선택"
SUBHEADER_SHAPE_SETTINGS = "🖼️ 패턴 모양 설정"
SUBHEADER_COLOR_SETTINGS = "🎨 색상 설정"
SUBHEADER_QR_SETTINGS = "🔨 QR 코드 설정"
SUBHEADER_FILENAME = "📄 파일명 설정"
SUBHEADER_PREVIEW = "📱 QR 코드 미리보기"
SUBHEADER_DOWNLOAD = "📥 다운로드"

# Messages and captions
INFO_MAX_CHARS = "최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다."
PLACEHOLDER_TEXTAREA = "이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다."
WARNING_CHAR_LIMIT_EXCEEDED = "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)"
WARNING_CHAR_LIMIT_NEAR = "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 문자 수에 근접)"
SUCCESS_CHAR_COUNT = "✅ 현재 입력된 총 문자 수: **{char_count}**"
CAPTION_CHAR_COUNT = "현재 입력된 총 문자 수: 0"
HELP_STRIP_OPTION = "입력한 내용 마지막에 공백이나 줄바꿈이 있을 경우 QR 코드는 완전히 달라집니다."
HELP_DELETE_TEXT = "입력한 내용을 전부 삭제합니다 (파일명은 유지)"
CAPTION_JPG_QUALITY = "ℹ️ JPG는 압축률에 따라 이미지 품질이 달라집니다."
HELP_JPG_QUALITY = "높은 품질(100)은 파일 크기가 크고 선명하며, 낮은 품질(1)은 파일 크기가 작고 화질이 저하됩니다."
WARNING_SVG_LIMITATION = "⚠️ SVG 형식은 사각만 지원합니다."
WARNING_SVG_COLOR_LIMITATION = "⚠️ SVG 파일은 벡터 형식으로 현재는 다양한 색상과 패턴을 지원하지 않습니다. 여러가지 스타일을 원한다면 'PNG' 또는 'JPG' 형식을 선택하세요."
WARNING_SVG_CORNER_LIMITATION = "⚠️ SVG 형식은 둥근 모서리를 지원하지 않습니다."
WARNING_SVG_GAP_LIMITATION = "⚠️ '사각' 패턴과 'SVG' 형식은 간격 조절을 지원하지 않습니다."
INFO_COLOR_HEX_EXAMPLE = "원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요."
CAPTION_HEX_EXAMPLE = "예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)"
PLACEHOLDER_HEX_PATTERN = "예: #000000"
PLACEHOLDER_HEX_BG = "예: #FFFFFF"
PLACEHOLDER_FILENAME = "이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)"
HELP_DELETE_FILENAME = "입력한 파일명을 삭제합니다"
SUCCESS_QR_GENERATED = "✅ 현재 입력된 내용으로 QR 코드를 생성하였습니다. 원하는 스타일로 선택한 후 아래의 다운로드를 클릭하세요."
CAPTION_QR_PREVIEW = "생성된 QR 코드"
HELP_DOWNLOAD_BUTTON = "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다."
INFO_NO_INPUT = "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 볼 수 있으며, 다운로드도 가능합니다."
BUTTON_RESET_ALL = "🔄 전체 초기화"
HELP_RESET_ALL = "모든 내용을 초기화 합니다."

# Error messages
ERROR_QR_DATA_GENERATION = "QR 코드 데이터 생성 오류: {error}"
ERROR_SVG_GENERATION = "QR 코드 SVG 생성 오류: {error}"
ERROR_GENERAL = "오류가 발생했습니다: {error}"
WARNING_SETTINGS_INVALID = "⚠️ 선택하신 설정으로는 QR 코드를 생성할 수 없습니다. 아래의 경고 메시지를 확인해주세요."
WARNING_HEX_PATTERN_EMPTY = "⚠️ 패턴 색의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다."
WARNING_HEX_BG_EMPTY = "⚠️ 배경 색의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다."
WARNING_HEX_PATTERN_INVALID = "⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요."
WARNING_HEX_BG_INVALID = "⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요."
WARNING_COLORS_SAME = "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다."

# Sidebar
SIDEBAR_HEADER_GUIDE = "📖 사용 방법"
SIDEBAR_GUIDE_TEXT = """
1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
2. **파일 형식**과 **패턴 모양**을 선택하세요
3. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
4. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
5. **파일명 설정**에서 파일명을 지정하세요
6. 모든 설정이 유효하면 **자동으로 미리보기와 다운로드 버튼이 표시됩니다**
"""

SIDEBAR_HEADER_TIPS = "💡 용도별 QR 코드 생성 팁"
SIDEBAR_TIPS_TEXT = """
- **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
- **웹사이트**: `https://www.example.com`
- **이메일**: `mailto:user@example.com`
- **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
- **전화번호**: `tel:type=CELL:+82 10-1234-5678`
- **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
- **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
- **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
"""

SIDEBAR_HEADER_SETTINGS = "⚙️ 설정 가이드"
SIDEBAR_SETTINGS_FORMAT = "**파일 형식:**"
SIDEBAR_SETTINGS_FORMAT_TEXT = """
- **PNG**: 무손실 압축으로 품질 저하가 없으며, 투명 배경을 지원합니다.
- **JPG**: 손실 압축으로 파일 크기가 작고, 사진에 주로 사용됩니다. **JPG 품질 슬라이더**로 압축률을 조절할 수 있습니다.
- **SVG**: 벡터 형식으로 해상도에 영향을 받지 않아 확대해도 깨지지 않습니다.
"""
SIDEBAR_SETTINGS_SHAPE = "**패턴 모양:**"
SIDEBAR_SETTINGS_SHAPE_TEXT = """
- 사각, 둥근사각, 동그라미, 마름모, 별, 십자가 중 선택
- **SVG** 파일 형식 선택 시에는 **사각**만 지원합니다.
"""
SIDEBAR_SETTINGS_GAP = "**패턴 간격:**"
SIDEBAR_SETTINGS_GAP_TEXT = """
- **사각 패턴**과 **SVG 파일**에서는 지원되지 않습니다.
- 슬라이더로 조절하며, 값이 높을수록 패턴의 크기가 작아져 간격이 넓어집니다.
"""
SIDEBAR_SETTINGS_COLOR = "**색상 입력:**"
SIDEBAR_SETTINGS_COLOR_TEXT = """
- **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
- **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
- **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.
"""
SIDEBAR_SETTINGS_QR = "**QR 코드 설정:**"
SIDEBAR_SETTINGS_EC = "**오류 보정 레벨:**"
SIDEBAR_SETTINGS_EC_TEXT = """
- **Low (7%)**: 손상되지 않는 환경
- **Medium (15%)**: 일반적인 사용
- **Quartile (25%)**: 약간의 손상 가능
- **High (30%)**: 로고 삽입, 손상이 잦은 환경
"""
SIDEBAR_SETTINGS_MASK = "**마스크 패턴:**"
SIDEBAR_SETTINGS_MASK_TEXT = """
- 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
"""

# Footer
FOOTER_TEXT = "© 2025 QR 코드 생성기 | Streamlit으로 제작 | 제작: 류종훈(redhat4u@gmail.com)"
