import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Water Intake Tracker",
    page_icon="💧",
    layout="wide"
)

# File to store water intake data
DATA_FILE = "water_intake_data.json"

# Initialize session state
if 'water_data' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            st.session_state.water_data = json.load(f)
    else:
        st.session_state.water_data = {}

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fffbea 0%, #e8f5e9 50%, #e3f2fd 100%);
    }
    .header-section {
        text-align: center;
        background: linear-gradient(135deg, #e3f2fd 0%, #f8bbd0 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(227, 242, 253, 0.6);
    }
    .header-title {
        font-size: 42px;
        font-weight: 700;
        color: #1976d2;
        margin: 0;
    }
    .header-subtitle {
        font-size: 14px;
        color: #5e35b1;
        margin-top: 8px;
    }
    .stats-card {
        background: linear-gradient(135deg, #fffbea 0%, #fff9c4 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(255, 251, 234, 0.5);
        text-align: center;
        margin: 10px;
        border: 2px solid #f9f3d6;
    }
    .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: #f57c00;
        margin: 8px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stat-label {
        font-size: 12px;
        color: #6d4c41;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    .progress-container {
        background: transparent;
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
    }
    .add-water-section {
        background: transparent;
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1976d2;
        margin-bottom: 15px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .quick-add-btn {
        background: linear-gradient(135deg, #4fc3f7 0%, #29b6f6 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        margin: 5px;
        box-shadow: 0 4px 12px rgba(79, 195, 247, 0.3);
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #424242;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <div class="header-title">💧 Water Intake Tracker</div>
        <div class="header-subtitle">Stay hydrated, stay healthy - Track your daily water intake</div>
    </div>
    """, unsafe_allow_html=True)

# Get today's date
today = datetime.now().strftime("%Y-%m-%d")

# Initialize today's data if not exists
if today not in st.session_state.water_data:
    st.session_state.water_data[today] = 0

# Daily goal in ml
DAILY_GOAL = 3000

# Current intake
current_intake = st.session_state.water_data[today]
progress_percentage = min((current_intake / DAILY_GOAL) * 100, 100)

# Stats Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Today's Intake</div>
            <div class="stat-value">{current_intake}</div>
            <div class="stat-label">ml</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Daily Goal</div>
            <div class="stat-value">{DAILY_GOAL}</div>
            <div class="stat-label">ml</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    remaining = max(DAILY_GOAL - current_intake, 0)
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Remaining</div>
            <div class="stat-value">{remaining}</div>
            <div class="stat-label">ml</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Progress</div>
            <div class="stat-value">{progress_percentage:.0f}%</div>
            <div class="stat-label">of goal</div>
        </div>
        """, unsafe_allow_html=True)

# Progress Bar and Add Water Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Daily Progress</div>', unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress_percentage / 100)
    
    # Message based on progress
    if progress_percentage >= 100:
        st.success("🎉 Congratulations! You've reached your daily goal!")
    elif progress_percentage >= 75:
        st.info("💪 Almost there! Keep it up!")
    elif progress_percentage >= 50:
        st.warning("⚡ Halfway done! Don't forget to drink more water!")
    else:
        st.error("🚰 You need to drink more water today!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weekly Hydration Chart in left column
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Weekly Hydration Chart</div>', unsafe_allow_html=True)
    
    # Get last 7 days of data
    dates = []
    intakes = []
    for i in range(6, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append((datetime.now() - timedelta(days=i)).strftime("%b %d"))
        intakes.append(st.session_state.water_data.get(date, 0))
    
    # Create the chart
    fig = go.Figure()
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=dates,
        y=intakes,
        marker=dict(
            color=intakes,
            colorscale=[[0, '#e3f2fd'], [0.5, '#4fc3f7'], [1, '#0288d1']],
            line=dict(color='#0277bd', width=2)
        ),
        text=[f'{val}ml' for val in intakes],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Water Intake: %{y}ml<extra></extra>'
    ))
    
    # Add goal line
    fig.add_hline(
        y=DAILY_GOAL,
        line_dash="dash",
        line_color="#f44336",
        annotation_text=f"Goal: {DAILY_GOAL}ml",
        annotation_position="right"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Water Intake (ml)",
        height=350,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color="#333"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="add-water-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add Water Intake</div>', unsafe_allow_html=True)
    
    # Custom amount input
    custom_amount = st.number_input("Custom Amount (ml)", min_value=0, max_value=2000, value=250, step=50, key="custom_water")
    
    if st.button("➕ Add Custom", use_container_width=True):
        st.session_state.water_data[today] += custom_amount
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.water_data, f)
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Quick Add:**")
    
    # Quick add buttons
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button("🥤 250ml", use_container_width=True):
            st.session_state.water_data[today] += 250
            with open(DATA_FILE, 'w') as f:
                json.dump(st.session_state.water_data, f)
            st.rerun()
        
        if st.button("🍶 500ml", use_container_width=True):
            st.session_state.water_data[today] += 500
            with open(DATA_FILE, 'w') as f:
                json.dump(st.session_state.water_data, f)
            st.rerun()
    
    with col_q2:
        if st.button("🥛 750ml", use_container_width=True):
            st.session_state.water_data[today] += 750
            with open(DATA_FILE, 'w') as f:
                json.dump(st.session_state.water_data, f)
            st.rerun()
        
        if st.button("💧 1000ml", use_container_width=True):
            st.session_state.water_data[today] += 1000
            with open(DATA_FILE, 'w') as f:
                json.dump(st.session_state.water_data, f)
            st.rerun()
    
    if st.button("🔄 Reset Today", use_container_width=True, type="secondary"):
        st.session_state.water_data[today] = 0
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.water_data, f)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 30px 20px; color: white;">
        <p style="font-size: 14px; font-weight: 500; letter-spacing: 0.5px;">
            Day 6 of 15 - Python Challenge 💧 | Water Intake Tracker
        </p>
    </div>
    """, unsafe_allow_html=True)
