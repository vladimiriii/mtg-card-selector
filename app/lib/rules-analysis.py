import pandas as pd
import pickle
from mlxtend.frequent_patterns import association_rules

# Load model
filename = 'app/static/models/standard_rules.sav'
frequent_itemsets = pickle.load(open(filename, 'rb'))
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Filter results
rules["a_len"] = rules["antecedents"].apply(lambda x: len(x))
rules["c_len"] = rules["consequents"].apply(lambda x: len(x))

rules[(rules['a_len'] == 1) & (rules['c_len'] == 1)].to_csv('./app/static/data/public/standard_rules.csv', index=False)
