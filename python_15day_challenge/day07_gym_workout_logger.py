import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Gym Workout Logger",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# File to store workout data
DATA_FILE = "workout_data.json"

# Initialize session state
if 'workout_data' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            st.session_state.workout_data = json.load(f)
    else:
        st.session_state.workout_data = []

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    .header-section {
        text-align: center;
        background: linear-gradient(135deg, #89CFF0 0%, #A7C7E7 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(137, 207, 240, 0.3);
    }
    .header-title {
        font-size: 42px;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    .header-subtitle {
        font-size: 14px;
        color: #34495e;
        margin-top: 8px;
    }
    .stats-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        text-align: center;
        margin: 10px;
    }
    .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: #2c3e50;
        margin: 8px 0;
    }
    .stat-label {
        font-size: 12px;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    .form-container {
        background: transparent;
        padding: 25px;
        border-radius: 15px;
        margin: 10px;
    }
    .table-container {
        background: transparent;
        padding: 25px;
        border-radius: 15px;
        margin: 10px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 15px;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <div class="header-title">🏋️‍♂️ Gym Workout Logger</div>
        <div class="header-subtitle">Track your exercises, sets, reps, and weights - Build your strength</div>
    </div>
    """, unsafe_allow_html=True)

# Calculate stats
total_workouts = len(st.session_state.workout_data)
total_exercises = len(set([w['exercise'] for w in st.session_state.workout_data])) if st.session_state.workout_data else 0
total_volume = sum([w['sets'] * w['reps'] * w['weight'] for w in st.session_state.workout_data]) if st.session_state.workout_data else 0

# Get this week's workouts
today = datetime.now()
week_start = today - timedelta(days=today.weekday())
this_week_workouts = len([w for w in st.session_state.workout_data if datetime.strptime(w['date'], "%Y-%m-%d") >= week_start])

# Stats Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Total Workouts</div>
            <div class="stat-value">{total_workouts}</div>
            <div class="stat-label">sessions</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Unique Exercises</div>
            <div class="stat-value">{total_exercises}</div>
            <div class="stat-label">types</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Total Volume</div>
            <div class="stat-value">{total_volume:,.0f}</div>
            <div class="stat-label">kg lifted</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">This Week</div>
            <div class="stat-value">{this_week_workouts}</div>
            <div class="stat-label">sessions</div>
        </div>
        """, unsafe_allow_html=True)

# Main content area
col_left, col_right = st.columns([2, 1])

with col_right:
    st.markdown('<div class="section-title">📝 Log New Workout</div>', unsafe_allow_html=True)
    
    # Form inputs
    exercise = st.text_input("Exercise Name", placeholder="e.g., Bench Press")
    
    col_s, col_r = st.columns(2)
    with col_s:
        sets = st.number_input("Sets", min_value=1, max_value=20, value=3, step=1)
    with col_r:
        reps = st.number_input("Reps", min_value=1, max_value=50, value=10, step=1)
    
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=20.0, step=2.5)
    
    workout_date = st.date_input("Date", value=datetime.now())
    
    notes = st.text_area("Notes (optional)", placeholder="Add any notes about your workout...")
    
    if st.button("💪 Log Workout", width="stretch", type="primary"):
        if exercise:
            new_workout = {
                "date": workout_date.strftime("%Y-%m-%d"),
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "weight": weight,
                "volume": sets * reps * weight,
                "notes": notes
            }
            st.session_state.workout_data.append(new_workout)
            with open(DATA_FILE, 'w') as f:
                json.dump(st.session_state.workout_data, f)
            st.success(f"✅ Logged {exercise}!")
            st.rerun()
        else:
            st.error("Please enter an exercise name!")
    
    if st.button("🗑️ Clear All Data", width="stretch", type="secondary"):
        st.session_state.workout_data = []
        with open(DATA_FILE, 'w') as f:
            json.dump(st.session_state.workout_data, f)
        st.rerun()

with col_left:
    # Workout History Table
    st.markdown('<div class="section-title">📋 Workout History</div>', unsafe_allow_html=True)
    
    if st.session_state.workout_data:
        # Convert to DataFrame and sort by date (most recent first)
        df = pd.DataFrame(st.session_state.workout_data)
        df = df.sort_values('date', ascending=False)
        
        # Format the display
        display_df = df[['date', 'exercise', 'sets', 'reps', 'weight', 'volume']].copy()
        display_df.columns = ['Date', 'Exercise', 'Sets', 'Reps', 'Weight (kg)', 'Volume (kg)']
        
        st.dataframe(display_df, width="stretch", hide_index=True)
    else:
        st.info("No workouts logged yet. Start logging your first workout!")
    
    # Weekly Progress Graph
    st.markdown('<div class="section-title">📊 Weekly Progress</div>', unsafe_allow_html=True)
    
    if st.session_state.workout_data:
        # Get last 7 days
        dates = []
        volumes = []
        workout_counts = []
        
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            date_label = (datetime.now() - timedelta(days=i)).strftime("%b %d")
            dates.append(date_label)
            
            # Calculate volume and count for this date
            day_workouts = [w for w in st.session_state.workout_data if w['date'] == date]
            day_volume = sum([w['volume'] for w in day_workouts])
            volumes.append(day_volume)
            workout_counts.append(len(day_workouts))
        
        # Create figure with secondary y-axis
        fig = go.Figure()
        
        # Add volume bars
        fig.add_trace(go.Bar(
            x=dates,
            y=volumes,
            name='Volume (kg)',
            marker=dict(
                color=volumes,
                colorscale=[[0, '#e3f2fd'], [0.5, '#667eea'], [1, '#764ba2']],
                line=dict(color='#5568d3', width=2)
            ),
            text=[f'{v:,.0f}kg' if v > 0 else '' for v in volumes],
            textposition='outside',
            yaxis='y'
        ))
        
        # Add workout count line
        fig.add_trace(go.Scatter(
            x=dates,
            y=workout_counts,
            name='Workouts',
            mode='lines+markers',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=10, color='#f5576c'),
            yaxis='y2'
        ))
        
        # Update layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis=dict(
                title="Volume (kg)",
                showgrid=True,
                gridcolor='#f0f0f0'
            ),
            yaxis2=dict(
                title="Number of Workouts",
                overlaying='y',
                side='right',
                showgrid=False
            ),
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial, sans-serif", size=12, color="#333"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(t=40, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Start logging workouts to see your weekly progress!")

# Footer
st.markdown("""
    <div style="text-align: center; padding: 30px 20px; color: white;">
        <p style="font-size: 14px; font-weight: 500; letter-spacing: 0.5px;">
            Day 7 of 15 - Python Challenge 🏋️‍♂️ | Gym Workout Logger
        </p>
    </div>
    """, unsafe_allow_html=True)
