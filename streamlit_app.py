import streamlit as st
import os

# App title
st.set_page_config(page_title="🍑💬 Taobao Products lists Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🍑💬 Taobao Products lists Chatbot')
    st.write('This chatbot is created for search the taobao products lists from taobao mall.')

    st.subheader('Models and parameters')
    input_pageStart = st.sidebar.slider('起始页', min_value=1.0, max_value=100.0, value=1.0, step=1.0)
    input_pageEnd = st.sidebar.slider('终止页', min_value=1.0, max_value=100.0, value=100.0, step=1.0)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.csdn.net/qq_46315152/article/details/140696405)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    output = '(_From_Taobao).xlsx'
    return output

# User-provided prompt
if prompt := st.chat_input("Please enter your message here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
