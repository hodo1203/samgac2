import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import random

# Page configuration
st.set_page_config(
    page_title="삼각함수 탐구 학습 웹앱",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #fcfcfc;
    }
    .stApp {
        background-color: #fcfcfc;
    }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #eaeaea;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .highlight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #3498db;
        margin: 10px 0;
    }
    .math-text {
        font-family: 'Times New Roman', serif;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to format radian values nicely
def format_radian(val):
    pi = np.pi
    fractions = [
        (0, "0"),
        (pi/6, "π/6"),
        (pi/4, "π/4"),
        (pi/3, "π/3"),
        (pi/2, "π/2"),
        (2*pi/3, "2π/3"),
        (3*pi/4, "3π/4"),
        (5*pi/6, "5π/6"),
        (pi, "π"),
        (7*pi/6, "7π/6"),
        (5*pi/4, "5π/4"),
        (4*pi/3, "4π/3"),
        (3*pi/2, "3π/2"),
        (5*pi/3, "5π/3"),
        (7*pi/4, "7π/4"),
        (11*pi/6, "11π/6"),
        (2*pi, "2π"),
        (-pi/6, "-π/6"),
        (-pi/4, "-π/4"),
        (-pi/3, "-π/3"),
        (-pi/2, "-π/2"),
        (-2*pi/3, "-2π/3"),
        (-3*pi/4, "-3π/4"),
        (-5*pi/6, "-5π/6"),
        (-pi, "-π"),
        (-3*pi/2, "-3π/2"),
        (-2*pi, "-2π")
    ]
    for rad, name in fractions:
        if abs(val - rad) < 1e-3:
            return name
    mult = val / pi
    for n in range(-10, 11):
        if n != 0 and abs(mult - n) < 1e-3:
            return f"{n}π" if n != 1 and n != -1 else ("π" if n == 1 else "-π")
    return f"{val:.4f}"

# Title Header
st.title("📐 삼각함수 탐구 학습 웹앱")
st.markdown("##### 그래프 · 단위원 · 역으로 x값 찾기 · 각변환 퀴즈 (각도 단위: **라디안(radian)**)")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("탐구 메뉴")
menu = st.sidebar.radio(
    "이동할 메뉴를 선택하세요:",
    ["1. 삼각함수 그래프 및 x값 찾기", "2. 원에 의한 삼각함수 보기", "3. 삼각함수 각변환 퀴즈", "4. 주요 각의 삼각함수 값 표"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **안내**: 본 웹앱은 모든 각도를 **라디안(radian)** 체계로 계산하고 표시합니다.")

# ==============================================================================
# MENU 1: 삼각함수 그래프 및 x값 찾기
# ==============================================================================
if menu == "1. 삼각함수 그래프 및 x값 찾기":
    st.header("1. 삼각함수 그래프 및 역으로 x값 찾기")
    st.markdown("함수 파라미터를 조절하여 그래프를 실시간으로 확인하고, 특정 y값에 해당하는 모든 x값을 찾아보세요.")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚙️ 삼각함수 그래프 설정")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            func_type = st.selectbox("함수 선택", ["sin", "cos", "tan"])
            amplitude = st.number_input("진폭 (A)", value=1.0, step=0.1)
        with col2:
            default_period = np.pi if func_type == "tan" else 2 * np.pi
            period = st.number_input("주기 (Period)", value=float(default_period), min_value=0.1, step=0.1)
            base_p = np.pi if func_type == "tan" else 2 * np.pi
            B = base_p / period
            
            phase_shift = st.number_input("수평 이동 (C, 라디안)", value=0.0, step=0.1, format="%.2f")
        with col3:
            vertical_shift = st.number_input("수직 이동 (D)", value=0.0, step=0.1)
            
            x_range_option = st.selectbox("x축 표시 범위 설정", ["-2π ~ 2π", "-π ~ π", "-4π ~ 4π", "사용자 지정"])
            if x_range_option == "-2π ~ 2π":
                x_min, x_max = -2 * np.pi, 2 * np.pi
            elif x_range_option == "-π ~ π":
                x_min, x_max = -np.pi, np.pi
            elif x_range_option == "-4π ~ 4π":
                x_min, x_max = -4 * np.pi, 4 * np.pi
            else:
                col_xmin, col_xmax = st.columns(2)
                with col_xmin:
                    x_min = st.number_input("시작값 (라디안)", value=-2.0 * np.pi, step=0.5)
                with col_xmax:
                    x_max = st.number_input("끝값 (라디안)", value=2.0 * np.pi, step=0.5)

        st.markdown('</div>', unsafe_allow_html=True)
        
    if func_type == "tan":
        max_val = "없음 (∞)"
        min_val = "없음 (-∞)"
    else:
        max_val = vertical_shift + amplitude
        min_val = vertical_shift - amplitude

    shift_str = ""
    if phase_shift != 0:
        sign = "-" if phase_shift > 0 else "+"
        shift_str = f"({B:.2f}x {sign} {abs(phase_shift):.2f})"
    else:
        if B == 1.0:
            shift_str = "x"
        else:
            shift_str = f"({B:.2f}x)"
            
    v_str = ""
    if vertical_shift > 0:
        v_str = f" + {vertical_shift}"
    elif vertical_shift < 0:
        v_str = f" - {abs(vertical_shift)}"
        
    formula_display = f"y = {amplitude} \\cdot \\text{{{func_type}}}{shift_str}{v_str}"
    
    st.markdown(f"""
    <div class="highlight-box">
        <h4>현재 함수식: <span class="math">{formula_display}</span></h4>
        <p><b>최댓값:</b> {max_val} &nbsp;&nbsp;|&nbsp;&nbsp; <b>최솟값:</b> {min_val} &nbsp;&nbsp;|&nbsp;&nbsp; <b>주기:</b> {period:.4f} (라디안)</p>
    </div>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(x_min, x_max, 2000)
    
    if func_type == "sin":
        y = amplitude * np.sin(B * (x - phase_shift)) + vertical_shift
    elif func_type == "cos":
        y = amplitude * np.cos(B * (x - phase_shift)) + vertical_shift
    else:
        y = amplitude * np.tan(B * (x - phase_shift)) + vertical_shift
        cos_check = np.cos(B * (x - phase_shift))
        y[np.abs(cos_check) < 1e-2] = np.nan

    ax.plot(x, y, label=f"y = {amplitude}{func_type}({B:.2f}(x-{phase_shift}))+{vertical_shift}", color="#3498db", linewidth=2)
    
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    tick_step = np.pi / 2
    ticks = np.arange(np.floor(x_min / tick_step) * tick_step, np.ceil(x_max / tick_step) * tick_step + tick_step, tick_step)
    ax.set_xticks(ticks)
    ax.set_xticklabels([format_radian(t) for t in ticks])
    
    ax.set_xlabel("x (라디안)", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.set_title("삼각함수 인터랙티브 그래프 (각도 단위: 라디안)", fontsize=14, fontweight='bold')
    ax.legend(loc="upper right")
    
    if "selected_x" in st.session_state and st.session_state["selected_x"] is not None:
        sel_x = st.session_state["selected_x"]
        if func_type == "sin":
            sel_y = amplitude * np.sin(B * (sel_x - phase_shift)) + vertical_shift
        elif func_type == "cos":
            sel_y = amplitude * np.cos(B * (sel_x - phase_shift)) + vertical_shift
        else:
            sel_y = amplitude * np.tan(B * (sel_x - phase_shift)) + vertical_shift
        ax.scatter([sel_x], [sel_y], color='red', s=100, zorder=5, label=f'선택된 해: x={format_radian(sel_x)}')
        ax.legend(loc="upper right")

    st.pyplot(fig)
    st.markdown("---")
    
    st.subheader("🔍 핵심 기능: y값으로부터 x값 찾기")
    st.markdown("지정한 x 범위 내에서 주어진 y값을 만족하는 모든 해(x)를 라디안과 소수 형태로 정확하게 계산합니다.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        target_y = st.number_input("찾을 y값 입력", value=0.5 if func_type != "tan" else 1.0, step=0.1)
    with col_f2:
        finder_xmin = st.number_input("x 범위 최소 (라디안)", value=float(x_min), step=0.5)
    with col_f3:
        finder_xmax = st.number_input("x 범위 최대 (라디안)", value=float(x_max), step=0.5)
        
    if st.button("모든 x 해 계산하기"):
        if amplitude == 0:
            st.warning("진폭이 0인 함수입니다.")
        else:
            val = (target_y - vertical_shift) / amplitude
            solutions = []
            
            if func_type in ["sin", "cos"]:
                if abs(val) > 1.0:
                    st.error(f"입력한 y값({target_y})이 함수의 치역범위([{min_val}, {max_val}])를 벗어나므로 실해가 존재하지 않습니다.")
                else:
                    x_grid = np.linspace(finder_xmin, finder_xmax, 10000)
                    if func_type == "sin":
                        y_grid = amplitude * np.sin(B * (x_grid - phase_shift)) + vertical_shift
                    else:
                        y_grid = amplitude * np.cos(B * (x_grid - phase_shift)) + vertical_shift
                        
                    diff = y_grid - target_y
                    sign_changes = np.where(np.diff(np.sign(diff)))[0]
                    for idx in sign_changes:
                        x1, x2 = x_grid[idx], x_grid[idx+1]
                        root = (x1 + x2) / 2
                        if not any(abs(root - s) < 1e-3 for s in solutions):
                            solutions.append(root)
                            
            elif func_type == "tan":
                base_val = np.arctan(val)
                period_val = np.pi / B
                k_min = int(np.floor((finder_xmin - phase_shift - np.pi) / period_val)) - 2
                k_max = int(np.ceil((finder_xmax - phase_shift + np.pi) / period_val)) + 2
                
                for k in range(k_min, k_max + 1):
                    root = phase_shift + (base_val + k * np.pi) / B
                    if finder_xmin <= root <= finder_xmax:
                        if not any(abs(root - s) < 1e-3 for s in solutions):
                            solutions.append(root)
            
            solutions = sorted(solutions)
            if len(solutions) == 0:
                st.info("입력한 범위에서는 해당 y값을 만족하는 x값이 없습니다.")
                st.session_state["selected_x"] = None
            else:
                st.success(f"총 {len(solutions)}개의 해를 찾았습니다!")
                for i, sol in enumerate(solutions):
                    rad_str = format_radian(sol)
                    col_res1, col_res2 = st.columns([2, 1])
                    with col_res1:
                        st.markdown(f"**해 {i+1}:** `x = {rad_str}` (약 `{sol:.4f}` 라디안)")
                    with col_res2:
                        if st.button(f"그래프에서 확인 #{i+1}", key=f"btn_sol_{i}"):
                            st.session_state["selected_x"] = sol
                            st.rerun()

# ==============================================================================
# MENU 2: 원에 의한 삼각함수 보기 (Plotly 활용 오류 수정본)
# ==============================================================================
elif menu == "2. 원에 의한 삼각함수 보기":
    st.header("2. 단위원(Unit Circle)과 삼각함수 그래프 연동")
    st.markdown("왼쪽 단위원의 각도를 선택하면, 오른쪽 삼각함수 그래프와 실시간으로 연동되어 나타납니다.")
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.subheader("좌측: 단위원 (Unit Circle)")
        theta_deg_slider = st.slider("각도 선택 (도 단위 슬라이더)", 0, 360, 45, 5)
        theta_rad = np.radians(theta_deg_slider)
        
        fig_uc, ax_uc = plt.subplots(figsize=(5, 5))
        circle = plt.Circle((0, 0), 1, color='#3498db', fill=False, linewidth=2, linestyle='--')
        ax_uc.add_patch(circle)
        
        px, py = np.cos(theta_rad), np.sin(theta_rad)
        ax_uc.plot([0, px], [0, py], color='red', linewidth=2, marker='o', label=f'P({px:.2f}, {py:.2f})')
        ax_uc.axhline(0, color='black', linewidth=1)
        ax_uc.axvline(0, color='black', linewidth=1)
        ax_uc.set_xlim(-1.3, 1.3)
        ax_uc.set_ylim(-1.3, 1.3)
        ax_uc.set_aspect('equal')
        ax_uc.grid(True, linestyle=':', alpha=0.6)
        ax_uc.set_title(f"단위원 (θ = {format_radian(theta_rad)})", fontsize=12, fontweight='bold')
        ax_uc.legend(loc="upper right")
        st.pyplot(fig_uc)
        
        sin_val = np.sin(theta_rad)
        cos_val = np.cos(theta_rad)
        if abs(np.cos(theta_rad)) < 1e-5:
            tan_str = "정의되지 않음"
        else:
            tan_val = np.tan(theta_rad)
            tan_str = f"{tan_val:.4f}"
            
        # 첫 번째 사진에 있던 불필요한 하단 실시간 값 박스는 완전히 제거되었습니다.

    with col_c2:
        st.subheader("우측: 삼각함수 그래프 연동")
        show_sin = st.checkbox("sin(θ) 표시", value=True)
        show_cos = st.checkbox("cos(θ) 표시", value=True)
        show_tan = st.checkbox("tan(θ) 표시", value=True)
        
        # Plotly를 활용한 안정적인 인터랙티브 그래프 구현 (오류 수정 완료)
        fig_tg = go.Figure()
        x_vals = np.linspace(0, 2 * np.pi, 500)
        
        if show_sin:
            fig_tg.add_trace(go.Scatter(x=x_vals, y=np.sin(x_vals), mode='lines', name='y = sin x', line=dict(color='#e74c3c', width=2)))
            fig_tg.add_trace(go.Scatter(x=[theta_rad % (2*np.pi)], y=[np.sin(theta_rad)], mode='markers', name='sin(θ)', marker=dict(color='#e74c3c', size=10)))
            
        if show_cos:
            fig_tg.add_trace(go.Scatter(x=x_vals, y=np.cos(x_vals), mode='lines', name='y = cos x', line=dict(color='#2ecc71', width=2)))
            fig_tg.add_trace(go.Scatter(x=[theta_rad % (2*np.pi)], y=[np.cos(theta_rad)], mode='markers', name='cos(θ)', marker=dict(color='#2ecc71', size=10)))
            
        if show_tan:
            y_t = np.tan(x_vals)
            y_t[np.abs(np.cos(x_vals)) < 1e-2] = np.nan
            fig_tg.add_trace(go.Scatter(x=x_vals, y=y_t, mode='lines', name='y = tan x', line=dict(color='#9b59b6', width=2)))
            if abs(np.cos(theta_rad)) > 1e-2:
                fig_tg.add_trace(go.Scatter(x=[theta_rad % (2*np.pi)], y=[np.tan(theta_rad)], mode='markers', name='tan(θ)', marker=dict(color='#9b59b6', size=10)))

        # 수직선 추가 오류 수정 (y0, y1 파라미터 정상 반영)
        fig_tg.add_shape(type="line", x0=theta_rad % (2*np.pi), y0=-2, x1=theta_rad % (2*np.pi), y1=2,
                         line=dict(color="gray", dash="dash", width=1))
        
        fig_tg.update_layout(
            title=f"삼각함수 그래프 (θ = {format_radian(theta_rad)})",
            xaxis_title="x (라디안)",
            yaxis_title="y",
            xaxis=dict(range=[0, 2 * np.pi], tickvals=[0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ticktext=["0", "π/2", "π", "3π/2", "2π"]),
            yaxis=dict(range=[-3, 3]),
            height=450,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_tg, use_container_width=True)

# ==============================================================================
# MENU 3: 삼각함수 각변환 퀴즈
# ==============================================================================
elif menu == "3. 삼각함수 각변환 퀴즈":
    st.header("3. 삼각함수 각변환 마스터 퀴즈 (총 10문항)")
    st.markdown("고등학교 수학 교육과정에 나오는 대표적인 삼각함수 각변환 공식 10문제를 풀어보세요.")
    
    if "quiz_questions" not in st.session_state:
        question_pool = [
            {"q": r"\sin(\pi - \theta)", "ans": r"\sin\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\pi - \theta$는 제2사분면의 각이므로 $\sin$의 부호는 양수(+)입니다. 따라서 $\sin(\pi - \theta) = \sin\theta$입니다."},
            {"q": r"\cos(\pi - \theta)", "ans": r"-\cos\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\pi - \theta$는 제2사분면의 각이므로 $\cos$의 부호는 음수(-)입니다. 따라서 $\cos(\pi - \theta) = -\cos\theta$입니다."},
            {"q": r"\tan(\pi - \theta)", "ans": r"-\tan\theta", "options": [r"\tan\theta", r"-\tan\theta", r"\frac{1}{\tan\theta}", r"-\frac{1}{\tan\theta}"], "expl": r"$\pi - \theta$는 제2사분면의 각이므로 $\tan$의 부호는 음수(-)입니다. 따라서 $\tan(\pi - \theta) = -\tan\theta$입니다."},
            {"q": r"\sin(\pi + \theta)", "ans": r"-\sin\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\pi + \theta$는 제3사분면의 각이므로 $\sin$의 부호는 음수(-)입니다. 따라서 $\sin(\pi + \theta) = -\sin\theta$입니다."},
            {"q": r"\cos(\pi + \theta)", "ans": r"-\cos\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\pi + \theta$는 제3사분면의 각이므로 $\cos$의 부호는 음수(-)입니다. 따라서 $\cos(\pi + \theta) = -\cos\theta$입니다."},
            {"q": r"\tan(\pi + \theta)", "ans": r"\tan\theta", "options": [r"\tan\theta", r"-\tan\theta", r"\frac{1}{\tan\theta}", r"-\frac{1}{\tan\theta}"], "expl": r"$\tan$의 주기는 $\pi$이므로 $\tan(\pi + \theta) = \tan\theta$입니다."},
            {"q": r"\sin\left(\frac{\pi}{2} - \theta\right)", "ans": r"\cos\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\frac{\pi}{2} - \theta$는 제1사분면의 각이며 여함수 공식에 의해 $\sin\left(\frac{\pi}{2} - \theta\right) = \cos\theta$입니다."},
            {"q": r"\cos\left(\frac{\pi}{2} - \theta\right)", "ans": r"\sin\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\frac{\pi}{2} - \theta$는 제1사분면이며 $\cos\left(\frac{\pi}{2} - \theta\right) = \sin\theta$입니다."},
            {"q": r"\sin\left(\frac{\pi}{2} + \theta\right)", "ans": r"\cos\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\frac{\pi}{2} + \theta$는 제2사분면이며 $\sin$은 양수이므로 $\sin\left(\frac{\pi}{2} + \theta\right) = \cos\theta$입니다."},
            {"q": r"\cos\left(\frac{\pi}{2} + \theta\right)", "ans": r"-\sin\theta", "options": [r"\sin\theta", r"-\sin\theta", r"\cos\theta", r"-\cos\theta"], "expl": r"$\frac{\pi}{2} + \theta$는 제2사분면이며 $\cos$는 음수이므로 $\cos\left(\frac{\pi}{2} + \theta\right) = -\sin\theta$입니다."}
        ]
        random.shuffle(question_pool)
        st.session_state["quiz_questions"] = question_pool[:10]
        st.session_state["quiz_status"] = ["unanswered"] * 10
        st.session_state["user_answers"] = [""] * 10

    if st.button("🔄 퀴즈 새로 고침 및 다시 시작"):
        random.shuffle(st.session_state["quiz_questions"])
        st.session_state["quiz_status"] = ["unanswered"] * 10
        st.session_state["user_answers"] = [""] * 10
        st.rerun()

    for idx, q_data in enumerate(st.session_state["quiz_questions"]):
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        st.markdown(f"#### 문제 {idx+1}. 다음 삼각함수를 간단히 하시오:")
        st.latex(f"{q_data['q']} = ?")
        
        status = st.session_state["quiz_status"][idx]
        options = q_data["options"]
        selected_ans = st.radio(f"보기 선택 #{idx+1}", options, key=f"q_radio_{idx}", index=None if st.session_state["user_answers"][idx] == "" else options.index(st.session_state["user_answers"][idx]) if st.session_state["user_answers"][idx] in options else 0)
        
        if st.button("답안 제출", key=f"sub_{idx}") and selected_ans is not None:
            st.session_state["user_answers"][idx] = selected_ans
            if selected_ans == q_data["ans"]:
                if st.session_state["quiz_status"][idx] == "unanswered":
                    st.session_state["quiz_status"][idx] = "correct"
                elif st.session_state["quiz_status"][idx] == "incorrect_once":
                    st.session_state["quiz_status"][idx] = "resolved_second"
                st.rerun()
            else:
                if st.session_state["quiz_status"][idx] == "unanswered":
                    st.session_state["quiz_status"][idx] = "incorrect_once"
                    st.rerun()
                elif st.session_state["quiz_status"][idx] == "incorrect_once":
                    st.session_state["quiz_status"][idx] = "failed"
                    st.rerun()

        if status == "correct":
            st.success("🎉 정답입니다!")
            st.markdown(f"**해설:** {q_data['expl']}")
        elif status == "incorrect_once":
            st.warning("⚠️ 틀렸습니다. 다시 한번 시도해보세요! (기회 1회 남음)")
        elif status == "resolved_second":
            st.success("✅ 두 번째 시도에서 맞혔습니다!")
            st.markdown(f"**해설:** {q_data['expl']}")
        elif status == "failed":
            st.error(f"❌ 오답입니다. 정답은 **{q_data['ans']}** 입니다.")
            st.markdown(f"**해설:** {q_data['expl']}")
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MENU 4: 주요 각의 삼각함수 값 표
# ==============================================================================
elif menu == "4. 주요 각의 삼각함수 값 표":
    st.header("4. 주요 각의 삼각함수 값 표")
    st.markdown("고등학교 수학 특수각(0°, 30°, 45°, 60°, 90°)에 대한 라디안 값과 삼각함수 값 표입니다.")
    
    data = [
        {"도(Degree)": "0°", "라디안(Radian)": "0", "sin": "0", "cos": "1", "tan": "0"},
        {"도(Degree)": "30°", "라디안(Radian)": "π/6", "sin": "1/2", "cos": "√3/2", "tan": "√3/3"},
        {"도(Degree)": "45°", "라디안(Radian)": "π/4", "sin": "√2/2", "cos": "√2/2", "tan": "1"},
        {"도(Degree)": "60°", "라디안(Radian)": "π/3", "sin": "√3/2", "cos": "1/2", "tan": "√3"},
        {"도(Degree)": "90°", "라디안(Radian)": "π/2", "sin": "1", "cos": "0", "tan": "정의되지 않음 (∞)"}
    ]
    df = pd.DataFrame(data)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)
