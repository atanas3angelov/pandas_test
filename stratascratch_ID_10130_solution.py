import pandas as pd

# reading of the DataFrame is not provided since stratascratch provides it already as the variable sf_restaurant_health_violations

# optional: focus only on relevant columns
violations = (
    sf_restaurant_health_violations[[
        'inspection_id', 
        'violation_id', 
        'inspection_type', 
        'risk_category']]
)

''' map risk_category to a rank number (+fill NaN vals with 0 for least severe)
    so that subsequent filtering leaves only 1 inspection per most severe violation
''' 
severity = {'High Risk': 3, 'Moderate Risk': 2, 'Low Risk': 1}
violations['severity_rank'] = (
    violations['risk_category'].map(severity).fillna(0)
)

''' add a column with the most severe violation rank 
    among groups with the same inspection id & type
'''
violations['most_severe'] = (
    violations.groupby(['inspection_id', 'inspection_type'])['severity_rank'].transform('max')
)

''' filter out less severe violations and
    leave only 1 violation per inspection
    (there can be several violations 'violation_id' with maximum severity 
    for the same inspection 'inspection_id')
'''
inspections = (
    violations[violations['severity_rank'] == violations['most_severe']]
    [['inspection_id', 'inspection_type', 'severity_rank']].drop_duplicates()
)

''' pivot into a table with inspection_type as its index
    and columns counting each sererity rank per inspection type
    (+fill NaN vals with 0)
'''
result = inspections.pivot_table(
    index='inspection_type',
    values='inspection_id',
    columns='severity_rank',
    aggfunc='count'
).fillna(0)

''' add a total column by summing all columns for each row 
    (total inspections of specific type)
'''
result['total_inspections'] = result.apply(
    lambda row: sum(row), 
    axis=1
)

''' rename the columns appropriately, 
    turn the index back into a column and 
    sort by total inspections in descending order
'''
result.rename(
    {
        0: 'no_risk_count', 
        1: 'low_risk_count', 
        2: 'moderate_risk_count', 
        3: 'high_risk_count'
    }, axis=1
).reset_index().sort_values('total_inspections', ascending=False)
