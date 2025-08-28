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
import qrcode.constants
from datetime import datetime
from io import BytesIO
import base64


# 페이지 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #34495e;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .info-text {
        color: #7f8c8d;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .preview-box {
        border: 2px solid #bdc3c7;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #f8f9fa;
        margin: 20px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# 메인 제목
st.markdown('<h1 class="main-header">📱 QR 코드 생성기</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">웹에서 간편하게 QR 코드를 생성하세요</p>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'preview_image' not in st.session_state:
    st.session_state.preview_image = None
if 'preview_info' not in st.session_state:
    st.session_state.preview_info = ""

# 메인 레이아웃
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ⚙️ QR 코드 설정")
    
    # QR 코드 내용 입력
    st.markdown("#### 📝 내용 입력")
    qr_text = st.text_area(
        "QR 코드에 넣을 내용을 입력하세요",
        height=120,
        placeholder="이곳에 QR 코드로 만들 내용을 입력해주세요.\n웹사이트 URL, 텍스트, 연락처 정보 등 무엇이든 가능합니다."
    )
    
    # 문자 수 표시
    char_count = len(qr_text)
    if char_count > 0:
        st.markdown(f'<p class="info-text">현재 입력된 문자 수: <strong>{char_count}</strong>자</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="info-text">(최대 입력 가능 문자: 약 2,400~2,900자)</p>', unsafe_allow_html=True)
    
    # 공백/줄바꿈 제거 옵션
    strip_whitespace = st.checkbox(
        "마지막 입력문자 이후 모든 공백/줄바꿈 제거",
        value=True,
        help="QR 코드 내용 끝의 불필요한 공백이나 줄바꿈을 자동으로 제거합니다."
    )
    
    st.markdown("---")
    
    # 고급 설정
    with st.expander("🔧 고급 설정", expanded=True):
        # 두 개의 컬럼으로 나누어 배치
        setting_col1, setting_col2 = st.columns(2)
        
        with setting_col1:
            # Cell 크기
            box_size = st.slider(
                "Cell 크기 (px)",
                min_value=1,
                max_value=100,
                value=20,
                help="QR 코드의 각 사각형(Cell) 크기를 설정합니다"
            )
            
            # 테두리
            border = st.slider(
                "테두리/여백",
                min_value=0,
                max_value=10,
                value=2,
                help="QR 코드 주변의 여백 크기를 설정합니다"
            )
            
            # 오류 보정 레벨
            error_levels = {
                "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
                "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
                "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
                "High (30%)": qrcode.constants.ERROR_CORRECT_H
            }
            error_level = st.selectbox(
                "오류 보정 레벨",
                options=list(error_levels.keys()),
                index=0,
                help="QR 코드가 손상되었을 때 복구 가능한 정도를 설정합니다"
            )
        
        with setting_col2:
            # 마스크 패턴
            mask_pattern = st.selectbox(
                "마스크 패턴 (0~7)",
                options=list(range(8)),
                index=2,
                help="같은 내용이라도 다른 패턴으로 QR 코드를 생성합니다"
            )
            
            # 색상 선택
            colors = [
                "black", "white", "red", "green", "blue", "purple", 
                "orange", "yellow", "brown", "midnightblue", 
                "lightyellow", "lightgreen", "lightcoral", "lightblue"
            ]
            
            pattern_color = st.selectbox(
                "패턴 색상",
                options=colors,
                index=0,
                help="QR 코드 패턴의 색상을 선택합니다"
            )
            
            background_color = st.selectbox(
                "배경 색상",
                options=colors,
                index=1,
                help="QR 코드 배경의 색상을 선택합니다"
            )

with col2:
    st.markdown("### 👀 미리보기 및 생성")
    
    # 미리보기 버튼
    if st.button("🔍 미리보기", type="secondary", use_container_width=True):
        if not qr_text.strip():
            st.error("생성할 QR 코드 내용을 입력해주세요.")
        elif pattern_color == background_color:
            st.error("패턴색과 배경색이 같습니다. 다른 색상을 선택해주세요.")
        else:
            try:
                # QR 코드 데이터 처리
                data = qr_text
                if strip_whitespace:
                    data = data.strip()
                
                # QR 코드 생성
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=error_levels[error_level],
                    box_size=box_size,
                    border=border,
                    mask_pattern=mask_pattern,
                )
                
                qr.add_data(data, optimize=0)
                qr.make(fit=True)
                
                # 이미지 생성
                img = qr.make_image(fill_color=pattern_color, back_color=background_color)
                
                # 이미지를 base64로 변환하여 세션에 저장
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                st.session_state.preview_image = img_base64
                st.session_state.preview_info = {
                    'version': qr.version,
                    'size': img.size,
                    'box_size': box_size,
                    'border': border
                }
                
                st.success("미리보기가 생성되었습니다!")
                
            except Exception as e:
                st.error(f"미리보기 생성 중 오류가 발생했습니다: {str(e)}")
    
    # 미리보기 표시
    if st.session_state.preview_image:
        st.markdown("#### 📱 미리보기")
        
        # 이미지 표시
        st.markdown(
            f'<div class="preview-box"><img src="data:image/png;base64,{st.session_state.preview_image}" style="max-width: 100%; height: auto;"></div>',
            unsafe_allow_html=True
        )
        
        # 정보 표시
        if st.session_state.preview_info:
            info = st.session_state.preview_info
            st.markdown(f"""
            **QR 코드 정보:**
            - QR 버전: {info['version']}
            - 이미지 크기: {info['size'][0]} x {info['size'][1]} px
            - Cell 크기: {info['box_size']} px
            - 테두리: {info['border']}
            """)
        
        # 다운로드 버튼
        st.markdown("#### 💾 다운로드")
        
        # 파일명 입력
        filename = st.text_input(
            "파일명 (확장자 제외)",
            value=datetime.now().strftime("QR_%Y-%m-%d_%H-%M-%S"),
            help="특수문자는 자동으로 '_'로 변환됩니다"
        )
        
        # 파일명 정리
        invalid_chars = '\\/:*?"<>|[]'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        filename = filename.strip() or datetime.now().strftime("QR_%Y-%m-%d_%H-%M-%S")
        
        # 다운로드 버튼
        img_bytes = base64.b64decode(st.session_state.preview_image)
        st.download_button(
            label="📥 PNG 파일로 다운로드",
            data=img_bytes,
            file_name=f"{filename}.png",
            mime="image/png",
            type="primary",
            use_container_width=True
        )
        
    else:
        st.markdown(
            '<div class="preview-box">미리보기 버튼을 클릭하면<br>생성될 QR 코드가 여기에 표시됩니다</div>',
            unsafe_allow_html=True
        )

