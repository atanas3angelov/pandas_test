import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the variable amazon_transactions

amazon_transactions['created_at'] = (
    pd.to_datetime(amazon_transactions['created_at'])
)

# keep only 1 transaction per day for each user
df = amazon_transactions.drop_duplicates(subset=['user_id', 'created_at'])

# sort before cummulative funcs
df = df.sort_values(['user_id', 'created_at'])

# the min date is the date of first purchase
df['first_purchase_date'] = (
    df.groupby('user_id')['created_at']
    .cummin()
)

# keep only transactions within 7 days of first one
df = df[
    (df['created_at'] > df['first_purchase_date']) & 
    (df['created_at'] <= df['first_purchase_date'] + pd.Timedelta(days=7))
]

# keep just 1 user id
df['user_id'].drop_duplicates().to_frame()

