import pandas as pd
import re

# reading of the DataFrame is not provided since stratascratch provides it already as the variable google_file_store

bull_occurences = (
    google_file_store['contents']
    .str.count(r'\bbull\b', flags=re.IGNORECASE)
    .sum()
)

bear_occurences = (
    google_file_store['contents']
    .str.count(r'\bbear\b', flags=re.IGNORECASE)
    .sum()
)

pd.DataFrame({
    'word': ['bull', 'bear'],
    'occurences': [bull_occurences, bear_occurences]
})