# 사이드바에 추가 기능
with st.sidebar:
    st.markdown("### 📋 사용법")
    st.markdown("""
    1. **내용 입력**: QR 코드로 만들고 싶은 내용을 입력하세요
    2. **설정 조정**: 필요에 따라 크기, 색상 등을 조정하세요  
    3. **미리보기**: 미리보기 버튼을 클릭하여 결과를 확인하세요
    4. **다운로드**: 만족스러우면 다운로드 버튼을 클릭하세요
    """)
    
    st.markdown("### 💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com`  
    - **전화번호**: `tel:010-1234-5678`
    - **SMS**: `sms:010-1234-5678`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명;P:비밀번호;;`
    - **텍스트**: `일반적인 텍스트를 입력합니다`
    """)
    
    st.markdown("### ⚠️ 주의사항")
    st.markdown("""
    - 너무 많은 내용을 넣으면 QR 코드 크기가 거대해집니다.
    - 패턴색과 배경색이 같으면 읽을 수 없습니다.
    - 휴대폰에서도 문제없이 잘 작동합니다.
    """)

# 하단 정보
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #32cd32;">© 2025 QR 코드 생성기  |  Streamlit으로 제작  |  제작: 류종훈(redhat4u@gmail.com)</p>',
    unsafe_allow_html=True
)






