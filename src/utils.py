from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

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
    Keep response short, in 50 words.
    """
    #Keep response short, in 20 words.
    prompt = ChatPromptTemplate.from_template(template)
    if model_name == "gpt-3.5":
        llm = ChatOpenAI()
    elif model_name == 'claude-3-sonnet':
        llm = ChatAnthropic(model_name="claude-3-sonnet-20240229")
    chain = prompt | llm | StrOutputParser()
    
    # Stream response
    response_generator=chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })
    
    return response_generator
