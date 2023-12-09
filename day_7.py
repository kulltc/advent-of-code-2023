import re

order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
order.reverse()

parsedHands = []
for line in open('day_7_input.txt'):
    hand, score = re.match(r'([\w\d]+) (\d+)', line).groups()
    #parse hand
    groups = {}
    cardNumbers = []
    for card in hand:
        groups[card] = groups.get(card, 0) + 1
        cardNumbers.append(str(order.index(card)).zfill(2))
    groups = dict(sorted(groups.items(), key=lambda i: i[1], reverse=True))
    
    #adjust for jokers
    jokers = groups.get('J', 0)
    if (0 < jokers and jokers < 5):
        del groups['J']
        groups[list(groups.keys())[0]] += jokers
    
    #store data
    groupValues = [str(val) for val in groups.values()]
    groupValuesPadded = ''.join(groupValues + ['0'] * (5 - len(groupValues)))
    parsedHands.append({'parsed': ''.join(groupValuesPadded) + ''.join(cardNumbers), 'score': int(score), 'hand': hand})

score = 0
for index, hand in enumerate(sorted(parsedHands, key=lambda h: h['parsed'])):
    score += (index + 1) * hand['score']
print(score)



    