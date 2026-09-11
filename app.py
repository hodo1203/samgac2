import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="30년차 수학 전문가의 인터랙티브 삼각함수 앱",
    page_icon="📐",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📐 인터랙티브 삼각함수 마스터 클래스</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">30년 경력의 수학 전문가가 설계한 단위 원과 삼각함수의 시각적 연결 및 특수각 트레이닝 센터</p>', unsafe_allow_html=True)

# Sidebar Navigation
tab_selection = st.sidebar.radio(
    "학습 메뉴 선택",
    ["1. 단위 원과 삼각함수 연동 시각화", "2. 특수각 학습 표", "3. 삼각함수 특수각 & 라디안 퀴즈 게임"]
)

if tab_selection == "1. 단위 원과 삼각함수 연동 시각화":
    st.markdown("### 🔍 단위 원(Unit Circle)과 삼각함수 그래프의 실시간 연동")
    st.markdown("오른쪽 슬라이더를 움직이거나 각도를 조절하여 각도 $\\theta$에 따른 **단위 원 위의 점 $( \\cos\\theta, \\sin\\theta )$**과 **삼각함수 그래프**가 어떻게 동시에 그려지는지 확인해보세요.")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("#### 🔵 좌측: 단위 원과 삼각비")
        angle_deg = st.slider("각도 선택 ($\theta$ 회전)", 0, 360, 45, 1, key="angle_slider")
        angle_rad = np.radians(angle_deg)
        
        # Unit circle plot using Plotly
        fig_circle = go.Figure()
        
        # Circle
        theta_full = np.linspace(0, 2*np.pi, 200)
        fig_circle.add_trace(go.Scatter(x=np.cos(theta_full), y=np.sin(theta_full), mode='lines', line=dict(color='#94A3B8', width=2), name='단위 원'))
        
        # Axes
        fig_circle.add_shape(type="line", x0=-1.3, y0=0, x1=1.3, y1=0, line=dict(color="gray", dash="dash"))
        fig_circle.add_shape(type="line", x0=0, y0=-1.3, x1=0, y1=1.3, line=dict(color="gray", dash="dash"))
        
        # Point on circle
        cos_val = np.cos(angle_rad)
        sin_val = np.sin(angle_rad)
        
        fig_circle.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines+markers', line=dict(color='#2563EB', width=4), marker=dict(size=10), name='동경'))
        fig_circle.add_trace(go.Scatter(x=[cos_val], y=[sin_val], mode='markers', marker=dict(size=14, color='#EF4444'), name=f'P({cos_val:.2f}, {sin_val:.2f})'))
        
        # Projection lines
        fig_circle.add_shape(type="line", x0=cos_val, y0=0, x1=cos_val, y1=sin_val, line=dict(color="#EF4444", dash="dot"))
        fig_circle.add_shape(type="line", x0=0, y0=sin_val, x1=cos_val, y1=sin_val, line=dict(color="#3B82F6", dash="dot"))
        
        fig_circle.update_layout(
            xaxis=dict(range=[-1.5, 1.5], zeroline=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.5, 1.5], zeroline=False),
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_circle, use_container_width=True)
        st.info(f"현재 각도: **{angle_deg}°** ( 라디안: **{angle_rad:.2f} rad** )  \n좌표 P = ( $\\cos {angle_deg}^\\circ$, $\\sin {angle_deg}^\\circ$ ) = ( **{cos_val:.3f}**, **{sin_val:.3f}** )")

    with col2:
        st.markdown("#### 📈 우측: 삼각함수 그래프 ($y = \\sin x, \\ y = \\cos x$)")
        
        # Sine and Cosine waves
        x_vals = np.linspace(0, 2*np.pi, 300)
        sin_vals = np.sin(x_vals)
        cos_vals = np.cos(x_vals)
        
        fig_trig = go.Figure()
        fig_trig.add_trace(go.Scatter(x=x_vals, y=sin_vals, mode='lines', line=dict(color='#EF4444', width=3), name='y = sin(x)'))
        fig_trig.add_trace(go.Scatter(x=x_vals, y=cos_vals, mode='lines', line=dict(color='#3B82F6', width=3, dash='dash'), name='y = cos(x)'))
        
        # Current active point on graph
        fig_trig.add_trace(go.Scatter(x=[angle_rad], y=[sin_val], mode='markers', marker=dict(size=14, color='#EF4444'), name='sin(θ) 위치'))
        fig_trig.add_trace(go.Scatter(x=[angle_rad], y=[cos_val], mode='markers', marker=dict(size=14, color='#3B82F6'), name='cos(θ) 위치'))
        
        fig_trig.update_layout(
            xaxis=dict(
                range=[0, 2*np.pi], 
                tickvals=[0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
                ticktext=['0', 'π/2', 'π', '3π/2', '2π'],
                zeroline=True
            ),
            yaxis=dict(range=[-1.5, 1.5], zeroline=True),
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=True
        )
        st.plotly_chart(fig_trig, use_container_width=True)
        st.success("원 위의 점 회전에 따라 삼각함수 파동 위의 해당 점이 실시간으로 이동하는 모습을 관찰할 수 있습니다.")

elif tab_selection == "2. 특수각 학습 표":
    st.markdown("### 📚 삼각함수 특수각 학습 가이드 & 공식 표")
    st.markdown("수학에서 가장 빈번하게 등장하는 **30°, 45°, 60°, 90°** (호도법: $\\frac{\\pi}{6}, \\frac{\\pi}{4}, \\frac{\\pi}{3}, \\frac{\\pi}{2}$)의 특수각 값을 완벽하게 정리한 표입니다. 다음 퀴즈 게임을 위해 꼼꼼히 학습해 보세요!")
    
    data = {
        "각도 (도)": ["0°", "30°", "45°", "60°", "90°", "180°", "270°", "360°"],
        "라디안 (호도법)": ["0", "π / 6", "π / 4", "π / 3", "π / 2", "π", "3π / 2", "2π"],
        "사인 (sin)": ["0", "1/2", "√2 / 2", "√3 / 2", "1", "0", "-1", "0"],
        "코사인 (cos)": ["1", "√3 / 2", "√2 / 2", "1/2", "0", "-1", "0", "1"],
        "탄젠트 (tan)": ["0", "√3 / 3", "1", "√3", "정의되지 않음 (∞)", "0", "정의되지 않음", "0"]
    }
    
    df = pd.DataFrame(data)
    st.table(df)
    
    st.markdown("---")
    st.markdown("#### 💡 30년차 베테랑의 암기 꿀팁")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.info("**사인(sin)의 분자 규칙성**\n* 0°, 30°, 45°, 60°, 90° 순서로\n* $\\frac{\\sqrt{0}}{2}, \\frac{\\sqrt{1}}{2}, \\frac{\\sqrt{2}}{2}, \\frac{\\sqrt{3}}{2}, \\frac{\\sqrt{4}}{2}$ 로 외우면 아주 쉽습니다!")
    with col_t2:
        st.info("**코사인(cos)의 규칙성**\n* sin 값의 순서를 정확히 **거꾸로** 적은 것과 같습니다.\n* 탄젠트(tan)는 $\\frac{\\sin}{\\cos}$ 임을 기억하세요!")

elif tab_selection == "3. 삼각함수 특수각 & 라디안 퀴즈 게임":
    st.markdown("### 🎮 삼각함수 특수각 & 라디안 마스터 챌린지")
    st.markdown("앞서 학습한 특수각과 라디안 변환, 그리고 삼각함수 값을 직접 테스트해보는 퀴즈 게임입니다!")
    
    # Initialize quiz state
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    questions = [
        {
            "q": "1. 30°를 라디안(호도법)으로 올바르게 변환한 것은?",
            "options": ["π / 6", "π / 4", "π / 3", "π / 2"],
            "answer": "π / 6"
        },
        {
            "q": "2. 45°의 코사인 값(cos 45°)은 얼마인가?",
            "options": ["1/2", "√2 / 2", "√3 / 2", "1"],
            "answer": "√2 / 2"
        },
        {
            "q": "3. 60°를 라디안(호도법)으로 올바르게 변환한 것은?",
            "options": ["π / 6", "π / 4", "π / 3", "π / 2"],
            "answer": "π / 3"
        },
        {
            "q": "4. tan 60°의 값은 얼마인가?",
            "options": ["√3 / 3", "1", "√3", "정의되지 않음"],
            "answer": "√3"
        },
        {
            "q": "5. 90°를 라디안(호도법)으로 올바르게 변환한 것은?",
            "options": ["π / 3", "π / 2", "π", "3π / 2"],
            "answer": "π / 2"
        }
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
                    st.success("🎉 정답입니다! 아주 훌륭해요!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 틀렸습니다. 정답은 **{curr_q['answer']}** 입니다.")
                
                st.session_state.q_index += 1
                st.rerun()
        else:
            st.markdown("---")
            st.markdown("### 🏆 퀴즈 종료! 수고하셨습니다.")
            final_score = st.session_state.score
            total_q = len(questions)
            st.metric("최종 점수", f"{final_score} / {total_q} 점")
            
            if final_score == total_q:
                st.balloons()
                st.success("완벽합니다! 30년차 수학 전문가로서 인정하는 삼각함수 마스터입니다!")
            elif final_score >= 3:
                st.info("좋은 성적입니다! 특수각 표를 다시 복습하면 만점이 가능해요.")
            else:
                st.warning("조금 더 연습이 필요해요! '특수각 학습 표' 탭을 다시 확인해보세요.")
                
            if st.button("🔄 퀴즈 다시 풀기"):
                st.session_state.quiz_started = False
                st.session_state.score = 0
                st.session_state.q_index = 0
                st.rerun()
