'''
QR 코드 생성 웹앱 - Streamlit 버전
휴대폰에서도 사용 가능

실행 방법:
1. pip install streamlit qrcode[pil]
2. streamlit run qrcode_web.py

또는 온라인에서 실행:
- Streamlit Cloud, Heroku, Replit 등에 배포 가능
'''

import streamlit as st
import qrcode
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔲",
    layout="wide"
)

# 파일명에 특수문자 포함시 '_' 문자로 치환
def sanitize_filename(name: str) -> str:
    invalid_chars = '\\/:*?"<>|[]'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()

# QR 코드 생성 함수
def generate_qr_code(data, box_size, border, error_correction, mask_pattern, fill_color, back_color):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            mask_pattern=mask_pattern,
        )
        
        qr.add_data(data, optimize=0)
        qr.make(fit=True)
        
        # QR 코드 이미지 생성
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Streamlit과 호환되도록 PIL Image로 확실히 변환
        if hasattr(img, 'convert'):
            img = img.convert('RGB')
        else:
            # PIL Image가 아닌 경우 BytesIO를 통해 변환
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img = Image.open(img_buffer)
        
        return img, qr
    except Exception as e:
        st.error(f"QR 코드 생성 오류: {str(e)}")
        return None, None


# 세션 상태 초기화
if 'qr_generated' not in st.session_state:
    st.session_state.qr_generated = False
if 'qr_image_bytes' not in st.session_state:
    st.session_state.qr_image_bytes = None
if 'qr_image' not in st.session_state:
    st.session_state.qr_image = None
if 'qr_info' not in st.session_state:
    st.session_state.qr_info = None
if 'preview_image' not in st.session_state:
    st.session_state.preview_image = None
if 'preview_info' not in st.session_state:
    st.session_state.preview_info = None
if 'last_preview_data' not in st.session_state:
    st.session_state.last_preview_data = ""

# 텍스트 영역 초기화를 위한 함수
def clear_text_input():
    # 위젯의 키를 직접 조작하는 대신 초기화 플래그 사용
    st.session_state.clear_requested = True
    st.session_state.qr_generated = False
    st.session_state.qr_image_bytes = None
    st.session_state.qr_image = None  
    st.session_state.qr_info = None
    st.session_state.preview_image = None
    st.session_state.preview_info = None
    st.session_state.last_preview_data = ""
    st.session_state.filename_input = ""

# 초기화 플래그 추가
if 'clear_requested' not in st.session_state:
    st.session_state.clear_requested = False


