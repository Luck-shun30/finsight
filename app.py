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