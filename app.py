import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fractions import Fraction

st.set_page_config(
    page_title="인터랙티브 삼각함수 마스터 클래스",
    page_icon="📐",
    layout="wide"
)

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📐 인터랙티브 삼각함수 마스터 클래스</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">단위 원 직접 클릭 및 라디안 분수 표현을 통한 실시간 연동 학습</p>', unsafe_allow_html=True)

tab_selection = st.sidebar.radio(
    "학습 메뉴 선택",
    ["1. 단위 원과 삼각함수 연동 시각화", "2. 특수각 학습 표", "3. 삼각함수 특수각 & 라디안 퀴즈 게임"]
)

def format_radian_fraction(rad):
    rad = rad % (2 * np.pi)
    standard_angles = [
        (0.0, "0"),
        (np.pi/6, "π/6"),
        (np.pi/4, "π/4"),
        (np.pi/3, "π/3"),
        (np.pi/2, "π/2"),
        (2*np.pi/3, "2π/3"),
        (3*np.pi/4, "3π/4"),
        (5*np.pi/6, "5π/6"),
        (np.pi, "π"),
        (7*np.pi/6, "7π/6"),
        (5*np.pi/4, "5π/4"),
        (4*np.pi/3, "4π/3"),
        (3*np.pi/2, "3π/2"),
        (5*np.pi/3, "5π/3"),
        (7*np.pi/4, "7π/4"),
        (11*np.pi/6, "11π/6"),
        (2*np.pi, "2π")
    ]
    for val, name in standard_angles:
        if abs(rad - val) < 0.04:
            return name
    f = Fraction(rad / np.pi).limit_denominator(12)
    if f.numerator == 0:
        return "0"
    elif f.numerator == 1:
        return "π" if f.denominator == 1 else f"π/{f.denominator}"
    else:
        return f"{f.numerator}π" if f.denominator == 1 else f"{f.numerator}π/{f.denominator}"

