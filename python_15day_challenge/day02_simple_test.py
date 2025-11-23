import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.title("🤝 SplitMate - Bill Splitter")

st.write("Testing basic Streamlit functionality")

# Simple test
total = st.number_input("Total Amount", value=100.0)
num_people = st.number_input("Number of People", min_value=1, value=2)

if total > 0 and num_people > 0:
    share = total / num_people
    st.success(f"Each person pays: ${share:.2f}")
    
    # Simple chart test
    try:
        fig = go.Figure(data=[go.Bar(x=['Person 1', 'Person 2'], y=[50, 50])])
        st.plotly_chart(fig)
        st.write("✅ Plotly chart working!")
    except Exception as e:
        st.error(f"Chart error: {e}")
