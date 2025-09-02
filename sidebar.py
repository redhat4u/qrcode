# 이 파일은 사이드바 UI를 구성하는 함수를 정의합니다.
# sidebar.py

import streamlit as st

def build_sidebar_ui():
    """사이드바를 빌드합니다."""
    st.header("📖 사용 방법")
    st.markdown("""
    1. **QR 코드 내용** 영역에 변환할 텍스트를 입력하세요
    2. **QR 코드 설정**에서 크기와 오류 보정 레벨을 조정하세요
    3. **패턴 모양**에서 QR 코드 점의 모양을 선택하세요 (SVG 형식은 사각형만 가능합니다)
    4. **색상 설정**에서 패턴과 배경 색상을 선택하세요 (SVG 형식은 기본색만 가능합니다)
    5. **파일 설정**에서 원하는 파일 형식(PNG/SVG)을 선택하고 파일명을 지정하세요
    6. **QR 코드 생성** 버튼으로 최종 파일을 다운로드하세요
    """)

    st.markdown("---")

    st.header("💡 용도별 QR 코드 생성 팁")
    st.markdown("""
    - **텍스트**: `QR 코드로 생성할 텍스트를 입력합니다`
    - **웹사이트**: `https://www.example.com`
    - **이메일**: `mailto:user@example.com`
    - **이메일(제목,본문, 여러 수신자 포함)**: `mailto:user1@example.com,user2@example.com?subject=제목&body=메시지 내용`
    - **전화번호**: `tel:type=CELL:+82 10-1234-5678`
    - **SMS (번호만)**: `sms:type=CELL:+82 10-1234-5678`
    - **SMS (메시지 포함)**: `sms:type=CELL:+82 10-1234-5678?body=메시지 내용`
    - **WiFi**: `WIFI:T:WPA;S:네트워크명(SSID);P:비밀번호;H:false;;`
    """)

    st.markdown("---")

    st.header("⚙️ 설정 가이드")
    st.markdown("**오류 보정 레벨:**")
    st.markdown("""
    - **Low (7%)**: 손상되지 않는 환경
    - **Medium (15%)**: 일반적인 사용
    - **Quartile (25%)**: 약간의 손상 가능
    - **High (30%)**: 로고 삽입, 손상이 잦은 환경
    """)

    st.markdown("**마스크 패턴:**")
    st.markdown("""
    - 0~7 중 선택 (같은 내용이라도 번호에 따라 패턴이 달라짐)
    """)

    st.markdown("**패턴 모양:**")
    st.markdown("""
    - 사각형, 둥근 사각, 원형, 마름모 중 선택
    - **SVG** 파일 형식 선택 시에는 **사각형**만 지원합니다.
    """)

    st.markdown("**색상 입력:**")
    st.markdown("""
    - **직접 입력**: 리스트에 없는 색상은 HEX 코드로 직접 입력 가능합니다.
    - **오류 메시지**: 색상 입력 시 유효성 검사를 진행하여 입력 칸이 비어 있거나 올바른 색상 값이 아닐 경우 경고 메시지가 표시됩니다.
    - **SVG** 파일 형식 선택 시에는 패턴:검은색, 배경:흰색만 지원합니다.
    """)
    
