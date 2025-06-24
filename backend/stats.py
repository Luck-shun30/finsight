import pandas as pd
from datetime import datetime, timedelta

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