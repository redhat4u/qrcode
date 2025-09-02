# messages.py
# 언어별 메시지를 관리하는 딕셔너리입니다.

MESSAGES = {
    "ko": {
        "page_title": "QR 코드 생성기",
        "page_icon": "🔲",
        "main_title": "QR 코드 생성기",
        "separator": "---",
        "header_settings": "⚙️ 입력 및 설정",
        "subheader_content": "📝 QR 코드 내용",
        "info_max_chars": "최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.",
        "text_area_label": "QR 코드로 생성할 내용을 입력해 주세요",
        "text_area_placeholder": "이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.",
        "char_count_error": "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)",
        "char_count_warning": "⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 문자 수에 근접)",
        "char_count_success": "✅ 현재 입력된 총 문자 수: **{char_count}**",
        "char_count_caption": "현재 입력된 총 문자 수: 0",
        "strip_whitespace_label": "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        "strip_whitespace_help": "입력한 내용 마지막에 공백이나 줄바꿈이 있을 경우 QR 코드는 완전히 달라집니다.",
        "button_clear_text": "🗑️ 입력 내용 삭제",
        "button_clear_text_help": "입력한 내용을 전부 삭제합니다 (파일명은 유지)",
        "subheader_file_format": "💾 파일 형식 선택",
        "file_format_label": "파일 형식",
        "file_format_info_jpg": "ℹ️ JPG는 압축률에 따라 이미지 품질이 달라집니다.",
        "jpg_quality_slider": "JPG 품질 (압축률)",
        "jpg_quality_help": "높은 품질(100)은 파일 크기가 크고 선명하며, 낮은 품질(1)은 파일 크기가 작고 화질이 저하됩니다.",
        "subheader_pattern_shape": "🖼️ 패턴 모양 설정",
        "info_svg_shape": "⚠️ SVG 형식은 사각만 지원합니다.",
        "label_normal_pattern": "일반 패턴 모양",
        "label_finder_pattern": "파인더 패턴 모양",
        "pattern_shape_options": ("사각", "둥근사각", "동그라미", "마름모", "별", "십자가"),
        "info_rounded_corners": "⚠️ SVG 형식은 둥근 모서리를 지원하지 않습니다.",
        "slider_corner_radius": "둥근 모서리 반경 (%)",
        "corner_radius_help": "모서리를 얼마나 둥글게 할지 결정합니다. 0%는 사각, 50%는 원에 가까워집니다.",
        "info_cell_gap": "⚠️ '사각' 패턴과 'SVG' 형식은 간격 조절을 지원하지 않습니다.",
        "slider_cell_gap": "패턴 간격 (%)",
        "cell_gap_help": "각 패턴 사이의 간격을 조절합니다. 0%는 간격 없음.",
        "subheader_colors": "🎨 색상 설정",
        "warning_svg_color": "⚠️ SVG 파일은 벡터 형식으로 현재는 다양한 색상과 패턴을 지원하지 않습니다. 여러가지 스타일을 원한다면 'PNG' 또는 'JPG' 형식을 선택하세요.",
        "color_direct_input": "<직접 입력>",
        "pattern_color_label": "패턴 색상",
        "bg_color_label": "배경 색상",
        "info_hex_color": "원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.",
        "example_hex": "예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)",
        "placeholder_pattern_hex": "예: #000000",
        "placeholder_bg_hex": "예: #FFFFFF",
        "subheader_qr_settings": "🔨 QR 코드 설정",
        "label_box_size": "QR 코드 1개의 사각 cell 크기 (px)",
        "label_border": "QR 코드 테두리/여백",
        "label_error_correction": "오류 보정 레벨",
        "error_correction_options": ("Low (7%) - 오류 보정", "Medium (15%) - 오류 보정", "Quartile (25%) - 오류 보정", "High (30%) - 오류 보정"),
        "label_mask_pattern": "마스크 패턴 선택 (0~7)",
        "subheader_filename": "📄 파일명 설정",
        "placeholder_filename": "이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
        "button_clear_filename": "🗑️ 파일명 삭제",
        "button_clear_filename_help": "입력한 파일명을 삭제합니다",
        "header_preview_download": "👀 미리보기 및 다운로드",
        "success_preview": "✅ 현재 입력된 내용으로 QR 코드를 생성하였습니다. 원하는 스타일로 선택한 후 아래의 다운로드를 클릭하세요.",
        "subheader_preview": "📱 QR 코드 미리보기",
        "caption_preview": "생성된 QR 코드",
        "info_qr_details": """
            **[ QR 코드 정보 ]**
            - QR 버전: {qr_version}
            ** **
            - 각 한줄의 cell 개수: {modules_count}개
            - 각 한줄의 좌/우 여백 총 개수: {border_size}개
            - 1개의 사각 cell 크기: {box_size}px
            - 이미지 크기 (아래 계산 방법 참고): {image_size_px} x {image_size_px} px
            ** **
            - **이미지 크기 계산 = (각 한줄의 cell 개수 + 각 한줄의 좌/우 여백 총 개수) × 1개의 사각 cell 크기**
            ** **
            - 패턴 색상: {pattern_color}
            - 배경 색상: {bg_color}
            """,
        "subheader_download": "📥 다운로드",
        "button_download": "💾 QR 코드 다운로드",
        "download_help": "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다.",
        "download_filename": "📄 다운로드 파일명: ",
        "warning_cannot_generate": "⚠️ 선택하신 설정으로는 QR 코드를 생성할 수 없습니다. 아래의 경고 메시지를 확인해주세요.",
        "warning_pattern_hex": "⚠️ 패턴 색의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다.",
        "warning_bg_hex": "⚠️ 배경 색의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다.",
        "warning_pattern_invalid_hex": "⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
        "warning_bg_invalid_hex": "⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
        "warning_same_color": "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.",
        "info_enter_content": "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 볼 수 있으며, 다운로드도 가능합니다.",
        "button_reset_all": "🔄 전체 초기화",
        "reset_all_help": "모든 내용을 초기화 합니다.",
        "sidebar_header_usage": "📖 사용 방법",
        "usage_guide": """
        1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
        2. **파일 형식**과 **패턴 모양**을 선택하세요
        3. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
        4. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
        5. **파일명 설정**에서 파일명을 지정하세요
        6. 모든 설정이 유효하면 **자동으로 미리보기와 다운로드 버튼이 표시됩니다**
        """,
        "sidebar_header_tips": "💡 용도별 QR 코드 생성 팁",
        "tips_text": "텍스트: QR 코드로 생성할 텍스트를 입력합니다",
        "tips_website": "https://www.example.com",
        "tips_email": "mailto:user@example.com",
        "tips_email_body": "mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용",
        "tips_phone": "tel:type=CELL:+82 10-1234-5678",
        "tips_sms": "sms:type=CELL:+82 10-1234-5678",
        "tips_sms_body": "sms:type=CELL:+82 10-1234-5678?body=메시지 내용",
        "tips_wifi": "WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;",
        "sidebar_header_guide": "⚙️ 설정 가이드",
        "guide_file_format_header": "**파일 형식:**",
        "guide_png": "- **PNG**: 무손실 압축으로 품질 저하가 없으며, 투명 배경을 지원합니다.",
        "guide_jpg": "- **JPG**: 손실 압축으로 파일 크기가 작고, 사진에 주로 사용됩니다. **JPG 품질 슬라이더**로 압축률을 조절할 수 있습니다.",
        "guide_svg": "- **SVG**: 벡터 형식으로 해상도에 영향을 받지 않아 확대해도 깨지지 않습니다.",
        "guide_pattern_shape_header": "**패턴 모양:**",
        "guide_pattern_shape_desc": "- 사각, 둥근사각, 동그라미, 마름모, 별, 십자가 중 선택",
        "guide_pattern_shape_svg_note": "- **SVG** 파일 형식 선택 시에는 **사각**만 지원합니다.",
        "guide_cell_gap_header": "**패턴 간격:**",
        "guide_cell_gap_desc1": "- **사각 패턴**과 **SVG 파일**에서는 지원되지 않습니다.",
        "guide_cell_gap_desc2": "- 슬라이더로 조절하며, 값이 높을수록 패턴의 크기가 작아져 간격이 넓어집니다.",
        "guide_color_header": "**색상 입력:**",
        "guide_color_desc1": "- **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.",
        "guide_color_desc2": "- **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.",
        "guide_color_desc3": "- **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.",
        "guide_qr_settings_header": "**QR 코드 설정:**",
        "guide_error_correction_header": "**오류 보정 레벨:**",
        "guide_error_correction_desc": """
        - **Low (7%)**: 손상되지 않는 환경
        - **Medium (15%)**: 일반적인 사용
        - **Quartile (25%)**: 약간의 손상 가능
        - **High (30%)**: 로고 삽입, 손상이 잦은 환경
        """,
        "guide_mask_pattern_header": "**마스크 패턴:**",
        "guide_mask_pattern_desc": "- 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)",
        "footer_text": "© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)",
        "file_creation_error": "QR 코드 데이터 생성 오류",
        "svg_creation_error": "QR 코드 SVG 생성 오류",
        "error_occurred": "오류가 발생했습니다",
    },
    "en": {
        "page_title": "QR Code Generator",
        "page_icon": "🔲",
        "main_title": "QR Code Generator",
        "separator": "---",
        "header_settings": "⚙️ Input & Settings",
        "subheader_content": "📝 QR Code Content",
        "info_max_chars": "The maximum number of characters you can enter is approximately 2,400 to 2,900, depending on the type.",
        "text_area_label": "Enter the content to be converted into a QR code",
        "text_area_placeholder": "Enter the content for the QR code here.\nCopy and paste is supported.",
        "char_count_error": "⚠️ Current total character count: **{char_count}** (Exceeds recommended maximum)",
        "char_count_warning": "⚠️ Current total character count: **{char_count}** (Approaching recommended character limit)",
        "char_count_success": "✅ Current total character count: **{char_count}**",
        "char_count_caption": "Current total character count: 0",
        "strip_whitespace_label": "Remove all spaces/newlines after the last character",
        "strip_whitespace_help": "If there are spaces or newlines at the end of the content, the QR code will be completely different.",
        "button_clear_text": "🗑️ Clear Content",
        "button_clear_text_help": "Deletes all entered content (keeps filename)",
        "subheader_file_format": "💾 Select File Format",
        "file_format_label": "File Format",
        "file_format_info_jpg": "ℹ️ JPG image quality varies with compression ratio.",
        "jpg_quality_slider": "JPG Quality (Compression Ratio)",
        "jpg_quality_help": "High quality (100) results in a larger, clearer file, while low quality (1) results in a smaller file with reduced quality.",
        "subheader_pattern_shape": "🖼️ Pattern Shape Settings",
        "info_svg_shape": "⚠️ SVG format only supports square patterns.",
        "label_normal_pattern": "Normal Pattern Shape",
        "label_finder_pattern": "Finder Pattern Shape",
        "pattern_shape_options": ("Square", "Rounded Square", "Circle", "Diamond", "Star", "Cross"),
        "info_rounded_corners": "⚠️ SVG format does not support rounded corners.",
        "slider_corner_radius": "Corner Radius (%)",
        "corner_radius_help": "Determines how rounded the corners are. 0% is a square, 50% is close to a circle.",
        "info_cell_gap": "⚠️ Gap adjustment is not supported for 'Square' patterns and 'SVG' files.",
        "slider_cell_gap": "Pattern Gap (%)",
        "cell_gap_help": "Adjust the gap between each pattern. 0% means no gap.",
        "subheader_colors": "🎨 Color Settings",
        "warning_svg_color": "⚠️ SVG files are vector format and currently do not support various colors and patterns. Select 'PNG' or 'JPG' for more styles.",
        "color_direct_input": "<Enter directly>",
        "pattern_color_label": "Pattern Color",
        "bg_color_label": "Background Color",
        "info_hex_color": "If your desired color is not on the list, enter the **HEX code** below.",
        "example_hex": "Example: #FF0000 (Red), #00FF00 (Green), #0000FF (Blue)",
        "placeholder_pattern_hex": "e.g., #000000",
        "placeholder_bg_hex": "e.g., #FFFFFF",
        "subheader_qr_settings": "🔨 QR Code Settings",
        "label_box_size": "QR code cell size (px)",
        "label_border": "QR code border/margin",
        "label_error_correction": "Error Correction Level",
        "error_correction_options": ("Low (7%) - Error Correction", "Medium (15%) - Error Correction", "Quartile (25%) - Error Correction", "High (30%) - Error Correction"),
        "label_mask_pattern": "Mask Pattern Selection (0~7)",
        "subheader_filename": "📄 Filename Settings",
        "placeholder_filename": "Enter the download filename here (autogenerated if left empty)",
        "button_clear_filename": "🗑️ Clear Filename",
        "button_clear_filename_help": "Deletes the entered filename",
        "header_preview_download": "👀 Preview & Download",
        "success_preview": "✅ The QR code has been generated with the current content. Select your desired style and click download below.",
        "subheader_preview": "📱 QR Code Preview",
        "caption_preview": "Generated QR Code",
        "info_qr_details": """
            **[ QR Code Information ]**
            - QR Version: {qr_version}
            ** **
            - Number of cells per row: {modules_count}
            - Total left/right border cells per row: {border_size}
            - Size of one cell: {box_size}px
            - Image size (see calculation below): {image_size_px} x {image_size_px} px
            ** **
            - **Image Size Calculation = (Number of cells per row + Total left/right border cells per row) × Size of one cell**
            ** **
            - Pattern Color: {pattern_color}
            - Background Color: {bg_color}
            """,
        "subheader_download": "📥 Download",
        "button_download": "💾 Download QR Code",
        "download_help": "Saves to the 'Download' folder on PC and mobile devices.",
        "download_filename": "📄 Download Filename: ",
        "warning_cannot_generate": "⚠️ The QR code cannot be generated with the selected settings. Please check the warning messages below.",
        "warning_pattern_hex": "⚠️ Please enter a HEX value for the pattern color. The QR code cannot be generated.",
        "warning_bg_hex": "⚠️ Please enter a HEX value for the background color. The QR code cannot be generated.",
        "warning_pattern_invalid_hex": "⚠️ The HEX value you entered for the pattern color is not a valid color. Please check again.",
        "warning_bg_invalid_hex": "⚠️ The HEX value you entered for the background color is not a valid color. Please check again.",
        "warning_same_color": "⚠️ The pattern and background cannot be the same color.",
        "info_enter_content": "Enter QR code content to preview the generated QR code and enable download.",
        "button_reset_all": "🔄 Reset All",
        "reset_all_help": "Resets all content and settings.",
        "sidebar_header_usage": "📖 How to Use",
        "usage_guide": """
        1. Enter the text to be converted in the **QR Code Content** area.
        2. Select **File Format** and **Pattern Shape**.
        3. Choose pattern and background colors from **Color Settings** (only default colors are available for SVG).
        4. Adjust the size and error correction level in **QR Code Settings**.
        5. Specify the filename in **Filename Settings**.
        6. If all settings are valid, the **preview and download button will be displayed automatically**.
        """,
        "sidebar_header_tips": "💡 QR Code Generation Tips by Use Case",
        "tips_text": "Text: Enter the text to be converted into a QR code",
        "tips_website": "https://www.example.com",
        "tips_email": "mailto:user@example.com",
        "tips_email_body": "mailto:user1@example.com,user2@example.com?subject=Title&body=Message Content",
        "tips_phone": "tel:type=CELL:+82 10-1234-5678",
        "tips_sms": "sms:type=CELL:+82 10-1234-5678",
        "tips_sms_body": "sms:type=CELL:+82 10-1234-5678?body=Message Content",
        "tips_wifi": "WIFI:T:WPA;S:Network Name(SSID);P:Password;H:false;;",
        "sidebar_header_guide": "⚙️ Settings Guide",
        "guide_file_format_header": "**File Format:**",
        "guide_png": "- **PNG**: Lossless compression, no quality degradation, and supports a transparent background.",
        "guide_jpg": "- **JPG**: Lossy compression, small file size, and primarily used for photos. You can adjust the compression ratio with the **JPG quality slider**.",
        "guide_svg": "- **SVG**: Vector format, not affected by resolution, and does not pixelate when enlarged.",
        "guide_pattern_shape_header": "**Pattern Shape:**",
        "guide_pattern_shape_desc": "- Select from Square, Rounded Square, Circle, Diamond, Star, Cross.",
        "guide_pattern_shape_svg_note": "- Only **Square** is supported when selecting the **SVG** file format.",
        "guide_cell_gap_header": "**Pattern Gap:**",
        "guide_cell_gap_desc1": "- Not supported for **Square patterns** and **SVG files**.",
        "guide_cell_gap_desc2": "- Adjust with the slider; a higher value results in smaller patterns and a wider gap.",
        "guide_color_header": "**Color Input:**",
        "guide_color_desc1": "- **Direct Input**: You can directly enter a HEX code for colors not on the list.",
        "guide_color_desc2": "- **Error Messages**: Validity checks are performed during color input, and a warning message will appear if the input is empty or an invalid color value.",
        "guide_color_desc3": "- For the **SVG** file format, only black patterns and white backgrounds are supported.",
        "guide_qr_settings_header": "**QR Code Settings:**",
        "guide_error_correction_header": "**Error Correction Level:**",
        "guide_error_correction_desc": """
        - **Low (7%)**: For environments without damage
        - **Medium (15%)**: For general use
        - **Quartile (25%)**: For slight damage
        - **High (30%)**: For environments with frequent damage or when inserting a logo
        """,
        "guide_mask_pattern_header": "**Mask Pattern:**",
        "guide_mask_pattern_desc": "- Select from 0-7 (the pattern changes based on the number even with the same content)",
        "footer_text": "© 2025 QR Code Generator | Made with Streamlit | Created by: Jong-hoon Ryu (redhat4u@gmail.com)",
        "file_creation_error": "QR Code Data Generation Error",
        "svg_creation_error": "QR Code SVG Generation Error",
        "error_occurred": "An error occurred",
    },
}
