# app.py  또는  pages/SF 소설 추천.py
import streamlit as st
import pandas as pd
from typing import List, Dict, Optional
import plotly.express as px

st.set_page_config(page_title="SF 소설 추천기", page_icon="🚀", layout="wide")

# =========================
# 유틸 & 안전 가드
# =========================
def _to_list(x):
    if isinstance(x, list): return [str(i) for i in x]
    if x is None or (isinstance(x, float) and pd.isna(x)): return []
    if isinstance(x, str):
        parts = [p.strip() for p in x.split(",") if p.strip()]
        return [str(p) for p in (parts if len(parts) > 1 else [x.strip()])]
    return [str(x)]

def _sanitize_defaults(default_vals, options):
    if not isinstance(default_vals, list): return []
    optset = set(str(o) for o in options)
    cleaned, seen = [], set()
    for d in default_vals:
        if isinstance(d, list):
            for dd in d:
                s = str(dd)
                if s in optset and s not in seen: cleaned.append(s); seen.add(s)
        else:
            s = str(d)
            if s in optset and s not in seen: cleaned.append(s); seen.add(s)
    return cleaned

def jaccard(a, b) -> float:
    A, B = set(_to_list(a)), set(_to_list(b))
    if not A and not B: return 0.0
    return len(A & B) / len(A | B)

def tone_match(book_tone: str, pref_tone: str) -> float:
    if book_tone == pref_tone: return 1.0
    neighbors = {
        "balanced":{"cool","hopeful","dark","quiet"},
        "cool":{"balanced","dark","quiet"},
        "hopeful":{"balanced","quiet"},
        "dark":{"cool","balanced"},
        "quiet":{"balanced","cool","hopeful"}
    }
    return 0.6 if pref_tone in neighbors and book_tone in neighbors[pref_tone] else 0.2

def add_book(title_ko_en: str, author: str, year: int,
             subgenres: List[str], themes: List[str],
             hardness: int, humanism: int, optimism: int, pace: int, tone: str,
             x_scienceification: float, y_systemness: float,
             summary: str = "", ko: bool = True,
             cover_url: Optional[str] = None, info_url: Optional[str] = None) -> Dict:
    tags = list(sorted(set(_to_list(subgenres) + _to_list(themes))))
    return {
        "title": title_ko_en, "author": author, "year": int(year),
        "subgenres": _to_list(subgenres), "themes": _to_list(themes), "tags": tags,
        "hardness": int(hardness), "humanism": int(humanism), "optimism": int(optimism), "pace": int(pace), "tone": str(tone),
        "x_axis": float(x_scienceification), "y_axis": float(y_systemness),
        "summary": summary.strip(), "ko": bool(ko),
        "cover_url": cover_url, "info_url": info_url
    }

