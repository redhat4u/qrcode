"""
다국어 지원을 위한 메시지 파일
"""

MESSAGES = {
    'ko': {
        # 페이지 설정
        'page_title': 'QR 코드 생성기',
        'page_icon': '🔲',
        'main_title': '🔲 QR 코드 생성기',
        
        # 언어 선택
        'language_select': '언어 선택',
        
        # 메인 섹션 헤더
        'input_settings_header': '⚙️ 입력 및 설정',
        'preview_download_header': '👀 미리보기 및 다운로드',
        
        # QR 코드 입력
        'qr_content_header': '📝 QR 코드 내용',
        'qr_content_info': '최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.',
        'qr_input_label': 'QR 코드로 생성할 내용을 입력해 주세요',
        'qr_input_placeholder': '이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.',
        
        # 문자 수 표시
        'char_count_exceeded': '⚠️ 현재 입력된 총 문자 수: **{}** (권장 최대 문자 수 초과)',
        'char_count_warning': '⚠️ 현재 입력된 총 문자 수: **{}** (권장 문자 수에 근접)',
        'char_count_success': '✅ 현재 입력된 총 문자 수: **{}**',
        'char_count_zero': '현재 입력된 총 문자 수: 0',
        
        # 공백/줄바꿈 제거 옵션
        'strip_option_label': '마지막 입력문자 이후 모든 공백/줄바꿈 제거',
        'strip_option_help': '입력한 내용 마지막에 공백이나 줄바꿈이 있을 경우 QR 코드는 완전히 달라집니다.',
        
        # 버튼
        'delete_content_btn': '🗑️ 입력 내용 삭제',
        'delete_content_help': '입력한 내용을 전부 삭제합니다 (파일명은 유지)',
        'delete_filename_btn': '🗑️ 파일명 삭제',
        'delete_filename_help': '입력한 파일명을 삭제합니다',
        'reset_all_btn': '🔄 전체 초기화',
        'reset_all_help': '모든 내용을 초기화 합니다.',
        
        # 파일 형식
        'file_format_header': '📄 파일 형식 선택',
        'file_format_label': '파일 형식',
        'jpg_quality_info': 'ℹ️ JPG는 압축률에 따라 이미지 품질이 달라집니다.',
        'jpg_quality_label': 'JPG 품질 (압축률)',
        'jpg_quality_help': '높은 품질(100)은 파일 크기가 크고 선명하며, 낮은 품질(1)은 파일 크기가 작고 화질이 저하됩니다.',
        
        # 패턴 모양
        'pattern_shape_header': '🖼️ 패턴 모양 설정',
        'svg_shape_warning': '⚠️ SVG 형식은 사각만 지원합니다.',
        'normal_pattern_label': '일반 패턴 모양',
        'finder_pattern_label': '파인더 패턴 모양',
        'corner_radius_warning': '⚠️ SVG 형식은 둥근 모서리를 지원하지 않습니다.',
        'corner_radius_label': '둥근 모서리 반경 (%)',
        'corner_radius_help': '모서리를 얼마나 둥글게 할지 결정합니다. 0%는 사각, 50%는 원에 가까워집니다.',
        'cell_gap_warning': '⚠️ \'사각\' 패턴과 \'SVG\' 형식은 간격 조절을 지원하지 않습니다.',
        'cell_gap_label': '패턴 간격 (%)',
        'cell_gap_help': '각 패턴 사이의 간격을 조절합니다. 0%는 간격 없음.',
        
        # 패턴 옵션
        'pattern_square': '사각',
        'pattern_rounded': '둥근사각',
        'pattern_circle': '동그라미',
        'pattern_diamond': '마름모',
        'pattern_star': '별',
        'pattern_cross': '십자가',
        
        # 색상 설정
        'color_settings_header': '🎨 색상 설정',
        'svg_color_warning': '⚠️ SVG 파일은 벡터 형식으로 현재는 다양한 색상과 패턴을 지원하지 않습니다. 여러가지 스타일을 원한다면 \'PNG\' 또는 \'JPG\' 형식을 선택하세요.',
        'pattern_color_label': '패턴 색상',
        'bg_color_label': '배경 색상',
        'custom_color_info': '원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.',
        'hex_example': '예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)',
        'pattern_hex_label': '패턴 색상 HEX 값',
        'bg_hex_label': '배경 색상 HEX 값',
        'hex_placeholder': '예: #000000',
        'hex_placeholder_white': '예: #FFFFFF',
        'custom_input': '<직접 입력>',
        
        # QR 코드 설정
        'qr_settings_header': '🔨 QR 코드 설정',
        'box_size_label': 'QR 코드 1개의 사각 cell 크기 (px)',
        'border_label': 'QR 코드 테두리/여백',
        'error_correction_label': '오류 보정 레벨',
        'mask_pattern_label': '마스크 패턴 선택 (0~7)',
        
        # 오류 보정 옵션
        'error_low': 'Low (7%) - 오류 보정',
        'error_medium': 'Medium (15%) - 오류 보정',
        'error_quartile': 'Quartile (25%) - 오류 보정',
        'error_high': 'High (30%) - 오류 보정',
        
        # 파일명 설정
        'filename_header': '💾 파일명 설정',
        'filename_input_label': '다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)',
        'filename_placeholder': '이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)',
        
        # 미리보기 및 다운로드
        'qr_preview_success': '✅ 현재 입력된 내용으로 QR 코드를 생성하였습니다. 원하는 스타일로 선택한 후 아래의 다운로드를 클릭하세요.',
        'qr_preview_header': '📱 QR 코드 미리보기',
        'qr_caption': '생성된 QR 코드',
        'qr_info_title': '**[ QR 코드 정보 ]**',
        'qr_version': 'QR 버전: {}',
        'modules_count': '각 한줄의 cell 개수: {}개',
        'border_count': '각 한줄의 좌/우 여백 총 개수: {}개',
        'cell_size': '1개의 사각 cell 크기: {}px',
        'image_size': '이미지 크기 (아래 계산 방법 참고): {} x {} px',
        'size_calculation': '**이미지 크기 계산 = (각 한줄의 cell 개수 + 각 한줄의 좌/우 여백 총 개수) × 1개의 사각 cell 크기**',
        'pattern_color_info': '패턴 색상: {}',
        'bg_color_info': '배경 색상: {}',
        
        # 다운로드
        'download_header': '📥 다운로드',
        'download_btn': '💾 QR 코드 다운로드',
        'download_help': 'PC는 \'Download\' 폴더, 휴대폰은 \'Download\' 폴더에 저장됩니다.',
        'download_filename': '📄 다운로드 파일명: ',
        
        # 경고 메시지
        'generation_warning': '⚠️ 선택하신 설정으로는 QR 코드를 생성할 수 없습니다. 아래의 경고 메시지를 확인해주세요.',
        'pattern_hex_empty': '⚠️ 패턴 색의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다.',
        'bg_hex_empty': '⚠️ 배경 색의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다.',
        'pattern_hex_invalid': '⚠️ 패턴 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.',
        'bg_hex_invalid': '⚠️ 배경 색으로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.',
        'same_color_warning': '⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.',
        'input_content_info': 'QR 코드 내용을 입력하면 생성될 QR 코드를 미리 볼 수 있으며, 다운로드도 가능합니다.',
        
        # 오류 메시지
        'qr_data_error': 'QR 코드 데이터 생성 오류: {}',
        'qr_svg_error': 'QR 코드 SVG 생성 오류: {}',
        'generation_error': '오류가 발생했습니다: {}',
        
        # 사이드바
        'sidebar_usage_title': '📖 사용 방법',
        'sidebar_usage_content': '''
1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
2. **파일 형식**과 **패턴 모양**을 선택하세요
3. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
4. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
5. **파일명 설정**에서 파일명을 지정하세요
6. 모든 설정이 유효하면 **자동으로 미리보기와 다운로드 버튼이 표시됩니다**
        ''',
        
        'sidebar_tips_title': '💡 용도별 QR 코드 생성 팁',
        'sidebar_tips_content': '''
- **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
- **웹사이트**: `https://www.example.com`
- **이메일**: `mailto:user@example.com`
- **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
- **전화번호**: `tel:type=CELL:+82 10-1234-5678`
- **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
- **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
- **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
        ''',
        
        'sidebar_guide_title': '⚙️ 설정 가이드',
        'sidebar_file_format_title': '**파일 형식:**',
        'sidebar_file_format_content': '''
- **PNG**: 무손실 압축으로 품질 저하가 없으며, 투명 배경을 지원합니다.
- **JPG**: 손실 압축으로 파일 크기가 작고, 사진에 주로 사용됩니다. **JPG 품질 슬라이더**로 압축률을 조절할 수 있습니다.
- **SVG**: 벡터 형식으로 해상도에 영향을 받지 않아 확대해도 깨지지 않습니다.
        ''',
        
        'sidebar_pattern_title': '**패턴 모양:**',
        'sidebar_pattern_content': '''
- 사각, 둥근사각, 동그라미, 마름모, 별, 십자가 중 선택
- **SVG** 파일 형식 선택 시에는 **사각**만 지원합니다.
        ''',
        
        'sidebar_gap_title': '**패턴 간격:**',
        'sidebar_gap_content': '''
- **사각 패턴**과 **SVG 파일**에서는 지원되지 않습니다.
- 슬라이더로 조절하며, 값이 높을수록 패턴의 크기가 작아져 간격이 넓어집니다.
        ''',
        
        'sidebar_color_title': '**색상 입력:**',
        'sidebar_color_content': '''
- **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
- **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
- **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.
        ''',
        
        'sidebar_qr_settings_title': '**QR 코드 설정:**',
        'sidebar_error_correction_title': '**오류 보정 레벨:**',
        'sidebar_error_correction_content': '''
- **Low (7%)**: 손상되지 않는 환경
- **Medium (15%)**: 일반적인 사용
- **Quartile (25%)**: 약간의 손상 가능
- **High (30%)**: 로고 삽입, 손상이 잦은 환경
        ''',
        
        'sidebar_mask_pattern_title': '**마스크 패턴:**',
        'sidebar_mask_pattern_content': '''
- 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
        ''',
        
        # 하단 정보
        'footer': '© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)',
    },
    
    'en': {
        # 페이지 설정
        'page_title': 'QR Code Generator',
        'page_icon': '🔲',
        'main_title': '🔲 QR Code Generator',
        
        # 언어 선택
        'language_select': 'Select Language',
        
        # 메인 섹션 헤더
        'input_settings_header': '⚙️ Input & Settings',
        'preview_download_header': '👀 Preview & Download',
        
        # QR 코드 입력
        'qr_content_header': '📝 QR Code Content',
        'qr_content_info': 'Maximum input characters are approximately 2,400~2,900 depending on the type.',
        'qr_input_label': 'Enter the content to generate QR code',
        'qr_input_placeholder': 'Enter the content to generate QR code here.\nYou can use copy/paste.',
        
        # 문자 수 표시
        'char_count_exceeded': '⚠️ Current total character count: **{}** (Exceeds recommended maximum)',
        'char_count_warning': '⚠️ Current total character count: **{}** (Approaching recommended limit)',
        'char_count_success': '✅ Current total character count: **{}**',
        'char_count_zero': 'Current total character count: 0',
        
        # 공백/줄바꿈 제거 옵션
        'strip_option_label': 'Remove all spaces/line breaks after the last input character',
        'strip_option_help': 'If there are spaces or line breaks at the end of your input, the QR code will be completely different.',
        
        # 버튼
        'delete_content_btn': '🗑️ Delete Content',
        'delete_content_help': 'Delete all input content (filename is preserved)',
        'delete_filename_btn': '🗑️ Delete Filename',
        'delete_filename_help': 'Delete the entered filename',
        'reset_all_btn': '🔄 Reset All',
        'reset_all_help': 'Reset all content.',
        
        # 파일 형식
        'file_format_header': '📄 File Format Selection',
        'file_format_label': 'File Format',
        'jpg_quality_info': 'ℹ️ JPG image quality varies depending on compression ratio.',
        'jpg_quality_label': 'JPG Quality (Compression)',
        'jpg_quality_help': 'High quality (100) results in large file size and sharp images, low quality (1) results in small file size and degraded quality.',
        
        # 패턴 모양
        'pattern_shape_header': '🖼️ Pattern Shape Settings',
        'svg_shape_warning': '⚠️ SVG format only supports squares.',
        'normal_pattern_label': 'Normal Pattern Shape',
        'finder_pattern_label': 'Finder Pattern Shape',
        'corner_radius_warning': '⚠️ SVG format does not support rounded corners.',
        'corner_radius_label': 'Corner Radius (%)',
        'corner_radius_help': 'Determines how rounded the corners will be. 0% is square, 50% is close to circle.',
        'cell_gap_warning': '⚠️ \'Square\' patterns and \'SVG\' format do not support gap adjustment.',
        'cell_gap_label': 'Pattern Gap (%)',
        'cell_gap_help': 'Adjusts the gap between each pattern. 0% means no gap.',
        
        # 패턴 옵션
        'pattern_square': 'Square',
        'pattern_rounded': 'Rounded Square',
        'pattern_circle': 'Circle',
        'pattern_diamond': 'Diamond',
        'pattern_star': 'Star',
        'pattern_cross': 'Cross',
        
        # 색상 설정
        'color_settings_header': '🎨 Color Settings',
        'svg_color_warning': '⚠️ SVG files are vector format and currently do not support various colors and patterns. If you want multiple styles, select \'PNG\' or \'JPG\' format.',
        'pattern_color_label': 'Pattern Color',
        'bg_color_label': 'Background Color',
        'custom_color_info': 'If the desired color is not in the list, enter the **HEX code** directly below.',
        'hex_example': 'Example: #FF0000 (Red), #00FF00 (Green), #0000FF (Blue)',
        'pattern_hex_label': 'Pattern Color HEX Value',
        'bg_hex_label': 'Background Color HEX Value',
        'hex_placeholder': 'e.g.: #000000',
        'hex_placeholder_white': 'e.g.: #FFFFFF',
        'custom_input': '<Custom Input>',
        
        # QR 코드 설정
        'qr_settings_header': '🔨 QR Code Settings',
        'box_size_label': 'QR code cell size (px)',
        'border_label': 'QR code border/margin',
        'error_correction_label': 'Error Correction Level',
        'mask_pattern_label': 'Mask Pattern Selection (0~7)',
        
        # 오류 보정 옵션
        'error_low': 'Low (7%) - Error Correction',
        'error_medium': 'Medium (15%) - Error Correction',
        'error_quartile': 'Quartile (25%) - Error Correction',
        'error_high': 'High (30%) - Error Correction',
        
        # 파일명 설정
        'filename_header': '💾 Filename Settings',
        'filename_input_label': 'Enter download filename (exclude extension, filename only)',
        'filename_placeholder': 'Enter filename here (auto-generated if empty)',
        
        # 미리보기 및 다운로드
        'qr_preview_success': '✅ QR code has been generated with the currently entered content. Select your desired style and click download below.',
        'qr_preview_header': '📱 QR Code Preview',
        'qr_caption': 'Generated QR Code',
        'qr_info_title': '**[ QR Code Information ]**',
        'qr_version': 'QR Version: {}',
        'modules_count': 'Cells per row: {}',
        'border_count': 'Total border cells per row: {}',
        'cell_size': 'Cell size: {}px',
        'image_size': 'Image size (see calculation below): {} x {} px',
        'size_calculation': '**Image size calculation = (Cells per row + Total border cells) × Cell size**',
        'pattern_color_info': 'Pattern color: {}',
        'bg_color_info': 'Background color: {}',
        
        # 다운로드
        'download_header': '📥 Download',
        'download_btn': '💾 Download QR Code',
        'download_help': 'Saved to \'Download\' folder on PC, \'Download\' folder on mobile.',
        'download_filename': '📄 Download filename: ',
        
        # 경고 메시지
        'generation_warning': '⚠️ Cannot generate QR code with the selected settings. Please check the warning messages below.',
        'pattern_hex_empty': '⚠️ Please enter HEX value for pattern color. Cannot generate QR code.',
        'bg_hex_empty': '⚠️ Please enter HEX value for background color. Cannot generate QR code.',
        'pattern_hex_invalid': '⚠️ The HEX value entered for pattern color is not a valid color value. Please check again.',
        'bg_hex_invalid': '⚠️ The HEX value entered for background color is not a valid color value. Please check again.',
        'same_color_warning': '⚠️ Pattern and background cannot use the same color.',
        'input_content_info': 'Enter QR code content to preview the generated QR code and enable download.',
        
        # 오류 메시지
        'qr_data_error': 'QR code data generation error: {}',
        'qr_svg_error': 'QR code SVG generation error: {}',
        'generation_error': 'An error occurred: {}',
        
        # 사이드바
        'sidebar_usage_title': '📖 How to Use',
        'sidebar_usage_content': '''
1. Enter the text to convert in the **QR Code Content** area
2. Select **File Format** and **Pattern Shape**
3. Choose pattern and background colors in **Color Settings** (SVG format supports basic colors only)
4. Adjust size and error correction level in **QR Code Settings**
5. Specify filename in **Filename Settings**
6. **Preview and download button will appear automatically** when all settings are valid
        ''',
        
        'sidebar_tips_title': '💡 QR Code Generation Tips by Purpose',
        'sidebar_tips_content': '''
- **Text**: `Enter text to generate QR code`
- **Website**: `https://www.example.com`
- **Email**: `mailto:user@example.com`
- **Email (with subject, body, multiple recipients)**: `mailto:user1@example.com,user2@example.com?subject=Subject&body=Message content`
- **Phone**: `tel:type=CELL:+82 10-1234-5678`
- **SMS (number only)**: `sms:type=CELL:+82 10-1234-5678`
- **SMS (with message)**: `sms:type=CELL:+82 10-1234-5678?body=Message content`
- **WiFi**: `WIFI:T:WPA;S:NetworkName(SSID);P:Password;H:false;;`
        ''',
        
        'sidebar_guide_title': '⚙️ Settings Guide',
        'sidebar_file_format_title': '**File Formats:**',
        'sidebar_file_format_content': '''
- **PNG**: Lossless compression with no quality degradation, supports transparent background.
- **JPG**: Lossy compression with smaller file size, mainly used for photos. **JPG quality slider** allows compression ratio adjustment.
- **SVG**: Vector format that is resolution-independent and doesn\'t pixelate when enlarged.
        ''',
        
        'sidebar_pattern_title': '**Pattern Shapes:**',
        'sidebar_pattern_content': '''
- Choose from Square, Rounded Square, Circle, Diamond, Star, Cross
- **SVG** file format only supports **Square**.
        ''',
        
        'sidebar_gap_title': '**Pattern Gap:**',
        'sidebar_gap_content': '''
- Not supported for **Square patterns** and **SVG files**.
- Adjust with slider, higher values make patterns smaller with wider gaps.
        ''',
        
        'sidebar_color_title': '**Color Input:**',
        'sidebar_color_content': '''
- **Custom Input**: Colors not in the list can be entered directly using HEX codes.
- **Error Messages**: Color input validation shows warning messages when input fields are empty or contain invalid color values.
- **SVG** file format only supports pattern:black, background:white.
        ''',
        
        'sidebar_qr_settings_title': '**QR Code Settings:**',
        'sidebar_error_correction_title': '**Error Correction Levels:**',
        'sidebar_error_correction_content': '''
- **Low (7%)**: Undamaged environment
- **Medium (15%)**: General use
- **Quartile (25%)**: Slightly damaged possible
- **High (30%)**: Logo insertion, frequently damaged environment
        ''',
        
        'sidebar_mask_pattern_title': '**Mask Pattern:**',
        'sidebar_mask_pattern_content': '''
- Choose from 0~7 (same content can have different patterns depending on number)
        ''',
        
        # 하단 정보
        'footer': '© 2025 QR Code Generator  |  Built with Streamlit  |  Created by: Jonghun Ryu(redhat4u@gmail.com)',
    }
}
