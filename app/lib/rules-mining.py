import pandas as pd
import pickle
from datetime import datetime, date, timedelta
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Import datasets
deck_df = pd.read_csv("./app/static/data/public/standard_deck_data.csv", index_col=False)
card_df = pd.read_csv("./app/static/data/public/standard_card_data.csv", index_col=False)

# Handle Data Oddities
deck_df['clean_name'] = deck_df['card'].apply(lambda x: x.split('/')[0].strip())
card_df['clean_name'] = card_df['name'].apply(lambda x: x.split('(')[0].strip())

# Merge Datasets
combined_df = deck_df.merge(card_df, how='left', on='clean_name')

# Filter and Transform dataset
filtered_df = combined_df[~combined_df['type'].str.contains('Land')]
filtered_df = filtered_df[filtered_df['set'] == 'GRN']
rules_df = filtered_df.groupby(['url', 'clean_name']).url.nunique().unstack('clean_name').fillna(0)
rules_df.drop([col for col, val in rules_df.sum().iteritems() if val <= 5], axis=1, inplace=True)

# Create sparse df to save memory
sparse_df = pd.SparseDataFrame(rules_df, columns=rules_df.columns, default_fill_value=False)

# Rules Mining
print("Running apriori model...")
frequent_itemsets = apriori(sparse_df, min_support=0.01, use_colnames=True, max_len=3)

# Save model results
print("Saving model...")
filename = 'app/static/models/standard_rules.sav'
pickle.dump(frequent_itemsets, open(filename, 'wb'))

# Filter results
print("Generating rule sets...")
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules.sort_values('lift', ascending=False).to_csv('./app/static/data/public/standard_rules.csv', index=False)

print("Done!")
