"""
Main Module for Fake Data Generator.
"""
import random
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
from tqdm import tqdm

random.seed(42)
Faker.seed(123)

class FakeData:
    def __init__(self, iter=100) -> None:
        """
        init function
        parameters
        ----------
        iter: iterations
        """
        self.fake = Faker()
        self.iter = iter
        self.ids = [random.randint(1, 1_000) for _ in range(iter)]
        self.rate_plan_ids = [random.randint(1, 16) for _ in range(iter)]
        self.gov = ['Cairo', 'Alex', 'Qena', 'Aswan', 'Hurgada', 'Asyut', 'Giza']
        self.qism = ['xyz', 'zxy', 'yxz', 'ooo', 'uuu', 'puy']
        self.region = ['south', 'med', 'north', 'east', 'west', 'sinai']
        self.nw_activity_cd = [random.randint(1, 3) for _ in range(iter)]

    def generate_revenue_data(self) -> pd.DataFrame:
        """
        create Fake data for revenue table
        """
        data = {
            'Subscription_Id':[],
            'Revenue_Date':[],
            'Total_Revenue':[],
            'Recharges':[],
            'Baki_Revenue':[],
            'Nota_Revenue':[],
            'Connect_Revenue':[],
            'Admin_Fees':[],
            'Tesla_Revenue':[],
            'Balance_Transfer_Fees':[],
        }
        for _ in tqdm(range(self.iter), desc="Revenue Data"):
            data['Subscription_Id'].append(random.choice(self.ids))
            data['Revenue_Date'].append(self.fake.date_between(start_date='-3000d', end_date='-1d'))
            data['Total_Revenue'].append(self.fake.random_number(digits=2, fix_len=4))
            data['Recharges'].append(self.fake.random_int(1, 60))
            data['Baki_Revenue'].append(self.fake.random_number(digits=2, fix_len=2))
            data['Nota_Revenue'].append(self.fake.random_number(digits=2, fix_len=2))
            data['Connect_Revenue'].append(self.fake.random_number(digits=2, fix_len=2))
            data['Admin_Fees'].append(self.fake.random_number(digits=2, fix_len=2))
            data['Tesla_Revenue'].append(self.fake.random_number(digits=2, fix_len=2))
            data['Balance_Transfer_Fees'].append(self.fake.random_number(digits=2, fix_len=2))
        df = pd.DataFrame(data)
        return df
    
    def generate_info_data(self) -> pd.DataFrame:
        """
        create Fake data for info table
        """
        data = {
            'Subscription_Id':[],
            'Running_Date':[],
            'Rate_Plan_Product_Id':[],
            'Call_Gap_Days':[],
            'Most_Used_Governorate':[],
            'Most_Used_Qism':[],
            'Most_Used_Region':[],
            'Duality_Flag':[],
        }
        for _ in tqdm(range(self.iter), desc="Info Data"):
            data['Subscription_Id'].append(random.choice(self.ids))
            data['Running_Date'].append(self.fake.date_between(start_date='-3000d', end_date='-1d'))
            data['Rate_Plan_Product_Id'].append(random.choice(self.rate_plan_ids))
            data['Call_Gap_Days'].append(self.fake.random_int(1, 60))
            data['Most_Used_Governorate'].append(random.choice(self.gov))
            data['Most_Used_Qism'].append(random.choice(self.qism))
            data['Most_Used_Region'].append(random.choice(self.region))
            data['Duality_Flag'].append(random.choice(['N', 'Y']))
        df = pd.DataFrame(data)
        return df
    
    def generate_activity_data(self) -> pd.DataFrame:
        """
        create Fake data for network activity table
        """
        data = {
            'Subscription_Id':[],
            'Rate_Plan_Product_Id':[],
            'Network_Activity_Type_Code':[],
            'Duration':[],
            'Data_Volumne':[],
            'Running_Date':[],
        }
        for _ in tqdm(range(self.iter), desc="Network Activity Data"):
            data['Subscription_Id'].append(random.choice(self.ids))
            data['Rate_Plan_Product_Id'].append(random.choice(self.rate_plan_ids))
            data['Network_Activity_Type_Code'].append(random.choice(self.nw_activity_cd))
            data['Duration'].append(self.fake.random_number(digits=2, fix_len=3))
            data['Data_Volumne'].append(self.fake.random_number(digits=2, fix_len=5))
            data['Running_Date'].append(self.fake.date_between(start_date='-3000d', end_date='-1d'))
        df = pd.DataFrame(data)
        return df
    
    def import_data(self, df: pd.DataFrame, table: str) -> None:
        engine = create_engine("sqlite:///data/dummy.sqlite")
        df.to_sql(
                name=table, 
                con=engine, 
                if_exists='append', 
                index=False
            )
    
