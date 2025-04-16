import streamlit as st

# 제목
st.title("🧠 MBTI 성격 유형 분석기")
st.write("당신의 MBTI를 선택하면, 어떤 사람인지 친절하게 알려드릴게요! 😊")

# MBTI 설명 사전
mbti_descriptions = {
    "ISTJ": """
### 🧱 **ISTJ - 청렴결백한 논리주의자**
<p style='font-size:18px'>
🧭 항상 <b><span style='color:#3366cc'>원칙</span></b>과 <b><span style='color:#3366cc'>규율</span></b>을 중시하며, 신뢰받는 <b><span style='color:#3366cc'>책임감 있는 리더</span></b>입니다.<br>
📊 철저하고 체계적인 사고로 일을 완수하며, 변화를 경계하는 보수적인 성향도 있습니다.<br>
🛠️ <b><span style='color:#3366cc'>현실적이고 실용적</span></b>이어서 복잡한 감정보다 명확한 규칙을 따르는 걸 선호해요.<br>
</p>
""",
    "ENFP": """
### 🌈 **ENFP - 재기발랄한 활동가**
<p style='font-size:18px'>
🌟 넘치는 <b><span style='color:#ff9900'>열정</span></b>과 <b><span style='color:#ff9900'>창의성</span></b>으로 세상을 다채롭게 바꾸려는 꿈을 가진 사람입니다.<br>
🗣️ 사람들과의 교류에서 <b><span style='color:#ff9900'>에너지</span></b>를 얻고, 아이디어가 많아 항상 새로운 가능성을 찾습니다.<br>
🎨 감성적이면서도 이상주의적이어서, <b><span style='color:#ff9900'>사람의 잠재력</span></b>을 믿고 도와주려는 경향이 강합니다.<br>
</p>
""",
    "INTJ": """
### 🧠 **INTJ - 용의주도한 전략가**
<p style='font-size:18px'>
📈 장기적인 목표를 향해 철저히 준비하고 계획하는 <b><span style='color:#9933cc'>논리적 리더</span></b>입니다.<br>
🔍 세상의 구조를 분석하고 더 나은 방식으로 재구성하려는 성향을 지니며,<br>
🙊 감정보다는 <b><span style='color:#9933cc'>논리와 효율성</span></b>을 중시합니다.<br>
🧩 독창적인 아이디어와 전략을 갖춘 <b><span style='color:#9933cc'>천생 혁신가</span></b>예요.<br>
</p>
""",
    "ISFP": """
### 🌿 **ISFP - 호기심 많은 예술가**
<p style='font-size:18px'>
🎨 감각이 뛰어나고 <b><span style='color:#66cc66'>자유로운 영혼</span></b>을 지닌 성격입니다.<br>
🦋 고요하고 차분해 보일 수 있지만, <b><span style='color:#66cc66'>내면에는 풍부한 감정</span></b>이 있습니다.<br>
🌼 타인을 잘 배려하며, <b><span style='color:#66cc66'>갈등을 피하고 조화를 중요시</span></b>합니다.<br>
🏞️ 규칙보다는 자신의 감각과 즉흥성을 따르며, 예술적인 재능이 뛰어난 경우가 많아요.<br>
</p>
""",
    # 여기에 나머지 12개 유형도 비슷한 형식으로 추가 가능
}

# 드롭다운 메뉴
selected_mbti = st.selectbox("📌 MBTI 유형을 선택하세요:", list(mbti_descriptions.keys()))

# 설명 출력
if selected_mbti:
    st.markdown(mbti_descriptions[selected_mbti], unsafe_allow_html=True)
