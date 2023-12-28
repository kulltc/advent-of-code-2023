import re, json
from itertools import chain

workflows = {}
parts = []
after_blank = False
evals = {
    '>': lambda a,b: int(a) > int(b),
    '<': lambda a,b: int(a) < int(b)
}


def process_workflow(string):
    key, workflow_string = re.match(r"(\w+)\{([^\}]+)\}", string).groups()
    rule_strings = workflow_string.split(',')
    rules = [re.match(r"([xmas])([<>])(\d+)\:(\w+)", rule_string).groups() for rule_string in rule_strings[:-1]]
    rules.append(('x','>', -1, rule_strings[-1]))
    return key, rules
    
def process_part(string):
    part = {}
    for letter, value in re.findall(r"([xmas])\=(\d+)",string):
        part[letter] = int(value)
    return part

def eval_part(part, workflow_name = 'in'):
    if workflow_name == 'R' or workflow_name == 'A':
        return workflow_name
    for rule in workflows[workflow_name]:
        if evals[rule[1]](part[rule[0]], rule[2]):
            return eval_part(part, rule[3])
    exit('error: unmatched rule', part, workflow_name, workflows[workflow_name])


for line in open('day_19_input.txt'):
    line = line.strip()
    if line == '':
        after_blank = True
        continue
    if after_blank:
        parts.append(process_part(line))
    else:
        key, rule = process_workflow(line)
        workflows[key] = rule

print(sum([sum(part.values()) for part in parts if eval_part(part) == 'A']))

def eval_cond(workflow_name, accepted_condition_sets = []):
    if workflow_name == 'A':
        return [accepted_condition_sets]
    if workflow_name == 'R': 
        return []
    sets = []
    for rule in workflows[workflow_name]:
        sets.append(eval_cond(rule[3], accepted_condition_sets + [(rule[0], rule[1], rule[2], True)]))
        accepted_condition_sets.append((rule[0], rule[1], rule[2], False))
    return list(chain(*sets))

def standardize_conds(conds):
    new = []
    print(conds)
    for cond in conds:
        if cond[3]:# Should be True
            new.append((cond[0], cond[1], int(cond[2])))
        #Should be False. Flip it around
        elif cond[1] == '>':
            #currently says > 100 must be False. Convert to < 100 + 1 must be True
            new.append((cond[0], '<', int(cond[2]) + 1))
        else:
            #currently says < 100 must be False. Convert to > 100 - 1 must be True
            new.append((cond[0], '>', int(cond[2]) - 1))
    return new

def deduplicate_conds(conds):
    std = {}
    for cond in conds:
        if cond[0] not in std:
            std[cond[0]] = {}
        if cond[1] in std[cond[0]]:
            if cond[1] == '>':
                std[cond[0]]['>'] = max(std[cond[0]][cond[1]], cond[2])
            else:
                std[cond[0]]['<'] = min(std[cond[0]][cond[1]], cond[2])
        else:
            std[cond[0]][cond[1]] = cond[2]
    return std

def is_valid(conds):
    for cond in conds.values():
        if '>' in cond and '<' in cond:
            if cond['<'] < cond['>']:
                return False
    return True

cond_sets = [deduplicate_conds(standardize_conds(cond_set)) for cond_set in eval_cond('in')]
cond_sets = [cond for cond in cond_sets if is_valid(cond)]
edges = {}
for cond_set in cond_sets:
    for key, rule in cond_set.items():
        if key not in edges:
            edges[key] = []
        if '>' in rule:
            edges[key].append(rule['>'] + 1)
        if '<' in rule:
            edges[key].append(rule['<'])

import pprint
for key in edges.keys():
    edges[key] = [edge for edge in edges[key] if edge > 1]
    edges[key] = sorted(list(set(edges[key])))
count = 0
pprint.pprint(workflows)
pprint.pprint(edges)

total = len(edges['x'])

def eval_condset(part, cond_set):
    for key, rule in cond_set.items():
         if key in part:
            if not part[key] < rule.get('<', 4001):
                return False
            if not part[key] > rule.get('>', 0):
                return False
    return True
pprint.pprint(len(cond_sets))

def filter_sets(sets, key, min, max):
    return [set for set in sets if eval_condset({key:min}, set)]

for counter, (x_min, x_max) in enumerate(list(zip([1] + edges['x'], edges['x'] + [4001]))):
    cond_subset_x = filter_sets(cond_sets, 'x', x_min, x_max)
    print(f"Currently at {counter} of {total}")
    for m_min, m_max in list(zip([1] + edges['m'], edges['m'] + [4001])):
        cond_subset_m = filter_sets(cond_subset_x, 'm', m_min, m_max)
        print('M is at', m_min)
        for a_min, a_max in list(zip([1] + edges['a'], edges['a'] + [4001])):
            cond_subset_a = filter_sets(cond_subset_m, 'a', a_min, a_max)
            for s_min, s_max in list(zip([1] + edges['s'], edges['s'] + [4001])):
                for condset in cond_subset_a:
                    if eval_condset({'x':x_min, 'm':m_min, 'a':a_min, 's':s_min}, condset):
                        count += (x_max - x_min) * (m_max - m_min) * (a_max - a_min) * (s_max - s_min)
                        break
                    

print(count)