# 메인 앱 ============================================================================================
st.title("🔲 QR 코드 생성기")
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header("⚙️ 입력 및 설정")
    
    # QR 코드 입력창
    st.subheader("📝 QR 코드 내용")
    st.info("최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.")
    
    # 초기화 요청이 있으면 빈 값으로 시작
    default_value = "" if st.session_state.clear_requested else st.session_state.get("qr_input_area", "")
    
    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=200,
        placeholder="이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다.",
        value=default_value,
        key="qr_input_area"
    )
    
    # 초기화 플래그 리셋
    if st.session_state.clear_requested:
        st.session_state.clear_requested = False
    
    # 문자 수 표시
    char_count = len(qr_data) if qr_data else 0
    
    # 문자 수에 따른 상태 메시지 표시
    if char_count > 0:
        if char_count > 2900:
            st.error(f"⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 최대 문자 수 초과)")
        elif char_count > 2400:
            st.warning(f"⚠️ 현재 입력된 총 문자 수: **{char_count}** (권장 문자 수에 근접)")
        else:
            st.success(f"✅ 현재 입력된 총 문자 수: **{char_count}**")
    else:
        st.caption("현재 입력된 총 문자 수: 0")
        
    # 입력 내용 삭제 버튼
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        if st.button("🗑️ 입력 내용 삭제", use_container_width=True, type="secondary"):
            clear_text_input()
            st.rerun()
    
    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=True,
        help="입력된 내용 맨끝에 공백/줄바꿈 문자가 한개라도 포함되면 완전히 다른 QR코드가 생성됩니다. 입력된 마지막 문자 뒤에 공백/줄바꿈이 추가되어도 QR코드에 반영되지 않도록 하고 싶다면, 이 옵션을 켜 두세요."
    )
    
    st.markdown("---")
    st.markdown("---")
    
    # QR 코드 설정
    st.subheader("🔧 QR 코드 설정")
    
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        # Box size 설정
        box_size = st.number_input(
            "QR 코드 1개의 사각 cell 크기 (px)",
            min_value=1,
            max_value=100,
            value=20
        )
        
        # Border 설정
        border = st.number_input(
            "QR 코드 테두리/여백",
            min_value=0,
            max_value=10,
            value=2
        )
    
    with col1_2:
        # 에러 보정 레벨
        error_correction_options = {
            "Low (7%) - 오류 보정": qrcode.constants.ERROR_CORRECT_L,
            "Medium (15%) - 오류 보정": qrcode.constants.ERROR_CORRECT_M,
            "Quartile (25%) - 오류 보정": qrcode.constants.ERROR_CORRECT_Q,
            "High (30%) - 오류 보정": qrcode.constants.ERROR_CORRECT_H
        }
        
        error_correction_choice = st.selectbox(
            "오류 보정 레벨",
            list(error_correction_options.keys()),
            index=0
        )
        error_correction = error_correction_options[error_correction_choice]
        
        # 마스크 패턴
        mask_pattern = st.selectbox(
            "마스크 패턴 선택 (0~7)",
            options=list(range(8)),
            index=2
        )
    
    st.markdown("---")

    # 색상 설정
    st.subheader("🔧 색상 설정")
    
    colors = [
        "<직접 선택>", "black", "white", "gray", "lightgray", 
        "lightyellow", "lightgreen", "lightcoral", "lightblue",
        "red", "green", "blue", "purple", "orange", "orangered",
        "darkorange", "maroon", "yellow", "brown", "navy", "mediumblue",
    ]

    col1_3, col1_4 = st.columns(2)
    
    with col1_3:
        pattern_color_choice = st.selectbox("패턴 색상", colors, index=1)  # 기본값: black
    
    with col1_4:
        bg_color_choice = st.selectbox("배경 색상", colors, index=2)  # 기본값: white
    
    # 직접 색상 입력 옵션
    st.markdown("원하는 색상이 리스트에 없다면, 아래에 직접 색상을 입력하세요.")
    st.caption("색상명 (예: crimson, gold) 또는 HEX 코드 (예: #FF5733, #00FF00)를 입력할 수 있습니다.")
    
    col1_5, col1_6 = st.columns(2)
    
    with col1_5:
        custom_pattern_color = st.text_input(
            "패턴 색상 직접 입력",
            placeholder="예: crimson 또는 #FF0000",
            disabled=(pattern_color_choice != "<직접 선택>"),
            help="패턴 색상에서 '<직접 선택>'을 선택하면 활성화됩니다."
        )
    
    with col1_6:
        custom_bg_color = st.text_input(
            "배경 색상 직접 입력",
            placeholder="예: lightcyan 또는 #E0FFFF",
            disabled=(bg_color_choice != "<직접 선택>"),
            help="배경 색상에서 '<직접 선택>'을 선택하면 활성화됩니다."
        )
    
    # 최종 색상 결정
    if pattern_color_choice == "<직접 선택>":
        pattern_color = custom_pattern_color if custom_pattern_color else "black"
    else:
        pattern_color = pattern_color_choice
    
    if bg_color_choice == "<직접 선택>":
        bg_color = custom_bg_color if custom_bg_color else "white"
    else:
        bg_color = bg_color_choice
    
    st.markdown("---")

    # 파일명 설정
    st.subheader("🔧 파일 설정")

    # text_input에서 기본값과 함께 초기화
    filename = st.text_input(
        "다운로드 파일명 입력 (확장자는 제외, 파일명만 입력)",
        placeholder="이 곳에 파일명을 입력해 주세요 (비어있으면 자동 생성됨)",
        key="filename_input",
        value=""   # ⭐ 기본값 지정으로 안전하게 초기화
    )
    st.caption("파일명이 입력되지 않을 경우 자동으로 파일이 생성되며, 특수문자가 입력될 경우에는 '_' 문자로 자동치환 됩니다.")

    # ⭐ 파일명 변경 감지용 상태 변수 초기화
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = ""  # 처음엔 빈 문자열로 시작

    # ⭐ 파일명이 입력되거나 변경되었을 때만 메시지 표시
    if st.session_state.qr_generated:
        current_filename = st.session_state.get("filename_input", "").strip()
    
        # 현재 파일명이 존재하고, 이전 값과 다를 때만 메시지 출력
        if current_filename and current_filename != st.session_state.last_filename:
            st.success("✅ 파일명이 변경되었습니다. 화면 아래의 [QR 코드 다운로드] 버튼을 클릭하세요.")
            st.session_state.last_filename = current_filename
    
    st.markdown("---")
    st.markdown("---")

