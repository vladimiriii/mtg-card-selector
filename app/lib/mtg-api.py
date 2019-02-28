import pandas as pd
from datetime import datetime, date, timedelta
from mtgsdk import Card, Set, Type, Supertype, Subtype

standard_sets = [
    'XLN'
    , 'RIX'
    , 'DOM'
    , 'GS1'
    , 'M19'
    , 'GRN'
]

# Extract all cards from sets
all_cards = []
for set in standard_sets:
    all_cards += Card.where(set=set).all()

# Put all the card data in a DataFrame
cards_output = []
for card in all_cards:
    cards_output.append({
        'id': card.multiverse_id
        , 'name': card.name
        , 'rarity': card.rarity
        , 'mana_cost': card.mana_cost
        , 'super_type': card.supertypes
        , 'type': card.type
        , 'colors': card.colors
        , 'set': card.set
        , 'set_name': card.set_name
    })

df = pd.DataFrame(cards_output)

df[['id', 'name', 'set', 'set_name', 'mana_cost', 'colors', 'type', 'super_type', 'rarity' ]].to_csv('./app/static/data/public/standard_card_data.csv', index=False)
