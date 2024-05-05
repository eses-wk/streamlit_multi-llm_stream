import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from utils import stream_response

load_dotenv()


# Main page
if "chat_history_openai" not in st.session_state:
    st.session_state.chat_history_openai = []
    
if "chat_history_claude" not in st.session_state:
    st.session_state.chat_history_claude = []
    
if "chat_history_gemini_pro" not in st.session_state:
    st.session_state.chat_history_gemini_pro = []

# app config
st.set_page_config(page_title="Multi-LLM Demo - 1", page_icon="🤖")
st.title("Multi-LLM Demo")
st.write("This is a demo of a Multi-LLM chatbot using Streamlit and Langchain. This page support ChatGPT-3.5-turbo, Claude-3-Sonnet, Gemini-Pro")

# Sidebar config
st.sidebar.header("Model Selected")
checkbox_options=['ChatGPT-3.5','Claude-3-Sonnet','Gemini-Pro']


# User Input
user_query = st.chat_input("Your message", key="user_input")


# If user input something, append to chat history
col1, col2 , col3 = st.columns(3)#(2,2,2)
with col1:
    if st.sidebar.checkbox(checkbox_options[0],True):
        st.subheader("OpenAI: GPT-3.5")
        # if st.sidebar.checkbox(checkbox_options[0]):
        #     st.write('Selected')
        
        # Show all historical messages
        for hist_message in st.session_state.chat_history_openai:
            if isinstance(hist_message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(hist_message.content)
            elif isinstance(hist_message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(hist_message.content)
            
        if user_query is not None and user_query != "":
            st.session_state.chat_history_openai.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                #ai_response=get_response_openai(user_query, st.session_state.chat_history)
                stream_generator=stream_response(user_query, st.session_state.chat_history_openai, "gpt-3.5")
                ai_response=st.write_stream(stream_generator)
                #st.markdown(ai_response)
                
            st.session_state.chat_history_openai.append(AIMessage(ai_response))
    
with col2:
    if st.sidebar.checkbox(checkbox_options[1],True):
        st.subheader("Anthropic: Claude-3-Sonnet")
        
        # Show all historical messages
        for hist_message in st.session_state.chat_history_claude:
            if isinstance(hist_message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(hist_message.content)
            elif isinstance(hist_message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(hist_message.content)
        
        
        if user_query is not None and user_query != "":
            st.session_state.chat_history_claude.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                #ai_response=get_response_openai(user_query, st.session_state.chat_history)
                stream_generator=stream_response(user_query, st.session_state.chat_history_claude, "claude-3-sonnet")
                ai_response=st.write_stream(stream_generator)
                #st.markdown(ai_response)
            
            st.session_state.chat_history_claude.append(AIMessage(ai_response))

with col3:
    if st.sidebar.checkbox(checkbox_options[2],True):
        st.subheader("Google: Gemini-Pro")
        
        # Show all historical messages
        for hist_message in st.session_state.chat_history_gemini_pro:
            if isinstance(hist_message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(hist_message.content)
            elif isinstance(hist_message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(hist_message.content)
        
        
        if user_query is not None and user_query != "":
            st.session_state.chat_history_gemini_pro.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                #ai_response=get_response_openai(user_query, st.session_state.chat_history)
                stream_generator=stream_response(user_query, st.session_state.chat_history_gemini_pro, "gemini_pro")
                ai_response=st.write_stream(stream_generator)
                #st.markdown(ai_response)
            
            st.session_state.chat_history_gemini_pro.append(AIMessage(ai_response))
            
