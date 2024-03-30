import os
import json
import shutil
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
from enum import Enum
import time

with st.sidebar:
    st.markdown(
        "## How to use\n"
        "1. Choose data sources.\n"
        "2. If CSV is chosen as a data source, upload a CSV file.\n"
    )
    st.markdown("---")
    st.markdown("# About")
    st.markdown(
        "AI app to find real-time news from various sources and articles (News_api)"
        "It uses Pathway’s [LLM App features](https://github.com/pathwaycom/llm-app) "
        "to build real-time LLM(Large Language Model)-enabled data pipeline in Python and join data from multiple input sources\n"

    )
    

    st.markdown("[View the source code on GitHub](https://github.com/Boburmirzo/chatgpt-api-python-sales)")

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "0.0.0.0")
api_port = int(os.environ.get("PORT", 8080))

# Paths for data files
rainforest_path = "../rainforest/news_sources.jsonl"
csv_path = "../data/csv_discounts.jsonl"


# Enum for data sources
class DataSource(Enum):
    RAINFOREST_API = 'NewsAPI'
    CSV = 'CSV'


# Streamlit UI elements
def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
             return json.load(f)

lottie_coding = load_lottiefile("./news.json")
st.title("News tracker with LLM App")
data_sources = st.multiselect(
    'Choose data sources',
    [source.value for source in DataSource]
)

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=("csv"),
    disabled=(DataSource.CSV.value not in data_sources)
)

# Handle CSV upload
if uploaded_file and DataSource.CSV.value in data_sources:
    df = pd.read_csv(uploaded_file)

    # Start progress bar
    progress_bar = st.progress(0, "Processing your file. Please wait.")
    total_rows = len(df)

    # Format the DataFrame rows and write to a jsonlines file
    formatted_rows = []

    for _, row in df.iterrows():
        # Format each row and append to the list
        formatted_rows.append(
            {"doc": ', '.join([f"{title}: {value}" for title, value in row.items()])}
        )

    # Write the formatted rows to the jsonlines file
    with open(csv_path, 'w') as outfile:
        for obj in formatted_rows:
            # Update the progress bar
            time.sleep(0.1)
            current_progress = (len(formatted_rows) / total_rows)
            progress_bar.progress(current_progress)
            outfile.write(json.dumps(obj) + '\n')

    # Finish progress bar when done
    progress_bar.progress(1.0, "Your file is uploaded successfully")

question = st.text_input(
    "Search for something",
    placeholder="News",
    disabled=not data_sources
)

# Handle data sources
if DataSource.RAINFOREST_API.value in data_sources:
    shutil.copy("../rainforest/rainforest_discounts.jsonl", rainforest_path)
elif os.path.exists(rainforest_path):
    os.remove(rainforest_path)

if DataSource.CSV.value not in data_sources and os.path.exists(csv_path):
    os.remove(csv_path)

# Handle Discounts API request if data source is selected and a question is provided
if data_sources and question:
    if not os.path.exists(csv_path) and not os.path.exists(rainforest_path):
        st.error("Failed to process discounts file")

    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to Discounts API. Status code: {response.status_code}")
