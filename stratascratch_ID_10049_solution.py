import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the variable yelp_business

cat_rev = (
    yelp_business[['review_count', 'categories']]   # focus on relevant columns
    .set_index('review_count')                      # preserve the review_count column by making it an index
    .apply(lambda x: x.str.split(';').explode())    # separate each category on separate row (drags review_count val as index)
    .reset_index()                                  # make the review_count a normal column again
    .groupby('categories')['review_count']
    .sum()
    .reset_index(name='rev_count')
    .sort_values('rev_count', ascending=False)
)
