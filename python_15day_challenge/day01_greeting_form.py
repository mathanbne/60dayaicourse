import streamlit as st

# Set page configuration
st.set_page_config(page_title="Personal Greeting Generator", page_icon="✨", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background: #d7f9f8;
    }
    .main {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stForm"] {
        background-color: #f1f8f4;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #c8e6c9;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='color: #2E7D32; text-align: center; font-size: 2.5rem; margin-bottom: 0.5rem;'>✨ Personal Greeting Generator ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #43A047; text-align: center; font-weight: 400; margin-bottom: 2rem;'>Discover your personalized welcome message</h3>", unsafe_allow_html=True)

# Sidebar with instructions
st.sidebar.header("📋 How to Use")
st.sidebar.markdown("""
### Follow these simple steps:

1️⃣ **Enter your name** in the text field

2️⃣ **Slide to select your age** using the slider

3️⃣ **Click 'Get Greeting'** to see your personalized message

---

💡 **Tip:** Different age ranges will give you different personalized messages!
""")

# Create a form
with st.form("greeting_form"):
    # Name input
    name = st.text_input("Enter your name:", placeholder="Enter your name")
    
    # Age slider
    age = st.slider("Select your age:", min_value=1, max_value=100, value=25)
    
    # Submit button
    submitted = st.form_submit_button("Get Greeting")

# Display greeting when form is submitted
if submitted:
    if name:
        st.success(f"Hello, {name}! 🎉")
        st.info(f"You are {age} years old.")
        
        # Additional personalized message based on age
        if age < 18:
            st.write("You're so young! Enjoy your youth! 🌟")
        elif age < 30:
            st.write("Great age to chase your dreams! 💪")
        elif age < 60:
            st.write("You're in your prime! Keep going strong! 🚀")
        else:
            st.write("Wisdom comes with age! You're amazing! 🌺")
    else:
        st.warning("Please enter your name to get a greeting!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #2E7D32; font-size: 0.9rem;'>Day 1 of 15 - Python Challenge 💚 | Streamlit Form Application</p>", unsafe_allow_html=True)
