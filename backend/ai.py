import os
import json
import requests
from datetime import date
from config import config
from .utils import categorize_by_keywords

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-large-latest"

HEADERS = {
    "Authorization": f"Bearer {config.MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def mistral_chat(messages, model=MISTRAL_MODEL, temperature=0.7):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def get_ai_insights(items):
    try:
        items_serializable = []
        for item in items:
            item_copy = item.copy()
            if 'Date' in item_copy and isinstance(item_copy['Date'], date):
                item_copy['Date'] = item_copy['Date'].isoformat()
            items_serializable.append(item_copy)
        prompt = f"""
        Analyze these spending items and provide small categorized bulleted insights:
        {json.dumps(items_serializable, indent=2)}
        Provide short bulleted points on:
        1. Potential Savings
        2. Educational Tips
        """
        messages = [
            {"role": "system", "content": "You are a financial insights assistant."},
            {"role": "user", "content": prompt}
        ]
        return mistral_chat(messages)
    except Exception as e:
        return f"Unable to generate insights at this time. Error: {str(e)}"

def categorize_items(items):
    try:
        for item in items:
            want_need_prompt = f"""
            Classify the following item as a 'Need' or a 'Want'.
            Answer with just 'Need' or 'Want'.
            Item: {item['Name']}
            Price: ${item['Price']}
            """
            want_need_messages = [
                {"role": "system", "content": "You are a financial categorization assistant."},
                {"role": "user", "content": want_need_prompt}
            ]
            want_need_response = mistral_chat(want_need_messages, temperature=0).strip()
            if want_need_response not in ["Want", "Need"]:
                category_guess = categorize_by_keywords(item["Name"])
                item["Want or Need"] = "Need" if category_guess in ["Groceries", "Household"] else "Want"
            else:
                item["Want or Need"] = want_need_response
            category_prompt = f"""
            Categorize this item into one of these categories: Groceries, Snacks, Household, Subscriptions, Other.
            Answer with just the category name.
            Item: {item['Name']}
            Price: ${item['Price']}
            """
            category_messages = [
                {"role": "system", "content": "You are a financial categorization assistant."},
                {"role": "user", "content": category_prompt}
            ]
            category_response = mistral_chat(category_messages, temperature=0).strip()
            if category_response not in ["Groceries", "Snacks", "Household", "Subscriptions", "Other"]:
                item["Category"] = categorize_by_keywords(item["Name"])
            else:
                item["Category"] = category_response
        return items
    except Exception as e:
        return items 