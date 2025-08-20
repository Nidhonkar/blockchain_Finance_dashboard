import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Blockchain vs Finance Dashboard", layout="wide")

st.title("📊 Blockchain vs Traditional Finance Dashboard")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Home", "Adoption", "Transactions", "Risks"])

# ---------------------------
# Page 1: Home
# ---------------------------
if page == "Home":
    st.subheader("Welcome to the Dashboard")
    st.write("This dashboard explores how Blockchain could disrupt Finance like the Internet disrupted Media.")
    st.markdown("""
    - **Adoption**: Compare Internet vs Blockchain user growth  
    - **Transactions**: BTC vs SWIFT daily scale, remittance costs  
    - **Risks**: Balanced view of risks vs opportunities  
    """)

# ---------------------------
# Page 2: Adoption
# ---------------------------
elif page == "Adoption":
    st.subheader("Adoption Trends (Illustrative Data)")
    df_internet = pd.DataFrame({
        "year": [1985, 1990, 1995, 2000, 2005],
        "internet_users_m": [1, 10, 100, 500, 1000]
    })
    df_blockchain = pd.DataFrame({
        "year": [2010, 2015, 2020, 2025],
        "blockchain_users_m": [1, 5, 50, 200]
    })

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(df_internet, x="year", y="internet_users_m", title="Internet Adoption")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.line(df_blockchain, x="year", y="blockchain_users_m", title="Blockchain Adoption")
        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# Page 3: Transactions
# ---------------------------
elif page == "Transactions":
    st.subheader("BTC vs SWIFT Transactions (Mock Data)")
    df_tx = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=10, freq="D"),
        "btc_tx": [300000, 320000, 310000, 330000, 340000, 350000, 360000, 370000, 380000, 390000],
        "swift_msgs": [35000000, 35500000, 36000000, 36500000, 37000000, 37500000, 38000000, 38500000, 39000000, 39500000]
    })
    fig = px.line(df_tx, x="date", y=["btc_tx", "swift_msgs"], title="BTC vs SWIFT Daily Transactions")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Page 4: Risks
# ---------------------------
elif page == "Risks":
    st.subheader("Risks vs Opportunities (Illustrative Data)")
    df_risks = pd.DataFrame({
        "factor": ["Transparency", "Volatility", "Inclusion", "Regulation"],
        "opportunity": [9, 3, 8, 5],
        "risk": [2, 8, 3, 6]
    })
    fig = px.bar(df_risks, x="factor", y=["opportunity", "risk"], barmode="group", title="Risks vs Opportunities")
    st.plotly_chart(fig, use_container_width=True)
