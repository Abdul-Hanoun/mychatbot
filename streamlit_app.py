import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import pickle
import os

# App title
st.set_page_config(page_title="🤗💬 HugChat")

# Sidebar instructions
with st.sidebar:
    st.title('Chat Bot')
    st.success('Proceed to entering your prompt message!', icon='👉')

# Funktion zum Laden oder Erstellen von Cookies
def get_cookies():
    if os.path.exists("cookies.pkl"):
        # Cookies aus der Datei laden
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
    else:
        # Einmaliger Login, um Cookies zu erstellen und zu speichern
        email = st.text_input("Email", type="default")
        passwd = st.text_input("Password", type="password")
        if email and passwd:
            sign = Login(email, passwd)
            cookies = sign.login().get_dict()
            with open("cookies.pkl", "wb") as f:
                pickle.dump(cookies, f)
        else:
            cookies = None
    return cookies

# Laden der Cookies
cookies = get_cookies()

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Funktion zur Erzeugung der Antwort des LLM
def generate_response(prompt_input, cookies):
    # ChatBot mit gespeicherten Cookies erstellen
    chatbot = hugchat.ChatBot(cookies=cookies)
    return chatbot.chat(prompt_input)

# Benutzer-Eingabe
if cookies:
    if prompt := st.chat_input("Enter your message:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generiere eine neue Antwort, wenn die letzte Nachricht nicht vom Assistenten ist
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, cookies)
                    st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
else:
    st.warning("Please enter your Hugging Face credentials in the sidebar.")


