import streamlit as st
import streamlit.components.v1 as components
import os
import base64

st.set_page_config(page_title="회절 스파이크 현상", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "optics_diffractionspikes.html")

# 이미지 파일을 읽어서 Base64 문자열로 변환하는 함수
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    # 1. HTML 파일 읽기
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_data = f.read()

    # 2. 각 이미지 파일의 절대 경로 설정
    img1_path = os.path.join(current_dir, "optics_diffraction_creation.png")
    img2_path = os.path.join(current_dir, "optics_diffraction_hubble.png")
    img3_path = os.path.join(current_dir, "optics_diffraction_webb.png")

    # 3. 파일이 존재하면 HTML 안의 파일명을 Base64 데이터로 치환
    if os.path.exists(img1_path):
        b64_img1 = get_base64_of_bin_file(img1_path)
        html_data = html_data.replace('src="optics_diffraction_creation.png"', f'src="data:image/jpeg;base64,{b64_img1}"')
        
    if os.path.exists(img2_path):
        b64_img2 = get_base64_of_bin_file(img2_path)
        html_data = html_data.replace('src="optics_diffraction_hubble.png"', f'src="data:image/jpeg;base64,{b64_img2}"')
        
    if os.path.exists(img3_path):
        b64_img3 = get_base64_of_bin_file(img3_path)
        html_data = html_data.replace('src="optics_diffraction_webb.png"', f'src="data:image/png;base64,{b64_img3}"')

    # 4. 변환된 HTML을 스트림릿에 렌더링
    components.html(html_data, height=2500, scrolling=False)

except FileNotFoundError:
    st.error("HTML 파일이나 이미지 파일을 찾을 수 없습니다. 같은 폴더에 있는지 확인해 주세요.")
