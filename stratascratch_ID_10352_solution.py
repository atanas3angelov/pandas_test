import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the variable facebook_web_log

facebook_web_log['timestamp'] = pd.to_datetime(facebook_web_log['timestamp'])

# create a date col to filter multiple starts/ends of the day session
facebook_web_log['year-month-day'] = facebook_web_log['timestamp'].dt.floor('D')

''' separate day sessions starts
    group them by user & date
    pick the latest start for each
'''
starts = (
    facebook_web_log[facebook_web_log['action'] == 'page_load']
    .groupby(['user_id', 'year-month-day'])['timestamp']
    .max()
    .to_frame('page_load')
)

''' separate day sessions ends
    group them by user & date
    pick the earliest start for each
'''
ends = (
    facebook_web_log[facebook_web_log['action'] == 'page_exit']
    .groupby(['user_id', 'year-month-day'])['timestamp']
    .min()
    .to_frame('page_exit')
)

''' merge the starts and ends for day sessions
    (silently removes ones without corresponding start/end)
'''
matches = (
    starts.merge(ends, on=['user_id', 'year-month-day'])
    .reset_index()
)

''' filter day sessions where the end is before its start
    (there were no such day sessions based on the data but it's still a necessary logical step)
'''
matches = matches[matches['page_exit'] > matches['page_load']]

# calc duration for individual days
matches['session_time'] = matches['page_exit'] - matches['page_load']

# calc average session duration for each user
result = (
    matches.groupby('user_id')['session_time']
    .mean()
    .reset_index()
    .rename({'session_time': 'avg_session_time'}, axis=1)
)
