import streamlit as st
import pandas as pd
import plotly.express as px
from mindee import Client, PredictResponse, product
import google.generativeai as genai
import json
from datetime import datetime, timedelta, date
import os
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
mindee_client = Client(api_key=os.getenv('MINDEE_API_KEY'))

if 'receipts_data' not in st.session_state:
    st.session_state.receipts_data = []

if 'budget_goal' not in st.session_state:
    st.session_state.budget_goal = 4000

st.set_page_config(
    page_title="FinSight",
    page_icon="💰",
    layout="wide"
)

def process_receipt(image):
    try:
        input_doc = mindee_client.source_from_path(image)
        result: PredictResponse = mindee_client.parse(product.ReceiptV5, input_doc)
        products = result.document.inference.prediction.line_items

        items = []
        
        for item in products:
            items.append({
                "Name": item.description,
                "Price": item.total_amount,
                "Date": datetime.now().date(),
                "Category": "Other",
                "Want or Need": "Need"
            })
        
        return items
    except Exception as e:
        st.error(f"Error processing receipt: {str(e)}")
        return []

def get_ai_insights(items):
    try:
        items_serializable = []
        for item in items:
            item_copy = item.copy()
            if 'Date' in item_copy and isinstance(item_copy['Date'], date):
                item_copy['Date'] = item_copy['Date'].isoformat()
            items_serializable.append(item_copy)

        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        Analyze these spending items and provide small categorized bulleted insights:
        {json.dumps(items_serializable, indent=2)}

        Provide short bulleted points on:
        1. Potential Savings
        2. Educational Tips
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error getting AI insights: {str(e)}")
        return "Unable to generate insights at this time."

def categorize_items(items):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        for item in items:
            want_need_prompt = f"""
            Is this item a want or a need? Answer with just 'Want' or 'Need':
            Item: {item['Name']}
            Price: ${item['Price']}
            """
            want_need_response = model.generate_content(want_need_prompt)
            item["Want or Need"] = want_need_response.text.strip()
            
            category_prompt = f"""
            Categorize this item into one of these categories: Groceries, Snacks, Household, Subscriptions, Other.
            Answer with just the category name:
            Item: {item['Name']}
            Price: ${item['Price']}
            """
            category_response = model.generate_content(category_prompt)
            item["Category"] = category_response.text.strip()
            
            if item["Category"] not in ["Groceries", "Snacks", "Household", "Subscriptions", "Other"]:
                item["Category"] = categorize_by_keywords(item["Name"])
        
        return items
    except Exception as e:
        st.error(f"Error categorizing items: {str(e)}")
        return items

def categorize_by_keywords(item_name):
    item_lower = item_name.lower()
    
    grocery_keywords = ["food", "grocery", "market", "produce", "meat", "dairy", "vegetable", "fruit", "bread", "milk", "eggs"]
    if any(keyword in item_lower for keyword in grocery_keywords):
        return "Groceries"
    
    snack_keywords = ["snack", "candy", "chocolate", "chip", "soda", "drink", "beverage", "coffee", "tea"]
    if any(keyword in item_lower for keyword in snack_keywords):
        return "Snacks"
    
    household_keywords = ["clean", "soap", "detergent", "paper", "towel", "shampoo", "toilet", "bath", "kitchen"]
    if any(keyword in item_lower for keyword in household_keywords):
        return "Household"
    
    subscription_keywords = ["netflix", "spotify", "prime", "subscription", "membership", "streaming"]
    if any(keyword in item_lower for keyword in subscription_keywords):
        return "Subscriptions"
    
    return "Other"

def get_spending_stats(df):
    today = datetime.now().date()
    current_month = today.replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    current_month_spending = df[df['Date'] >= current_month]['Price'].sum()
    
    last_month_spending = df[(df['Date'] >= last_month) & (df['Date'] < current_month)]['Price'].sum()
    
    week_start = today - timedelta(days=today.weekday())
    weekly_spending = df[df['Date'] >= week_start]['Price'].sum()
    
    return {
        "Current Month": current_month_spending,
        "Last Month": last_month_spending,
        "This Week": weekly_spending
    }

st.title("💰 FinSight Dashboard")
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