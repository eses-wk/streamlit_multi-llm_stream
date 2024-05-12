import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from utils import stream_response, download_history
load_dotenv()


st.set_page_config(page_title="Multi-LLM Demo - 2", page_icon="🌍")
st.title("Multi-LLM Demo - Open Models")

# Initialize chat history
if "chat_history_llama3" not in st.session_state:
    st.session_state['chat_history_'+'llama3'] = []
    
if "chat_history_mistral" not in st.session_state:
    st.session_state['chat_history_'+'mistral'] = []

if "chat_history_gemma" not in st.session_state:
    st.session_state['chat_history_'+'gemma'] = []


st.write("This page is for Llama3-70b, Mistral-8x7b, and Gemma-7b.")

user_query = st.chat_input("Your message", key="user_input")

# Sidebar config
st.sidebar.header("Model Selected")
checkbox_options=['Meta-Llama3 (Groq)','Mistral-8x7b (Groq)','Google-Gemma-7b (Groq)']



col4, col5 , col6 = st.columns(3)
with col4:
    if st.sidebar.checkbox(checkbox_options[0],True):
        st.subheader("Meta: Llama3-70b")
        
        # Show all historical messages
        for hist_message in st.session_state.chat_history_llama3:
            if isinstance(hist_message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(hist_message.content)
            elif isinstance(hist_message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(hist_message.content)
        
        if user_query is not None and user_query != "":
            st.session_state.chat_history_llama3.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                #ai_response=get_response_openai(user_query, st.session_state.chat_history)
                stream_generator=stream_response(user_query, st.session_state.chat_history_llama3, "llama3-70b")
                ai_response=st.write_stream(stream_generator)
                #st.markdown(ai_response)
            
            st.session_state.chat_history_llama3.append(AIMessage(ai_response))
    
with col5:
    if st.sidebar.checkbox(checkbox_options[1],True):
        st.subheader("Mistral: Mistral-8x7b")
        
        # Show all historical messages
        for hist_message in st.session_state.chat_history_mistral:
            if isinstance(hist_message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(hist_message.content)
            elif isinstance(hist_message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(hist_message.content)
        
        if user_query is not None and user_query != "":
            st.session_state.chat_history_mistral.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                #ai_response=get_response_openai(user_query, st.session_state.chat_history)
                stream_generator=stream_response(user_query, st.session_state.chat_history_mistral, "mistral-8x7b")
                ai_response=st.write_stream(stream_generator)
                #st.markdown(ai_response)
            
            st.session_state.chat_history_mistral.append(AIMessage(ai_response))

with col6:
    if st.sidebar.checkbox(checkbox_options[2],True):
        st.subheader("Google: Gemma-7b")
        
        # Show all historical messages
        for hist_message in st.session_state.chat_history_gemma:
            if isinstance(hist_message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(hist_message.content)
            elif isinstance(hist_message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(hist_message.content)
        
        
        if user_query is not None and user_query != "":
            st.session_state.chat_history_gemma.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                #ai_response=get_response_openai(user_query, st.session_state.chat_history)
                stream_generator=stream_response(user_query, st.session_state.chat_history_gemma, "gemma-7b")
                ai_response=st.write_stream(stream_generator)
                #st.markdown(ai_response)
            
            st.session_state.chat_history_gemma.append(AIMessage(ai_response))

history_dict={
             "Llama3-70b-instruct":st.session_state['chat_history_'+'llama3'],
             "Mistral-8x7b":st.session_state['chat_history_'+'mistral'],
             "Gemma-7b": st.session_state['chat_history_'+'gemma']
             }

st.sidebar.markdown('#') # as spacer

btn = st.sidebar.download_button(
            label="Export all chats",
            data=download_history(history_dict),
            file_name=f'All_history.md',
            mime="text/markdown",
            use_container_width=True,
        )