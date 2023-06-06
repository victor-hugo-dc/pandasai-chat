import os
import streamlit as st
from streamlit_chat import message

from pandasai import PandasAI
from constants import file_format, models
import matplotlib.pyplot as plt

@st.cache_data
def load_data(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    if ext in file_format:
        return file_format[ext](uploaded_file)

def generate_response(question_input, dataframes, option, api_key):
    llm = models[option](api_key)
    pandas_ai = PandasAI(llm)
    if len(dataframes) == 1:
        return pandas_ai(dataframes[0], prompt = question_input, is_conversational_answer = True) 
    else:
        return pandas_ai(dataframes, prompt = question_input, is_conversational_answer = True)    

st.set_page_config(page_title="PandasAI Chat", page_icon=":panda_face:")
st.title("PandasAI Chat :panda_face:")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

if "plots" not in st.session_state:
    st.session_state["plots"] = []

left, right = st.columns([1, 2])
with left:
    model_option = st.selectbox('Model', models.keys())

with right:
    api_key = st.text_input('API Key', '', type = 'password')
    if not api_key:
        st.info(f"Please input API Token for {model_option}.")

question_input = None
uploaded_files = st.file_uploader("Upload a file", type=list(file_format.keys()), accept_multiple_files=True)
dataframes = []

if not uploaded_files:
    st.info("Please upload your dataset(s) to begin asking questions!")

else:
    for uploaded_file in uploaded_files:
        dataframe = load_data(uploaded_file)
        dataframes.append(dataframe)

        with st.expander(uploaded_file.name):
            st.write(dataframe.head())

    question_input = st.text_input("Enter question")

st.markdown("---")

response = None
if question_input and uploaded_files and api_key:
    with st.spinner("Generating..."):
        try:
            response = generate_response(question_input, dataframes, model_option, api_key)

        except Exception as e:
            st.error("An error occurred: either your API token is invalid \
                     or no code was found in the response generated.")

        if len(plt.get_fignums()) > 0:
            fig = plt.gcf()
            st.session_state.plots.append(fig)
        else:
            st.session_state.plots.append("None")

        if response:
            st.session_state.past.append(question_input)
            st.session_state.generated.append(response)

if "generated" in st.session_state and st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        if st.session_state["plots"][i] != "None":
            st.pyplot(st.session_state["plots"][i])

        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    