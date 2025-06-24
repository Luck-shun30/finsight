from mindee import Client, PredictResponse, product
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

mindee_client = Client(api_key=os.getenv('MINDEE_API_KEY'))

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
        return [] 