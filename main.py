import streamlit as st

# 1. 페이지 기본 설정
# 사이드바 전체는 열려있게(expanded) 설정합니다.
st.set_page_config(page_title="DIY물리실험", layout="wide", initial_sidebar_state="expanded")

# --- 2. 홈 화면(소개글)을 그리는 함수 정의 ---
def intro_page():
    st.title("⚡ DIY 물리실험")
    st.markdown("""
    이 웹사이트는 물리학을 이해하는 데에 도움이 되는 정보를 제공합니다.
    
    유튜브 채널 [**DIY물리실험**](https://www.youtube.com/@dhpark5)과 같이 운영합니다.
    """)
    # st.info("👈 화면 왼쪽의 메뉴를 펼쳐 시뮬레이션을 시작하세요!")

# 3. 사이드바 메뉴에 들어갈 개별 페이지들을 정의합니다.
page_home = st.Page(intro_page, title="DIY물리실험", icon="🏠", default=True)

# 전자기학
page_Thevenin1 = st.Page("pages/테브난정리기본.py", title="테브난 정리 기본", icon="▪️")
page_Thevenin2 = st.Page("pages/테브난정리심화.py", title="테브난 정리 심화", icon="▪️")
page_RLC = st.Page("pages/교류회로.py", title="교류회로", icon="▪️")

# 광학
page_lens = st.Page("pages/볼록렌즈.py", title="볼록렌즈 시뮬레이션", icon="▪️")
page_brewster = st.Page("pages/브루스터법칙.py", title="브루스터 법칙", icon="▪️")

# SF
page_sf = st.Page("pages/SF소설추천.py", title="SF 소설 추천", icon="▪️")

# 4. 기본 네비게이션 숨기기
# 모든 페이지를 리스트로 묶고, position="hidden"을 사용하여 스트림릿의 기본 메뉴를 안 보이게 지웁니다.
all_pages = [page_home, page_Thevenin1, page_Thevenin2, page_RLC, page_lens, page_brewster, page_sf]
pg = st.navigation(all_pages, position="hidden")

# 5. 커스텀 사이드바 직접 만들기 (접이식 카테고리 구현)
with st.sidebar:
    #st.subheader("메뉴")
    
    # 홈 화면은 카테고리 밖에 단독으로 둡니다.
    st.page_link(page_home)
    
    # 외부 링크 (유튜브 채널) 추가
    st.page_link("https://www.youtube.com/@dhpark5", label="DIY물리실험 유튜브", icon="📺")
    
    # 메뉴 구분을 위한 얇은 가로선 추가
    st.divider()
    
    # expanded=False 파라미터를 통해 처음 접속 시 메뉴가 닫혀 있도록 설정합니다.
    #with st.expander("역학", expanded=False):

    with st.expander("전자기학", expanded=False):
        st.page_link(page_Thevenin1)
        st.page_link(page_Thevenin2)
        st.page_link(page_RLC)
        
    with st.expander("광학", expanded=False):
        st.page_link(page_lens)
        st.page_link(page_brewster)
        
    with st.expander("SF", expanded=False):
        st.page_link(page_sf)

# 6. 선택된 페이지 렌더링
pg.run()