# =========================
# DB (확장)
# =========================
BOOKS = [
    add_book("노인의 전쟁 (Old Man's War)", "John Scalzi", 2005,
             ["Space Opera","Military SF"], ["identity","war","ethics","society"],
             3,4,3,4,"balanced", 0.35, 0.35,
             "노년의 이들이 첨단 육체를 얻고 우주전의 전사가 된다. 재청춘의 기쁨과 전쟁의 윤리가 충돌하는 군사 SF.",
             info_url="https://en.wikipedia.org/wiki/Old_Man%27s_War"),
    add_book("레비아탄 각성 (Leviathan Wakes)", "James S. A. Corey", 2011,
             ["Space Opera","Hard SF","Political"], ["politics","war","survival","society"],
             4,4,3,4,"balanced", 0.45, 0.40, "태양계 리얼리즘과 정치 스릴러가 결합한 익스팬스 1권."),
    add_book("견인도시 (Mortal Engines)", "Philip Reeve", 2001,
             ["Dystopia","Steampunk","Adventure"], ["memory","society","ecology"],
             2,5,3,4,"hopeful", 0.20, 0.25, "바퀴 달린 도시들이 서로를 사냥하는 세계. 성장과 세대의 기억이 문명의 폭주를 비춘다.",
             info_url="https://en.wikipedia.org/wiki/Mortal_Engines"),
    add_book("세븐 이브스 (Seveneves)", "Neal Stephenson", 2015,
             ["Hard SF","Apocalypse"], ["survival","engineering","society","math"],
             5,2,2,2,"dark", 0.90, 0.80, "달 붕괴 이후 궤도에서 인류 보존을 설계하는 극하드 SF."),
    add_book("라마와의 랑데부 (Rendezvous with Rama)", "Arthur C. Clarke", 1973,
             ["Hard SF","First Contact"], ["mystery","exploration","physics"],
             4,2,3,3,"cool", 0.75, 0.70, "태양계에 진입한 거대 실린더 내부 탐사. 침묵하는 신비와 과학적 경외."),
    add_book("2001 스페이스 오디세이 (2001: A Space Odyssey)", "Arthur C. Clarke", 1968,
             ["Hard SF","Philosophical"], ["ai","evolution","mystery"],
             4,2,2,2,"cool", 0.80, 0.70, "모노리스, HAL, 인류 진화가 교차하는 장중한 우주 서사."),
    add_book("하이페리온 (Hyperion)", "Dan Simmons", 1989,
             ["Space Opera","Philosophical"], ["religion","memory","time"],
             3,3,2,3,"dark", 0.50, 0.50, "성지 순례자들의 이야기로 짜인 시적 스페이스 오페라."),
    add_book("마션 (The Martian)", "Andy Weir", 2011,
             ["Hard SF","Survival"], ["engineering","humor","survival"],
             4,4,4,4,"hopeful", 0.55, 0.45, "화성 고립 생존기. 공학적 상상력과 유머가 돋보인다."),
    add_book("콘택트 (Contact)", "Carl Sagan", 1985,
             ["Hard SF","First Contact","Philosophical"], ["faith","science","communication"],
             3,4,3,3,"balanced", 0.55, 0.45, "외계 신호 해독 여정. 과학과 신앙, 소통의 가능성."),
    add_book("스노 크래시 (Snow Crash)", "Neal Stephenson", 1992,
             ["Cyberpunk","Dystopia"], ["media","language","society","technology"],
             3,2,2,5,"dark", 0.70, 0.70, "메타버스·언어 바이러스가 교차하는 하이퍼 액션 사이버펑크."),
    add_book("멋진 신세계 (Brave New World)", "Aldous Huxley", 1932,
             ["Dystopia"], ["bioethics","society","freedom"],
             1,4,1,3,"dark", 0.60, 0.60, "쾌락과 유전 조작으로 유지되는 안정 사회의 대가."),
    add_book("1984 (Nineteen Eighty-Four)", "George Orwell", 1949,
             ["Dystopia"], ["surveillance","language","politics"],
             1,3,1,3,"dark", 0.60, 0.70, "감시와 언어 통제가 지배하는 전체주의 구조 해부."),
    add_book("화씨 451 (Fahrenheit 451)", "Ray Bradbury", 1953,
             ["Dystopia"], ["media","censorship","freedom"],
             1,4,2,3,"dark", 0.55, 0.55, "책을 불태우는 소방관의 각성. 검열 사회의 저항."),
    add_book("나를 보내지 마 (Never Let Me Go)", "Kazuo Ishiguro", 2005,
             ["Dystopia","Biopunk","Philosophical"], ["identity","memory","ethics"],
             1,5,1,2,"sad", 0.35, 0.40, "평범한 기숙학교의 비밀. 정체성과 존엄을 묻는 서정."),
    add_book("시간의 아이들 (Children of Time)", "Adrian Tchaikovsky", 2015,
             ["Space Opera","Evolution"], ["evolution","ecology","ai"],
             3,3,3,3,"balanced", 0.55, 0.55, "테라포밍 실험이 낳은 뜻밖의 지성과의 평행 진화."),
    add_book("어둠의 왼손 (The Left Hand of Darkness)", "Ursula K. Le Guin", 1969,
             ["Anthropological","Philosophical"], ["gender","culture","politics"],
             2,5,3,2,"cool", 0.30, 0.30, "젠더가 유동적인 혹성에서 문화 이해의 윤리를 탐구."),
    add_book("듄 (Dune)", "Frank Herbert", 1965,
             ["Space Opera","Political","Ecology"], ["politics","religion","ecology"],
             3,3,2,3,"dark", 0.50, 0.60, "사막 행성의 향신료를 둘러싼 권력·예언·생태의 장편 서사."),
    add_book("엔더의 게임 (Ender’s Game)", "Orson Scott Card", 1985,
             ["Military SF","YA"], ["war","ethics","identity"],
             2,3,3,5,"balanced", 0.45, 0.50, "천재 소년의 전술 훈련과 승리 뒤의 윤리."),
    add_book("얼터드 카본 (Altered Carbon)", "Richard K. Morgan", 2002,
             ["Cyberpunk","Noir"], ["identity","memory","inequality","technology"],
             3,2,1,4,"dark", 0.70, 0.75, "의식 저장·이식 사회의 느와르 추적극."),
    add_book("당신 인생의 이야기 (Story of Your Life)", "Ted Chiang", 1998,
             ["Philosophical","First Contact"], ["language","time","love"],
             2,5,3,2,"quiet", 0.25, 0.25, "외계 언어 학습이 시간 감각을 변형하는 섬세한 서사."),
    add_book("숨 (Exhalation)", "Ted Chiang", 2008,
             ["Philosophical"], ["entropy","consciousness"],
             2,5,3,2,"quiet", 0.30, 0.30, "기계 생명체의 자가 해부로 우주의 운명을 성찰."),
    add_book("격리 (Quarantine)", "Greg Egan", 1992,
             ["Hard SF","Philosophical"], ["quantum","consciousness","physics"],
             5,2,2,3,"cool", 0.85, 0.75, "지구가 양자 거품에 갇힌 세계. 관찰과 의식의 과격한 가설 실험."),
    add_book("삼체 (The Three-Body Problem)", "Liu Cixin", 2006,
             ["Hard SF","Cosmic"], ["civilization","math","survival","physics"],
             4,2,1,3,"dark", 0.80, 0.80, "문혁의 상처와 우주적 위기의 결절. 수학·물리 퍼즐이 서사를 견인."),
    add_book("보조정의 (Ancillary Justice)", "Ann Leckie", 2013,
             ["Space Opera","AI"], ["identity","ai","empire"],
             3,3,3,3,"cool", 0.55, 0.55, "함대 AI의 파편이 인간 개체로 살아남아 제국에 맞선다."),
    add_book("솔라리스 (Solaris)", "Stanislaw Lem", 1961,
             ["Philosophical","First Contact"], ["memory","alien","consciousness"],
             3,3,2,2,"sad", 0.45, 0.50, "바다 행성의 지성이 인간 기억을 실체화하는 타자성의 심연."),
    add_book("빼앗긴 자들 (The Dispossessed)", "Ursula K. Le Guin", 1974,
             ["Political","Philosophical"], ["utopia","anarchism","ethics"],
             2,5,3,2,"quiet", 0.30, 0.35, "두 행성의 상반된 체제 사이에서 과학자가 다리를 놓는다."),
    add_book("파운데이션 (Foundation)", "Isaac Asimov", 1951,
             ["Space Opera","Political"], ["history","society","math"],
             2,2,3,3,"cool", 0.70, 0.70, "역사를 확률적으로 예측하는 과학과 제국의 흥망."),
    add_book("뉴로맨서 (Neuromancer)", "William Gibson", 1984,
             ["Cyberpunk"], ["ai","media","society","technology"],
             3,2,2,4,"dark", 0.65, 0.65, "사이버펑크의 정초. 네온빛 자본과 정체성의 파편."),
    add_book("영원한 전쟁 (The Forever War)", "Joe Haldeman", 1974,
             ["Military SF","Relativistic"], ["war","time","alienation"],
             3,3,2,3,"cool", 0.60, 0.55, "상대론적 시간 지연 속에서 병사는 고향과 시대를 잃는다."),
    add_book("깊은 숲 속의 불 (A Fire Upon the Deep)", "Vernor Vinge", 1992,
             ["Space Opera","Hard SF"], ["ai","evolution","cosmic"],
             4,3,3,3,"balanced", 0.65, 0.60, "지성의 영역이 구획된 우주에서 슈퍼지성의 위협에 맞선다."),
    add_book("무기 사용 지침 (Use of Weapons)", "Iain M. Banks", 1990,
             ["Space Opera","Philosophical"], ["ethics","war","culture"],
             3,3,2,3,"dark", 0.55, 0.55, "개입주의 문명 컬처의 어두운 수행자—비선형 구조의 윤리."),
    add_book("엔더의 그림자 (Speaker for the Dead)", "Orson Scott Card", 1986,
             ["First Contact","Philosophical"], ["ethics","culture","memory"],
             3,4,3,3,"quiet", 0.45, 0.45, "타자 문명을 오독하지 않기 위한 ‘말하는 자’의 의식."),
    add_book("유년기의 끝 (Childhood’s End)", "Arthur C. Clarke", 1953,
             ["Hard SF","Philosophical"], ["evolution","mystery","transcendence"],
             3,3,2,2,"cool", 0.70, 0.60, "자애로운 외계 간섭 아래 인류가 초월로 나아간다.")
]
df = pd.DataFrame(BOOKS)
df["tags"] = df["tags"].apply(_to_list)

