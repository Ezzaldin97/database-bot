from src.generate_data.fake_data import FakeData

if __name__ == "__main__":
    generator = FakeData(iter = 10_000)
    df1 = generator.generate_info_data()
    df2 = generator.generate_revenue_data()
    df3 = generator.generate_activity_data()
    generator.import_data(df1, 'info_model')
    generator.import_data(df2, 'agg_revenue_subs_daily')
    generator.import_data(df3, 'agg_network_activity_daily')
