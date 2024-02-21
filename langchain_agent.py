import streamlit as st
from langchain.utilities import SQLDatabase
from langchain.llms.google_palm import GooglePalm
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from dotenv import dotenv_values

st.set_page_config(
    page_title="Langcahin",
    page_icon="🦜",
)

st.title("Langcahin 🦜 streamlit interface")

ENV = dotenv_values(".env")
db = SQLDatabase.from_uri("sqlite:///data/dummy.sqlite")
llm = GooglePalm(
    google_api_key=ENV['GOOGLE_PALM_API'],
)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

with st.form("Question"):
    question = st.text_input("Question", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.chat_message("assistant"):
            response = agent_executor.run(question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
    else:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]