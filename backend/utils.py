import streamlit as st

def categorize_by_keywords(item_name):
    item_lower = item_name.lower()
    grocery_keywords = ["food", "grocery", "market", "produce", "meat", "dairy", "vegetable", "fruit", "bread", "milk", "eggs", "rice", "pasta", "flour", "oil", "butter", "cheese", "cereal", "grain", "chicken", "beef", "fish", "salt", "sugar", "spice", "onion", "potato", "tomato"]
    if any(keyword in item_lower for keyword in grocery_keywords):
        return "Groceries"
    snack_keywords = ["snack", "candy", "chocolate", "chip", "soda", "drink", "beverage", "coffee", "tea", "cookie", "biscuit", "cracker", "juice", "popcorn"]
    if any(keyword in item_lower for keyword in snack_keywords):
        return "Snacks"
    household_keywords = ["clean", "soap", "detergent", "paper", "towel", "shampoo", "toilet", "bath", "kitchen", "dish", "laundry", "bleach", "mop", "broom", "trash", "bin", "bucket"]
    if any(keyword in item_lower for keyword in household_keywords):
        return "Household"
    subscription_keywords = ["netflix", "spotify", "prime", "subscription", "membership", "streaming"]
    if any(keyword in item_lower for keyword in subscription_keywords):
        return "Subscriptions"
    return "Other"

def nav_dropdown(current_page: str):
    page = st.sidebar.selectbox(
        'Navigate',
        ['Dashboard', 'Upload Receipt', 'AI Insights'],
        index=['Dashboard', 'Upload Receipt', 'AI Insights'].index(current_page)
    )
    if page != current_page:
        st.switch_page(f'pages/{page.lower().replace(" ", "_")}.py')
        st.stop() 