# =========================
# 프리셋 (최대 7개)
# =========================
SIMPLE_PRESETS = {
    "선택 안 함": {},
    "리얼리즘 스페이스 오페라": {
        "tags": ["Space Opera","Political","society","war","survival"],
        "hard": 3, "human": 4, "pace": 4, "tone": "balanced"
    },
    "철저한 하드SF": {
        "tags": ["Hard SF","engineering","exploration","math","physics","First Contact"],
        "hard": 5, "human": 3, "pace": 3, "tone": "cool"
    },
    "철학적·인문적 SF": {
        "tags": ["Philosophical","identity","consciousness","memory","ethics","language"],
        "hard": 2, "human": 5, "pace": 2, "tone": "quiet"
    },
    "디스토피아와 사회 비판": {
        "tags": ["Dystopia","society","politics","freedom","bioethics","censorship"],
        "hard": 2, "human": 4, "pace": 3, "tone": "dark"
    },
    "사이버펑크 & 테크누아르": {
        "tags": ["Cyberpunk","AI","media","inequality","noir","technology"],
        "hard": 3, "human": 2, "pace": 4, "tone": "dark"
    },
    "우주 탐사 & 초월": {
        "tags": ["exploration","mystery","evolution","cosmic","transcendence"],
        "hard": 4, "human": 3, "pace": 3, "tone": "cool"
    },
    "휴머니즘·감성 중심 SF": {
        "tags": ["love","family","bond","memory","ethics","society"],
        "hard": 2, "human": 5, "pace": 3, "tone": "hopeful"
    }
}

