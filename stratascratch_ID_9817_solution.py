import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the variable google_file_store

word_counts = (
    google_file_store['contents']
    .str.lower()
    .str.replace(r'[^\w\s]+', '', regex=True)   # remove punctuation
    .str.split(r'\s')
    .explode()
    .reset_index(name='word')
    .groupby('word')['index']
    .count()
    .reset_index(name='occurrences')
    .sort_values('occurrences', ascending=False)
)
