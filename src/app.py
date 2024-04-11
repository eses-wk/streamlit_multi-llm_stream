import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage


from utils import stream_response, get_response_openai

load_dotenv()

if "chat_history_openai" not in st.session_state:
    st.session_state.chat_history_openai = []
    
if "chat_history_claude" not in st.session_state:
    st.session_state.chat_history_claude = []

# app config
st.set_page_config(page_title="Multi-LLM Demo", page_icon="🤖")
st.title("Multi-LLM Demo")

user_query = st.chat_input("Your message", key="user_input")



# If user input something, append to chat history
col1, col2 = st.columns((2,2))
with col1:
    st.subheader("OpenAI - GPT-3.5")
    
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
    st.subheader("Anthropic - Claude-3-Sonnet")
    
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
