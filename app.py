# Let's write the complete Streamlit app code for the Trig Learning Web App.
# We will create a single self-contained app.py and a requirements.txt.

app_code = '''import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

# Page configuration
st.set_page_config(
    page_title="삼각함수 탐구 학습 웹앱",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(\"\"\"
<style>
    .main {
        background-color: #f8fafc;
    }
    .stApp {
        background-color: #f8fafc;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .highlight-box {
        background-color: #fef3c7;
        border: 1px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
</style>
\"\"\", unsafe_allow_html=True)

# Helper function to format radian nicely
def format_radian(val):
    # Check common fractions of pi
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
        (-pi, "-π"),
        (-3*pi/2, "-3π/2"),
        (-2*pi, "-2π")
    ]
    
    for f_val, f_str in fractions:
        if abs(val - f_val) < 1e-3:
            return f_str
    
    # Check multiples of pi
    mult = val / pi
    for n in range(-6, 7):
        if abs(mult - n) < 1e-3:
            if n == 0:
                return "0"
            elif n == 1:
                return "π"
            elif n == -1:
                return "-π"
            else:
                return f"{n}π"
        if abs(mult - (n + 0.5)) < 1e-3:
            num = 2*n + 1
            if num == 1:
                return "π/2"
            elif num == -1:
                return "-π/2"
            else:
                return f"{num}π/2"
        if abs(mult - n/6) < 1e-3 and n != 0:
            return f"{n}π/6"
        if abs(mult - n/4) < 1e-3 and n != 0:
            return f"{n}π/4"
        if abs(mult - n/3) < 1e-3 and n != 0:
            return f"{n}π/3"

    return f"{val:.4f}"

# Main Title and Subtitle
st.title("📐 삼각함수 탐구 학습 웹앱")
st.markdown("##### 그래프 · 단위원 · 역으로 x값 찾기 · 각변환 퀴즈 | **각도 단위: 라디안 (Radian)**")
st.markdown("---")

# Navigation Menu
menu = st.sidebar.radio("📚 학습 메뉴 선택", [
    "1. 삼각함수 그래프 및 역으로 x값 찾기",
    "2. 원에 의한 삼각함수 보기",
    "3. 삼각함수 각변환 퀴즈",
    "4. 주요 각의 삼각함수 값 표"
], index=0)

st.sidebar.markdown("---")
st.sidebar.info("💡 **안내**: 모든 계산과 표시는 **라디안(radian)** 단위를 기준으로 동작합니다.")

# ==========================================
# 1. 삼각함수 그래프 및 역으로 x값 찾기
# ==========================================
if menu == "1. 삼각함수 그래프 및 역으로 x값 찾기":
    st.header("📈 1. 삼각함수 그래프 및 역으로 x값 찾기")
    st.markdown("상단에서 삼각함수 파라미터를 조절하여 그래프를 실시간으로 확인하고, 하단에서 y값에 해당하는 x값들을 찾아보세요.")
    
    with st.container():
        st.markdown("### ⚙️ 삼각함수 그래프 설정")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            func_type = st.selectbox("함수 선택", ["sin", "cos", "tan"], index=0)
            amplitude = st.number_input("진폭 (A)", value=1.0, step=0.5)
            
        with col2:
            default_period = np.pi if func_type == "tan" else 2 * np.pi
            period = st.number_input("주기 (T)", value=float(default_period), min_value=0.1, step=0.1)
            # B calculation: period = 2*pi / B => B = 2*pi / period
            B = (np.pi if func_type == "tan" else 2 * np.pi) / period
            
        with col3:
            phase_shift = st.number_input("수평 이동 (C, 라디안)", value=0.0, step=0.1)
            vertical_shift = st.number_input("수직 이동 (D)", value=0.0, step=0.5)
            
        with col4:
            x_min_mult = st.number_input("x축 시작 (×π)", value=-2.0, step=0.5)
            x_max_mult = st.number_input("x축 끝 (×π)", value=2.0, step=0.5)
            x_min = x_min_mult * np.pi
            x_max = x_max_mult * np.pi

    # Max / Min calculation info
    st.markdown("---")
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        if func_type == "tan":
            st.metric("최댓값 (Max)", "없음 (∞)")
        else:
            max_val = vertical_shift + abs(amplitude)
            st.metric("최댓값 (Max)", f"{max_val:.2f}")
    with col_info2:
        if func_type == "tan":
            st.metric("최솟값 (Min)", "없음 (-∞)")
        else:
            min_val = vertical_shift - abs(amplitude)
            st.metric("최솟값 (Min)", f"{min_val:.2f}")
    with col_info3:
        st.metric("현재 주기 (T)", f"{period:.4f} ({format_radian(period)})")

    # Formula string construction
    amp_str = f"{amplitude}" if amplitude != 1.0 else ("-" if amplitude == -1 else "")
    if amplitude == 1.0:
        amp_str = ""
    elif amplitude == -1.0:
        amp_str = "-"
        
    b_str = f"{B:.2f}" if abs(B - 1.0) > 1e-3 else ""
    c_sign = "-" if phase_shift >= 0 else "+"
    c_val = abs(phase_shift)
    c_str = f" - {format_radian(c_val)}" if phase_shift > 0 else (f" + {format_radian(c_val)}" if phase_shift < 0 else "")
    
    if phase_shift != 0:
        inner_expr = f"{b_str if b_str else '1'}(x{c_str})" if b_str else f"x{c_str}"
    else:
        inner_expr = f"{b_str}x" if b_str else "x"
        
    d_str = f" + {vertical_shift}" if vertical_shift > 0 else (f" - {abs(vertical_shift)}" if vertical_shift < 0 else "")
    
    func_eq = f"y = {amp_str}{func_type}({inner_expr}){d_str}"
    st.markdown(f"### 📝 현재 함수식: `{func_eq}`")

    # Plotting Graph with Plotly
    x_vals = np.linspace(x_min, x_max, 1000)
    if func_type == "sin":
        y_vals = amplitude * np.sin(B * (x_vals - phase_shift)) + vertical_shift
    elif func_type == "cos":
        y_vals = amplitude * np.cos(B * (x_vals - phase_shift)) + vertical_shift
    else:
        # For tan, handle asymptotes by setting to NaN
        arg = B * (x_vals - phase_shift)
        y_vals = amplitude * np.tan(arg) + vertical_shift
        # Mask near asymptotes: cos(arg) close to 0
        cos_vals = np.cos(arg)
        y_vals[np.abs(cos_vals) < 0.02] = np.nan

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=func_eq, line=dict(color='#0284c7', width=3)))
    
    # Axes and layout
    fig.update_layout(
        title=dict(text=f"Graph of {func_eq}", font=dict(size=18)),
        xaxis=dict(
            title="x (radians)",
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=1.5,
            range=[x_min, x_max]
        ),
        yaxis=dict(
            title="y",
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=1.5
        ),
        hovermode="x unified",
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------
    # Core Feature: Find x from y value
    # ------------------------------------------
    st.markdown("---")
    st.markdown("### 🔍 y값으로부터 모든 x값 찾기")
    st.markdown("지정한 범위 내에서 입력한 y값을 만족하는 모든 해(x)를 라디안과 소수로 찾아냅니다.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        target_y = st.number_input("목표 y값", value=0.0, step=0.5)
    with col_f2:
        search_min_mult = st.number_input("탐색 x 범위 시작 (×π)", value=-2.0, step=0.5)
        search_min = search_min_mult * np.pi
    with col_f3:
        search_max_mult = st.number_input("탐색 x 범위 끝 (×π)", value=2.0, step=0.5)
        search_max = search_max_mult * np.pi

    # Solve for x
    # y = A * trig(B(x - C)) + D  ==>  trig(B(x - C)) = (y - D) / A
    solutions = []
    if func_type in ["sin", "cos"]:
        val_to_check = (target_y - vertical_shift) / amplitude
        if -1.0 <= val_to_check <= 1.0:
            if func_type == "sin":
                base_angles = [np.arcsin(val_to_check), np.pi - np.arcsin(val_to_check)]
            else:
                base_angles = [np.arccos(val_to_check), -np.arccos(val_to_check)]
            
            # Period of B(x-C) is 2pi, so period in x is 2pi/B
            T_func = 2 * np.pi / B
            # Generate solutions across integers k
            for k in range(-10, 11):
                for ba in base_angles:
                    x_sol = ba / B + phase_shift + k * T_func
                    if search_min <= x_sol <= search_max:
                        # Check uniqueness
                        if not any(abs(x_sol - s) < 1e-4 for s in solutions):
                            solutions.append(x_sol)
        solutions.sort()
    elif func_type == "tan":
        if amplitude == 0:
            if vertical_shift == target_y:
                st.info("진폭이 0인 상수함수입니다.")
        else:
            val_to_check = (target_y - vertical_shift) / amplitude
            base_angle = np.arctan(val_to_check)
            T_func = np.pi / B
            for k in range(-20, 21):
                x_sol = base_angle / B + phase_shift + k * T_func
                if search_min <= x_sol <= search_max:
                    if not any(abs(x_sol - s) < 1e-4 for s in solutions):
                        solutions.append(x_sol)
        solutions.sort()

    if len(solutions) > 0:
        st.success(f"총 {len(solutions)}개의 해를 찾았습니다!")
        sol_cols = st.columns(min(len(solutions), 4))
        for idx, sol in enumerate(solutions):
            with sol_cols[idx % len(sol_cols)]:
                st.markdown(f"""
                <div class='metric-card'>
                    <b>해 {idx+1}</b><br>
                    라디안: <b>{format_radian(sol)}</b><br>
                    소수: <code>{sol:.4f}</code>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("입력한 범위에서는 해당 y값을 만족하는 x값이 없거나, 함수의 치역을 벗어납니다.")

# ==========================================
# 2. 원에 의한 삼각함수 보기
# ==========================================
elif menu == "2. 원에 의한 삼각함수 보기":
    st.header("⚪ 2. 단위원과 삼각함수 그래프 연동")
    st.markdown("왼쪽 단위원의 각도 $\\theta$를 조절하면, 오른쪽 삼각함수 그래프에 실시간으로 값이 연동되어 표시됩니다.")

    col_ctrl1, col_ctrl2 = st.columns([1, 2])
    with col_ctrl1:
        theta_deg = st.slider("각도 θ 선택 (도 단위 슬라이더로 조작 후 라디안 변환)", 0, 360, 45, 5)
        theta = np.radians(theta_deg)
        st.markdown(f"**현재 각도 θ**: `{format_radian(theta)}` ({theta:.4f} rad)")
        
        show_sin = st.checkbox("sin(θ) 표시", value=True)
        show_cos = st.checkbox("cos(θ) 표시", value=True)
        show_tan = st.checkbox("tan(θ) 표시", value=True)

    with col_ctrl2:
        # Display exact values
        val_sin = np.sin(theta)
        val_cos = np.cos(theta)
        
        # Format exact trigonometric values
        sin_exact_map = {0: "0", np.pi/6: "1/2", np.pi/4: "√2/2", np.pi/3: "√3/2", np.pi/2: "1", 
                           2*np.pi/3: "√3/2", 3*np.pi/4: "√2/2", 5*np.pi/6: "1/2", np.pi: "0",
                           3*np.pi/2: "-1", 2*np.pi: "0"}
        cos_exact_map = {0: "1", np.pi/6: "√3/2", np.pi/4: "√2/2", np.pi/3: "1/2", np.pi/2: "0",
                           2*np.pi/3: "-1/2", 3*np.pi/4: "-√2/2", 5*np.pi/6: "-√3/2", np.pi: "-1",
                           3*np.pi/2: "0", 2*np.pi: "1"}
        
        # Check closest in map
        s_str = f"{val_sin:.4f}"
        c_str = f"{val_cos:.4f}"
        for k, v in sin_exact_map.items():
            if abs(theta - k) < 1e-2:
                s_str = f"{v} (≈ {val_sin:.4f})"
                break
        for k, v in cos_exact_map.items():
            if abs(theta - k) < 1e-2:
                c_str = f"{v} (≈ {val_cos:.4f})"
                break

        tan_str = "정의되지 않음" if abs(val_cos) < 1e-3 else f"{np.tan(theta):.4f}"
        if abs(val_cos) >= 1e-3:
            t_val = np.tan(theta)
            if abs(t_val - 1) < 1e-2: tan_str = "1 (산술값)"
            elif abs(t_val - 1/np.sqrt(3)) < 1e-2: tan_str = "√3/3"
            elif abs(t_val - np.sqrt(3)) < 1e-2: tan_str = "√3"
            elif abs(t_val) < 1e-2: tan_str = "0"

        st.markdown(f"""
        <div class='highlight-box'>
            <b>📊 실시간 삼각함수 값 계산 결과 ($\\theta$ = {format_radian(theta)})</b><br>
            • <b>sin θ</b> = {s_str}<br>
            • <b>cos θ</b> = {c_str}<br>
            • <b>tan θ</b> = {tan_str}
        </div>
        """, unsafe_allow_html=True)

    # Two column plots: Unit Circle & Trig Graphs
    col_u1, col_u2 = st.columns(2)
    
    with col_u1:
        # Unit Circle Plot
        fig_uc = go.Figure()
        # Circle
        circle_t = np.linspace(0, 2*np.pi, 200)
        fig_uc.add_trace(go.Scatter(x=np.cos(circle_t), y=np.sin(circle_t), mode='lines', line=dict(color='gray', dash='dash'), name='Unit Circle'))
        # Point P
        px, py = np.cos(theta), np.sin(theta)
        fig_uc.add_trace(go.Scatter(x=[0, px], y=[0, py], mode='lines+markers', line=dict(color='#0284c7', width=3), marker=dict(size=10), name='P(cos θ, sin θ)'))
        # Projections
        if show_cos:
            fig_uc.add_trace(go.Scatter(x=[0, px], y=[0, 0], mode='lines', line=dict(color='red', width=2, dash='dot'), name='cos θ'))
        if show_sin:
            fig_uc.add_trace(go.Scatter(x=[px, px], y=[0, py], mode='lines', line=dict(color='green', width=2, dash='dot'), name='sin θ'))
            
        fig_uc.update_layout(
            title="단위원 (Unit Circle)",
            xaxis=dict(range=[-1.5, 1.5], zeroline=True, zerolinecolor='black'),
            yaxis=dict(range=[-1.5, 1.5], zeroline=True, zerolinecolor='black', scaleanchor="x", scaleratio=1),
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_uc, use_container_width=True)

    with col_u2:
        # Trig Functions Combined Plot
        fig_tg = go.Figure()
        x_t = np.linspace(0, 2*np.pi, 400)
        if show_sin:
            fig_tg.add_trace(go.Scatter(x=x_t, y=np.sin(x_t), mode='lines', name='sin(x)', line=dict(color='green', width=2)))
            fig_tg.add_trace(go.Scatter(x=[theta], y=[np.sin(theta)], mode='markers', marker=dict(size=12, color='green'), name='sin(θ) point'))
        if show_cos:
            fig_tg.add_trace(go.Scatter(x=x_t, y=np.cos(x_t), mode='lines', name='cos(x)', line=dict(color='red', width=2)))
            fig_tg.add_trace(go.Scatter(x=[theta], y=[np.cos(theta)], mode='markers', marker=dict(size=12, color='red'), name='cos(θ) point'))
        if show_tan:
            y_tan = np.tan(x_t)
            y_tan[np.abs(np.cos(x_t)) < 0.05] = np.nan
            fig_tg.add_trace(go.Scatter(x=x_t, y=y_tan, mode='lines', name='tan(x)', line=dict(color='purple', width=2)))
            if abs(np.cos(theta)) > 0.05:
                fig_tg.add_trace(go.Scatter(x=[theta], y=[np.tan(theta)], mode='markers', marker=dict(size=12, color='purple'), name='tan(θ) point'))

        # Vertical line at current theta
        fig_tg.add_shape(type="line", x0=theta, y0=-2, x1=theta, y2=2, line=dict(color="black", dash="dash", width=1))

        fig_tg.update_layout(
            title="삼각함수 그래프 및 현재 θ 위치",
            xaxis=dict(range=[0, 2*np.pi], zeroline=True, zerolinecolor='black'),
            yaxis=dict(range=[-2.5, 2.5], zeroline=True, zerolinecolor='black'),
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_tg, use_container_width=True)

# ==========================================
# 3. 삼각함수 각변환 퀴즈
# ==========================================
elif menu == "3. 삼각함수 각변환 퀴즈":
    st.header("📝 3. 삼각함수 각변환 퀴즈 (총 10문제)")
    st.markdown("고등학교 수학 교육과정에 기반한 삼각함수 각변환 문제 10문제를 풀어보세요. 오답 시 한 번 더 기회가 주어집니다.")

    # Define 10 distinct quiz questions
    quiz_bank = [
        {
            "id": 1, "q": "sin(π - θ)", "ans": "sin(θ)", "options": ["sin(θ)", "-sin(θ)", "cos(θ)", "-cos(θ)"],
            "formula": "sin(π - θ) = sin(θ) (2사분면에서 sin은 양수)",
            "explanation": "π - θ는 제2사분면의 각이며, 제2사분면에서 sin 값은 양수입니다. 따라서 부호는 그대로 양수가 되고 함수 이름은 변하지 않아 sin(θ)가 됩니다."
        },
        {
            "id": 2, "q": "cos(π + θ)", "ans": "-cos(θ)", "options": ["cos(θ)", "-cos(θ)", "sin(θ)", "-sin(θ)"],
            "formula": "cos(π + θ) = -cos(θ) (3사분면에서 cos은 음수)",
            "explanation": "π + θ는 제3사분면의 각이며, 제3사분면에서 cos 값은 음수입니다. 따라서 -cos(θ)가 됩니다."
        },
        {
            "id": 3, "q": "tan(π - θ)", "ans": "-tan(θ)", "options": ["tan(θ)", "-tan(θ)", "1/tan(θ)", "-1/tan(θ)"],
            "formula": "tan(π - θ) = -tan(θ) (2사분면에서 tan은 음수)",
            "explanation": "π - θ는 제2사분면의 각이며, 제2사분면에서 tan 값은 음수입니다. 따라서 -tan(θ)가 됩니다."
        },
        {
            "id": 4, "q": "sin(π + θ)", "ans": "-sin(θ)", "options": ["sin(θ)", "-sin(θ)", "cos(θ)", "-cos(θ)"],
            "formula": "sin(π + θ) = -sin(θ) (3사분면에서 sin은 음수)",
            "explanation": "π + θ는 제3사분면의 각이며, 제3사분면에서 sin 값은 음수이므로 -sin(θ)가 됩니다."
        },
        {
            "id": 5, "q": "cos(2π - θ)", "ans": "cos(θ)", "options": ["cos(θ)", "-cos(θ)", "sin(θ)", "-sin(θ)"],
            "formula": "cos(2π - θ) = cos(θ) (4사분면에서 cos은 양수)",
            "explanation": "2π - θ는 제4사분면의 각이며, 제4사분면에서 cos 값은 양수입니다. 따라서 cos(θ)가 됩니다."
        },
        {
            "id": 6, "q": "tan(π + θ)", "ans": "tan(θ)", "options": ["tan(θ)", "-tan(θ)", "-1/tan(θ)", "cot(θ)"],
            "formula": "tan(π + θ) = tan(θ) (3사분면에서 tan은 양수)",
            "explanation": "tan의 주기는 π이므로 tan(π + θ) = tan(θ)가 성립합니다. 또한 제3사분면에서 tan은 양수입니다."
        },
        {
            "id": 7, "q": "sin(π/2 - θ)", "ans": "cos(θ)", "options": ["sin(θ)", "-sin(θ)", "cos(θ)", "-cos(θ)"],
            "formula": "sin(π/2 - θ) = cos(θ) (여각 공식)",
            "explanation": "π/2 ± θ 형태에서는 sin이 cos으로 바뀝니다. 제1사분면이므로 양수입니다."
        },
        {
            "id": 8, "q": "cos(π/2 - θ)", "ans": "sin(θ)", "options": ["cos(θ)", "-cos(θ)", "sin(θ)", "-sin(θ)"],
            "formula": "cos(π/2 - θ) = sin(θ) (여각 공식)",
            "explanation": "π/2 - θ에서 cos은 sin으로 바뀌며, 제1사분면이므로 양수 sin(θ)가 됩니다."
        },
        {
            "id": 9, "q": "sin(π/2 + θ)", "ans": "cos(θ)", "options": ["sin(θ)", "-sin(θ)", "cos(θ)", "-cos(θ)"],
            "formula": "sin(π/2 + θ) = cos(θ) (2사분면에서 sin은 양수)",
            "explanation": "π/2 + θ는 제2사분면이며, 원래 함수인 sin이 양수이므로 +cos(θ)가 됩니다."
        },
        {
            "id": 10, "q": "cos(π/2 + θ)", "ans": "-sin(θ)", "options": ["sin(θ)", "-sin(θ)", "cos(θ)", "-cos(θ)"],
            "formula": "cos(π/2 + θ) = -sin(θ) (2사분면에서 cos은 음수)",
            "explanation": "π/2 + θ는 제2사분면이며, 제2사분면에서 cos은 음수이므로 -sin(θ)가 됩니다."
        }
    ]

    # Initialize session state for quiz if not exists
    if "quiz_states" not in st.session_state:
        st.session_state.quiz_states = {q["id"]: {"attempts": 0, "solved": False, "failed": False, "user_ans": None} for q in quiz_bank}

    score_correct_first = 0
    score_correct_second = 0
    total_solved = 0

    for idx, q in enumerate(quiz_bank):
        q_id = q["id"]
        q_state = st.session_state.quiz_states[q_id]
        
        st.markdown(f"---")
        st.markdown(f"#### 문제 {idx+1}. 다음 식을 간단히 하시오: **{q['q']}**")
        
        # Radio for options
        selected = st.radio(f"보기 선택 (문제 {idx+1})", q["options"], key=f"q_radio_{q_id}", index=None if q_state["user_ans"] is None else q["options"].index(q_state["user_ans"]) if q_state["user_ans"] in q["options"] else 0)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            submit_btn = st.button(f"정답 제출 (문제 {idx+1})", key=f"submit_{q_id}")
            
        if submit_btn and selected is not None:
            q_state["user_ans"] = selected
            if selected == q["ans"]:
                q_state["solved"] = True
                if q_state["attempts"] == 0:
                    st.success("🎉 정답입니다!")
                else:
                    st.success("👍 두 번째 시도만에 맞혔습니다!")
            else:
                q_state["attempts"] += 1
                if q_state["attempts"] == 1:
                    st.warning("❌ 틀렸습니다. 한 번 더 기회가 있습니다! 다시 생각해 보세요.")
                else:
                    q_state["failed"] = True
                    st.error(f"❌ 틀렸습니다. 정답은 **{q['ans']}** 입니다.")

        # Show status and explanation if solved or failed
        if q_state["solved"] or q_state["failed"]:
            if q_state["solved"]:
                if q_state["attempts"] == 0:
                    st.info("✅ **[정답 처리]** 첫 시도 정답")
                else:
                    st.info("✅ **[정답 처리]** 재시도 정답")
            else:
                st.info("❌ **[오답 처리]** 기회 소진")
                
            st.markdown(f"""
            <div class='highlight-box'>
                <b>📖 개념 해설 및 풀이</b><br>
                • <b>정답</b>: {q['ans']}<br>
                • <b>사용 공식</b>: {q['formula']}<br>
                • <b>풀이 과정</b>: {q['explanation']}
            </div>
            """, unsafe_allow_html=True)

        # Tally stats
        if q_state["solved"]:
            total_solved += 1
            if q_state["attempts"] == 0:
                score_correct_first += 1
            else:
                score_correct_second += 1

    st.markdown("---")
    st.markdown("### 📊 퀴즈 결과 요약")
    if st.button("🔄 퀴즈 초기화 및 다시 풀기"):
        st.session_state.quiz_states = {q["id"]: {"attempts": 0, "solved": False, "failed": False, "user_ans": None} for q in quiz_bank}
        st.rerun()

    accuracy = (total_solved / len(quiz_bank)) * 100
    st.metric("현재 맞힌 문제 수 / 전체", f"{total_solved} / {len(quiz_bank)}")
    st.metric("전체 정답률", f"{accuracy:.1f}%")

# ==========================================
# 4. 주요 각의 삼각함수 값 표
# ==========================================
elif menu == "4. 주요 각의 삼각함수 값 표":
    st.header("📋 4. 주요 각의 삼각함수 값 표")
    st.markdown("고등학교 수학에서 가장 자주 다루는 주요 특수각들에 대한 삼각함수 값 표입니다. 교육적 목적에 따라 **도(degree)**와 **라디안(radian)**을 함께 비교하여 제공합니다.")

    data = [
        {"도": "0°", "라디안": "0", "sin": "0", "cos": "1", "tan": "0"},
        {"도": "30°", "라디안": "π/6", "sin": "1/2", "cos": "√3/2", "tan": "√3/3"},
        {"도": "45°", "라디안": "π/4", "sin": "√2/2", "cos": "√2/2", "tan": "1"},
        {"도": "60°", "라디안": "π/3", "sin": "√3/2", "cos": "1/2", "tan": "√3"},
        {"도": "90°", "라디안": "π/2", "sin": "1", "cos": "0", "tan": "정의되지 않음 (∞)"}
    ]

    df_trig = pd.DataFrame(data)
    
    # Styled dataframe
    st.table(df_trig)
    
    st.markdown("---")
    st.markdown("### 💡 학습 포인트 및 핵심 요약")
    st.markdown("""
    - **라디안 체계의 중요성**: 고등학교 및 대학교 수학에서는 각도의 단위로 도(degree) 대신 실수인 **라디안(radian)**을 표준으로 사용합니다.
    - **삼각비의 대칭성과 주기성**: 특수각의 값을 완벽히 암기하고 있으면 그래프의 평행이동이나 대칭성을 이해하는 데 큰 도움이 됩니다.
    - **탄젠트의 점근선**: $x = \\frac{\\pi}{2} + k\\pi$ (단, $k$는 정수)에서 $\\cos x = 0$이 되므로 탄젠트 값은 정의되지 않습니다.
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>© 2026 삼각함수 탐구 학습 웹앱 | 고등학교 수학과제탐구 수행평가 전용</p>", unsafe_allow_html=True)
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

req_content = '''streamlit>=1.32.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.18.0
'''

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(req_content)

print("Files generated successfully.")
