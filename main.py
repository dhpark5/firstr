import streamlit as st

st.set_page_config(page_title="MBTI 동물 성격 분석기", page_icon="🐾")

# MBTI 데이터 (16개 유형 전부 포함)
mbti_data = {
    "ISTJ": {
        "title": "🧱 ISTJ - 청렴결백한 논리주의자",
        "description": "책임감 있고 신뢰할 수 있는 실천가로, 원칙과 규율을 중시합니다. 체계적이며 신중한 의사결정을 내립니다.",
        "animal": "거북이 🐢",
        "animal_traits": "느리지만 꾸준히, 목표를 향해 한 걸음씩 나아가는 침착한 동물.",
        "image": "https://images.unsplash.com/photo-1607746882042-944635dfe10e"
    },
    "ISFJ": {
        "title": "🛡️ ISFJ - 용감한 수호자",
        "description": "배려심 깊고 헌신적인 성격으로, 조화를 이루며 주변을 돕는 데 주력합니다.",
        "animal": "사슴 🦌",
        "animal_traits": "온순하고 조용하지만, 가족과 무리를 지키는 데 헌신적인 동물.",
        "image": "https://images.unsplash.com/photo-1600181954238-84a2c7ce5a9b"
    },
    "INFJ": {
        "title": "🔮 INFJ - 통찰력 있는 옹호자",
        "description": "조용하지만 강한 신념을 가지고 있으며, 깊이 있는 통찰력과 직관으로 세상을 이해합니다.",
        "animal": "올빼미 🦉",
        "animal_traits": "지혜롭고 신중한 통찰력을 가진 밤의 철학자.",
        "image": "https://images.unsplash.com/photo-1579941804091-9a08a0d7c79d"
    },
    "INTJ": {
        "title": "🧠 INTJ - 전략적인 사색가",
        "description": "독립적이고 분석적인 사고를 통해 장기적 계획을 세우며 목표를 실현합니다.",
        "animal": "독수리 🦅",
        "animal_traits": "높은 시야와 날카로운 분석력으로 멀리 보는 전략가.",
        "image": "https://images.unsplash.com/photo-1610878180933-5f79d191fe87"
    },
    "ISTP": {
        "title": "🔧 ISTP - 만능 해결사",
        "description": "실용적이고 문제 해결에 강한 성격. 즉흥적이지만 신중한 선택을 합니다.",
        "animal": "표범 🐆",
        "animal_traits": "조용하고 독립적이며, 빠르게 움직이는 기민한 사냥꾼.",
        "image": "https://images.unsplash.com/photo-1601758064222-5fe19ea906ec"
    },
    "ISFP": {
        "title": "🎨 ISFP - 예술적인 모험가",
        "description": "감성적이고 섬세한 성격. 자유롭고 조용한 환경에서 자신의 색깔을 표현합니다.",
        "animal": "고양이 🐱",
        "animal_traits": "조용하지만 예민하고 감각적인 독립자.",
        "image": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6"
    },
    "INFP": {
        "title": "🌸 INFP - 열정적인 중재자",
        "description": "깊은 감정과 가치 중심의 삶을 사는 이상주의자. 창의력과 상상력이 풍부합니다.",
        "animal": "수달 🦦",
        "animal_traits": "장난기 많고 감성적인 존재. 혼자만의 시간을 즐기면서도 애정이 풍부해요.",
        "image": "https://images.unsplash.com/photo-1605460375648-278bcbd579a6"
    },
    "INTP": {
        "title": "📚 INTP - 논리적인 사색가",
        "description": "지적 호기심이 풍부하며 새로운 개념과 이론을 탐구하는 데 즐거움을 느낍니다.",
        "animal": "문어 🐙",
        "animal_traits": "지능이 매우 높고 환경에 유연하게 적응하는 천재 생명체.",
        "image": "https://images.unsplash.com/photo-1585241645927-5a0b4fcd8e64"
    },
    "ESTP": {
        "title": "🏍️ ESTP - 에너지 넘치는 활동가",
        "description": "도전적이고 현실적인 성격. 빠른 판단과 행동으로 문제를 해결합니다.",
        "animal": "치타 🐆",
        "animal_traits": "세상에서 가장 빠르고 민첩한 포식자. 순간 집중력의 대명사.",
        "image": "https://images.unsplash.com/photo-1611080626919-b80434f43775"
    },
    "ESFP": {
        "title": "🎉 ESFP - 자유로운 연예인",
        "description": "사교적이고 감각적인 성격. 현재를 즐기며 분위기를 밝게 만듭니다.",
        "animal": "강아지 🐶",
        "animal_traits": "친근하고 사교적이며, 주변을 행복하게 만드는 존재.",
        "image": "https://images.unsplash.com/photo-1558788353-f76d92427f16"
    },
    "ENFP": {
        "title": "🌈 ENFP - 재기발랄한 활동가",
        "description": "창의적이고 열정적이며 사람들과의 연결에서 에너지를 얻습니다.",
        "animal": "앵무새 🦜",
        "animal_traits": "다채롭고 에너지 넘치며 사교적인 존재.",
        "image": "https://images.unsplash.com/photo-1609945174518-0ac53d325e8f"
    },
    "ENTP": {
        "title": "⚡ ENTP - 논쟁을 즐기는 발명가",
        "description": "기발한 아이디어와 끝없는 호기심. 새롭고 혁신적인 해결책을 제시합니다.",
        "animal": "돌고래 🐬",
        "animal_traits": "지적이고 유쾌하며 협동적이고 창의적인 해양의 천재.",
        "image": "https://images.unsplash.com/photo-1590080877400-c61e0e34f92d"
    },
    "ESTJ": {
        "title": "📋 ESTJ - 엄격한 관리자",
        "description": "조직적이고 실용적인 리더형. 규율과 책임을 중시합니다.",
        "animal": "사자 🦁",
        "animal_traits": "무리의 질서를 유지하며 책임감 있게 이끄는 왕.",
        "image": "https://images.unsplash.com/photo-1610878180933-5f79d191fe87"
    },
    "ESFJ": {
        "title": "🤝 ESFJ - 사교적인 돌봄이",
        "description": "사람들을 돕고 조화를 이루는 데 기쁨을 느끼며, 타인의 감정을 잘 살핍니다.",
        "animal": "펭귄 🐧",
        "animal_traits": "무리 속에서 협력하고 다정한 분위기를 만드는 소셜러.",
        "image": "https://images.unsplash.com/photo-1590099541118-9d46e11c7f0a"
    },
    "ENFJ": {
        "title": "✨ ENFJ - 정의로운 사회운동가",
        "description": "타인의 성장을 도우며 카리스마 있게 이끄는 사려 깊은 리더입니다.",
        "animal": "코끼리 🐘",
        "animal_traits": "따뜻하고 지혜로우며, 집단을 돌보는 강력한 감성 리더.",
        "image": "https://images.unsplash.com/photo-1605051443003-9fce50f50f19"
    },
    "ENTJ": {
        "title": "🚀 ENTJ - 대담한 통솔자",
        "description": "결단력 있고 전략적이며 효율적으로 목표를 달성합니다.",
        "animal": "호랑이 🐅",
        "animal_traits": "자기주도적이고 강한 리더십을 지닌 위풍당당한 존재.",
        "image": "https://images.unsplash.com/photo-1602491673986-6f2c8d4a1e83"
    }
}

# UI 시작
st.title("🐾 MBTI 동물 성격 분석기")
st.write("당신의 MBTI를 선택하면 성격에 어울리는 동물 친구를 소개해줄게요! 🐶🦁🐧")

selected = st.selectbox("📌 당신의 MBTI 유형은?", list(mbti_data.keys()))

if selected:
    st.balloons()  # 풍선 효과
    profile = mbti_data[selected]

    st.header(profile["title"])
    st.markdown(f"""
    <p style='font-size:18px'>{profile["description"]}</p>
    <h4>🐾 관련 동물: <span style='color:#ff6600'>{profile["animal"]}</span></h4>
    <p style='font-size:17px'>{profile["animal_traits"]}</p>
    """, unsafe_allow_html=True)

    st.image(profile["image"], use_column_width=True, caption=f"{profile['animal']}를 닮은 당신!")
