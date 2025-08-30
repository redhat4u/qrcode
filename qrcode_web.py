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
                    
                    st.success("🎉 QR 코드 생성 완료! 좌측 파일명을 변경하고 아래 다운로드 버튼을 클릭하세요.")

    # 저장된 미리보기가 있고 입력 내용이 변경되지 않았다면 미리보기 표시
    if st.session_state.preview_image is not None:
        # 현재 입력 데이터 확인
        current_data = qr_data
        if strip_option:
            current_data = current_data.strip()
            
        # 입력 내용이 변경되지 않았다면 미리보기 유지
        if current_data == st.session_state.last_preview_data:
            st.subheader("📱 QR 코드 미리보기")
            st.image(st.session_state.preview_image, caption="생성된 QR 코드", width=500)
            st.info(st.session_state.preview_info)
        else:
            # 입력 내용이 변경되었으면 미리보기 초기화
            st.session_state.preview_image = None
            st.session_state.preview_info = None
            st.session_state.last_preview_data = ""

    # 생성된 QR 코드가 있다면 다운로드 버튼 표시
    if st.session_state.qr_generated and st.session_state.qr_image_bytes is not None:
        st.markdown("---")
        st.subheader("📥 다운로드")
        
        # 현재 시각 가져오기
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        
        # 파일명 처리 (현재 입력된 값 사용)
        current_filename = st.session_state.get("filename_input", "")
        if not current_filename.strip():
            current_filename = now.strftime("QR_%Y-%m-%d_%H-%M-%S")
        current_filename = sanitize_filename(current_filename)
        download_filename = f"{current_filename}.png"
        
        # 다운로드 버튼
        st.download_button(
            label="📥 QR 코드 다운로드 (PNG)",
            data=st.session_state.qr_image_bytes,
            file_name=download_filename,
            mime="image/png",
            use_container_width=True,
            help="PC에서는 Downloads 폴더에, 휴대폰에서는 다운로드 폴더에 저장됩니다."
        )
        
        # 현재 다운로드될 파일명 표시
        st.caption(f"📄 다운로드 파일명: `{download_filename}`")
        
        # 새 QR 코드 생성 버튼
        if st.button("🔄 새 QR 코드 생성", use_container_width=True):
            st.session_state.qr_generated = False
            st.session_state.qr_image_bytes = None
            st.session_state.qr_image = None
            st.session_state.qr_info = None
            st.rerun()


