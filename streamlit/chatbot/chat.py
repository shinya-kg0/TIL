import streamlit as st
from chat_ruby import Rubify
from chat_eliza import Doctor
from chat_translation import Translator

def on_select():
    del st.session_state["transactions"]
    
if "ルビ振り" not in st.session_state:
    st.session_state["ルビ振り"] = Rubify()
    
if "セラピー" not in st.session_state:
    st.session_state["セラピー"] = Doctor()
    
if "日英通訳" not in st.session_state:
    st.session_state["日英通訳"] = Translator()
    
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []
    

options = ['ルビ振り', 'セラピー', '日英通訳']

with st.sidebar:
    st.header("チャットサービス")
    selected = st.selectbox(
        label="サービスを選んでください",
        options=options,
        index=0,
        on_change=on_select
    )
    
chat = st.session_state[selected]
st.html(f"> {chat.initial()}")

text = st.chat_input()

if text:
    response = chat.respond(text)
    st.session_state.transactions.append(text)
    st.session_state.transactions.append(f"> {response}")
    
for show in st.session_state["transactions"]:
    st.html(show)