from mtgsdk import Card, Set, Type, Supertype, Subtype

cards = Card.where(name='guild').where(set='GRN').all()

for c in cards:
    print(c.name, c.set)
