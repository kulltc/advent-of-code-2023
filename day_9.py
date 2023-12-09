

def get_next_number(range):
    diffs = []
    non_zero = False
    for prev_index, num in enumerate(range[1:]):
        diff = num - range[prev_index]
        non_zero = non_zero or diff != 0
        diffs.append(diff)
    new_diff = 0
    if non_zero:
        new_diff = get_next_number(diffs)
    return num + new_diff

def get_prev_number(range):
    return get_next_number(list(reversed(range)))

predictions = []
reverse_predictions = []
for line in open('day_9_input.txt'):
    numbers = [int(num) for num in line.strip().split(' ')]
    predictions.append(get_next_number(numbers))
    reverse_predictions.append(get_prev_number(numbers))

print(predictions)
print(sum(predictions))

print(reverse_predictions)
print(sum(reverse_predictions))
    

