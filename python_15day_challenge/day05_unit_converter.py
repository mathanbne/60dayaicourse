import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    }
    .header-section {
        text-align: center;
        background: white;
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .header-title {
        font-size: 48px;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    .header-subtitle {
        font-size: 16px;
        color: #888;
        margin-top: 10px;
    }
    .converter-box {
        background: transparent;
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
        height: 100%;
    }
    .converter-title {
        font-size: 18px;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 15px;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .result-display {
        background: linear-gradient(135deg, #7c8adb 0%, #9b6dc2 100%);
        padding: 25px 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .result-value {
        font-size: 36px;
        font-weight: 700;
        margin: 8px 0;
        line-height: 1.2;
    }
    .result-label {
        font-size: 11px;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        font-weight: 500;
    }
    div[data-testid="column"] {
        flex: 1;
        min-width: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <div class="header-title">🔄 Unit Converter</div>
        <div class="header-subtitle">Quick and easy unit conversions</div>
    </div>
    """, unsafe_allow_html=True)

# Create 4 columns for all converters with equal width
col1, col2, col3, col4 = st.columns(4, gap="large")

# Currency Conversion
with col1:
    st.markdown("<div class='converter-box'>", unsafe_allow_html=True)
    st.markdown("<div class='converter-title'>💱 Currency</div>", unsafe_allow_html=True)
    
    amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0, key="currency_amount", label_visibility="collapsed")
    from_currency = st.selectbox("From", ["INR (₹)", "USD ($)"], key="from_curr", label_visibility="collapsed")
    
    to_currency = "USD ($)" if from_currency == "INR (₹)" else "INR (₹)"
    
    if from_currency == "INR (₹)":
        result = amount / 83.0
        result_symbol = "$"
    else:
        result = amount * 83.0
        result_symbol = "₹"
    
    st.markdown(f"""
        <div class="result-display">
            <div class="result-label">{to_currency}</div>
            <div class="result-value">{result_symbol}{result:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Temperature Conversion
with col2:
    st.markdown("<div class='converter-box'>", unsafe_allow_html=True)
    st.markdown("<div class='converter-title'>🌡️ Temperature</div>", unsafe_allow_html=True)
    
    temp = st.number_input("Temp", value=25.0, step=0.1, key="temp_value", label_visibility="collapsed")
    from_temp = st.selectbox("From", ["Celsius (°C)", "Fahrenheit (°F)"], key="from_temp", label_visibility="collapsed")
    
    to_temp = "Fahrenheit (°F)" if from_temp == "Celsius (°C)" else "Celsius (°C)"
    
    if from_temp == "Celsius (°C)":
        result = (temp * 9/5) + 32
        result_unit = "°F"
    else:
        result = (temp - 32) * 5/9
        result_unit = "°C"
    
    st.markdown(f"""
        <div class="result-display">
            <div class="result-label">{to_temp}</div>
            <div class="result-value">{result:.1f}{result_unit}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Length Conversion
with col3:
    st.markdown("<div class='converter-box'>", unsafe_allow_html=True)
    st.markdown("<div class='converter-title'>📏 Length</div>", unsafe_allow_html=True)
    
    length = st.number_input("Length", min_value=0.0, value=100.0, step=1.0, key="length_value", label_visibility="collapsed")
    from_length = st.selectbox("From", ["Centimeters (cm)", "Inches (in)"], key="from_length", label_visibility="collapsed")
    
    to_length = "Inches (in)" if from_length == "Centimeters (cm)" else "Centimeters (cm)"
    
    if from_length == "Centimeters (cm)":
        result = length / 2.54
        result_unit = "in"
    else:
        result = length * 2.54
        result_unit = "cm"
    
    st.markdown(f"""
        <div class="result-display">
            <div class="result-label">{to_length}</div>
            <div class="result-value">{result:.2f} {result_unit}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Weight Conversion
with col4:
    st.markdown("<div class='converter-box'>", unsafe_allow_html=True)
    st.markdown("<div class='converter-title'>⚖️ Weight</div>", unsafe_allow_html=True)
    
    weight = st.number_input("Weight", min_value=0.0, value=70.0, step=0.1, key="weight_value", label_visibility="collapsed")
    from_weight = st.selectbox("From", ["Kilograms (kg)", "Pounds (lb)"], key="from_weight", label_visibility="collapsed")
    
    to_weight = "Pounds (lb)" if from_weight == "Kilograms (kg)" else "Kilograms (kg)"
    
    if from_weight == "Kilograms (kg)":
        result = weight * 2.20462
        result_unit = "lb"
    else:
        result = weight / 2.20462
        result_unit = "kg"
    
    st.markdown(f"""
        <div class="result-display">
            <div class="result-label">{to_weight}</div>
            <div class="result-value">{result:.2f} {result_unit}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 30px 20px; color: white;">
        <p style="font-size: 14px; font-weight: 500; letter-spacing: 0.5px;">
            Day 5 of 15 - Python Challenge 🤍 | Unit Converter
        </p>
    </div>
    """, unsafe_allow_html=True)
