# state_manager.py
import streamlit as st

def initialize_session_state():
    """
    세션 상태 변수를 초기화합니다.
    """
    if "qr_data" not in st.session_state:
        st.session_state.qr_data = "https://www.google.com"
    if "download_initiated" not in st.session_state:
        st.session_state.download_initiated = False
    # 기타 필요한 세션 상태 변수 초기화

def reset_all_settings():
    """
    모든 세션 상태를 초기화합니다.
    """
    st.session_state.qr_data = ""
    st.session_state.download_initiated = False
    # 기타 필요한 세션 상태 변수 초기화

def clear_text_input():
    """
    텍스트 입력 필드를 초기화합니다.
    """
    st.session_state.qr_data = ""
    
def clear_filename_callback():
    """
    다운로드 파일명을 초기화합니다.
    """
    st.session_state.download_initiated = False

def on_qr_setting_change():
    """
    QR 설정 변경 시 호출되는 콜백 함수입니다.
    """
    pass

def set_download_initiated():
    """
    다운로드 시작 상태를 설정합니다.
    """
    st.session_state.download_initiated = True
