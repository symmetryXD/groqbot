import streamlit as st
import os
from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os 

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']

def main():

    st.title("Groq Bots")

    st.sidebar.title('Select an LLM')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama-3.3-70b-versatile', 'mixtral-8x7b-32768', 'gemma2-9b-it']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

    memory=ConversationBufferWindowMemory(k=conversational_memory_length)

    user_question = st.text_area("Ask a question:")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})

    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )

    conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
    )

    if user_question:
        response = conversation(user_question)
        message = {'human':user_question,'AI':response['response']}
        st.session_state.chat_history.append(message)
        st.write("Chatbot:", response['response'])

if __name__ == "__main__":
    main()