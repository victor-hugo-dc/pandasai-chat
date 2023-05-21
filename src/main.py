import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.llm.open_assistant import OpenAssistant
from pandasai.llm.starcoder import Starcoder
import os

response = None

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
    "OpenAI" : OpenAI,
    "Starcoder" : Starcoder,
    "Open-Assistant" : OpenAssistant
}

def make_request(question_input: str):
    if uploaded_file is not None:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
        dataframe = file_format[ext](uploaded_file)

    llm = models[option](api_token=api_key)
    pandas_ai = PandasAI(llm, 
                         conversational=True,
                         verbose=_verbose,
                         enforce_privacy=_enforce_privacy)
    return pandas_ai.run(
        data_frame = dataframe, 
        prompt = question_input,
        is_conversational_answer = True
    )


st.header("PandasAI Chat")

st.markdown("""---""")

question_input = st.text_input("Enter question")
rerun_button = st.button("Rerun")


left, right = st.columns([1, 2])
with left:
    option = st.selectbox(
    'Model',
    ('OpenAI', 'Starcoder', 'Open-Assistant'))

# Add components to the second column
with right:
    api_key = st.text_input('API Key', '')

uploaded_file = st.file_uploader("Upload a file", type=list(file_format.keys()))

with st.expander("Advanced Options"):
    _verbose = st.checkbox("Show Details About Python Code generated")
    _enforce_privacy = st.checkbox("Enforce Privacy About Personal Data", value=True)

st.markdown("""---""")

if question_input and uploaded_file and api_key:
    response = make_request(question_input)
else:
    pass

if rerun_button:
    response = make_request(question_input)
else:
    pass

if response:
    st.write("Response:")
    st.write(response)
else:
    pass

