import streamlit as st
st.title("인구분포")
st.write("연령별 인구분포")

import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="cp949")
    df.columns = df.columns.str.replace("2025년05월_계_", "")
    df["행정구역"] = df["행정구역"].str.replace(r"\s*\(.*\)", "", regex=True)
    return df

df = load_data()

# 지역 선택
region = st.selectbox("지역을 선택하세요", df["행정구역"].unique())

# 선택한 지역의 데이터 필터링
region_row = df[df["행정구역"] == region].iloc[0]
age_data = region_row[3:]  # 앞 3열은 메타데이터
age_data = age_data.apply(lambda x: int(str(x).replace(",", "").split('.')[0]))  # 문자열 정제
age_data = age_data.reset_index()
age_data.columns = ["연령", "인구수"]
age_data["연령"] = age_data["연령"].str.replace("세", "").str.replace("이상", "+").str.replace(" ", "")
age_data["인구수"] = age_data["인구수"].astype(int)

# 시각화
fig = px.bar(age_data, 
             x="인구수", 
             y="연령", 
             orientation="h",
             title=f"{region}의 연령별 인구 구조",
             labels={"연령": "연령", "인구수": "인구 수"},
             height=900)
fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)