# =========================
# 세션 상태 초기화
# =========================
if "applied" not in st.session_state:
    st.session_state.applied = {
        "pick_tags": [],
        "hard": 3, "human": 4, "pace": 3, "tone": "balanced",
        "need_ko": True, "year_min": int(df["year"].min()), "year_max": 2025,
        "weights": dict(w_tags=1.2, w_hard=1.0, w_human=1.2, w_pace=0.8, w_tone=0.8),
        "top_n": 8
    }

# temp_* 컨트롤 상태(왼쪽 UI에 보이는 값)를 한 번만 초기화
if "temp_initialized" not in st.session_state:
    ap = st.session_state.applied
    st.session_state.temp_pick_tags = ap["pick_tags"]
    st.session_state.temp_hard = ap["hard"]
    st.session_state.temp_human = ap["human"]
    st.session_state.temp_pace = ap["pace"]
    st.session_state.temp_tone = ap["tone"]
    st.session_state.temp_need_ko = ap["need_ko"]
    st.session_state.temp_year_min = ap["year_min"]
    st.session_state.temp_year_max = ap["year_max"]
    st.session_state.temp_top_n = ap["top_n"]
    st.session_state.temp_initialized = True

# =========================
# 프리셋 변경 시 즉시 왼쪽 컨트롤에 반영
# (폼 없이 on_change 사용)
# =========================
def on_preset_change():
    selected = st.session_state.preset
    if selected != "선택 안 함":
        p = SIMPLE_PRESETS[selected]
        # 태그만 옵션에 있는 값으로 정리
        all_tags_local = sorted({str(t) for row in df["tags"] for t in _to_list(row)})
        st.session_state.temp_pick_tags = _sanitize_defaults(p["tags"], all_tags_local)
        st.session_state.temp_hard = p["hard"]
        st.session_state.temp_human = p["human"]
        st.session_state.temp_pace = p["pace"]
        st.session_state.temp_tone = p["tone"]
    # 연도/번역우선/추천개수는 유지(요청 의도)

