from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_ibm import WatsonxLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import streamlit as st


from langchain_core.output_parsers import StrOutputParser

import os
import io

# https://www.ibm.com/docs/en/watsonx/saas?topic=solutions-supported-foundation-models#third-party-provided



def get_response_openai(user_query, chat_history):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    
    response=chain.invoke({
        "chat_history": chat_history,
        "user_question": user_query,
    })
    
    return response

def stream_response(user_query, chat_history, model_name):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}

    Output format: 
    - Keep response concise, in 50 words.
    - Output in string format.
    """
    #Keep response short, in 20 words.
    prompt = ChatPromptTemplate.from_template(template)
    if model_name == "gpt-3.5":
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    elif model_name == 'claude-3-sonnet':
        llm = ChatAnthropic(model_name="claude-3-sonnet-20240229")
    elif model_name == 'gemini_pro':
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        
    elif model_name == 'llama3-70b':    
        llm = ChatGroq(temperature=0.1, 
                       model_name="llama3-70b-8192")
    elif model_name == 'mistral-8x7b':
        llm = ChatGroq(temperature=0.1,
                       model_name="mixtral-8x7b-32768")
    elif model_name == 'gemma-7b':    
        llm = ChatGroq(temperature=0.1, 
                       model_name="gemma-7b-it")
        
    elif model_name == 'mistral-7b':
        llm = ChatMistralAI(model_name="open-mistral-7b9")
    elif model_name == 'llama3-8b':
         llm = ChatGroq(temperature=0.1,
                        model_name="llama3-8b-8192")
    else:
        raise ValueError(f"Model {model_name} not supported.")
    
        
        
    # elif model_name == 'llama2-13b':
    #     llm = get_watsonx_model('meta-llama/llama-2-13b-chat')    
    # elif model_name == 'llama2-70b':
    #     llm = get_watsonx_model('meta-llama/llama-2-70b-chat')   
    # elif model_name == 'llama3-8b':
    #     llm = get_watsonx_model('meta-llama/llama-3-8b-instruct')
    # #elif model_name == 'llama3-70b':
    # #    llm = get_watsonx_model('meta-llama/llama-3-70b-instruct')
    
    
    chain = prompt | llm | StrOutputParser()
    
    # Stream response
    response_generator=chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })
    
    return response_generator

def get_watsonx_model(model_name):
    watsonx_llm = WatsonxLLM(
    model_id=model_name,
    url="https://us-south.ml.cloud.ibm.com",
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params={"decoding_method": "sample","max_new_tokens": 200,
    "min_new_tokens": 1,"temperature": 0.1,
    "top_k": 50,"top_p": 1,},
    streaming=True,
    )
    return watsonx_llm


@st.cache_data(max_entries=20, show_spinner=False)
def download_history(history: list):
    md_text = ""
    for msg in history:
        if msg['role'] == 'user':
            md_text += f'## HumanMessage：\n{msg["content"]}\n'
        elif msg['role'] == 'assistant':
            md_text += f'## AIMessage：\n{msg["content"]}\n'
    output = io.BytesIO()
    output.write(md_text.encode('utf-8'))
    output.seek(0)
    return output