import os
import streamlit as st
from streamlit_chat import message

import pandas as pd
from pandasai import PandasAI
from constants import file_format, models

@st.cache_data
def load_data(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    if ext in file_format:
        return file_format[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None

def generate_response(question_input, dataframe, option, api_key):
    llm = models[option](api_key)
    pandas_ai = PandasAI(llm, conversational=False)
    return pandas_ai.run(dataframe, prompt=question_input, is_conversational_answer=True)

st.set_page_config(page_title="PandasAI Chat", page_icon=":panda_face:")
st.title("PandasAI Chat")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

question_input = st.text_input("Enter question")

left, right = st.columns([1, 2])
with left:
    model_option = st.selectbox('Model', models.keys())

with right:
    api_key = st.text_input('API Key', '')

uploaded_file = st.file_uploader("Upload a file", type=list(file_format.keys()))

st.markdown("---")

if question_input and uploaded_file and api_key:
    dataframe = load_data(uploaded_file)
    response = generate_response(question_input, dataframe, model_option, api_key)
    st.session_state.past.append(question_input)
    st.session_state.generated.append(response)
else:
    response = None

if "generated" in st.session_state and st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    