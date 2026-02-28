import streamlit as st

# 1. 사이드바 메뉴에 들어갈 개별 페이지들을 정의합니다.
# st.Page("파일경로", title="메뉴에 보일 이름", icon="아이콘")

# 역학

# 전자기학
page_Thevenin1 = st.Page("pages/테브난정리기본.py", title="테브난 정리 기본", icon="-")
page_Thevenin2 = st.Page("pages/테브난정리심화.py", title="테브난 정리 심화", icon="-")


# 광학
page_brewster = st.Page("pages/브루스터법칙.py", title="브루스터 법칙", icon="-")
page_lens = st.Page("pages/볼록렌즈.py", title="볼록렌즈 시뮬레이션", icon="-")
# page_circuit = st.Page("pages/교류회로.py", title="교류회로 실험", icon="-")

# SF
page_sf = st.Page("pages/SF소설추천.py", title="SF 소설 추천", icon="-")

# 2. 카테고리(폴더) 구조로 페이지들을 묶어줍니다 (딕셔너리 형태).
# 왼쪽 메뉴에 굵은 글씨로 카테고리 제목이 생성되고, 그 아래에 페이지들이 배치됩니다.
nav_structure = {
    "역학": [],
    "전자기학": [page_Thevenin1, page_Thevenin2], 
    "광학": [page_lens, page_brewster],
    "SF": [page_sf],
}

# 3. 네비게이션 객체를 생성하고 실행합니다.
pg = st.navigation(nav_structure)

# (선택) 모든 페이지에 공통으로 적용될 상단 설정이 필요하다면 여기에 작성합니다.
st.set_page_config(page_title="통합 시뮬레이션 플랫폼", layout="wide")

# 선택된 페이지 렌더링
pg.run()
