import streamlit as st

st.title("Test App")
st.write("Hello World!")
st.write("If you can see this, Streamlit is working!")

try:
    import plotly
    st.success("✅ Plotly imported successfully")
except Exception as e:
    st.error(f"❌ Plotly error: {e}")

try:
    import pandas
    st.success("✅ Pandas imported successfully")
except Exception as e:
    st.error(f"❌ Pandas error: {e}")