if tab_selection == "1. 단위 원과 삼각함수 연동 시각화":
    st.markdown("### 🔍 단위 원 직접 클릭 및 실시간 연동 시각화")
    st.markdown("좌측 **단위 원 그래프 안의 원하는 지점을 클릭**하거나 하단 슬라이더를 움직여 보세요. 원 위의 점과 삼각함수 그래프가 실시간으로 연동됩니다.")
    
    col_opt1, col_opt2, _ = st.columns([1, 1, 3])
    with col_opt1:
        show_sin = st.checkbox("y = sin(x) 그래프 표시", value=True)
    with col_opt2:
        show_cos = st.checkbox("y = cos(x) 그래프 표시", value=True)
    
    if "radian_val" not in st.session_state:
        st.session_state["radian_val"] = float(np.pi / 4)

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("#### 🔵 좌측: 단위 원과 동경 ($x^2 + y^2 = 1$)")
        
        angle_rad = st.slider(
            "라디안 선택 (θ rad)", 
            min_value=0.0, 
            max_value=float(2 * np.pi), 
            value=st.session_state["radian_val"], 
            step=0.01, 
            format="%.2f rad",
            key="slider_input"
        )
        
        if angle_rad != st.session_state["radian_val"]:
            st.session_state["radian_val"] = angle_rad

        angle_deg = np.degrees(st.session_state["radian_val"])
        rad_str = format_radian_fraction(st.session_state["radian_val"])
        
        fig_circle = go.Figure()
        
        theta_full = np.linspace(0, 2*np.pi, 200)
        fig_circle.add_trace(go.Scatter(x=np.cos(theta_full), y=np.sin(theta_full), mode='lines', line=dict(color='#94A3B8', width=2), name='단위 원'))
        
        fig_circle.add_shape(type="line", x0=-1.3, y0=0, x1=1.3, y1=0, line=dict(color="gray", dash="dash"))
        fig_circle.add_shape(type="line", x0=0, y0=-1.3, x1=0, y1=1.3, line=dict(color="gray", dash="dash"))
        
        cos_val = np.cos(st.session_state["radian_val"])
        sin_val = np.sin(st.session_state["radian_val"])
        
        fig_circle.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines+markers', line=dict(color='#2563EB', width=4), marker=dict(size=10), name='동경'))
        fig_circle.add_trace(go.Scatter(x=[cos_val], y=[sin_val], mode='markers', marker=dict(size=14, color='#EF4444'), name=f'P({cos_val:.2f}, {sin_val:.2f})'))
        
        fig_circle.add_shape(type="line", x0=cos_val, y0=0, x1=cos_val, y1=sin_val, line=dict(color="#EF4444", dash="dot"))
        fig_circle.add_shape(type="line", x0=0, y0=sin_val, x1=cos_val, y1=sin_val, line=dict(color="#3B82F6", dash="dot"))
        
        fig_circle.update_layout(
            xaxis=dict(range=[-1.5, 1.5], zeroline=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.5, 1.5], zeroline=False),
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=False
        )
        
        # Streamlit 내장 on_select를 활용한 원 클릭 조작
        event = st.plotly_chart(fig_circle, on_select="rerun", key="circle_plot", use_container_width=True)
        
        if event and "selection" in event and "points" in event["selection"]:
            points = event["selection"]["points"]
            if points:
                pt = points[0]
                x_c = pt.get("x")
                y_c = pt.get("y")
                if x_c is not None and y_c is not None:
                    new_rad = np.arctan2(y_c, x_c)
                    if new_rad < 0:
                        new_rad += 2 * np.pi
                    if abs(new_rad - st.session_state["radian_val"]) > 0.005:
                        st.session_state["radian_val"] = float(new_rad)
                        st.rerun()

        st.info(f"현재 각도: **{angle_deg:.1f}°** ( 호도법: **{rad_str}** / **{st.session_state['radian_val']:.3f} rad** )  \n점 P 좌표 = ( $\\cos\\theta$, $\\sin\\theta$ ) = ( **{cos_val:.3f}**, **{sin_val:.3f}** )")

    with col2:
        st.markdown("#### 📈 우측: 삼각함수 그래프")
        
        x_vals = np.linspace(0, 2*np.pi, 300)
        fig_trig = go.Figure()
        
        if show_sin:
            fig_trig.add_trace(go.Scatter(x=x_vals, y=np.sin(x_vals), mode='lines', line=dict(color='#EF4444', width=3), name='y = sin(x)'))
            fig_trig.add_trace(go.Scatter(x=[st.session_state["radian_val"]], y=[sin_val], mode='markers', marker=dict(size=14, color='#EF4444'), name='sin(θ)'))
            
        if show_cos:
            fig_trig.add_trace(go.Scatter(x=x_vals, y=np.cos(x_vals), mode='lines', line=dict(color='#3B82F6', width=3, dash='dash'), name='y = cos(x)'))
            fig_trig.add_trace(go.Scatter(x=[st.session_state["radian_val"]], y=[cos_val], mode='markers', marker=dict(size=14, color='#3B82F6'), name='cos(θ)'))
        
        fig_trig.update_layout(
            xaxis=dict(
                range=[0, 2*np.pi], 
                tickvals=[0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
                ticktext=['0', 'π/2', 'π', '3π/2', '2π'],
                zeroline=True
            ),
            yaxis=dict(range=[-1.5, 1.5], zeroline=True),
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=True
        )
        st.plotly_chart(fig_trig, use_container_width=True)
        st.success("원 그래프를 클릭하거나 슬라이더를 움직여 실시간으로 연동되는 파동을 확인해 보세요.")

elif tab_selection == "2. 특수각 학습 표":
    st.markdown("### 📚 삼각함수 특수각 학습 가이드 & 공식 표")
    st.markdown("수학에서 가장 빈번하게 등장하는 특수각의 도(Degree)와 분수식 라디안(Radian) 대응표입니다.")
    
    data = {
        "각도 (도)": ["0°", "30°", "45°", "60°", "90°", "180°", "270°", "360°"],
        "라디안 (호도법)": ["0", "π/6", "π/4", "π/3", "π/2", "π", "3π/2", "2π"],
        "사인 (sin)": ["0", "1/2", "√2 / 2", "√3 / 2", "1", "0", "-1", "0"],
        "코사인 (cos)": ["1", "√3 / 2", "√2 / 2", "1/2", "0", "-1", "0", "1"],
        "탄젠트 (tan)": ["0", "√3 / 3", "1", "√3", "정의되지 않음 (∞)", "0", "정의되지 않음", "0"]
    }
    st.table(pd.DataFrame(data))

elif tab_selection == "3. 삼각함수 특수각 & 라디안 퀴즈 게임":
    st.markdown("### 🎮 삼각함수 특수각 & 라디안 마스터 챌린지")
    
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    questions = [
        {"q": "1. 30°를 라디안(호도법)으로 올바르게 변환한 것은?", "options": ["π/6", "π/4", "π/3", "π/2"], "answer": "π/6"},
        {"q": "2. 45°의 코사인 값(cos 45°)은 얼마인가?", "options": ["1/2", "√2 / 2", "√3 / 2", "1"], "answer": "√2 / 2"},
        {"q": "3. 60°를 라디안(호도법)으로 올바르게 변환한 것은?", "options": ["π/6", "π/4", "π/3", "π/2"], "answer": "π/3"},
        {"q": "4. tan 60°의 값은 얼마인가?", "options": ["√3 / 3", "1", "√3", "정의되지 않음"], "answer": "√3"},
        {"q": "5. 90°를 라디안(호도법)으로 올바르게 변환한 것은?", "options": ["π/3", "π/2", "π", "3π/2"], "answer": "π/2"}
    ]

    if not st.session_state.quiz_started:
        if st.button("🚀 퀴즈 시작하기", type="primary"):
            st.session_state.quiz_started = True
            st.session_state.score = 0
            st.session_state.q_index = 0
            st.rerun()
    else:
        q_idx = st.session_state.q_index
        if q_idx < len(questions):
            curr_q = questions[q_idx]
            st.markdown(f"#### [문제 {q_idx + 1} / {len(questions)}] {curr_q['q']}")
            user_choice = st.radio("보기 중 정답을 선택하세요:", curr_q['options'], key=f"q_{q_idx}")
            
            if st.button("정답 제출", key=f"submit_{q_idx}"):
                if user_choice == curr_q['answer']:
                    st.success("🎉 정답입니다!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 틀렸습니다. 정답은 **{curr_q['answer']}** 입니다.")
                st.session_state.q_index += 1
                st.rerun()
        else:
            st.markdown("---")
            st.markdown(f"### 🏆 퀴즈 종료! 최종 점수: {st.session_state.score} / {len(questions)} 점")
            if st.button("🔄 퀴즈 다시 풀기"):
                st.session_state.quiz_started = False
                st.session_state.score = 0
                st.session_state.q_index = 0
                st.rerun()
