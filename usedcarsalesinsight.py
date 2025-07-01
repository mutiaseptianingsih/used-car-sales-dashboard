# ========================= IMPORT LIBRARIES ========================= #
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plotly.colors as pc
import numpy as np
# ========================= DASHBOARD CONFIG ========================= #
st.markdown("""
<style>
#github-btn {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
}
#github-btn button {
    background: linear-gradient(135deg, #0ea5e9, #38bdf8);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}
#github-btn button:hover {
    background: linear-gradient(135deg, #38bdf8, #0ea5e9);
    transform: scale(1.05);
}
</style>

<div id='github-btn'>
    <a href='https://github.com/mutiaseptianingsih/used-car-sales-dashboard' target='_blank' style='text-decoration: none;'>
        <button>
            🔗 View on GitHub
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Used Car Sales Insight Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ========================= CUSTOM STYLING ========================= #
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%);
        color: #0c4a6e;
    }

    .stButton>button {
        background: white;
        color: black;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 6px rgba(14, 165, 233, 0.3);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: #38bdf8;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(14, 165, 233, 0.4);
    }

    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.9);
        color: #0c4a6e;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(14, 165, 233, 0.1);
        backdrop-filter: blur(10px);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #0c4a6e;
        text-shadow: 0 2px 4px rgba(14, 165, 233, 0.1);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #bae6fd 0%, #7dd3fc 100%);
        border-right: 2px solid rgba(14, 165, 233, 0.2);
    }

    .css-1cpxqw2, .css-1d391kg, .css-1v0mbdj, .css-10trblm {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #0c4a6e !important;
        border: 2px solid rgba(14, 165, 233, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px);
    }

    .css-1p05b0s {
        color: #0c4a6e !important;
        font-weight: 600;
    }

    label {
        color: #0c4a6e !important;
        font-weight: 600;
    }

    .metric-box {
        background-color: #f0f9ff;
        padding: 15px 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-top: 10px;
    }

    .metric-box:hover {
        background-color: #7dd3fc;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
    }

    .metric-item {
        margin-bottom: 20px;
    }

    .metric-box h2 {
        color: #0d6efd;
        margin: 5px 0 0 0;
    }

    .metric-box h4 {
        color: #333;
        margin: 0 0 5px 0;
    }

    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        border: 2px solid rgba(14, 165, 233, 0.3);
        color: #0c4a6e;
        font-weight: 600;
        width: auto;
        min-width: 0;
        padding: 8px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: #38bdf8;
        color: white;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #0c4a6e;
    }

    .sidebar-checkbox {
        margin-top: -10px;
        margin-bottom: 15px;
        font-size: 14px;
        color: #0c4a6e;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .sidebar-checkbox .stMarkdown {
        margin-bottom: 0px;
    }

    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .metric-box:hover {
        transform: scale(1.05);
        transition: all 0.3s ease-in-out;
        background-color: #7dd3fc;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
    }

    .stMetric:hover {
    transform: scale(1.03);
    transition: all 0.3s ease-in-out;
    box-shadow: 0 8px 16px rgba(14, 165, 233, 0.25);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ========================= LOAD & VALIDATE DATA ========================= #
with st.spinner("🚗 Memuat data mobil bekas..."):
    data = pd.read_csv("used_car_sales.csv")

# Rename columns if necessary
if "Purchased Price-$" in data.columns:
    data.rename(columns={"Purchased Price-$": "Purchased"}, inplace=True)
if "Sales Agent Name" in data.columns:
    data.rename(columns={"Sales Agent Name": "Sales Agent"}, inplace=True)

required_columns = ["Purchased", "Sold Price-$", "Margin-%", "Sales Agent", "Sales Commission-$", "Sold Date"]
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"⚠️ Dataset kamu tidak memiliki kolom: {', '.join(missing_columns)}. Harap periksa file CSV-nya.")
    st.stop()

try:
    data["Sold Date"] = pd.to_datetime(data["Sold Date"], format="%Y-%m-%d")
except Exception as e:
    st.error(f"❌ Gagal konversi tanggal: {e}")
    st.stop()

# Feature Engineering
data["Year"] = data["Sold Date"].dt.year
data["Profit"] = data["Sold Price-$"] - data["Purchased"]

# ============================= SIDEBAR FILTERS ============================= #
st.sidebar.header("🎯 Filter Panel")

# 🗓️ Date Filter
min_date, max_date = data["Sold Date"].min(), data["Sold Date"].max()
date_range = st.sidebar.date_input("🗓️ Filter by Sold Date:", [min_date, max_date])

st.sidebar.markdown("----")

# 🔘 Custom Multiselect with "Select All"
def smart_multiselect(label, col):
    all_options = sorted(data[col].dropna().unique())
    selected = st.sidebar.multiselect(
        label,
        options=["🔘 Select All"] + all_options,
        default=all_options,
        help=f"Select one or more {col.lower()}"
    )
    return all_options if "🔘 Select All" in selected else selected

# 🛠️ Filter Inputs
gearbox_sel = smart_multiselect("⚙️ Gearbox Type:", "Gearbox")
energy_sel = smart_multiselect("🔋 Energy Type:", "Energy")
year_sel = smart_multiselect("📅 Purchase Year:", "Year")
location_sel = smart_multiselect("📍 Location:", "Location")

# 📊 Filtered Data
data_selection = data[
    (data["Gearbox"].isin(gearbox_sel)) &
    (data["Energy"].isin(energy_sel)) &
    (data["Year"].isin(year_sel)) &
    (data["Location"].isin(location_sel)) &
    (data["Sold Date"] >= pd.to_datetime(date_range[0])) &
    (data["Sold Date"] <= pd.to_datetime(date_range[1]))
]

# ⚠️ Empty Check
if data_selection.empty:
    st.warning("⚠️ No matching records found. Try adjusting your filters.")

# ========================= TITLE & KPI's ========================= #
st.markdown("<h1 class='fade-in' style='text-align: center;'>🚗 Used Car Sales Insight Dashboard 💡</h1>", unsafe_allow_html=True)

st.markdown("""
<p class='fade-in' style='text-align: center; font-size:20px; font-weight:bold;'>
Visualizing Sales, Profit & Market Trends – Powered by Coursera Recognition Team 1
</p>
""", unsafe_allow_html=True)

st.markdown("""
<p class='fade-in' style='font-size:16px; font-weight:600; color:#0c4a6e;'>
ℹ️ Hover over charts to explore values. Click on legends to isolate trends.
</p>
""", unsafe_allow_html=True)

# KPI Calculations
if not data_selection.empty:
    total_sales = int(data_selection["Sold Price-$"].sum())
    total_cost = int(data_selection["Purchased"].sum())
    total_profit = total_sales - total_cost
    average_margin = round(data_selection["Margin-%"].mean(), 2)
    total_commission = int(data_selection["Sales Commission-$"].sum())

    agent_profit = data_selection.groupby("Sales Agent")["Profit"].sum().reset_index()
    top_agent = agent_profit.sort_values("Profit", ascending=False).iloc[0]

# KPI Display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.metric("💵 Total Sales", f"${total_sales:,}")
        st.metric("🧾 Total Cost", f"${total_cost:,}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='fade-in' style='animation-delay: 0.2s;'>", unsafe_allow_html=True)
        st.metric("💰 Total Profit", f"${total_profit:,}")
        st.metric("📊 Avg Margin", f"{average_margin}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='fade-in' style='animation-delay: 0.4s;'>", unsafe_allow_html=True)
        st.metric("💸 Commission Paid", f"${total_commission:,}")
        st.metric("🥇 Top Agent", f"{top_agent['Sales Agent']} (${int(top_agent['Profit']):,})")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# ============================= NAVIGATION & GUIDE ============================= #
st.markdown("---")
st.markdown("""
<h2 style='text-align: center; font-weight: bold;'>
📌 Explore Detailed Insights
</h2>
""", unsafe_allow_html=True)
st.markdown("Use the tabs below to explore profit summaries, monthly trends, agent performance, profit distribution, and more.")

with st.expander("🧭 Dashboard Guide"):
    st.markdown("""
    - 💡 **Overview**: Profit summary by category  
    - 📈 **Profit Trend**: Monthly sales and profit trend
    - 🧑‍💼 **Agent Performance**: Agent performance and ratings  
    - 📊 **Profit Distribution**: Profit spread by type  
    - 📦 **Sale Status**: Number of transactions by status  
    - 📏 **Descriptive Stats**: Descriptive statistics  
    - 🗃️ **Data Table**: Downloadable raw data  
    """)

st.markdown("---")

# ========================= TABS ========================= #
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💡 Overview",
    "📈 Profit Trend", 
    "🧑‍💼 Agent Performance", 
    "📊 Profit Distribution", 
    "📦 Sale Status",
    "📏 Descriptive Stats", 
    "🗃️ Data Table"
])

# === TAB 1: OVERVIEW === #
with tab1:
    st.markdown("<h2 style='text-align: center;'>💡 Summary by Category</h2>", unsafe_allow_html=True)

    # ========== Profit per Location ==========
    st.markdown("#### 📍 Profit by Location")

    profit_by_location = data_selection.groupby("Location")["Profit"].sum().reset_index().sort_values("Profit", ascending=True)

    fig_loc = px.bar(
        profit_by_location,
        x="Profit",
        y="Location",
        orientation='h',
        color="Profit",
        color_continuous_scale=px.colors.sequential.Blues,  # gradasi biru
        labels={"Profit": "Total Profit (US$)"},
        template="plotly_dark"
    )

    fig_loc.update_layout(
        height=400,
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white"),
        xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
        yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"))
    )

    st.plotly_chart(fig_loc, use_container_width=True)

    # ========== Margin per Gearbox ==========
    st.markdown("#### ⚙️ Avg Margin by Gearbox Type")

    margin_by_gearbox = data_selection.groupby("Gearbox")["Margin-%"].mean().reset_index().sort_values("Margin-%", ascending=True)

    fig_gear = px.bar(
        margin_by_gearbox,
        x="Margin-%",
        y="Gearbox",
        orientation='h',
        color="Margin-%",
        color_continuous_scale=px.colors.sequential.Blues,
        labels={"Margin-%": "Average Margin (%)"},
        template="plotly_dark"
    )

    fig_gear.update_layout(
        height=350,
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white"),
        xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
        yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"))
    )

    st.plotly_chart(fig_gear, use_container_width=True)

    # ========== Profit by Energy Type ==========
    st.markdown("#### 🔋 Profit by Energy Type")

    profit_by_energy = data_selection.groupby("Energy")["Profit"].sum().reset_index().sort_values("Profit", ascending=True)

    fig_energy = px.bar(
        profit_by_energy,
        x="Profit",
        y="Energy",
        orientation='h',
        color="Profit",
        color_continuous_scale=px.colors.sequential.Blues,
        labels={"Profit": "Total Profit (US$)"},
        template="plotly_dark"
    )

    fig_energy.update_layout(
        height=350,
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white"),
        xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
        yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"))
    )

    st.plotly_chart(fig_energy, use_container_width=True)

    st.markdown("""
    ### 📌 How to read these charts?

    👉 **Profit by Location:**  
    This chart shows how much total profit was earned from each location.  

    👉 **Average Margin by Gearbox Type:**  
    This chart shows the average profit percentage for each gearbox type.  

    👉 **Profit by Energy Type:**  
    This chart shows total profit earned from different types of car energy (e.g., petrol, diesel, electric).  

    💡 *Tip: Hover over the bars to see exact numbers!*
    """)

# === TAB 2: PROFIT TREND === #
with tab2:
    st.markdown("<h2 style='text-align: center;'>📈 Monthly Profit Trend</h2>", unsafe_allow_html=True)

    # Filter mobil yang sudah terjual
    sold_data = data_selection[data_selection["Car Sale Status"] == "Sold"].copy()
    sold_data["Month"] = sold_data["Sold Date"].dt.to_period("M").dt.to_timestamp()

    # Hitung agregat bulanan
    monthly = sold_data.groupby("Month").agg({
        "Purchased": "sum",
        "Sold Price-$": "sum",
        "Profit": "sum"
    }).reset_index()

    # Buat grafik
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Sold Price-$"],
        name="Sales",
        line=dict(color="#0ea5e9", width=3),
        mode="lines+markers"
    ))

    fig.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Purchased"],
        name="Cost",
        line=dict(color="#64748b", width=2, dash="dot"),
        mode="lines+markers"
    ))

    fig.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Profit"],
        name="Profit",
        line=dict(color="#22c55e", width=3),
        mode="lines+markers"
    ))

    fig.update_layout(
        title=dict(text="📊 Sales, Cost, and Profit per Month", font=dict(color="white")),
        xaxis=dict(
            title=dict(text="Month", font=dict(color="white")),
            tickfont=dict(color="white"),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text="Amount (US$)", font=dict(color="white")),
            tickfont=dict(color="white"),
            showgrid=False
        ),
        legend=dict(
            title=dict(text="Legend", font=dict(color="white")),
            font=dict(color="white")
        ),
        height=500,
        template="plotly_dark",
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tambahkan penjelasan
    st.markdown("""
    ### 📊 How to read this chart?

    This chart shows the monthly trend of:
    - **Total Sales**: The total money earned from cars that were successfully sold each month.
    - **Total Cost**: The total amount spent to purchase those cars.
    - **Total Profit**: The difference between sales and cost (*profit = sales - cost*).
                
    ✅ When the **green profit line** is higher, it means the business made more money that month.  
    ✅ A steady increase in blue and green lines means more sales and better profits.  

    💡 *Tip: You can hover over the lines to see exact values per month!*
    """)


# === TAB 3: AGENT PERFORMANCE === #
with tab3:
    st.markdown("<h2 style='text-align: center;'>🧑‍💼 Sales Agent Performance</h2>", unsafe_allow_html=True)

    # ========================== PROFIT PER AGENT ==========================
    st.markdown("### 💰 Total Profit per Agent")

    agent_profit = data_selection.groupby("Sales Agent")["Profit"].sum().reset_index().sort_values("Profit", ascending=True)

    fig1 = px.bar(
        agent_profit,
        x="Profit",
        y="Sales Agent",
        orientation='h',
        color="Profit",
        color_continuous_scale="Blues",
        labels={"Profit": "Total Profit (US$)"},
        template="plotly_dark"
    )

    fig1.update_layout(
        coloraxis_colorbar=dict(title="Profit"),
        height=500,
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white"),
        xaxis=dict(title=dict(text="Profit (US$)", font=dict(color="white")), tickfont=dict(color="white")),
        yaxis=dict(title=dict(text="Sales Agent", font=dict(color="white")), tickfont=dict(color="white"))
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ========================== AVERAGE RATING PER AGENT ==========================
    st.markdown("### ⭐ Average Sales Rating per Agent")

    rating_by_agent = data_selection.groupby("Sales Agent")["Sales Rating"].mean().reset_index().sort_values("Sales Rating", ascending=True)

    fig_rating = px.bar(
        rating_by_agent,
        x="Sales Rating",
        y="Sales Agent",
        orientation='h',
        color="Sales Rating",
        color_continuous_scale="Blues",
        labels={"Sales Rating": "Avg. Rating"},
        template="plotly_dark"
    )

    fig_rating.update_layout(
        coloraxis_colorbar=dict(title="Avg. Rating"),
        height=500,
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white"),
        xaxis=dict(title=dict(text="Average Rating", font=dict(color="white")), tickfont=dict(color="white")),
        yaxis=dict(title=dict(text="Sales Agent", font=dict(color="white")), tickfont=dict(color="white"))
    )

    st.plotly_chart(fig_rating, use_container_width=True)

    # ========================== TRANSACTIONS PER AGENT ==========================
    st.markdown("### 📊 Number of Transactions per Agent")

    agent_count = data_selection["Sales Agent"].value_counts().reset_index()
    agent_count.columns = ["Sales Agent", "Transaction Count"]
    agent_count = agent_count.sort_values("Transaction Count", ascending=True)

    fig2 = px.bar(
        agent_count,
        x="Transaction Count",
        y="Sales Agent",
        orientation='h',
        color="Transaction Count",
        color_continuous_scale="Blues",
        labels={"Transaction Count": "Transactions"},
        template="plotly_dark"
    )

    fig2.update_layout(
        coloraxis_colorbar=dict(title="Transactions"),
        height=500,
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="white"),
        xaxis=dict(title=dict(text="Number of Transactions", font=dict(color="white")), tickfont=dict(color="white")),
        yaxis=dict(title=dict(text="Sales Agent", font=dict(color="white")), tickfont=dict(color="white"))
    )

    st.plotly_chart(fig2, use_container_width=True)

# === TAB 4: PROFIT DISTRIBUTION === #
with tab4:
    st.markdown("<h2 style='text-align: center;'>📊 Distribution of Profit by Category</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Profit Distribution by Energy")
        fig1 = px.box(
            data_selection,
            x="Energy",
            y="Profit",
            color="Energy",
            title="Profit by Energy Type",
            color_discrete_sequence=px.colors.qualitative.Pastel, 
            template="plotly_dark"
        )
        fig1.update_layout(
            yaxis_tickprefix="$",
            plot_bgcolor="#1e293b",
            paper_bgcolor="#1e293b",
            font=dict(color="white"),
            title_font=dict(color="white"),
            xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            legend=dict(font=dict(color="white"))
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### ⚙️ Profit Distribution by Gearbox")
        fig2 = px.box(
            data_selection,
            x="Gearbox",
            y="Profit",
            color="Gearbox",
            title="Profit by Gearbox Type",
            color_discrete_sequence=px.colors.qualitative.Set2,  # pastel tapi beda dari kiri
            template="plotly_dark"
        )
        fig2.update_layout(
            yaxis_tickprefix="$",
            plot_bgcolor="#1e293b",
            paper_bgcolor="#1e293b",
            font=dict(color="white"),
            title_font=dict(color="white"),
            xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            legend=dict(font=dict(color="white"))
        )
        st.plotly_chart(fig2, use_container_width=True)

# === TAB 5: STATUS === #
with tab5:
    st.markdown("<h2 style='text-align: center;'>📦 Transaction Counts by Status</h2>", unsafe_allow_html=True)
    status_counts = data_selection["Car Sale Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    cols = st.columns(len(status_counts))
    for col, row in zip(cols, status_counts.itertuples(index=False)):
     col.metric(row.Status, f"{int(row.Count)}")

    st.markdown("""
    
    🚗 *This means only around 22% of cars in the dataset have been sold.*  
    🚘 *The large number of unsold cars could signal challenges in demand, pricing strategy, or inventory management.*  

    """)


# === TAB 6: DESCRIPTIVE === #
with tab6:
    st.markdown("<h2 style='text-align: center;'>📏 Descriptive Statistics Analysis</h2>", unsafe_allow_html=True)
    cols_to_analyze = {
        "Sold Price-$": "Selling Price (US$)",
        "Profit": "Profit (US$)",
        "Margin-%": "Margin (%)"
    }

    for col, label in cols_to_analyze.items():
        st.markdown(f"### 📌 {label}")

        if col in data_selection.columns:
            values = data_selection[col].dropna()

            std_dev = values.std()
            variance = values.var()
            data_range = values.max() - values.min()
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            coef_var = (std_dev / values.mean()) * 100 if values.mean() != 0 else 0
            z_scores = np.abs((values - values.mean()) / std_dev) if std_dev != 0 else np.zeros_like(values)
            outliers = (z_scores > 2).sum()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📈 Std. Deviation", f"{std_dev:,.2f}")
            col2.metric("📏 Range", f"{data_range:,.2f}")
            col3.metric("📐 IQR", f"{iqr:,.2f}")
            col4.metric("🚨 Outliers (Z > 2)", f"{int(outliers)}")

            col5, col6 = st.columns(2)
            col5.metric("📊 Variance", f"{variance:,.2f}")
            col6.metric("📌 Coeff. of Variation", f"{coef_var:.1f}%")

            st.markdown("---")
        else:
            st.warning(f"⚠️ Kolom {col} tidak tersedia di dataset.")

# === TAB 7: RAW DATA TABLE === #
with tab7:
    st.markdown("<h2 style='text-align: center;'>🗃️ Raw Data Table</h2>", unsafe_allow_html=True)

    # Tampilkan tabel
    st.dataframe(data_selection, use_container_width=True)

    # Buat file CSV dari data yang terfilter
    csv = data_selection.to_csv(index=False).encode('utf-8')

    # Tombol download
    st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_profit_data.csv",
    mime='text/csv'
    )

st.markdown("---")
with st.expander("ℹ️ About this Dashboard"):
    st.markdown("""
    <div style='line-height: 1.8'>
    <strong>👥 Developed by:</strong><br>
    <b>Coursera Recognition Team 1</b><br><br>

    <strong>📊 Dataset:</strong>  
    <a href='https://www.kaggle.com/datasets/sandeep1080/used-car-sales' target='_blank'>
    Kaggle – Used Car Sales 🔗</a><br><br>

    <strong>🧑‍💻 Team Members:</strong><br>
    <ol>
        <li><b>Ivonny Asya Tatristya Febriyanti</b> (M0722043)</li>
        <li><b>Khaeruniah Hikmah Taulani</b> (M0722045)</li>
        <li><b>Lutfiya Eka Rahmawati</b> (M0722047)</li>
        <li><b>Mutia Septianingsih</b> (M0722053)</li>
        <li><b>Nico Dwi Nugroho</b> (M0722059)</li>
    </ol>
    </div>
    
    <div style='text-align: center; margin-top: 30px; font-style: italic; color: #0c4a6e; font-size:18px;'>
    <b>"Alone we can do so little, together we can do so much."<b>
    </div>
    """, unsafe_allow_html=True)
