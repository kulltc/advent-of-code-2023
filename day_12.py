
import re, itertools
from math import factorial
# current count is >0 when 'inside' a list of broken parts.

def stars_bars(n_stars, k_bars):
    return factorial(n_stars + k_bars) / (factorial(n_stars) * factorial(k_bars))

print(stars_bars(51, 25))
exit()

def options(remaining_parts, remaining_counts, current_count = 0):
    # print(remaining_parts, remaining_counts, current_count)
    # too few remaining parts to get to the correct total broken parts.
    if sum([len(part) for part in remaining_parts]) < sum(remaining_counts) + len(remaining_counts) - current_count - 1:
        return 0
    
    # too many broken parts to get to the correct total broken parts.
    broken_parts = [len(part) for part in remaining_parts if part[0] == '#']
    if sum(broken_parts) > sum(remaining_counts) - current_count:
        return 0
    # invalid tree:
    if current_count > 0 and len(remaining_counts) == 0 or current_count > 0 and len(remaining_counts) == 0 or current_count > 0 and remaining_counts[0] < current_count:
        return 0
    
    if len(broken_parts) > 0 and min(broken_parts) > (max(remaining_counts) if len(remaining_counts) > 0 else 0):
        return 0

    if len(remaining_parts) == 0:
        # if this was the last sequence and the length is correct we're good.
        if len(remaining_counts) == 1 and remaining_counts[0] == current_count:
            return 1
        
        #otherwise it's only ok if remaining_counts is also empty
        return 1 if len(remaining_counts) == 0 and current_count == 0 else 0
    if (remaining_parts[0][0] == '?'):
        # has to be interpreted as broken
        if len(remaining_parts[0]) > 1:
            one_off_remaining = [x for x in remaining_parts]
            one_off_remaining[0] = remaining_parts[0][1:]  
        else:
            one_off_remaining = remaining_parts[1:]
        if current_count > 0 and current_count < remaining_counts[0]:
            return options(one_off_remaining, remaining_counts, current_count + 1)

        # has to be interpreted as not broken
        elif current_count > 0 and remaining_counts[0] == current_count:
            return options(one_off_remaining, remaining_counts[1:], 0)
        
        # find an efficient way to find the number of ways to end up in certain exit scenario's
        option_count = 0
        # scenario 1: don't do any broken parts in this ? range.
        # option_count += options(remaining_parts[1:], remaining_counts, 0)

        #create full sequence(s)
        #note you may need a question mark to separate this sequence from the next.
        question_marks = len(remaining_parts[0])
        sequences = 0
        option_count = 0
        while True:
            if sequences > len(remaining_counts) or sum(remaining_counts[0:sequences]) > question_marks:
                break

            full_sequences_length = sum(remaining_counts[0:sequences])
            partial_sequences_lengths = [0]
            if len(remaining_counts) > sequences and len(remaining_parts) > 1 and remaining_parts[1][0] == '#':
                partial_sequences_lengths += [i for i in range(1, remaining_counts[sequences])]
            
            for partial in partial_sequences_lengths:
                #between sequences
                separators = (sequences - 1) if sequences > 1 else 0
                #end of sequences
                separators += 1 if (len(remaining_parts) > 1 and remaining_parts[1][0] == '#' and sequences > 0) else 0
                
                total_used_qs = full_sequences_length + separators + partial
                
                if total_used_qs > question_marks:
                    continue
                stars_bars_cnt = stars_bars(question_marks - total_used_qs, sequences)
                cur_options = options(remaining_parts[1:], remaining_counts[sequences:], partial)
                option_count += cur_options * stars_bars_cnt
                # if len(remaining_parts) == 5:
                #     print(remaining_parts, remaining_counts, 'parts', partial, 'sequences', sequences, 'cur', cur_options, 'strs_brs', stars_bars_cnt, 'qs', question_marks, 'qs used', total_used_qs, 'options', option_count)
            sequences += 1
        return option_count


    if (remaining_parts[0][0] == '.'):
        if (current_count > 0 and current_count == remaining_counts[0]):
            return options(remaining_parts[1:], remaining_counts[1:], 0)
        elif (current_count > 0 and current_count != remaining_counts[0]):
            return 0
        else:
            return options(remaining_parts[1:], remaining_counts, 0)
    
    # remaining_parts[0] must be '###'
    return options(remaining_parts[1:], remaining_counts, current_count + len(remaining_parts[0]))
       
        
result = []
for line in open('day_12_input.txt'):
    full, summ = line.strip().split(' ')
    full = f"{full}?{full}?{full}?{full}?{full}"
    summ = f"{summ},{summ},{summ},{summ},{summ}"
    counts = [int(s) for s in summ.split(',')]
    string_parts = re.findall(r"(#+)|(\?+)|(\.+)", full)
    string_parts = [part for part in itertools.chain(*string_parts) if part != '']
    val = options(string_parts, counts)
    print(full, summ, 'options:', val)
    result.append(val)

print('sum', sum(result))

