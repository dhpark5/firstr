import streamlit as st

# 1. 페이지 기본 설정 (최상단)
st.set_page_config(page_title="DIY물리실험", layout="wide", initial_sidebar_state="collapsed")

# --- 2. 홈 화면(소개글)을 그리는 함수 정의 ---
def intro_page():
    st.title("⚡ DIY 물리실험")
    st.markdown("""
    이 웹사이트는 물리학을 이해하는 데에 도움이 되는 정보를 제공합니다.
    
    유튜브 채널 DIY물리실험과 같이 운영합니다.
      
    
    """)
    
#    st.info("👈 화면 왼쪽 위의 화살표를 눌러 시뮬레이션을 시작하세요!")

# 3. 사이드바 메뉴에 들어갈 개별 페이지들을 정의합니다.
# 위에서 만든 intro_page 함수를 첫 화면(default=True)으로 지정합니다.
page_home = st.Page(intro_page, title="DIY물리실험", icon="▪️", default=True)

# 전자기학
page_Thevenin1 = st.Page("pages/테브난정리기본.py", title="테브난 정리 기본", icon="▪️")
page_Thevenin2 = st.Page("pages/테브난정리심화.py", title="테브난 정리 심화", icon="▪️")
page_RLC = st.Page("pages/교류회로.py", title="교류회로", icon="▪️")

# 광학
page_brewster = st.Page("pages/브루스터법칙.py", title="브루스터 법칙", icon="▪️")
page_lens = st.Page("pages/볼록렌즈.py", title="볼록렌즈 시뮬레이션", icon="▪️")

# SF
page_sf = st.Page("pages/SF소설추천.py", title="SF 소설 추천", icon="▪️")

# 4. 카테고리(폴더) 구조로 페이지들을 묶어줍니다.
nav_structure = {
    "🏠DIY물리실험": [page_home],  # 소개 페이지 카테고리
    "🔹역학": [],
    "🔹전자기학": [page_Thevenin1, page_Thevenin2, page_RLC], 
    "🔹광학": [page_lens, page_brewster],
    "🔹SF": [page_sf],
}

# 5. 네비게이션 객체를 생성하고 실행합니다.
pg = st.navigation(nav_structure)
pg.run()
