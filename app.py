
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Parallels & Adoption — Internet vs Blockchain", page_icon="💠", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📈 Parallels & Adoption",
    "💸 Transactions & Costs",
    "🧩 Use Cases",
    "⚖️ Risks & Opportunities",
    "🔭 Outlook"
])

presentation = st.sidebar.checkbox("Presentation Mode (simplify visuals)", value=True)
st.sidebar.caption("Data are illustrative and offline-ready. Replace CSVs in /data to go live.")

def apply_template(fig):
    if presentation:
        fig.update_layout(template="plotly_white", legend_title_text="")
        fig.update_xaxes(showgrid=False, title_font={"size":14})
        fig.update_yaxes(showgrid=False, title_font={"size":14})
    return fig

def kpi_card(title, value, subtext=""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f"<h2 style='margin-top:-6px;'>{value}</h2>", unsafe_allow_html=True)
        if subtext:
            st.caption(subtext)

@st.cache_data
def load_data():
    base = "data"
    df_internet = pd.read_csv(f"{base}/adoption_internet.csv")
    df_blockchain = pd.read_csv(f"{base}/adoption_blockchain.csv")
    df_tx = pd.read_csv(f"{base}/transactions_comparison.csv", parse_dates=["date"])
    df_fees = pd.read_csv(f"{base}/remittance_fees.csv")
    df_remit_top = pd.read_csv(f"{base}/global_remittance_corridors.csv")
    df_cbdc = pd.read_csv(f"{base}/cbdc_projects.csv")
    df_risk = pd.read_csv(f"{base}/risks_opportunities.csv")
    df_token = pd.read_csv(f"{base}/tokenization_assets.csv")
    return df_internet, df_blockchain, df_tx, df_fees, df_remit_top, df_cbdc, df_risk, df_token

df_internet, df_blockchain, df_tx, df_fees, df_remit_top, df_cbdc, df_risk, df_token = load_data()

if page == "🏠 Home":
    st.title("Streamlit Dashboard: Parallels & Adoption — Internet vs Blockchain")
    st.write("This dashboard tells a 5-part story: **Parallels & Adoption → Architecture & Process → Outcomes → Balance → Outlook**.")
    c1, c2, c3 = st.columns(3)
    with c1:
        years_since_genesis = datetime.now().year - 2009
        kpi_card("Years since Bitcoin genesis block", f"{years_since_genesis}+", "Bitcoin (2009) as blockchain’s 'email' killer app.")
    with c2:
        kpi_card("CBDC projects listed (sample)", f"{len(df_cbdc)}", "Swap with BIS/IMF data for live counts.")
    with c3:
        last30 = df_tx.tail(30)["btc_daily_tx"].mean()
        kpi_card("Avg daily Bitcoin tx (last 30 days, mock)", f"{int(last30):,}", "Replace with live series when available.")
    st.markdown("---")
    st.subheader("How to use this dashboard")
    st.markdown('''
    - Navigate pages from the sidebar.
    - Toggle **Presentation Mode** to simplify visuals live on stage.
    - Replace CSVs in `/data` with official sources to go beyond illustrative data.
    ''')

elif page == "📈 Parallels & Adoption":
    st.header("Parallels & Adoption — Internet vs Blockchain")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(df_internet, x="year", y="users_millions_est", title="Internet Adoption (estimated, millions)",
                      labels={"users_millions_est":"Users (M)", "year":"Year"})
        st.plotly_chart(apply_template(fig), use_container_width=True)
    with c2:
        fig = px.area(df_blockchain, x="year", y="users_millions_est", title="Blockchain/Crypto Adoption (estimated, millions)",
                      labels={"users_millions_est":"Users (M)", "year":"Year"})
        st.plotly_chart(apply_template(fig), use_container_width=True)

    st.subheader("Layers Analogy (Architecture & Process)")
    st.markdown('''
    **Internet stack:** Ethernet ➜ TCP/IP ➜ HTTP ➜ Web Apps  
    **Blockchain stack:** Networking ➜ Consensus ➜ Smart Contracts ➜ dApps/DeFi  
    *Standardization and open protocols unlock innovation (e.g., ERC‑20, Lightning).*
    ''')

