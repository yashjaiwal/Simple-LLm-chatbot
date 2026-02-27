import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os

## page config

st.set_page_config(
    page_title="Simple Langchain Chatbot",page_icon="💥"
)
    
#title
st.title("💥 Simple Langchain Chat with Groq")
st.markdown("Learn Langchain Basic with Groq")

with st.sidebar:
    st.header("settings")

    #api key 

    api_key = st.text_input("Groq_api_key",type = "password",help="Get_Free_api key at console.groq.com")

    ## model selection
    model_name = st.selectbox(
        "Model",
        ["llama-3.1-8b-instant","openai/gpt-oss-120b"],
        index=0
    )
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

### initialize LLm
@st.cache_resource
def get_chain(api_key,model_names):
    if not api_key:
        return None
    
    #initialize the Groq model
    llm = ChatGroq(groq_api_key = api_key,
             model_name = model_names,
             temperature=0.7,
             streaming=True)
    
    prompt = ChatPromptTemplate([
        ("system","You are ahelpful assistent powered by Groq . Answer questions clearly and concisely"),
        ("user","{question}")
    ])
    chain = prompt | llm | StrOutputParser()

    return chain

chain = get_chain(api_key,model_names=model_name)

if not chain:
    st.warning("Please enter the Groq Api key in the sidebar to start chatting")
    st.warning("[get free api key here](https://console.groq.com/)")

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    ## chat inpurt
    if question:= st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # stream response
                for chunk in chain.stream({"question":question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "|")
                message_placeholder.markdown(full_response)
            
                #add to history

                st.session_state.messages.append({"role":"assistant","content":full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")





