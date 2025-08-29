"""
QR 코드 생성 웹앱 - Streamlit 버전
휴대폰에서도 사용 가능

실행 방법:
1. pip install streamlit qrcode[pil]
2. streamlit run qrcode_web.py

또는 온라인에서 실행:
- Streamlit Cloud, Heroku, Replit 등에 배포 가능
"""

import streamlit as st
import qrcode
import io
from datetime import datetime
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성 프로그램",
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


# 메인 앱 ============================================================================================
st.title("🔲 QR 코드 생성 프로그램")
st.markdown("---")

# 레이아웃 설정 (2개 컬럼)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header("설정")
    
    # QR 코드 입력창
    st.subheader("📝 QR 코드 내용")
    st.info("최대 입력 가능한 문자는 종류에 따라 약 2,400~2,900자 정도입니다.")
    
    qr_data = st.text_area(
        "QR 코드로 생성할 내용을 입력해 주세요",
        height=120,
        placeholder="이 곳에 QR 코드를 생성할 내용을 입력해 주세요.\n복사/붙여넣기를 사용할 수 있습니다."
    )
    
    # 문자 수 표시
    if qr_data:
        st.caption(f"현재 입력된 총 문자 수: {len(qr_data)}")
    else:
        st.caption("현재 입력된 총 문자 수: 0")
    
    # 공백/줄바꿈 제거 옵션
    strip_option = st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=True,
        help="입력된 내용 맨끝에 공백/줄바꿈 문자가 한개라도 포함되면 완전히 다른 QR코드가 생성됩니다. 입력된 마지막 문자 뒤에 공백/줄바꿈이 추가되어도 QR코드에 반영되지 않도록 하고 싶다면, 이 옵션을 켜 두세요."
    )
    
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
    
    # 색상 설정
    st.subheader("색상 설정")
    
    colors = [
        "white", "black", "gray", "lightgray", "lightyellow",
        "lightgreen", "lightcoral", "lightblue", "darkorange",
        "red", "green", "blue", "purple", "orange", "orangered",
        "maroon", "yellow", "brown", "navy", "mediumblue"
    ]
    
    col1_3, col1_4 = st.columns(2)
    
    with col1_3:
        pattern_color = st.selectbox("패턴 색상", colors, index=1)  # 기본값: black
    
    with col1_4:
        bg_color = st.selectbox("배경 색상", colors, index=0)  # 기본값: white
    
    # 파일명 설정
    st.subheader("파일 설정")
    filename = st.text_input(
        "파일명 입력 (확장자 제외)",
        placeholder="파일명을 입력해 주세요 (비어있으면 자동 생성)"
    )
    st.caption("파일명이 입력되지 않을 경우 자동으로 파일이 생성되며, 특수문자가 입력될 경우에는 '_' 문자로 자동치환 됩니다.")

with col2:
    st.header("👀 미리보기 및 생성")
    
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
        else:
            # QR 코드 생성
            img, qr = generate_qr_code(
                processed_data, int(box_size), int(border), error_correction,
                int(mask_pattern), pattern_color, bg_color
            )

            if img is not None and qr is not None:
            
                # 미리보기 표시
                st.subheader("📱 QR 코드 미리보기")
                st.image(img, caption="생성된 QR 코드")
                
                # QR 코드 정보 표시
                st.info(f"""
                **QR 코드 정보**
                - QR 버전: {qr.version}
                - 가로/세로 각 cell 개수: {qr.modules_count}개
                - 이미지 크기: {img.size[0]} x {img.size[1]} px
                
                - 이미지 크기 = (각 cell 개수 + 좌/우 여백 총 개수) × 1개의 사각 cell 크기
                """)
                
                # 파일 다운로드
                if generate_btn:
                    # 파일명 처리
                    if not filename:
                        filename = datetime.now().strftime("QR_%Y-%m-%d_%H-%M-%S")
                    
                    filename = sanitize_filename(filename)
                    download_filename = f"{filename}.png"
                    
                    # 이미지를 바이트로 변환
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_bytes = img_buffer.getvalue()
                    
                    st.success(f"QR 코드가 생성되었습니다!")

                    # Streamlit 다운로드 버튼 사용
                    st.download_button(
                        label="📥 QR 코드 다운로드",
                        data=img_bytes,
                        file_name=download_filename,
                        mime="image/png",
                        use_container_width=True
                    )


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

    st.header("💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **텍스트**: `가장 보편적인 방식으로 텍스트를 입력합니다`
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com`  
    - **전화번호**: `tel:010-1234-5678`
    - **SMS**: `sms:010-1234-5678`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명;P:비밀번호;;`
    """)

    st.header("⚙️ 설정 가이드")
    st.markdown("""
    **오류 보정 레벨:**
    - **Low (7%)**: 손상되지 않는 환경
    - **Medium (15%)**: 일반적인 사용
    - **Quartile (25%)**: 약간의 손상 가능
    - **High (30%)**: 로고 삽입, 손상이 잦은 환경
    
    **마스크 패턴:**
    - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #228b22;">© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)</p>',
    unsafe_allow_html=True
)