elif page == "💸 Transactions & Costs":
    st.header("Transactions & Costs — BTC vs SWIFT, Fees, and Process")
    sel = st.selectbox("Choose a comparison", ["Daily Volume (BTC vs SWIFT)", "Remittance Fees by Corridor"])
    if sel == "Daily Volume (BTC vs SWIFT)":
        fig = px.line(df_tx, x="date", y=["btc_daily_tx", "swift_daily_msgs"],
                      labels={"value":"Count", "date":"Date", "variable":"Series"},
                      title="Daily Volume — BTC Transactions vs SWIFT Messages (illustrative)")
        st.plotly_chart(apply_template(fig), use_container_width=True)
        st.caption("Scale differs significantly today; focus is architectural efficiency and transparency, not raw throughput (yet).")
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_fees["corridor"], y=df_fees["traditional_fee_pct"], name="Traditional (%)"))
        fig.add_trace(go.Bar(x=df_fees["corridor"], y=df_fees["blockchain_fee_pct"], name="Blockchain (%)"))
        fig.update_layout(barmode="group", title="Average Remittance Fees by Corridor (illustrative)",
                          xaxis_title="Corridor", yaxis_title="Fee (%)")
        st.plotly_chart(apply_template(fig), use_container_width=True)
        st.dataframe(df_fees, use_container_width=True)

    st.markdown("---")
    st.subheader("Process Flows (Narrative)")
    st.markdown('''
    **Traditional path:** Sender ➜ Bank ➜ Correspondent/Clearing ➜ SWIFT ➜ Recipient  
    **On‑chain path:** Sender ➜ Blockchain Network ➜ Recipient  
    **Implications:** Fewer intermediaries, potentially faster settlement, greater transparency.
    ''')

elif page == "🧩 Use Cases":
    st.header("Use Cases — Remittances, Smart Contracts, Tokenization")
    tabs = st.tabs(["Remittances (Top Corridors)", "Smart-Contract Demo", "Tokenization"])
    with tabs[0]:
        st.markdown("**Global Remittance Market (Top Corridors — illustrative):**")
        st.dataframe(df_remit_top, use_container_width=True)
        fig = px.bar(df_remit_top, x="corridor", y="amount_usd_bn_est", title="Top Remittance Corridors by Amount (USD bn, est.)",
                     labels={"amount_usd_bn_est":"USD bn (est.)", "corridor":"Corridor"})
        st.plotly_chart(apply_template(fig), use_container_width=True)
    with tabs[1]:
        st.markdown("**Simulated Smart-Contract Payout** — toy example for live demos.")
        amount = st.number_input("Claim amount (USD)", min_value=0, step=100, value=1000)
        trigger = st.button("Execute smart contract (simulate)")
        if trigger:
            payout = amount * 0.95  # illustrative logic
            st.success(f"✅ Contract executed: Approved payout = ${payout:,.2f}")
            st.caption("Logic is illustrative; replace with a real on-chain call in production.")
    with tabs[2]:
        st.markdown("**Tokenization of Real‑World Assets (illustrative):**")
        fig = px.pie(df_token, names="asset_class", values="tokenized_value_usd_bn_est",
                     title="Tokenized Asset Value by Class (USD bn, est.)")
        st.plotly_chart(apply_template(fig), use_container_width=True)

elif page == "⚖️ Risks & Opportunities":
    st.header("Balanced View — Risks vs Opportunities")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df_risk, x="factor", y="opportunity_score", title="Opportunities (1–10)",
                     labels={"opportunity_score":"Score"})
        st.plotly_chart(apply_template(fig), use_container_width=True)
    with c2:
        fig = px.bar(df_risk, x="factor", y="risk_score", title="Risks (1–10)",
                     labels={"risk_score":"Score"})
        st.plotly_chart(apply_template(fig), use_container_width=True)
    st.markdown('''
    **Key concerns:** hype/fake blockchains, rigid 'code as law', volatility, regulatory uncertainty.  
    **Key upsides:** transparency, financial inclusion, lower cost, automation & new products.
    ''')

elif page == "🔭 Outlook":
    st.header("Outlook — Watchlist & Next Steps")
    st.markdown('''
    - **CBDCs:** Track pilots and policy moves; monitor wholesale vs retail designs.
    - **Tokenized deposits & securities:** Bank pilots and interbank settlement trials.
    - **Interoperability standards:** Identity, cross-chain messaging, compliance.
    - **Regulatory clarity:** Structured rules for custody, stablecoins, market conduct.
    ''')
    st.subheader("CBDC Projects (Sample Table)")
    st.dataframe(df_cbdc, use_container_width=True)
    st.info("Replace with BIS/IMF or central-bank sources for production-ready dashboards.")
