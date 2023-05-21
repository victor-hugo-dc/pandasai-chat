import os
import streamlit as st
from streamlit_chat import message

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.llm.open_assistant import OpenAssistant
from pandasai.llm.starcoder import Starcoder


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

@st.cache_data
def load_data(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    if ext in file_format:
        return file_format[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None

def generate_response(question_input, dataframe, option, api_key):
    llm = models[option](api_token=api_key)
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
    model_option = st.selectbox('Model', ('OpenAI', 'Starcoder', 'Open-Assistant'))

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
    