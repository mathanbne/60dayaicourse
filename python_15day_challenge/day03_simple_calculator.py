import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Simple Calculator",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: #f5f7fa;
    }
    .calculator-container {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #f09819 0%, #edde5d 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(240, 152, 25, 0.3);
        color: white;
    }
    .calc-title {
        font-size: 48px;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .calc-subtitle {
        font-size: 16px;
        opacity: 0.95;
        margin-top: 10px;
    }
    .result-display {
        background: white;
        padding: 50px 30px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }
    .calculation-text {
        color: #f09819;
        font-size: 48px;
        font-weight: 700;
        margin: 0;
    }
    .input-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="calculator-container">
        <div class="calc-title">✨ Calculator</div>
        <div class="calc-subtitle">Perform calculations with ease</div>
    </div>
    """, unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 🔢 Enter Numbers & Select Operation")

# Create three columns for inputs
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    num1 = st.number_input(
        "First Number",
        value=0.0,
        step=1.0,
        format="%.2f",
        key="num1"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    operation = st.selectbox(
        "Operation",
        ["➕ Add", "➖ Subtract", "✖ Multiply", "➗ Divide"],
        key="operation"
    )

with col3:
    num2 = st.number_input(
        "Second Number",
        value=0.0,
        step=1.0,
        format="%.2f",
        key="num2"
    )

st.markdown('</div>', unsafe_allow_html=True)  # Close input section

# Perform calculation instantly
result = None
error_message = None

if operation == "➕ Add":
    result = num1 + num2
    operation_symbol = "+"
elif operation == "➖ Subtract":
    result = num1 - num2
    operation_symbol = "-"
elif operation == "✖ Multiply":
    result = num1 * num2
    operation_symbol = "×"
elif operation == "➗ Divide":
    if num2 != 0:
        result = num1 / num2
        operation_symbol = "÷"
    else:
        error_message = "⚠️ Cannot divide by zero!"
        operation_symbol = "÷"

# Display result
if error_message:
    st.markdown("""
        <div class="result-display">
            <div style="color: #e74c3c; font-size: 24px; margin-bottom: 20px;">
                ⚠️ Error
            </div>
            <p style="color: #666; font-size: 18px; margin: 0;">{}</p>
        </div>
        """.format(error_message), unsafe_allow_html=True)
else:
    # Display the calculation
    st.markdown(f"""
        <div class="result-display">
            <div style="color: #999; font-size: 20px; margin-bottom: 15px;">Result</div>
            <div class="calculation-text">{num1} {operation_symbol} {num2} = {result:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 30px 20px 20px 20px;">
        <p style="font-size: 13px; color: #999;">
            Day 3 of 15 - Python Challenge 🧡 | Simple Calculator
        </p>
    </div>
    """, unsafe_allow_html=True)
