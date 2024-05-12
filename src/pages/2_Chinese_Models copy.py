import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from utils import stream_response
load_dotenv()



st.set_page_config(page_title="Image Model Demo", page_icon="🌍")
st.title("Multi-Image Model Demo")
st.write("Work in Progress🚧🛠️")

