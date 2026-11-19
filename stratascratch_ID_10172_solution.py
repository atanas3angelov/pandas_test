import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the var online_retail

# truncate to month (or just get it with dt)
online_retail['month'] = online_retail['invoicedate'].dt.month

# calculate invoice bill (price for all units)
online_retail['price'] = online_retail['unitprice'] * online_retail['quantity']

# ignore returns and cancelations
online_retail = online_retail[online_retail['price'] > 0]

# calculate total sales grouped by month and item (its description)
# also sort rows by total sales descending for the next step - ranking
best_selling_items = (
    online_retail.groupby(['month', 'description'])['price']
    .sum()
    .reset_index(name='total_sales')
    .sort_values('total_sales', ascending=False)
)

# calculate ranks for each month (there might be several items ranking 1st for a month)
best_selling_items['rnk'] = (
    best_selling_items.groupby('month')['total_sales']
    .rank(method='min', ascending=False)
)

# filter to items that ranked 1st for each month and present the result appropriately
(
    best_selling_items[best_selling_items['rnk'] == 1]
    .drop(columns='rnk')
    .sort_values('month')
)