with col2:
    st.header("👀 미리보기 및 생성")
    
    # QR 코드가 생성된 상태라면 다운로드 버튼도 표시
    if st.session_state.qr_generated and st.session_state.qr_image is not None:
        st.success("✅ QR 코드 생성 완료! 필요시 파일명을 변경하고 다운로드하세요.")
    else:
        st.caption("[QR 코드 생성 버튼]을 클릭하면, QR 코드가 생성되고 다운로드 버튼이 활성화됩니다.")

    # 미리보기/생성 버튼
    col2_1, col2_2 = st.columns(2)
    
    with col2_1:
        preview_btn = st.button("🔍 미리 보기", use_container_width=True)
    
    with col2_2:
        generate_btn = st.button("⚡ QR 코드 생성", use_container_width=True)
    
    st.markdown("---")
    
    # QR 코드 처리
    if preview_btn or generate_btn:
        # 데이터 검증
        processed_data = qr_data
        if strip_option:
            processed_data = processed_data.strip()
        
        if not processed_data:
            st.error("생성할 QR 코드 내용을 입력해 주세요.")
        elif pattern_color == bg_color:
            st.error("패턴과 배경은 같은 색을 사용할 수 없습니다.")
        elif pattern_color_choice == "<직접 선택>" and not custom_pattern_color.strip():
            st.error("패턴 색상을 직접 입력해 주세요.")
        elif bg_color_choice == "<직접 선택>" and not custom_bg_color.strip():
            st.error("배경 색상을 직접 입력해 주세요.")
        else:
            # QR 코드 생성
            img, qr = generate_qr_code(
                processed_data, int(box_size), int(border), error_correction,
                int(mask_pattern), pattern_color, bg_color
            )

            if img is not None and qr is not None:
            
                # QR 코드 정보 텍스트 미리 생성
                qr_info_text = f"""
                **QR 코드 정보**
                - QR 버전: {qr.version}
                - 가로/세로 각 cell 개수: {qr.modules_count}개
                - 이미지 크기: {img.size[0]} x {img.size[1]} px
                - 패턴 색상: {pattern_color}
                - 배경 색상: {bg_color}
                
                - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
                """
                
                # 미리보기 데이터를 세션에 저장
                st.session_state.preview_image = img
                st.session_state.preview_info = qr_info_text
                st.session_state.last_preview_data = processed_data
                
                # 생성 버튼을 눌렀을 때 세션 상태에 저장
                if generate_btn:
                    # 이미지를 바이트로 변환
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_bytes = img_buffer.getvalue()
                    
                    # 세션 상태에 저장
                    st.session_state.qr_generated = True
                    st.session_state.qr_image_bytes = img_bytes
                    st.session_state.qr_image = img
                    st.session_state.qr_info = qr_info_text
                    
                    st.success("🎉 QR 코드 생성 완료! 원하는 파일명으로 변경하고, 아래 다운로드 버튼을 클릭하세요.")

    # 저장된 미리보기가 있고 입력 내용이 변경되지 않았다면 미리보기 표시
    if st.session_state.preview_image is not None:
        # 현재 입력 데이터 확인
        current_data = qr_data.strip() if strip_option else qr_data
        
        if current_data == st.session_state.last_preview_data:
            st.subheader("📱 QR 코드 미리보기")
            st.image(st.session_state.preview_image, caption="생성된 QR 코드", width=600)
            st.info(st.session_state.preview_info)
        else:
            # 입력 내용이 변경되었으면 전체 상태 초기화
            st.session_state.preview_image = None
            st.session_state.preview_info = None
            st.session_state.qr_generated = False   # 생성 완료 메시지도 초기화
            st.session_state.qr_image_bytes = None
            st.session_state.qr_image = None
            st.session_state.qr_info = None
            st.session_state.filename_input = ""    # 파일명도 초기화
            st.session_state.last_filename = ""     # 파일명 변경 메시지도 초기화

        # 마지막 입력값을 갱신
        st.session_state.last_preview_data = current_data

    # 생성된 QR 코드가 있다면 다운로드 버튼 표시
    if st.session_state.qr_generated and st.session_state.qr_image_bytes is not None:
        st.success("✅ QR 코드 생성 완료! 필요시 파일명을 변경하고 다운로드하세요.")

        st.markdown("---")
        st.subheader("📥 다운로드")
        
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        current_filename = st.session_state.get("filename_input", "")
        if not current_filename.strip():
            current_filename = now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        current_filename = sanitize_filename(current_filename)
        download_filename = f"{current_filename}.png"
        
        st.download_button(
            label="📥 QR 코드 다운로드 (PNG)",
            data=st.session_state.qr_image_bytes,
            file_name=download_filename,
            mime="image/png",
            use_container_width=True,
            help="휴대폰에서는 Download 폴더에 저장됩니다."
        )
        
        st.caption(f"📄 다운로드 파일명: `{download_filename}`")
        
        # 새 QR 코드 생성 버튼
        if st.button("🔄 새 QR 코드 생성", use_container_width=True):
            st.session_state.qr_generated = False
            st.session_state.qr_image_bytes = None
            st.session_state.qr_image = None
            st.session_state.qr_info = None
            st.session_state.filename_input = ""  # 새 QR 코드 생성 시 파일명도 초기화
            st.rerun()


# 사이드바에 추가 정보
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
    2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
    3. **색상 설정**에서 패턴과 배경 색상을 선택하세요
    4. **미리 보기** 버튼으로 결과를 확인하세요
    5. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
    """)

    st.markdown("""---------------------------------------------------""")

    st.header("💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com`  
    - **전화번호**: `tel:010-1234-5678`
    - **SMS**: `sms:010-1234-5678`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
    """)

    st.markdown("""---------------------------------------------------""")

    st.header("⚙️ 설정 가이드")
    st.markdown("""
    **오류 보정 레벨:**
    - **Low (7%)**: 손상되지 않는 환경
    - **Medium (15%)**: 일반적인 사용
    - **Quartile (25%)**: 약간의 손상 가능
    - **High (30%)**: 로고 삽입, 손상이 잦은 환경
    
    **마스크 패턴:**
    - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
    
    **색상 입력:**
    - **색상명**: red, blue, green, crimson, gold 등
    - **HEX 코드**: #FF0000, #0000FF, #00FF00 등
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: darkorange; font-size: 16px;">© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)</p>',
    unsafe_allow_html=True
)

