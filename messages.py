"""
# 다국어 지원을 위한 메시지 파일
# messages.py
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
        
        # QR 코드 설정
        'qr_settings_header': '🎨 QR 코드 설정',
        'box_size_slider': '박스 크기',
        'border_slider': '테두리',
        'error_correction_label': '오류 복원 레벨',
        'error_correction_L': '낮음 (7%)',
        'error_correction_M': '보통 (15%)',
        'error_correction_Q': '준고 (25%)',
        'error_correction_H': '높음 (30%)',

        # 색상 옵션
        'pattern_color_label': '패턴 색상',
        'color_black': '검정',
        'color_navy': '네이비',
        'color_dark_green': '진녹색',
        'color_red': '빨강',
        'color_brown': '갈색',
        'color_custom': '직접 입력',
        'pattern_color_custom_input': '패턴 색상 (HEX 코드)',
        
        'background_color_label': '배경 색상',
        'color_white': '하양',
        'color_light_gray': '옅은 회색',
        'color_light_blue': '옅은 파랑',
        'color_light_yellow': '옅은 노랑',
        'color_light_green': '옅은 녹색',
        'background_color_custom_input': '배경 색상 (HEX 코드)',

        # 파일 형식
        'file_format_label': '파일 형식',
        'jpg_quality_slider': 'JPG 품질 (0-100)',
        
        # 미리보기 및 다운로드
        'qr_content_empty_warning': 'QR 코드 내용을 입력해 주세요.',
        'qr_generation_error': 'QR 코드 생성 중 오류가 발생했습니다: {}',
        'preview_header': '미리보기',
        'qr_preview_caption': '생성된 QR 코드',
        'download_header': '다운로드',
        'download_button_label': 'QR 코드 다운로드',

        # 사이드바
        'sidebar_title': '도움말 및 정보',
        'sidebar_help_header': '도움말',
        'sidebar_help_content': 'QR 코드는 다양한 정보를 담을 수 있는 2차원 바코드입니다. 웹사이트 링크, 텍스트, 이메일 주소, 전화번호 등 다양한 정보를 저장할 수 있습니다. QR 코드를 스캔하면 저장된 정보에 쉽게 접근할 수 있습니다.',
        
        'sidebar_file_format_title': '파일 형식:',
        'sidebar_file_format_content': '''
- **PNG**: 무손실 압축으로 품질 저하가 없으며, 투명 배경을 지원합니다.
- **JPG**: 손실 압축으로 파일 크기가 작고, 사진에 주로 사용됩니다. **JPG 품질 슬라이더**로 압축률을 조절할 수 있습니다.
- **SVG**: 벡터 형식으로 해상도에 영향을 받지 않아 확대해도 깨지지 않습니다.
''',
        'sidebar_qr_settings_title': 'QR 코드 설정:',
        'sidebar_error_correction_title': '오류 복원 레벨:',
        'sidebar_error_correction_content': '''
- **낮음 (L)**: 훼손되지 않은 환경에 적합 (약 7% 복원 가능)
- **보통 (M)**: 일반적인 사용에 적합 (약 15% 복원 가능)
- **준고 (Q)**: 일부 훼손된 경우에도 사용 가능 (약 25% 복원 가능)
- **높음 (H)**: 로고 삽입, 자주 훼손되는 환경에 적합 (약 30% 복원 가능)
''',
        'sidebar_mask_pattern_title': '마스크 패턴:',
        'sidebar_mask_pattern_content': '0~7 중에서 선택할 수 있습니다. (동일한 내용도 숫자에 따라 다른 패턴이 될 수 있습니다)',
        
        'sidebar_color_title': '색상 입력:',
        'sidebar_color_content': '''
- **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
- **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
- **SVG** 파일 형식은 패턴과 배경 색상 변경을 지원하지 않습니다.
''',
        
        # 하단 정보
        'footer': '© 2024 QR Code Generator'
    },
    'en': {
        # Page settings
        'page_title': 'QR Code Generator',
        'page_icon': '🔲',
        'main_title': '🔲 QR Code Generator',
        
        # Language selection
        'language_select': 'Select Language',
        
        # Main section headers
        'input_settings_header': '⚙️ Input and Settings',
        'preview_download_header': '👀 Preview and Download',
        
        # QR code input
        'qr_content_header': '📝 QR Code Content',
        'qr_content_info': 'The maximum number of characters you can enter is about 2,400-2,900, depending on the type.',
        'qr_input_label': 'Please enter the content to generate a QR code',
        'qr_input_placeholder': 'Enter the content for your QR code here.\nCopy and paste can be used.',
        
        # Character count
        'char_count_exceeded': '⚠️ Total characters entered: **{}** (exceeds recommended maximum)',
        'char_count_warning': '⚠️ Total characters entered: **{}** (approaching recommended limit)',
        'char_count_success': '✅ Total characters entered: **{}**',
        
        # QR code settings
        'qr_settings_header': '🎨 QR Code Settings',
        'box_size_slider': 'Box Size',
        'border_slider': 'Border',
        'error_correction_label': 'Error Correction Level',
        'error_correction_L': 'Low (7%)',
        'error_correction_M': 'Medium (15%)',
        'error_correction_Q': 'Quartile (25%)',
        'error_correction_H': 'High (30%)',

        # Color options
        'pattern_color_label': 'Pattern Color',
        'color_black': 'Black',
        'color_navy': 'Navy',
        'color_dark_green': 'Dark Green',
        'color_red': 'Red',
        'color_brown': 'Brown',
        'color_custom': 'Custom',
        'pattern_color_custom_input': 'Pattern Color (HEX Code)',
        
        'background_color_label': 'Background Color',
        'color_white': 'White',
        'color_light_gray': 'Light Gray',
        'color_light_blue': 'Light Blue',
        'color_light_yellow': 'Light Yellow',
        'color_light_green': 'Light Green',
        'background_color_custom_input': 'Background Color (HEX Code)',

        # File format
        'file_format_label': 'File Format',
        'jpg_quality_slider': 'JPG Quality (0-100)',

        # Preview and download
        'qr_content_empty_warning': 'Please enter content for the QR code.',
        'qr_generation_error': 'An error occurred while generating the QR code: {}',
        'preview_header': 'Preview',
        'qr_preview_caption': 'Generated QR Code',
        'download_header': 'Download',
        'download_button_label': 'Download QR Code',

        # Sidebar
        'sidebar_title': 'Help & Info',
        'sidebar_help_header': 'Help',
        'sidebar_help_content': 'A QR code is a 2D barcode that can hold various types of information. It can store website links, text, email addresses, phone numbers, and more. You can easily access the stored information by scanning the QR code.',
        
        'sidebar_file_format_title': 'File Format:',
        'sidebar_file_format_content': '''
- **PNG**: Lossless compression with no quality loss and supports transparent backgrounds.
- **JPG**: Lossy compression results in a smaller file size, primarily used for photos. The **JPG Quality slider** can be used to adjust the compression rate.
- **SVG**: Vector format that is not affected by resolution and does not pixelate when enlarged.
''',
        'sidebar_qr_settings_title': 'QR Code Settings:',
        'sidebar_error_correction_title': 'Error Correction Levels:',
        'sidebar_error_correction_content': '''
- **Low (L)**: Suitable for an undamaged environment (approx. 7% recoverable)
- **Medium (M)**: Suitable for general use (approx. 15% recoverable)
- **Quartile (Q)**: Usable even if partially damaged (approx. 25% recoverable)
- **High (H)**: Suitable for logo insertion or environments with frequent damage (approx. 30% recoverable)
''',
        'sidebar_mask_pattern_title': 'Mask Pattern:',
        'sidebar_mask_pattern_content': 'You can select from 0-7. (The same content can have a different pattern depending on the number)',
        
        'sidebar_color_title': 'Color Input:',
        'sidebar_color_content': '''
- **Custom Input**: Colors not in the list can be entered directly using HEX codes.
- **Error Messages**: Color input validation shows warning messages when input fields are empty or contain invalid color values.
- **SVG** file format does not support pattern and background color changes.
''',
        
        # Footer
        'footer': '© 2024 QR Code Generator'
    }
}
