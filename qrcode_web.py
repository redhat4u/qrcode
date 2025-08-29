import streamlit as st

# 가장 기본적인 테스트 버전
st.title("🔲 QR 코드 생성 프로그램 - 테스트")
st.write("앱이 정상적으로 로드되었습니다!")

try:
    import qrcode
    st.success("qrcode 라이브러리 로드 성공!")
except ImportError as e:
    st.error(f"qrcode 라이브러리 로드 실패: {e}")

try:
    from PIL import Image
    st.success("PIL 라이브러리 로드 성공!")
except ImportError as e:
    st.error(f"PIL 라이브러리 로드 실패: {e}")

st.write("기본 테스트가 완료되었습니다.")

# 간단한 QR 코드 테스트
if st.button("간단한 QR 코드 테스트"):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data("Hello World")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        st.image(img, caption="테스트 QR 코드")
        st.success("QR 코드 생성 성공!")
    except Exception as e:
        st.error(f"QR 코드 생성 실패: {e}")