# =========================
# 사이드바 (실시간 반영 + 적용 버튼 1개)
# =========================
with st.sidebar:
    st.title("🎛️ 취향 설정")

    # 프리셋: 선택 바꾸면 즉시 temp_*에 반영
    st.selectbox("빠른 프리셋", list(SIMPLE_PRESETS.keys()),
                 key="preset", on_change=on_preset_change)

    all_tags = sorted({str(t) for row in df["tags"] for t in _to_list(row)})
    # temp_pick_tags가 옵션에 없을 수 있으니 정리
    st.session_state.temp_pick_tags = _sanitize_defaults(st.session_state.temp_pick_tags, all_tags)

    st.multiselect("선호 태그(서브장르/테마 통합)", all_tags,
                   key="temp_pick_tags")

    colA, colB = st.columns(2)
    with colA:
        st.slider("난이도(하드함)", 1, 5, key="temp_hard")
        st.slider("휴머니즘", 1, 5, key="temp_human")
        st.slider("전개 속도", 1, 5, key="temp_pace")
    with colB:
        st.select_slider("톤", options=["dark","cool","balanced","hopeful","quiet"], key="temp_tone")
        st.checkbox("한국어 번역 우선", key="temp_need_ko")
        st.slider("추천 개수", 3, 12, key="temp_top_n")

    st.slider("출간 연도 범위",
              min_value=int(df["year"].min()), max_value=2025,
              value=(st.session_state.temp_year_min, st.session_state.temp_year_max),
              key=None)  # 표시만; 아래 두 개를 따로 유지
    # 위 슬라이더를 두 값으로 나누어 저장하려면 아래처럼 커스텀 처리도 가능하지만,
    # 간단히는 범위 슬라이더를 직접 키에 바인딩:
    st.session_state.temp_year_min, st.session_state.temp_year_max = st.slider(
        "연도 범위(동일 기능, 상태 반영용)", min_value=int(df["year"].min()), max_value=2025,
        value=(st.session_state.temp_year_min, st.session_state.temp_year_max)
    )

    # 적용 버튼 하나만 유지
    if st.button("왼쪽 설정 전체 적용"):
        st.session_state.applied = {
            "pick_tags": _sanitize_defaults(st.session_state.temp_pick_tags, all_tags),
            "hard": st.session_state.temp_hard,
            "human": st.session_state.temp_human,
            "pace": st.session_state.temp_pace,
            "tone": st.session_state.temp_tone,
            "need_ko": st.session_state.temp_need_ko,
            "year_min": st.session_state.temp_year_min,
            "year_max": st.session_state.temp_year_max,
            "weights": st.session_state.applied["weights"],  # 가중치는 유지
            "top_n": st.session_state.temp_top_n
        }
        st.success("왼쪽 설정 전체가 적용되었습니다.")

