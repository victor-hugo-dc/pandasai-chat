import streamlit as st
import pandas as pd
import sqlite3
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.llm.open_assistant import OpenAssistant
from pandasai.llm.starcoder import Starcoder
import os

file_format = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
    "json": pd.read_json,
    "html": pd.read_html,
    "sql": pd.read_sql,
    "feather": pd.read_feather,
    "parquet": pd.read_parquet,
    "dta": pd.read_stata,
    "sas7bdat": pd.read_sas,
    "h5": pd.read_hdf,
    "hdf5": pd.read_hdf,
    "pkl": pd.read_pickle,
    "pickle": pd.read_pickle,
    "gbq": pd.read_gbq,
    "orc": pd.read_orc,
    "xpt": pd.read_sas,
    "sav": pd.read_spss,
    "gz": pd.read_csv,
    "zip": pd.read_csv,
    "bz2": pd.read_csv,
    "xz": pd.read_csv,
    "txt": pd.read_csv,
    "xml": pd.read_xml,
}

models = {
    "OpenAI": OpenAI,
    "Starcoder": Starcoder,
    "Open-Assistant": OpenAssistant
}

def create_chat_table():
    conn = sqlite3.connect("chats.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, response TEXT, chat_id INTEGER)")
    conn.commit()
    conn.close()

def save_chat(question, response, chat_id):
    conn = sqlite3.connect("chats.db")
    c = conn.cursor()
    c.execute("INSERT INTO chats (question, response, chat_id) VALUES (?, ?, ?)", (question, response, chat_id))
    conn.commit()
    conn.close()

def get_chats(chat_id):
    conn = sqlite3.connect("chats.db")
    c = conn.cursor()
    if chat_id:
        c.execute("SELECT * FROM chats WHERE chat_id=?", (chat_id,))
    else:
        c.execute("SELECT * FROM chats")
    chats = c.fetchall()
    conn.close()
    return chats

@st.cache_data
def load_data(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    if ext in file_format:
        return file_format[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None

def make_request(question_input, dataframe, option, api_key):
    llm = models[option](api_token=api_key)
    pandas_ai = PandasAI(llm, conversational=False)
    return pandas_ai.run(dataframe, prompt=question_input, is_conversational_answer=True)

# Create the chat table if it doesn't exist
create_chat_table()

st.set_page_config(page_title="PandasAI Chat", page_icon=":panda_face:")

st.sidebar.title("Chat History")
chat_ids = sorted(set([chat[3] for chat in get_chats(None)]))
if len(chat_ids) == 0:
    st.sidebar.warning("No chats selected.")
else:
    selected_chat_ids = st.sidebar.multiselect("Select chat(s)", chat_ids)
    # for chat_id in selected_chat_ids:
    #     st.sidebar.markdown(f"**Chat {chat_id}**")
    #     for chat in get_chats(chat_id):
    #         st.sidebar.write(f"- **Q:** {chat[1]}")
    #         st.sidebar.write(f"  **A:** {chat[2]}")

st.sidebar.title("New Chat")
question_input = st.sidebar.text_input("Enter question")
rerun_button = st.sidebar.button("Rerun")

left, right = st.columns([1, 2])
with left:
    model_option = st.selectbox('Model', ('OpenAI', 'Starcoder', 'Open-Assistant'))

with right:
    api_key = st.text_input('API Key', '')

uploaded_file = st.file_uploader("Upload a file", type=list(file_format.keys()))

st.title("PandasAI Chat")
st.markdown("---")

if question_input and uploaded_file and api_key:
    chat_ids = set([chat[3] for chat in get_chats(None)])
    if len(chat_ids) == 0:
        chat_id = 1
    else:
        chat_id = max(chat_ids) + 1
    dataframe = load_data(uploaded_file)
    response = make_request(question_input, dataframe, model_option, api_key)
    save_chat(question_input, response, chat_id) # Save the chat to the database
else:
    response = None

if rerun_button:
    response = make_request(question_input, dataframe, model_option, api_key)
    save_chat(question_input, response, chat_id) # Save the chat to the database

if response:
    st.write("Response:")
    st.write(response)

st.markdown("---")
st.subheader("Chat History")

if len(chat_ids) == 0:
    st.warning("No chats selected.")
else:
    for chat_id in selected_chat_ids:
        st.write("")
        st.write(f"**Chat {chat_id}**")
        for chat in get_chats(chat_id):
            st.write("**Q:**", chat[1])
            st.write("**A:**", chat[2])
            st.write("--")