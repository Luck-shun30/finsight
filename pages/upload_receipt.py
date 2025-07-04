import streamlit as st
import pandas as pd
from datetime import datetime
import os
from backend.ocr import process_receipt
from backend.ai import categorize_items
from backend.utils import nav_dropdown

if 'receipts_data' not in st.session_state:
    st.session_state.receipts_data = []

if 'budget_goal' not in st.session_state:
    st.session_state.budget_goal = 4000

nav_dropdown('Upload Receipt')

st.title("📄 Upload Receipt")

def process_image(image_path):
    try:
        with st.spinner('Processing receipt with OCR...'):
            items = process_receipt(image_path)
        if items:
            with st.spinner('Categorizing items with AI...'):
                categorized_items = categorize_items(items)
            
            batch_key = f"receipt_batch_{datetime.now().timestamp()}"
            
            if 'receipt_batches' not in st.session_state:
                st.session_state.receipt_batches = {}
            
            st.session_state.receipt_batches[batch_key] = categorized_items
            
            st.success("Receipt processed successfully!")
            
            edited_df = st.data_editor(
                pd.DataFrame(categorized_items),
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
                key=batch_key
            )
            
            st.session_state.receipt_batches[batch_key] = edited_df.to_dict('records')
            
            st.session_state.receipts_data = []
            for batch in st.session_state.receipt_batches.values():
                st.session_state.receipts_data.extend(batch)
            
            os.remove(image_path)
        else:
            st.error("No items found in the receipt. Please try again with a clearer image.")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        if os.path.exists(image_path):
            os.remove(image_path)

upload_method = st.radio("Choose upload method:", ["File Upload", "Camera"])

if upload_method == "File Upload":
    uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        with open("temp_receipt.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        process_image("temp_receipt.jpg")
else:
    img_file_buffer = st.camera_input("Take a picture of your receipt")
    if img_file_buffer is not None:
        with open("temp_receipt.jpg", "wb") as f:
            f.write(img_file_buffer.getbuffer())
        process_image("temp_receipt.jpg")

if st.session_state.receipts_data:
    receipt_count = len(st.session_state.receipt_batches) if 'receipt_batches' in st.session_state else 1
    
    if receipt_count > 1:
        st.subheader("All Receipts")
        all_receipts_df = st.data_editor(
            pd.DataFrame(st.session_state.receipts_data),
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
            key="all_receipts_editor"
        )
        
        st.session_state.receipts_data = all_receipts_df.to_dict('records')