import streamlit as st
import pandas as pd
from src.pandasai_agent.read_schema import ReadSchema
from pandasai.llm import GoogleGemini, OpenAI, GooglePalm
from dotenv import dotenv_values
from typing import List
from sqlalchemy import create_engine

st.set_page_config(
    page_title="PandasAI",
    page_icon="🐼",
)
ENV = dotenv_values(".env")

st.title("pandas-ai 🐼 streamlit interface")

llm = GooglePalm(
    api_key=ENV['GOOGLE_PALM_API'],
    temperature=0
)

schema_reader = ReadSchema()
tables = schema_reader.get_all_tables()

@st.cache_data(ttl="2h")
def get_data(tables: List[str]) -> List[pd.DataFrame]:
    dfs = []
    engine = create_engine('sqlite:///data/dummy.sqlite')
    with engine.connect() as conn:
        for tbl in tables:
            dfs.append(
                pd.read_sql_table(tbl, con=conn)
            )
    return dfs
dfs=get_data(tables)
sdl = schema_reader.create_smart_datalake(
    llm=llm, dfs=dfs, streamlit_response=True, private_data=False
)

with st.form("Question"):
    question = st.text_input("Question", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.chat_message("assistant"):
            #sdl.clear_memory()
            response = sdl.chat(question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
    else:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]






