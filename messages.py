# messages.py

# 한국어 메시지
MESSAGES_KR = {
    # 페이지 및 UI
    "page_title": "QR 코드 생성기",
    "main_title": "🔲 QR 코드 생성기",
    "separator": "---",
    "header_settings": "⚙️ 입력 및 설정",
    "subheader_content": "📝 QR 코드 내용",
    "info_max_chars": "최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.",
    "text_area_label": "QR 코드로 생성할 내용을 입력해 주세요",
    "text_area_placeholder": "이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.",
    "char_count_exceeded_error": "⚠️ 현재 입력된 총 문자 수: **{}** (권장 최대 문자 수 초과)",
    "char_count_warning": "⚠️ 현재 입력된 총 문자 수: **{}** (권장 문자 수에 근접)",
    "char_count_success": "✅ 현재 입력된 총 문자 수: **{}**",
    "char_count_caption": "현재 입력된 총 문자 수: 0",
    "strip_option_label": "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
    "strip_option_help": "입력한 내용 마지막에 공백이나 줄바꿈이 있을 경우 QR 코드는 완전히 달라집니다.",
    "delete_content_button": "🗑️ 입력 내용 삭제",
    "delete_content_help": "입력한 내용을 전부 삭제합니다 (파일명은 유지)",
    
    # 파일 형식
    "subheader_file_format": "💾 파일 형식 선택",
    "file_format_label": "파일 형식",
    "jpg_info_caption": "ℹ️ JPG는 압축률에 따라 이미지 품질이 달라집니다.",
    "jpg_quality_label": "JPG 품질 (압축률)",
    "jpg_quality_help": "높은 품질(100)은 파일 크기가 크고 선명하며, 낮은 품질(1)은 파일 크기가 작고 화질이 저하됩니다.",
    
    # 패턴 모양
    "subheader_pattern_shape": "🖼️ 패턴 모양 설정",
    "svg_shape_warning": "⚠️ SVG 형식은 사각만 지원합니다.",
    "pattern_shape_label": "일반 패턴 모양",
    "finder_pattern_shape_label": "파인더 패턴 모양",
    "rounded_corners_radius_label": "둥근 모서리 반경 (%)",
    "rounded_corners_radius_help": "모서리를 얼마나 둥글게 할지 결정합니다. 0%는 사각, 50%는 원에 가까워집니다.",
    "svg_no_rounded_corners_warning": "⚠️ SVG 형식은 둥근 모서리를 지원하지 않습니다.",
    "cell_gap_label": "패턴 간격 (%)",
    "cell_gap_help": "각 패턴 사이의 간격을 조절합니다. 0%는 간격 없음.",
    "no_gap_warning": "⚠️ '사각' 패턴과 'SVG' 형식은 간격 조절을 지원하지 않습니다.",

    # 색상 설정
    "subheader_color_settings": "🎨 색상 설정",
    "svg_color_warning": "⚠️ SVG 파일은 벡터 형식으로 현재는 다양한 색상과 패턴을 지원하지 않습니다. 여러가지 스타일을 원한다면 'PNG' 또는 'JPG' 형식을 선택하세요.",
    "direct_input_color_option": "<직접 입력>",
    "pattern_color_label": "패턴 색상",
    "bg_color_label": "배경 색상",
    "hex_code_info": "원하는 색상이 리스트에 없다면, 아래에 직접 **HEX 코드**를 입력하세요.",
    "hex_code_caption": "예: #FF0000 (빨강), #00FF00 (초록), #0000FF (파랑)",
    "pattern_hex_input_label": "패턴 색상 HEX 값",
    "bg_hex_input_label": "배경 색상 HEX 값",
    "hex_input_placeholder": "예: #000000",
    "bg_hex_input_placeholder": "예: #FFFFFF",
    
    # QR 코드 설정
    "subheader_qr_settings": "🔨 QR 코드 설정",
    "box_size_label": "QR 코드 1개의 사각 cell 크기 (px)",
    "border_label": "QR 코드 테두리/여백",
    "error_correction_label": "오류 보정 레벨",
    "mask_pattern_label": "마스크 패턴 선택 (0~7)",
    "error_correction_options_low": "Low (7%) - 오류 보정",
    "error_correction_options_medium": "Medium (15%) - 오류 보정",
    "error_correction_options_quartile": "Quartile (25%) - 오류 보정",
    "error_correction_options_high": "High (30%) - 오류 보정",
    
    # 파일명 설정
    "subheader_filename": "📄 파일명 설정",
    "filename_input_label": "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)",
    "filename_placeholder": "이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
    "delete_filename_button": "🗑️ 파일명 삭제",
    "delete_filename_help": "입력한 파일명을 삭제합니다",
    
    # 미리보기 및 다운로드
    "header_preview_download": "👀 미리보기 및 다운로드",
    "success_message": "✅ 현재 입력된 내용으로 QR 코드를 생성하였습니다. 원하는 스타일로 선택한 후 아래의 다운로드를 클릭하세요.",
    "subheader_preview": "📱 QR 코드 미리보기",
    "preview_caption": "생성된 QR 코드",
    "qr_info_title": "**[ QR 코드 정보 ]**",
    "qr_version": "- QR 버전: {}",
    "qr_cells": "- 각 한줄의 cell 개수: {}개",
    "qr_border_cells": "- 각 한줄의 좌/우 여백 총 개수: {}개",
    "qr_box_size": "- 1개의 사각 cell 크기: {}px",
    "qr_image_size": "- 이미지 크기 (아래 계산 방법 참고): {} x {} px",
    "qr_calc_method": "**이미지 크기 계산 = (각 한줄의 cell 개수 + 각 한줄의 좌/우 여백 총 개수) × 1개의 사각 cell 크기**",
    "qr_pattern_color": "- 패턴 색상: {}",
    "qr_bg_color": "- 배경 색상: {}",
    "subheader_download": "📥 다운로드",
    "download_button_label": "💾 QR 코드 다운로드",
    "download_button_help": "PC는 'Download' 폴더, 휴대폰은 'Download' 폴더에 저장됩니다.",
    "download_filename_display": "📄 다운로드 파일명:",
    "download_error_warning": "⚠️ 선택하신 설정으로는 QR 코드를 생성할 수 없습니다. 아래의 경고 메시지를 확인해주세요.",
    "hex_input_missing_warning": "⚠️ {}의 HEX 값을 입력해 주세요. QR 코드를 생성할 수 없습니다.",
    "hex_input_invalid_warning": "⚠️ {}로 입력한 HEX 값은 올바른 색상 값이 아닙니다. 다시 확인해주세요.",
    "same_color_warning": "⚠️ 패턴과 배경은 같은 색을 사용할 수 없습니다.",
    "no_content_info": "QR 코드 내용을 입력하면 생성될 QR 코드를 미리 볼 수 있으며, 다운로드도 가능합니다.",
    "reset_button_label": "🔄 전체 초기화",
    "reset_button_help": "모든 내용을 초기화 합니다.",
    
    # 사이드바
    "sidebar_guide_title": "📖 사용 방법",
    "sidebar_guide_1": "1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요",
    "sidebar_guide_2": "2. **파일 형식**과 **패턴 모양**을 선택하세요",
    "sidebar_guide_3": "3. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)",
    "sidebar_guide_4": "4. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요",
    "sidebar_guide_5": "5. **파일명 설정**에서 파일명을 지정하세요",
    "sidebar_guide_6": "6. 모든 설정이 유효하면 **자동으로 미리보기와 다운로드 버튼이 표시됩니다**",
    "sidebar_tips_title": "💡 용도별 QR 코드 생성 팁",
    "tip_text": "- **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`",
    "tip_website": "- **웹사이트**: `https://www.example.com`",
    "tip_email": "- **이메일**: `mailto:user@example.com`",
    "tip_email_full": "- **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`",
    "tip_phone": "- **전화번호**: `tel:type=CELL:+82 10-1234-5678`",
    "tip_sms": "- **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`",
    "tip_sms_full": "- **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`",
    "tip_wifi": "- **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`",
    "sidebar_settings_title": "⚙️ 설정 가이드",
    "sidebar_file_format_title": "**파일 형식:**",
    "sidebar_png_desc": "- **PNG**: 무손실 압축으로 품질 저하가 없으며, 투명 배경을 지원합니다.",
    "sidebar_jpg_desc": "- **JPG**: 손실 압축으로 파일 크기가 작고, 사진에 주로 사용됩니다. **JPG 품질 슬라이더**로 압축률을 조절할 수 있습니다.",
    "sidebar_svg_desc": "- **SVG**: 벡터 형식으로 해상도에 영향을 받지 않아 확대해도 깨지지 않습니다.",
    "sidebar_pattern_shape_title": "**패턴 모양:**",
    "sidebar_pattern_shape_desc": "- 사각, 둥근사각, 동그라미, 마름모, 별, 십자가 중 선택",
    "sidebar_pattern_shape_warning": "- **SVG** 파일 형식 선택 시에는 **사각**만 지원합니다.",
    "sidebar_cell_gap_title": "**패턴 간격:**",
    "sidebar_cell_gap_desc_1": "- **사각 패턴**과 **SVG 파일**에서는 지원되지 않습니다.",
    "sidebar_cell_gap_desc_2": "- 슬라이더로 조절하며, 값이 높을수록 패턴의 크기가 작아져 간격이 넓어집니다.",
    "sidebar_color_input_title": "**색상 입력:**",
    "sidebar_color_input_desc_1": "- **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.",
    "sidebar_color_input_desc_2": "- **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.",
    "sidebar_color_input_desc_3": "- **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.",
    "sidebar_qr_settings_title": "**QR 코드 설정:**",
    "sidebar_error_correction_title": "**오류 보정 레벨:**",
    "sidebar_error_correction_low": "- **Low (7%)**: 손상되지 않는 환경",
    "sidebar_error_correction_medium": "- **Medium (15%)**: 일반적인 사용",
    "sidebar_error_correction_quartile": "- **Quartile (25%)**: 약간의 손상 가능",
    "sidebar_error_correction_high": "- **High (30%)**: 로고 삽입, 손상이 잦은 환경",
    "sidebar_mask_pattern_title": "**마스크 패턴:**",
    "sidebar_mask_pattern_desc": "- 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)",
    "footer_info": '© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)',
}

def get_message(lang_code, key, *args):
    """지정된 언어 코드와 키에 해당하는 메시지를 반환합니다."""
    messages = {}
    if lang_code == 'ko':
        messages = MESSAGES_KR
    
    msg = messages.get(key, f"Translation missing for key: {key}")
    return msg.format(*args)
    