# =========================
# 추천 & 표시
# =========================
ap = st.session_state.applied

def score_row(row) -> float:
    try:
        s_tags = jaccard(ap.get("pick_tags", []), row.get("tags", [])) if ap.get("pick_tags") else 0.5
        s_hard = 1 - (abs(float(row.get("hardness", 3)) - float(ap.get("hard", 3))) / 4)
        s_human = 1 - (abs(float(row.get("humanism", 3)) - float(ap.get("human", 3))) / 4)
        s_pace = 1 - (abs(float(row.get("pace", 3)) - float(ap.get("pace", 3))) / 4)
        s_tone = tone_match(str(row.get("tone", "balanced")), str(ap.get("tone", "balanced")))
        w = ap.get("weights", {"w_tags":1.2, "w_hard":1.0, "w_human":1.2, "w_pace":0.8, "w_tone":0.8})
        score = (w["w_tags"]*s_tags + w["w_hard"]*s_hard + w["w_human"]*s_human +
                 w["w_pace"]*s_pace + w["w_tone"]*s_tone)
        if ap.get("need_ko", True) and bool(row.get("ko", True)): score += 0.2
        return float(score)
    except Exception:
        return 0.0

mask = df["year"].between(ap["year_min"], ap["year_max"])
if ap["need_ko"]: mask &= df["ko"]
df_f = df[mask].copy()
df_f["score"] = df_f.apply(score_row, axis=1).astype(float)
df_f = df_f.sort_values("score", ascending=False)
results = df_f.head(ap["top_n"])

st.title("🚀 개인 취향 기반 SF 소설 추천기")
st.caption("‘빠른 프리셋’을 바꾸면 왼쪽 컨트롤이 즉시 바뀝니다. **왼쪽 설정 전체 적용**을 눌러 최종 반영하세요.")

st.subheader("추천 결과")
for _, r in results.iterrows():
    st.markdown(f"""
**{r['title']}** · *{r['author']}* ({int(r['year'])})  
- 요약: {r['summary']}  
- 태그: `{", ".join(_to_list(r['tags']))}`  
- 점수: **{r['score']:.2f}**
""")
    if r.get("info_url"):
        st.markdown(f"[자세히 보기]({r['info_url']})")
    st.divider()

st.subheader("철학 좌표에서 보기")
fig = px.scatter(
    results, x="x_axis", y="y_axis",
    text="title", hover_name="title",
    hover_data={"author": True, "year": True, "summary": True, "x_axis": False, "y_axis": False},
    labels={"x_axis": "← 과학의 서사화 | 서사의 과학화 →",
            "y_axis": "인간 중심 ↓ | 시스템 중심 ↑"}
)
fig.update_traces(textposition="top center", marker=dict(size=10))
fig.add_vline(x=0.5, line_width=3, line_color="black")
fig.add_hline(y=0.5, line_width=3, line_color="black")
st.plotly_chart(fig, use_container_width=False)


st.caption("""
**축 해석 안내**  
- **가로축(X)**: 왼쪽은 *과학의 서사화* — 이야기(인물·감정)가 중심이고 과학은 서사를 돕는 재료.  
  오른쪽은 *서사의 과학화* — 과학·공학적 규칙과 시스템이 서사의 추진력.  
- **세로축(Y)**: 위쪽은 *시스템 중심* — 정치·경제·생태·기술 같은 거대 구조가 핵심.  
  아래쪽은 *인간 중심* — 관계·감정·윤리의 비중이 큼.
""")
