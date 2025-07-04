import streamlit as st
import pandas as pd
from datetime import date
from backend.ai import get_ai_insights
from backend.utils import nav_dropdown

if 'receipts_data' not in st.session_state:
    st.session_state.receipts_data = []
if 'budget_goal' not in st.session_state:
    st.session_state.budget_goal = 4000

nav_dropdown('AI Insights')

st.title('🎓 Smart Spending Insights')

if st.session_state.receipts_data:
    items_serializable = []
    for item in st.session_state.receipts_data:
        item_copy = item.copy()
        if 'Date' in item_copy and isinstance(item_copy['Date'], date):
            item_copy['Date'] = item_copy['Date'].isoformat()
        items_serializable.append(item_copy)
    with st.spinner('Generating AI insights...'):
        insights_text = get_ai_insights(items_serializable)
    st.markdown(insights_text)
    st.subheader('💡 Quick Tips for Smart Spending')
    st.markdown('''
    - **Track Every Dollar**: Use apps or spreadsheets to monitor spending
    - **Wait 24 Hours**: Avoid impulse buys by waiting a day
    - **Compare Prices**: Always shop around for better deals
    - **Plan Meals**: Reduce food waste and save on groceries
    - **Review Subscriptions**: Cancel unused services monthly
    ''')
else:
    st.info('Upload some receipts to get personalized spending insights and learn how to save money!')