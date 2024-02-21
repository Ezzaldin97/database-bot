import streamlit as st
import pandas as pd
from src.pandasai_agent.read_schema import ReadSchema
from sqlalchemy import create_engine

st.set_page_config(
    page_title="SQLCoder",
    page_icon="🤖",
)
#ENV = dotenv_values(".env")

st.title("sqlcoder 🤖 streamlit interface")

schema_reader = ReadSchema()
tables = schema_reader.get_all_tables()
schema = schema_reader.get_ddls()
engine = create_engine('sqlite:///data/dummy.sqlite')

with st.form("Query"):
    query = st.text_input("Query", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.chat_message("assistant"):
            with engine.connect() as conn:
                 response = pd.read_sql_query(query, con=conn)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
    else:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]