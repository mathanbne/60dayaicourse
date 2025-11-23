import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)

# Exchange rates (base: 1 USD)
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'INR': 83.12,
    'JPY': 149.50,
    'AUD': 1.52,
    'CAD': 1.36,
    'CHF': 0.88
}

# Currency symbols
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
    'JPY': '¥',
    'AUD': 'A$',
    'CAD': 'C$',
    'CHF': 'Fr'
}

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .header-section {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .header-title {
        font-size: 48px;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    .header-subtitle {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 10px;
    }
    .converter-container {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    .result-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .result-value {
        font-size: 42px;
        font-weight: 700;
        color: white;
        margin: 10px 0;
    }
    .exchange-rate {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
        border-left: 4px solid #667eea;
    }
    .rate-text {
        font-size: 14px;
        color: #495057;
        font-weight: 500;
    }
    .section-label {
        font-size: 16px;
        font-weight: 600;
        color: #495057;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-section">
        <div class="header-title">💱 Currency Converter</div>
        <div class="header-subtitle">Fast and easy currency conversion with live rates</div>
    </div>
    """, unsafe_allow_html=True)

# Main converter container
st.markdown('<div class="converter-container">', unsafe_allow_html=True)

# Input section
st.markdown('<div class="section-label">Amount to Convert</div>', unsafe_allow_html=True)
amount = st.number_input("Amount", min_value=0.0, value=100.0, step=10.0, format="%.2f", label_visibility="collapsed")

# From and To currency selection
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">From Currency</div>', unsafe_allow_html=True)
    from_currency = st.selectbox(
        "From",
        options=list(EXCHANGE_RATES.keys()),
        index=3,  # Default to INR
        format_func=lambda x: f"{x} ({CURRENCY_SYMBOLS[x]})",
        key="from_curr",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-label">To Currency</div>', unsafe_allow_html=True)
    to_currency = st.selectbox(
        "To",
        options=list(EXCHANGE_RATES.keys()),
        index=0,  # Default to USD
        format_func=lambda x: f"{x} ({CURRENCY_SYMBOLS[x]})",
        key="to_curr",
        label_visibility="collapsed"
    )

# Conversion calculation
if amount > 0:
    # Convert from source currency to USD, then to target currency
    amount_in_usd = amount / EXCHANGE_RATES[from_currency]
    converted_amount = amount_in_usd * EXCHANGE_RATES[to_currency]
    
    # Exchange rate
    rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
    
    # Display result
    st.markdown(f"""
        <div class="result-box">
            <div class="result-label">{amount:,.2f} {from_currency} =</div>
            <div class="result-value">{CURRENCY_SYMBOLS[to_currency]}{converted_amount:,.2f}</div>
            <div class="result-label">{to_currency}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display exchange rate
    st.markdown(f"""
        <div class="exchange-rate">
            <div class="rate-text">
                1 {from_currency} = {rate:.4f} {to_currency}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Swap button
    if st.button("🔄 Swap Currencies", use_container_width=True):
        # This will trigger a rerun with swapped values
        st.session_state.from_curr = to_currency
        st.session_state.to_curr = from_currency
        st.rerun()

else:
    st.info("💡 Enter an amount to see the conversion")

st.markdown('</div>', unsafe_allow_html=True)

# Popular conversions reference table
st.markdown("### 📊 Quick Reference Rates")

reference_col1, reference_col2 = st.columns(2)

with reference_col1:
    st.markdown("""
        **From USD:**
        - 1 USD = 0.92 EUR
        - 1 USD = 0.79 GBP
        - 1 USD = 83.12 INR
        - 1 USD = 149.50 JPY
    """)

with reference_col2:
    st.markdown("""
        **From EUR:**
        - 1 EUR = 1.09 USD
        - 1 EUR = 0.86 GBP
        - 1 EUR = 90.35 INR
        - 1 EUR = 162.50 JPY
    """)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 30px 20px; color: #6c757d;">
        <p style="font-size: 14px; font-weight: 500; letter-spacing: 0.5px;">
            Day 8 of 15 - Python Challenge 💱 | Currency Converter
        </p>
        <p style="font-size: 12px; margin-top: 10px;">
            Note: Exchange rates are static and for demonstration purposes only
        </p>
    </div>
    """, unsafe_allow_html=True)
