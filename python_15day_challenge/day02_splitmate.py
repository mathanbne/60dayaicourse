import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="SplitMate - Split Bills Fairly",
    page_icon="🤝",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .logo-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Logo and Title
st.markdown("""
    <div class="logo-container">
        <h1 style="font-size: 48px; margin: 10px 0;">💰🤝 SplitMate</h1>
        <p style="font-size: 18px; font-style: italic;">Your friendly expense splitting companion</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Split bills fairly among friends, family, or colleagues!")
st.divider()

# Initialize session state
if 'num_people' not in st.session_state:
    st.session_state.num_people = 2
if 'people_data' not in st.session_state:
    st.session_state.people_data = []

# ============= STEP 1: BASIC DETAILS =============
st.header("📝 Step 1: Basic Details")

col1, col2 = st.columns(2)

with col1:
    total_amount = st.number_input(
        "💵 Total Bill Amount ($)",
        min_value=0.0,
        value=100.0,
        step=1.0,
        help="Enter the total amount to be split"
    )

with col2:
    num_people = st.number_input(
        "👥 Number of People",
        min_value=1,
        max_value=20,
        value=st.session_state.num_people,
        step=1,
        help="How many people are splitting the bill?"
    )
    st.session_state.num_people = num_people

# Calculate equal share
if total_amount > 0 and num_people > 0:
    equal_share = total_amount / num_people
    st.info(f"💵 **Equal Share Per Person: ${equal_share:.2f}**")
else:
    equal_share = 0
    st.info("💡 Enter total amount and number of people to calculate equal share")

st.divider()

# ============= STEP 2: ADD PEOPLE & CONTRIBUTIONS =============
st.header("👥 Step 2: Add People & Contributions")
st.caption("Enter each person's name and the amount they paid")

# Initialize people data based on number of people
if len(st.session_state.people_data) != num_people:
    st.session_state.people_data = [
        {"name": f"Person {i+1}", "paid": 0.0} 
        for i in range(num_people)
    ]

# Create input fields for each person
for i in range(num_people):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        name = st.text_input(
            f"👤 Name of Person {i+1}",
            value=st.session_state.people_data[i]["name"],
            key=f"name_{i}",
            placeholder=f"e.g., John, Sarah..."
        )
        st.session_state.people_data[i]["name"] = name
    
    with col2:
        paid = st.number_input(
            f"💳 Amount Paid ($)",
            min_value=0.0,
            value=st.session_state.people_data[i]["paid"],
            step=1.0,
            key=f"paid_{i}"
        )
        st.session_state.people_data[i]["paid"] = paid

st.divider()

# ============= CALCULATE BUTTON =============
calculate_col1, calculate_col2, calculate_col3 = st.columns([1, 2, 1])

with calculate_col2:
    calculate_button = st.button(
        "🧮 Calculate Split", 
        type="primary", 
        use_container_width=True
    )

if calculate_button:
    
    # Validation
    total_paid = sum([person["paid"] for person in st.session_state.people_data])
    
    if total_paid == 0:
        st.error("❌ Please enter the amounts paid by each person!")
    elif abs(total_paid - total_amount) > 0.01:  # Allow small floating point errors
        st.warning(f"⚠️ **Warning:** Total contributions (${total_paid:.2f}) doesn't match total bill (${total_amount:.2f})")
        st.info(f"💡 Difference: ${abs(total_paid - total_amount):.2f}")
    else:
        st.success("✅ Calculations complete! Scroll down to see results.")
    
    # Calculate balances
    balances = []
    for person in st.session_state.people_data:
        balance = person["paid"] - equal_share
        balances.append({
            "name": person["name"],
            "paid": person["paid"],
            "fair_share": equal_share,
            "balance": balance
        })
    
    st.divider()
    
    # ============= VISUAL ANALYSIS =============
    st.header("📊 Visual Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    # PIE CHART - Contribution Breakdown
    with chart_col1:
        st.subheader("🥧 Contribution Breakdown")
        st.caption("Who paid what percentage of the total bill")
        
        # Filter out people who paid nothing for cleaner pie chart
        pie_data = [p for p in st.session_state.people_data if p["paid"] > 0]
        
        if pie_data:
            fig_pie = go.Figure(data=[go.Pie(
                labels=[p["name"] for p in pie_data],
                values=[p["paid"] for p in pie_data],
                hole=0.3,
                marker=dict(
                    colors=px.colors.qualitative.Set3
                ),
                textinfo='label+percent',
                textposition='auto',
                hovertemplate='<b>%{label}</b><br>Paid: $%{value:.2f}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("💡 No contributions recorded yet")
    
    # BAR CHART - Paid vs Fair Share
    with chart_col2:
        st.subheader("📊 Paid vs Fair Share")
        st.caption("Compare what each person paid vs their fair share")
        
        # Create data for the chart
        names = [person['name'] for person in balances]
        paid_amounts = [person['paid'] for person in balances]
        fair_shares = [person['fair_share'] for person in balances]
        
        fig_bar = go.Figure()
        
        # Add bars for amount paid
        fig_bar.add_trace(go.Bar(
            name='Amount Paid',
            x=names,
            y=paid_amounts,
            marker_color='#667eea',
            text=[f'${val:.2f}' for val in paid_amounts],
            textposition='outside'
        ))
        
        # Add bars for fair share
        fig_bar.add_trace(go.Bar(
            name='Fair Share',
            x=names,
            y=fair_shares,
            marker_color='#f39c12',
            text=[f'${val:.2f}' for val in fair_shares],
            textposition='outside'
        ))
        
        fig_bar.update_layout(
            barmode='group',
            height=400,
            xaxis_title="People",
            yaxis_title="Amount ($)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(t=60, b=60, l=50, r=20),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    
    # ============= RESULTS: WHO OWES WHAT =============
    st.header("📋 Results: Who Owes What")
    
    # Separate into three categories
    to_receive = [b for b in balances if b["balance"] > 0.01]
    owes_money = [b for b in balances if b["balance"] < -0.01]
    balanced = [b for b in balances if abs(b["balance"]) <= 0.01]
    
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.markdown("### 💚 To Receive")
        if to_receive:
            for person in to_receive:
                st.success(f"**{person['name']}**  \nPaid: ${person['paid']:.2f}  \nShould get back: **${person['balance']:.2f}**")
        else:
            st.info("No one is owed money")
    
    with result_col2:
        st.markdown("### ❌ Owes Money")
        if owes_money:
            for person in owes_money:
                st.error(f"**{person['name']}**  \nPaid: ${person['paid']:.2f}  \nOwes: **${abs(person['balance']):.2f}**")
        else:
            st.info("No one owes money")
    
    with result_col3:
        st.markdown("### ✅ Balanced")
        if balanced:
            for person in balanced:
                st.warning(f"**{person['name']}**  \nPaid: ${person['paid']:.2f}  \nAll settled! ✓")
        else:
            st.info("No one is perfectly balanced")
    
    st.divider()
    
    # ============= SETTLEMENT PLAN =============
    st.header("💸 Settlement Plan")
    st.markdown("**Optimal transactions to settle all debts:**")
    
    # Create settlement transactions
    creditors = sorted(to_receive, key=lambda x: x["balance"], reverse=True)
    debtors = sorted(owes_money, key=lambda x: x["balance"])
    
    transactions = []
    
    # Create copies to work with
    creditors_copy = [{"name": c["name"], "amount": c["balance"]} for c in creditors]
    debtors_copy = [{"name": d["name"], "amount": abs(d["balance"])} for d in debtors]
    
    # Match debtors with creditors
    while creditors_copy and debtors_copy:
        creditor = creditors_copy[0]
        debtor = debtors_copy[0]
        
        # Calculate transaction amount
        transaction_amount = min(creditor["amount"], debtor["amount"])
        
        transactions.append({
            "from": debtor["name"],
            "to": creditor["name"],
            "amount": transaction_amount
        })
        
        # Update balances
        creditor["amount"] -= transaction_amount
        debtor["amount"] -= transaction_amount
        
        # Remove if settled
        if creditor["amount"] < 0.01:
            creditors_copy.pop(0)
        if debtor["amount"] < 0.01:
            debtors_copy.pop(0)
    
    # Display transactions
    if transactions:
        for i, txn in enumerate(transactions, 1):
            st.info(f"**Transaction {i}:**  \n**{txn['from']}** pays **{txn['to']}** → **${txn['amount']:.2f}**")
        
        st.balloons()
        st.success("🎉 **Everyone is settled! All debts cleared!**")
    else:
        st.info("✅ No transactions needed - everyone is already settled!")

# Footer
st.divider()
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="font-size: 16px; color: #666;">
            Made with ❤️ by <b>SplitMate</b> | 💡 Tip: Make sure total contributions match the total bill!
        </p>
    </div>
    """, unsafe_allow_html=True)