import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import platform

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(page_title="볼록렌즈 광선 추적", layout="wide")

# 2. 한글 폰트 설정 (운영체제별 처리)
os_name = platform.system()
if os_name == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif os_name == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
else:
    # Linux (스트림릿 클라우드 등)
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

st.title("🔍 볼록렌즈 광선 추적 시뮬레이션")
st.markdown("기존 HTML/JS 시뮬레이션을 **Streamlit 네이티브 파이썬 환경**으로 완벽하게 변환한 버전입니다.")

# 3. 레이아웃 분할: 왼쪽 컨트롤, 오른쪽 시각화
col_ctrl, col_viz = st.columns([1, 3])

with col_ctrl:
    st.header("⚙️ 변인 설정")
    # 기존 HTML의 <input type="range">를 스트림릿의 st.slider로 변환
    f = st.slider("초점 거리 (f) [cm]", min_value=40, max_value=200, value=80, step=1)
    a = st.slider("물체 거리 (a) [cm]", min_value=10, max_value=600, value=200, step=1)
    h_obj = st.slider("물체 높이 (h) [cm]", min_value=10, max_value=120, value=60, step=1)
    zoom = st.slider("화면 축소/확대 (Zoom) [%]", min_value=20, max_value=150, value=100, step=1) / 100.0

# 4. 물리량 계산 (렌즈 방정식)
if a == f:
    b = float('inf')
    m = float('inf')
    h_img = float('inf')
    is_real = None
else:
    b = (a * f) / (a - f)
    m = -b / a
    h_img = m * h_obj
    is_real = b > 0

with col_viz:
    # 기존 HTML의 info-bar 영역을 스트림릿의 st.metric으로 변환
    m1, m2, m3 = st.columns(3)
    if a == f:
        m1.metric("상 위치 (b)", "∞")
        m2.metric("배율 (m)", "-")
        m3.metric("상 종류", "상이 맺히지 않음")
    else:
        m1.metric("상 위치 (b)", f"{abs(b):.1f} cm")
        m2.metric("배율 (m)", f"{abs(m):.2f}")
        type_str = "도립 실상" if is_real else "정립 허상"
        size_str = "같은 크기" if abs(abs(m) - 1) < 0.01 else ("확대" if abs(m) > 1 else "축소")
        m3.metric("상 종류", f"{type_str}, {size_str}")

    # 5. Matplotlib을 이용한 광선 추적 시각화
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_aspect('equal') # 기하학적 왜곡 방지를 위해 x, y 비율 고정
    ax.axis('off')         # 기본 테두리 제거

    # 광축
    ax.axhline(0, color='#cbd5e1', linestyle='--', linewidth=1.5, zorder=1)

    # 렌즈 그리기
    lens_width = 15 * min(zoom, 1.2)
    lens_height = 150 * zoom
    lens = patches.Ellipse((0, 0), width=lens_width, height=lens_height,
                           facecolor='#bae6fd', edgecolor='#0ea5e9', alpha=0.5, linewidth=2, zorder=2)
    ax.add_patch(lens)

    # 초점 (F, F')
    ax.plot([-f, f], [0, 0], 'o', color='#1e293b', markersize=5, zorder=3)
    ax.text(-f, -15*zoom, 'F', color='#1e293b', ha='center', va='top', fontweight='bold')
    ax.text(f, -15*zoom, "F'", color='#1e293b', ha='center', va='top', fontweight='bold')

    # 화살표 그리는 보조 함수
    def draw_arrow(x, y_tip, color, label):
        ax.annotate('', xy=(x, y_tip), xytext=(x, 0),
                    arrowprops=dict(arrowstyle='-|>', color=color, lw=2.5, mutation_scale=15), zorder=4)
        offset = 15*zoom if y_tip > 0 else -25*zoom
        ax.text(x, y_tip + offset, label, color=color, ha='center', fontweight='bold')

    # 물체(O) 그리기
    draw_arrow(-a, h_obj, '#2563eb', '물체(O)')

    # 상(I) 및 광선 추적 그리기
    if a != f and abs(b) < 5000:
        img_color = '#ef4444' if is_real else '#8b5cf6'
        draw_arrow(b, h_img, img_color, '실상(I)' if is_real else '허상(I)')

        # 광선 1: 주축에 평행하게 입사 -> 초점(F') 통과
        ax.plot([-a, 0], [h_obj, h_obj], color='#f59e0b', lw=1.5, zorder=1)
        slope1 = (h_img - h_obj) / b
        if is_real:
            ext_x = max(b, f + 100)
            ax.plot([0, ext_x], [h_obj, h_obj + slope1 * ext_x], color='#f59e0b', lw=1.5, zorder=1)
        else:
            ax.plot([0, 600], [h_obj, h_obj + slope1 * 600], color='#f59e0b', lw=1.5, zorder=1)
            ax.plot([b, 0], [h_img, h_obj], color='#f59e0b', linestyle='--', lw=1.5, zorder=1)

        # 광선 2: 렌즈 중심 통과 -> 직진
        ax.plot([-a, 0], [h_obj, 0], color='#10b981', lw=1.5, zorder=1)
        slope2 = -h_obj / -a
        if is_real:
            ext_x = max(b, f + 100)
            ax.plot([0, ext_x], [0, slope2 * ext_x], color='#10b981', lw=1.5, zorder=1)
        else:
            ax.plot([0, 600], [0, slope2 * 600], color='#10b981', lw=1.5, zorder=1)
            ax.plot([b, 0], [h_img, 0], color='#10b981', linestyle='--', lw=1.5, zorder=1)

    # 치수선 그리는 보조 함수
    def draw_dim(x1, x2, y, label, color):
        ax.plot([x1, x2], [y, y], color=color, lw=1, alpha=0.7)
        ax.plot([x1, x1], [y-5*zoom, y+5*zoom], color=color, lw=1, alpha=0.7)
        ax.plot([x2, x2], [y-5*zoom, y+5*zoom], color=color, lw=1, alpha=0.7)
        ax.text((x1+x2)/2, y-10*zoom, label, color=color, ha='center', va='top', fontsize=9, alpha=0.8)

    # a, b, f 치수선 표시
    draw_dim(-a, 0, -30*zoom, f"a = {a}cm", "#64748b")
    draw_dim(0, f, -60*zoom, f"f = {f}cm", "#1e293b")
    if a != f and abs(b) < 5000:
        y_img = h_img - 20*zoom if is_real else h_img + 20*zoom
        draw_dim(0, b, y_img, f"b = {abs(b):.1f}cm", img_color)

    # 줌에 따른 화면 뷰포트 자동 조절
    base_window_x = 450 / zoom
    base_window_y = 250 / zoom
    ax.set_xlim(-base_window_x, base_window_x)
    ax.set_ylim(-base_window_y, base_window_y)

    # 6. 스트림릿에 그래프 렌더링
    st.pyplot(fig)
