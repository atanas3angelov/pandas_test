import pandas as pd

# reading of DFs - not provided since stratascratch provides them already as the vars fb_comments_count & fb_active_users

# filter to comments between Dec 2019 & Jan 2020
df = fb_comments_count[
    (fb_comments_count['created_at'] >= '2019-12-01') & 
    (fb_comments_count['created_at'] < '2020-02-01')
]

# merge the 2 DFs
merged = df.merge(fb_active_users, on='user_id')

# truncate date to month (or just take the computed month with dt)
merged['month'] = merged['created_at'].dt.month

# groupby month & country to calc total comments (sum)
# also sort the result so ranking & shifting won't need 2 separate sorts
result = (
    merged.groupby(['month', 'country'])['number_of_comments']
    .sum()
    .reset_index(name='total_comments')
    .sort_values(['month', 'total_comments'], ascending=[False, False])
)

# rank countries' total comments by month
result['rnk'] = (
    result.groupby('month')['total_comments']
    .rank(method='dense', ascending=False)
)

# find prev rank for countries with groupby country & shift of rank
result['prev_rnk'] = (
    result.groupby('country')['rnk'].shift(1)
)

# filter to countries that increased their rank (old rank > new rank)
result[result['prev_rnk'] > result['rnk']][['country']]
