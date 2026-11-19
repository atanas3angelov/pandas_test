import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the var sf_events

# get user activity per date
user_date_activity = (
    sf_events[['record_date', 'user_id']]
    .drop_duplicates()
    .sort_values(['user_id', 'record_date'])
)

''' using the trick for finding consequtiveness
    (subtract the auto-increasing num by 1 from date, that forms groups of same date
    -> use cummulative counting, then filter)
'''
# get an auto-incrementing num (optional: restart for each user)
user_date_activity['rnk'] = (
    user_date_activity.groupby('user_id')['record_date']
    .rank(method='first')
)

# form groups by subtracting
user_date_activity['group'] = (
    user_date_activity['record_date'] 
    - pd.to_timedelta(user_date_activity['rnk'], unit='D')
)

# cumulatively count group size to form streaks
user_date_activity['streak'] = (
    user_date_activity.groupby(['user_id','group']).cumcount() + 1
)

# filter above certain streak
(
    user_date_activity[user_date_activity['streak'] >= 3][['user_id']]
    .drop_duplicates()
)
