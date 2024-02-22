import streamlit as st
import pandas as pd
from src.pandasai_agent.read_schema import ReadSchema
from pandasai.llm import GoogleGemini, OpenAI, GooglePalm
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

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

with st.form("Please Ask Your Question"):
    question = st.text_input("Please Ask Your Question", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.chat_message("assistant"):
            response = sdl.chat(question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)






