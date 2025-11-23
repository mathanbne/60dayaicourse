import streamlit as st

# Page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="🏋️",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    .main-container {
        background: white;
        padding: 50px;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        margin: 30px auto;
        max-width: 800px;
    }
    .header-section {
        text-align: center;
        margin-bottom: 40px;
        padding-bottom: 20px;
        border-bottom: 3px solid #f0f0f0;
    }
    .header-title {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    .header-subtitle {
        font-size: 18px;
        color: #888;
        font-weight: 400;
    }
    .bmi-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        margin: 40px 0;
        color: white;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    .bmi-result::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    .bmi-value {
        font-size: 72px;
        font-weight: 800;
        margin: 15px 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    .bmi-category {
        font-size: 36px;
        font-weight: 700;
        margin: 15px 0;
        letter-spacing: 1px;
    }
    .category-card {
        padding: 20px;
        border-radius: 15px;
        margin: 12px 0;
        text-align: center;
        font-weight: 600;
        font-size: 16px;
        transition: transform 0.2s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .underweight {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
    }
    .normal {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    .overweight {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
    }
    .obese {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
    }
    .input-label {
        font-weight: 600;
        color: #555;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <div class="header-title">🏋️ BMI Calculator</div>
        <div class="header-subtitle">Track your health with Body Mass Index</div>
    </div>
    """, unsafe_allow_html=True)

# Input section
st.markdown("<h3 style='color: #667eea; font-weight: 600; margin-bottom: 25px;'>📏 Enter Your Measurements</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    height_cm = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=170.0,
        step=1.0,
        help="Enter your height in centimeters"
    )

with col2:
    weight_kg = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        value=70.0,
        step=0.1,
        help="Enter your weight in kilograms"
    )

# Calculate BMI
if height_cm > 0 and weight_kg > 0:
    # Convert height to meters
    height_m = height_cm / 100
    
    # Calculate BMI
    bmi = weight_kg / (height_m ** 2)
    
    # Determine category and color
    if bmi < 18.5:
        category = "Underweight"
        category_class = "underweight"
        emoji = "😟"
        advice = "You may need to gain weight. Consult a healthcare provider."
    elif 18.5 <= bmi < 25:
        category = "Normal"
        category_class = "normal"
        emoji = "😊"
        advice = "Great! You're in a healthy weight range."
    elif 25 <= bmi < 30:
        category = "Overweight"
        category_class = "overweight"
        emoji = "😐"
        advice = "Consider a balanced diet and regular exercise."
    else:
        category = "Obese"
        category_class = "obese"
        emoji = "😔"
        advice = "Consult a healthcare provider for guidance."
    
    # Display BMI result
    st.markdown(f"""
        <div class="bmi-result">
            <div style="font-size: 18px; opacity: 0.9; letter-spacing: 2px; text-transform: uppercase;">Your BMI Score</div>
            <div class="bmi-value">{bmi:.1f}</div>
            <div class="bmi-category">{emoji} {category}</div>
            <div style="font-size: 17px; margin-top: 20px; opacity: 0.95; line-height: 1.6;">{advice}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # BMI Categories Reference
    st.markdown("<div style='margin: 40px 0 20px 0; border-top: 2px solid #f0f0f0;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #667eea; font-weight: 600; margin-bottom: 25px;'>📊 BMI Categories Reference</h3>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
            <div class="category-card underweight">
                😟 Underweight<br>
                <span style="font-size: 14px; font-weight: normal;">BMI < 18.5</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="category-card normal">
                😊 Normal<br>
                <span style="font-size: 14px; font-weight: normal;">BMI 18.5 - 24.9</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
            <div class="category-card overweight">
                😐 Overweight<br>
                <span style="font-size: 14px; font-weight: normal;">BMI 25 - 29.9</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="category-card obese">
                😔 Obese<br>
                <span style="font-size: 14px; font-weight: normal;">BMI ≥ 30</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional info
    st.markdown("<div style='margin: 30px 0 20px 0;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: #e8f4f8; padding: 20px; border-radius: 12px; border-left: 5px solid #3498db;'>
            <p style='margin: 0; color: #2c3e50; font-size: 15px; line-height: 1.7;'>
                💡 <strong>Important Note:</strong> BMI is a screening tool and doesn't directly measure body fat. 
                For personalized health advice, please consult healthcare professionals.
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("⚠️ Please enter valid height and weight values.")

st.markdown('</div>', unsafe_allow_html=True)  # Close main container

# Footer
st.markdown("""
    <div style="text-align: center; padding: 30px 20px; color: white;">
        <p style="font-size: 14px; font-weight: 500; letter-spacing: 0.5px;">
            Day 4 of 15 - Python Challenge 💜 | BMI Calculator
        </p>
    </div>
    """, unsafe_allow_html=True)
