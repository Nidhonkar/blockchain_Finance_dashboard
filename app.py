import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(
    page_title="Parallels & Adoption — Internet vs Blockchain",
    page_icon="💠",
    layout="wide"
)

# -----------------------
# Helpers
# -----------------------
DATA_DIR = Path("data")

def load_csv(name: str, default_df: pd.DataFrame) -> pd.DataFrame:
    """Load CSV from /data; if missing, use provided default."""
    try:
        p = DATA_DIR / name
        if p.exists():
            return pd.read_csv(p)
        else:
            return default_df.copy()
    except Exception:
        return default_df.copy()

def metric_card(label: str, value: str, helptext: str = ""):
    with st.container(border=True):
        st.markdown(f"**{label}**")
        st.markdown(f"<h2 style='margin-top:-6px;'>{value}</h2>", unsafe_allow_html=True)
        if helptext:
            st.caption(helptext)

# -----------------------
# Default illustrative data (used if CSVs not found)
# Replace with your own CSVs in /data when ready
# -----------------------
df_internet_default = pd.DataFrame({
    "year": [1985, 1990, 1995, 2000, 2005],
    "users_millions_est": [1, 10, 100, 500, 1100]
})
df_blockchain_default = pd.DataFrame({
    "year": [2009, 2015, 2020, 2025],
    "users_millions_est": [0.1, 5, 50, 250]
})

start = datetime.today().date() - timedelta(days=179)
df_tx_default = pd.DataFrame({
    "date": pd.date_range(start, periods=180, freq="D"),
    "btc_daily_tx": [300000 + (i % 50) * 1000 for i in range(180)],
    "swift_daily_msgs": [35000000 + (i % 50) * 100000 for i in range(180)],
})

df_fees_default = pd.DataFrame({
    "corridor": ["UAE→India", "UAE→Philippines", "KSA→Pakistan", "US→Mexico", "EU→Morocco"],
    "traditional_fee_pct": [6.5, 7.2, 6.8, 5.9, 6.1],
    "blockchain_fee_pct":  [2.2, 2.5, 2.3, 1.8, 2.1],
})

df_remit_top_default = pd.DataFrame({
    "corridor": ["UAE→India", "UAE→Philippines", "KSA→Pakistan", "US→Mexico", "EU→Morocco"],
    "amount_usd_bn_est": [20.5, 7.9, 8.2, 55.5, 6.4],
})

df_cbdc_default = pd.DataFrame({
    "country": ["China", "EU", "UAE", "India", "Brazil", "Singapore"],
    "project": ["e‑CNY", "Digital Euro", "mBridge/Aber", "Digital Rupee", "Drex", "Ubin/Orchid"],
    "status":  ["Pilot", "Preparation", "Pilot", "Pilot", "Pilot", "Experimentation"]
})

df_risk_default = pd.DataFrame({
    "factor": ["Transparency", "Financial Inclusion", "Cost Efficiency", "Speed/Settlement",
               "Volatility", "Regulatory Clarity", "Scams/Fraud", "Security"],
    "opportunity_score": [9, 8, 8, 8, 3, 5, 4, 7],
    "risk_score":        [2, 3, 3, 2, 8, 6, 7, 4],
})

df_token_default = pd.DataFrame({
    "asset_class": ["Real Estate", "Art", "Bonds", "Equity", "Commodities"],
    "tokenized_value_usd_bn_est": [3.2, 0.6, 5.1, 4.0, 2.3],
})

# -----------------------
# Load data (CSV override if present)
# -----------------------
df_internet = load_csv("adoption_internet.csv", df_internet_default)
df_blockchain = load_csv("adoption_blockchain.csv", df_blockchain_default)
df_tx = load_csv("transactions_comparison.csv", df_tx_default)
if "date" in df_tx.columns:
    df_tx["date"] = pd.to_datetime(df_tx["date"])
df_fees = load_csv("remittance_fees.csv", df_fees_default)
df_remit_top = load_csv("global_remittance_corridors.csv", df_remit_top_default)
df_cbdc = load_csv("cbdc_projects.csv", df_cbdc_default)
df_risk = load_csv("risks_opportunities.csv", df_risk_default)
df_token = load_csv("tokenization_assets.csv", df_token_default)

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📈 Parallels & Adoption", "💸 Transactions & Costs",
     "🧩 Use Cases", "⚖️ Risks & Opportunities", "🔭 Outlook"]
)
presentation = st.sidebar.checkbox("Presentation Mode (simplify visuals)", value=True)

# -----------------------
# Pages
# -----------------------
if page == "🏠 Home":
    st.title("Streamlit Dashboard: Parallels & Adoption — Internet vs Blockchain")
    st.write("This dashboard tells a 5‑part story: **Parallels & Adoption → Architecture & Process → Outcomes → Balance → Outlook**.")

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Years since Bitcoin genesis block", f"{datetime.now().year - 2009}+",
                    "Bitcoin (2009) as blockchain’s “email” killer app.")
    with c2:
        metric_card("CBDC projects listed (sample)", f"{len(df_cbdc)}",
                    "Swap with BIS/IMF sources for live counts.")
    with c3:
        last30 = df_tx.tail(30)["btc_daily_tx"].mean()
        metric_card("Avg daily BTC tx (last 30 days, mock)", f"{int(last30):,}",
                    "Replace with live series when available.")

    st.markdown("---")
    st.subheader("How to use this dashboard")
    st.markdown(
        "- Navigate pages from the sidebar.\n"
        "- Toggle **Presentation Mode** to simplify visuals live on stage.\n"
        "- Replace CSVs in `/data` with official sources to go beyond illustrative data."
    )

