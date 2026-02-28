import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 기본 설정 (화면을 넓게 사용)
st.set_page_config(page_title="굴절 법칙", layout="wide")

# 현재 파이썬 파일과 같은 위치에 있는 HTML 파일의 경로를 자동으로 찾음
current_dir = os.path.dirname(os.path.abspath(__file__))

# 한글 인코딩(Mac 자소 분리) 오류를 원천 차단하기 위해 영문 파일명 사용
html_file_path = os.path.join(current_dir, "optics_snell.html")

# HTML 파일 읽어오기 및 에러 처리
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_data = f.read()
    
    # 스트림릿 화면에 HTML 렌더링 (height를 넉넉히 주어 스크롤 없이 다 보이게 설정)
    components.html(html_data, height=1300, scrolling=True)

except FileNotFoundError:
    st.error(f"'{html_file_path}' 파일을 찾을 수 없습니다. 깃허브에서 HTML 파일 이름이 정확히 'optics_snell.html'로 변경되었는지 확인해주세요.")
