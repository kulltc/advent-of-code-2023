LOW = 0
HIGH = 1
BC = 'roadcaster'
counter = {LOW:0, HIGH: 0}
import json

class Module:

    def __init__(self, name, pulse_queue):
        self.name = name
        self.destinations = []
        self.sources = []
        self.pulse_queue = pulse_queue

    def handle_pulse(self, sender, pulse):
        pass
    
    def add_source(self, source):
        #avoid circular references
        if self.name not in [s.name for s in source.sources]:
            self.sources.append(source)
    
    def hash(self):
        return str(id(self))
    
    def is_initial_state(self):
        return True
    
    def add_destination(self, destination):
        destination.add_source(self)
        self.destinations.append(destination)
       
    def _broadcast(self, pulse):
        for d in self.destinations:
            self.pulse_queue.add(self.name, pulse, d.name)
        
    
class FlipFlop(Module):
    
    def __init__(self, *args, **kwargs):
        super(FlipFlop, self).__init__(*args, **kwargs)
        self.ON = False
    
    def handle_pulse(self, _, pulse):
        if pulse == LOW:
            self.ON = not self.ON
            return self._broadcast(HIGH if self.ON else LOW)
        
    def hash(self):
        return str(self.ON) + super().hash()
    
    def is_initial_state(self):
        return self.ON == False and super().is_initial_state()
    

class Conjunction(Module):

    def __init__(self, *args, **kwargs):
        super(Conjunction, self).__init__(*args, **kwargs)
        self.input_cache = {}

    def hash(self):
        return ','.join([str(val) for val in self.input_cache.values()]) + super().hash()
    
    def is_initial_state(self):
            for cache in self.input_cache.values():
                if cache != LOW:
                    return False
                
            return super().is_initial_state()
    
    def add_source(self, source):
        self.input_cache[id(source)] = LOW
        super().add_source(source)

    def handle_pulse(self, sender, pulse):
        if sender not in self.input_cache:
            print(self.name, sender)
            exit('sender not in input cache. stopped')
        self.input_cache[sender] = pulse
        for last_pulse in self.input_cache.values():
            if last_pulse == LOW:
                return self._broadcast(HIGH)
        return self._broadcast(LOW)

class Broadcaster(Module):
    
    def handle_pulse(self, sender, pulse): 
        return self._broadcast(pulse)
    
class Sink(Module):

    def handle_pulse(self, sender, pulse):
        return

class PulseQueue:

    def __init__(self, modules, counter):
        self.button_press = 0
        self.modules = modules
        self.queue = []
        self.counter = counter
        self.rx_check = False
        self.jm_cache = {'sg': [], 'lm': [], 'db': [], 'dh': []}
        self.cache_final = {'sg': False, 'lm': False, 'db': False, 'dh': False}

    def set_ancestry(self):
        self.jm_ancestry = {
            'sg': list(set(self.modules['gj'].destinations + self.modules['gj'].sources)),
            'lm': list(set(self.modules['qq'].destinations + self.modules['qq'].sources)),
            'db': list(set(self.modules['bx'].destinations + self.modules['bx'].sources)),
            'dh': list(set(self.modules['bc'].destinations + self.modules['bc'].sources)),
        }

    def add(self, sender, pulse, dest):
        self.counter[pulse] += 1
        if dest == 'jm' and not self.cache_final[sender]:
            if len(self.jm_cache[sender]) == 0 or self.jm_cache[sender][-1]['pulse'] != pulse:
                self.jm_cache[sender].append({'pulse': pulse, 'count': sum(self.counter.values()), 'press': self.button_press})
        self.queue.append((sender, pulse, dest))

    def run(self):
        self.button_press += 1
        while len(self.queue) > 0:
            pulse = self.queue[0]
            self.queue = self.queue[1:]
            self.modules[pulse[2]].handle_pulse(id(self.modules[pulse[0]]), pulse[1])

g_modules = {}
g_pq = PulseQueue(g_modules, counter)
g_destinations = {}
g_types = {
    '%': FlipFlop,
    '&': Conjunction,
    'b': Broadcaster
}
g_modules['rx'] = Sink('rx', g_pq)

import re

for line in open('day_20_input.txt'):
    type, name, destination_string = re.match(r"(.)(\w+) -> (.*)", line.strip()).groups()
    g_modules[name] = g_types[type](name, g_pq)
    g_destinations[name] = [dest.strip() for dest in destination_string.split(',')]

for name, dest_array in g_destinations.items():
    for dest in dest_array:
        if dest not in g_modules:
            dest = 'rx'
        g_modules[name].add_destination(g_modules[dest])

g_pq.set_ancestry()

i = 0
ran = True
hash_history = {'sg': {}, 'lm': {}, 'db': {}, 'dh': {}}
while ran:
    i += 1
    g_pq.add('roadcaster', LOW, 'roadcaster')
    g_pq.run()
    ran = False
    for main, ancestors in g_pq.jm_ancestry.items():
        if g_pq.cache_final[main]:
            continue

        ran = True
        hash_string = ''
        for ancestor in ancestors:
            hash_string += ancestor.hash()
        
        if hash_string in hash_history[main]:
            print('loop detected for ', main, i)
            open(f'./day_20/{main}.json', 'w').write(json.dumps([hash_history[main][hash_string], g_pq.jm_cache[main], g_pq.button_press, i]))
            g_pq.cache_final[main] = True
        else:
            hash_history[main][hash_string] = g_pq.button_press
        if i % 1_000_000 == 0:
            print(i)
        
print(counter, counter[HIGH] * counter[LOW])