elif page == "📈 Parallels & Adoption":
    st.header("Parallels & Adoption — Internet vs Blockchain")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Internet Adoption (estimated, millions)")
        st.line_chart(df_internet.set_index("year")["users_millions_est"])
    with c2:
        st.caption("Blockchain/Crypto Adoption (estimated, millions)")
        st.line_chart(df_blockchain.set_index("year")["users_millions_est"])

    st.subheader("Layers Analogy (Architecture & Process)")
    st.markdown(
        "**Internet stack:** Ethernet → TCP/IP → HTTP → Web Apps  \n"
        "**Blockchain stack:** Networking → Consensus → Smart Contracts → dApps/DeFi  \n"
        "*Standardization and open protocols unlock innovation (e.g., ERC‑20, Lightning).*"
    )

elif page == "💸 Transactions & Costs":
    st.header("Transactions & Costs — BTC vs SWIFT, Fees, and Process")
    sel = st.selectbox("Choose a comparison", ["Daily Volume (BTC vs SWIFT)", "Remittance Fees by Corridor"])
    if sel == "Daily Volume (BTC vs SWIFT)":
        show = df_tx[["date", "btc_daily_tx", "swift_daily_msgs"]].set_index("date")
        st.line_chart(show)
        st.caption("Scale differs significantly today; focus is architecture & transparency, not raw throughput (yet).")
    else:
        st.write("Average Remittance Fees by Corridor (illustrative)")
        fees_plot = df_fees.set_index("corridor")[["traditional_fee_pct", "blockchain_fee_pct"]]
        st.bar_chart(fees_plot)
        st.dataframe(df_fees, use_container_width=True)

    st.markdown("---")
    st.subheader("Process Flows (Narrative)")
    st.markdown(
        "**Traditional path:** Sender → Bank → Correspondent/Clearing → SWIFT → Recipient  \n"
        "**On‑chain path:** Sender → Blockchain Network → Recipient  \n"
        "**Implications:** Fewer intermediaries, potentially faster settlement, greater transparency."
    )

elif page == "🧩 Use Cases":
    st.header("Use Cases — Remittances, Smart Contracts, Tokenization")
    tabs = st.tabs(["Remittances (Top Corridors)", "Smart‑Contract Demo", "Tokenization"])

    with tabs[0]:
        st.markdown("**Global Remittance Market (Top Corridors — illustrative):**")
        st.dataframe(df_remit_top, use_container_width=True)
        st.bar_chart(df_remit_top.set_index("corridor"))

    with tabs[1]:
        st.markdown("**Simulated Smart‑Contract Payout** — toy example for live demos.")
        amount = st.number_input("Claim amount (USD)", min_value=0, step=100, value=1000)
        if st.button("Execute smart contract (simulate)"):
            payout = amount * 0.95  # illustrative logic
            st.success(f"✅ Contract executed: Approved payout = ${payout:,.2f}")
            st.caption("Logic is illustrative; replace with a real on‑chain call in production.")

    with tabs[2]:
        st.markdown("**Tokenization of Real‑World Assets (illustrative):**")
        st.bar_chart(df_token.set_index("asset_class"))

elif page == "⚖️ Risks & Opportunities":
    st.header("Balanced View — Risks vs Opportunities")
    cols = st.columns(2)
    with cols[0]:
        st.caption("Opportunities (1–10)")
        st.bar_chart(df_risk.set_index("factor")[["opportunity_score"]])
    with cols[1]:
        st.caption("Risks (1–10)")
        st.bar_chart(df_risk.set_index("factor")[["risk_score"]])

    st.markdown(
        "**Key concerns:** hype/fake blockchains, rigid 'code as law', volatility, regulatory uncertainty.  \n"
        "**Key upsides:** transparency, financial inclusion, lower cost, automation & new products."
    )

elif page == "🔭 Outlook":
    st.header("Outlook — Watchlist & Next Steps")
    st.markdown(
        "- **CBDCs:** Track pilots and policy moves; monitor wholesale vs retail designs.  \n"
        "- **Tokenized deposits & securities:** Bank pilots and interbank settlement trials.  \n"
        "- **Interoperability standards:** Identity, cross‑chain messaging, compliance.  \n"
        "- **Regulatory clarity:** Structured rules for custody, stablecoins, market conduct."
    )
    st.subheader("CBDC Projects (Sample Table)")
    st.dataframe(df_cbdc, use_container_width=True)
    st.info("Replace with BIS/IMF or central‑bank sources for production‑ready dashboards.")
