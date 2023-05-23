<h1 align="center">PandasAI Chat</h1>

PandasAI Chat is a web application built with Streamlit that allows users to have interactive conversations with their data using Language Models (LLMs). With the power of the [PandasAI](https://github.com/gventuri/pandas-ai) library, you can effortlessly explore and gain insights from your datasets by engaging in a natural language conversation.

## Features

- **Converse with your data**: PandasAI Chat enables you to interact with your data in a conversational manner. You can ask questions, request summaries, apply filters, and perform various data manipulations using plain English.

- **Seamless integration with PandasAI**: The application leverages the capabilities of the PandasAI library, which utilizes advanced Language Models to understand and process your data-related queries. You can tap into the power of LLMs without writing complex code.

- **Dynamic visualizations**: PandasAI Chat generates visual representations of your data on the fly. You can explore different chart types, such as bar plots, line graphs, scatter plots, and more, simply by expressing your visualization preferences through conversations.

- **Quick data exploration**: PandasAI Chat provides intuitive commands to quickly explore your datasets. You can inquire about column names, view a sample of your data, obtain descriptive statistics, or identify unique values in a column, all within the chat interface.

- **Data manipulation made easy**: Whether you want to filter your data based on specific criteria, sort it, group it, or perform calculations, PandasAI Chat simplifies these operations by accepting natural language instructions. You can effortlessly transform your data without writing complex Pandas code.

## Installation

To run PandasAI Chat locally, follow these steps:

1. Clone the repository: `git clone https://github.com/victor-hugo-dc/pandasai-ui.git`
1. Navigate to the project directory: `cd pandasai-ui`
1. Install the dependencies: `pip install -r requirements.txt`
1. Launch the application: `streamlit run src/main.py`

## Usage
Once you have the application up and running, follow these steps to start conversing with your data:

1. Input your API token: In the text box, write your API token for any of the accepted LLMs (OpenAI, Open Assistant, Starcoder and Google Palm).
1. Upload your dataset: Browse files and select the desired CSV or Excel (or any acceptable format) file from your local machine.
1. Explore your data: Begin the conversation by typing in the chat box. Ask questions about your data, request visualizations, or specify data manipulations using plain English.
1. Visualize your data: Ask for charts by providing the desired visualization type and the columns to include. PandasAI Chat will generate the requested chart dynamically.
1. Perform data manipulations: Instruct PandasAI Chat to filter, sort, group, or perform calculations on your data. The application will interpret your instructions and provide the desired results.