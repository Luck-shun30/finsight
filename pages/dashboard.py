import streamlit as st

st.set_page_config(
    page_title="FinSight Dashboard",
    page_icon="💰",
    layout="wide"
)
import pandas as pd
import plotly.express as px
from backend.stats import get_spending_stats
from config import config
from backend.utils import nav_dropdown

nav_dropdown('Dashboard')

st.title("💰 Cash Coach Dashboard")

if 'receipts_data' not in st.session_state:
    st.session_state.receipts_data = []
if 'budget_goal' not in st.session_state:
    st.session_state.budget_goal = config.DEFAULT_BUDGET

if st.session_state.receipts_data:
    df = pd.DataFrame(st.session_state.receipts_data)
    stats = get_spending_stats(df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Month", f"${stats['Current Month']:.2f}")
    with col2:
        st.metric("Last Month", f"${stats['Last Month']:.2f}")
    with col3:
        st.metric("This Week", f"${stats['This Week']:.2f}")
    st.subheader("Monthly Budget")
    budget_col1, budget_col2 = st.columns(2)
    with budget_col1:
        if st.session_state.budget_goal > 0:
            progress = (stats['Current Month'] / st.session_state.budget_goal) * 100
            st.progress(min(progress, 100) / 100)
            st.write(f"Progress: ${stats['Current Month']:.2f} / ${st.session_state.budget_goal:.2f} ({min(progress, 100):.1f}%)")
        else:
            st.info("Set a budget goal to track your progress")
    with budget_col2:
        new_goal = st.number_input("Set your monthly budget goal", min_value=0, max_value=1000000000000, step=1, value=st.session_state.budget_goal)
        if st.button("Update Budget Goal"):
            st.session_state.budget_goal = new_goal
    col1, col2 = st.columns(2)
    with col1:
        want_need_filter = st.multiselect(
            "Want & Needs:",
            ["Want", "Need"],
            default=["Want", "Need"]
        )
    with col2:
        category_filter = st.multiselect(
            "Product Type:",
            ["Groceries", "Snacks", "Household", "Subscriptions", "Other"],
            default=["Groceries", "Snacks", "Household", "Subscriptions", "Other"]
        )
    filtered_data = st.session_state.receipts_data.copy()
    if want_need_filter:
        filtered_data = [item for item in filtered_data if item["Want or Need"] in want_need_filter]
    if category_filter and "All" not in category_filter:
        filtered_data = [item for item in filtered_data if item["Category"] in category_filter]
    edited_df = st.data_editor(
        pd.DataFrame(filtered_data),
        column_config={
            "Name": st.column_config.TextColumn("Name"),
            "Price": st.column_config.NumberColumn("Price", format="$%.2f"),
            "Date": st.column_config.DateColumn("Date"),
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Groceries", "Snacks", "Household", "Subscriptions", "Other"]
            ),
            "Want or Need": st.column_config.SelectboxColumn(
                "Want or Need",
                options=["Want", "Need"]
            )
        },
        num_rows="dynamic",
        key="receipts_editor"
    )
    if not edited_df.empty:
        fig = px.pie(edited_df, values='Price', names='Category', title='Spending by Category')
        st.plotly_chart(fig)
else:
    st.info("No spending data available. Upload receipts to see your dashboard.") 