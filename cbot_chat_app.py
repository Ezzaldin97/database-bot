import streamlit as st
import pandas as pd
from src.pandasai_agent.read_schema import ReadSchema
from pandasai.llm import GooglePalm
from dotenv import dotenv_values
from typing import List
from sqlalchemy import create_engine
import os

st.set_page_config(
    page_title="C-Bot",
    page_icon=os.path.join('imgs', 'logo-new.svg'),
)
ENV = dotenv_values(".env")

st.image(os.path.join('imgs', 'logo-new.svg'), caption='Artifical Intelligence')
st.title("Etisalat C-Bot")

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
            df = pd.read_sql_table(tbl, con=conn)
            for col in df.columns:
                if 'Date' in col:
                    df[col] = pd.to_datetime(df[col])
            dfs.append(
                df
            )
    return dfs
dfs=get_data(tables)
sdl = schema_reader.create_smart_datalake(
    llm=llm, dfs=dfs, streamlit_response=True, private_data=False
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if not isinstance(message["content"], pd.DataFrame):
            st.markdown(message["content"])
        else:
            st.write(message["content"])

# Accept user input
if prompt := st.chat_input("Please Ask Your Question"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = sdl.chat(prompt)
        if not isinstance(response, pd.DataFrame):
            st.markdown(response)
        else:
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})