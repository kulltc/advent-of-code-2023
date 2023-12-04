# import re, math

# points = 0
# for line in open('day_4_input.txt').readlines():
#     winningString, yourString = re.match(r"Card\s+\d+\:([\d\s]*)\|([\d\s]*?)\n?$", line).groups()
    
#     winning = winningString.split(' ')
#     yourNumbers = yourString.split(' ')
#     print(winning, yourNumbers)
#     currentPoint = 0.5
#     for winningNum in winning:
#         if not winningNum.isdigit():
#             continue
#         if winningNum in yourNumbers:
#             currentPoint *= 2
#     print(line, math.floor(currentPoint))
#     points += math.floor(currentPoint)

# print(points)

import re, math
results = {'part1': {}, 'part2':{}}
for cardIndex, line in enumerate(open('day_4_input.txt').readlines()):
    cardNumber, winningString, yourString = re.match(r"Card\s+(\d+)\:([\d\s]*)\|([\d\s]*?)\n?$", line).groups()
    for index, winningNum in enumerate([num for num in re.findall(r'(\d+)', winningString) if num in re.findall(r'(\d+)', yourString)]):
        results['part1'][int(cardNumber)] = (2**index)
        results['part2'][int(cardNumber) + index + 1] = results['part2'].get(int(cardNumber) + index + 1, 0) + 1 + results['part2'].get(int(cardNumber), 0)
print(sum(results['part1'].values()), cardIndex + 1 + sum(results['part2'].values()))
