import streamlit as st

st.set_page_config(page_title="MBTI 유명인사 검색기", page_icon="🌟")

st.title("🔍 MBTI 유형으로 유명한 사람은 누구일까?")
st.write("당신의 MBTI 유형을 선택하면, 관련된 유명인을 사진과 함께 소개해줄게요! 😊")

# MBTI 유형별 데이터 (몇 개만 샘플로 작성, 확장 가능)
mbti_info = {
    "ISTJ": {
        "desc": "책임감 있고 조직적인 현실주의자. 원칙과 신뢰를 중시합니다.",
        "celebrities": [
            {
                "name": "조지 워싱턴",
                "desc": "미국 초대 대통령, 신중하고 원칙을 지킨 리더.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/George_Washington_by_Gilbert_Stuart%2C_1797.jpg"
            },
            {
                "name": "나탈리 포트만",
                "desc": "배우이자 하버드 졸업생, 조용하고 논리적인 성향.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Natalie_Portman_Cannes_2015_5.jpg"
            }
        ]
    },
    "ENFP": {
        "desc": "열정적이고 창의적인 활동가. 새로운 사람과 아이디어를 사랑합니다.",
        "celebrities": [
            {
                "name": "로빈 윌리엄스",
                "desc": "유쾌함과 깊은 감성을 겸비한 배우.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/4/42/Robin_Williams_2011a_%28cropped%29.jpg"
            },
            {
                "name": "로버트 다우니 주니어",
                "desc": "아이언맨으로 유명한 매력적인 배우.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Robert_Downey_Jr_2014_Comic_Con_%28cropped%29.jpg"
            }
        ]
    },
    "INFJ": {
        "desc": "이상주의적이며 통찰력 있는 성격. 조용하지만 영향력 있는 사람.",
        "celebrities": [
            {
                "name": "테일러 스위프트",
                "desc": "감성적이고 진솔한 가사로 세계를 감동시키는 가수.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Taylor_Swift_2_-_2019_by_Glenn_Francis.jpg"
            },
            {
                "name": "마틴 루터 킹 주니어",
                "desc": "비폭력 저항운동의 상징, 깊은 신념의 리더.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/2/24/Martin_Luther_King%2C_Jr..jpg"
            }
        ]
    },
    "INTP": {
        "desc": "호기심 많고 분석적인 철학자. 독창적인 아이디어에 열정적입니다.",
        "celebrities": [
            {
                "name": "앨버트 아인슈타인",
                "desc": "상대성이론을 만든 천재 물리학자.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg"
            },
            {
                "name": "빌 게이츠",
                "desc": "마이크로소프트 창업자, 지적이고 분석적인 경영자.",
                "img": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Bill_Gates_2018.jpg"
            }
        ]
    },
    # 여기에 나머지 12개 유형도 같은 형식으로 계속 추가 가능
}

# 사용자가 MBTI 선택
selected_mbti = st.selectbox("당신의 MBTI 유형을 선택하세요 👇", list(mbti_info.keys()))

if selected_mbti:
    st.balloons()
    mbti = mbti_info[selected_mbti]
    
    # MBTI 설명
    st.header(f"📘 {selected_mbti} 유형")
    st.markdown(f"**{mbti['desc']}**")

    # 유명인사 출력
    st.subheader("🌟 유명한 {0} 유형 사람들".format(selected_mbti))
    for celeb in mbti['celebrities']:
        st.image(celeb['img'], width=200, caption=celeb['name'])
        st.markdown(f"**{celeb['name']}**: {celeb['desc']}")
        st.markdown("---")
