from pandasai import SmartDatalake
from pandasai.responses.streamlit_response import StreamlitResponse
from sqlalchemy import create_engine
from typing import Optional, List
import pandas as pd

class ReadSchema:
    def __init__(
            self, 
            skip_tables: Optional[List[str]] = None
    ) -> None:
        self.skip_tables = skip_tables
        self.engine = create_engine('sqlite:///data/dummy.sqlite')
    
    def get_all_tables(self) -> List[str]:
        with self.engine.connect() as conn:
            schema_df = pd.read_sql_table(
                'sqlite_master', 
                con=conn
            )
        all_tables = schema_df['name'].tolist()
        if self.skip_tables:
            all_tables = set(all_tables).difference(self.skip_tables)
        return all_tables
    
    def get_ddls(self) -> str:
        schema='\n'
        with self.engine.connect() as conn:
            schema_df = pd.read_sql_table(
                'sqlite_master', 
                con=conn
            )
        all_tables = schema_df['sql'].tolist()
        schema.join(all_tables)
        return schema
    
    def create_smart_datalake(
            self, 
            llm,
            dfs: List[pd.DataFrame],
            private_data: bool=False,
            verbose: bool=False,
            streamlit_response: bool=False
    ) -> List[pd.DataFrame]:
        if streamlit_response:
            config={
                'llm':llm,
                'enforce_privacy': private_data,
                'verbose': verbose,
                "response_parser": StreamlitResponse,
            }
        else:
            config={
                'llm':llm,
                'enforce_privacy': private_data,
                'verbose': verbose,
            }
        sdl = SmartDatalake(
            dfs,
            config=config
        )
        return sdl
