from collections import deque
import graphviz

# Part 1 Solution:
# Low signal = 0, high signal = 1
# Signal-sending events are represented as tuples of the form:
# (source module, signal type, destination module)

class FlipFlop:
    """
    A flip-flop module transmits no signals if the input signal is high.
    Otherwise it returns a high signal if the switch is on and a low signal
    if the switch is off. Afterwards, the switch is switched to the other position.
    On initialization all switches are set to the off position.
    """
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.on = False
    def __str__(self):
        return f"%{self.name}, destinations: {self.destinations}, {'on' if self.on else 'off'}"
    def send_signals(self, source, signal):
        if signal == 1:
            return ()
        else:
            self.on = not self.on
            if self.on:
                return ((self.name, 1, dest) for dest in self.destinations)
            else:
                return ((self.name, 0, dest) for dest in self.destinations)

class Conjunction:
    """
    A conjuction module remembers the type of the last signal sent to it for all of
    the modules which can send signals to the conjunction. At the beginning, the memory is
    set to a low signal for all connected modules. The records are upated each time a signal
    is received. The conjunction sends a high signal if any of the records is a low signal
    and it sends a low signal only if the last sent signal was high from all the incoming modules.
    """
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.states = {}
    def __str__(self):
        return f"&{self.name}, destinations: {self.destinations}, connections:{self.states}"
    def send_signals(self, source, signal):
        self.states[source] = signal 
        for key in self.states:
            if self.states[key] == 0: # End iterations as a low signal was found
                return ((self.name, 1, dest) for dest in self.destinations)
        # Else we know all input signal records are high signals
        return ((self.name, 0, dest) for dest in self.destinations)

with open("day20.txt", "r") as file:
    modules = {}
    file_text = file.readlines()
    for line in file_text:
        source, dest_string = line.strip('\n').split(' -> ')
        destinations = dest_string.split(', ')
        if source == "broadcaster":
            # Broadcaster module
            # There is only one broadcaster and it is a special module
            # No normal modules can send signals to it and its only input
            # is the button module which sends a low pulse on user input
            broadcaster = destinations
            continue
        mod_type, name = source[0], source[1:]
        if mod_type == "%":
            # Flip-flop module
            modules[name] = FlipFlop(name, destinations)
        elif mod_type == "&":
            # Conjunction module
            modules[name] = Conjunction(name, destinations) 

# Loop through all modules and look at their destinations.
# If the destination of a given module is a conjunction,
# initialize the states hashmap with the original module name as the key
for source_name, module in modules.items():
    for dest in module.destinations:
        if dest in modules and isinstance(modules[dest], Conjunction):
            modules[dest].states[source_name] = 0

low_pulses = 0
high_pulses = 0
for _ in range(1000):
    low_pulses += 1 # Records the pulse sent by the button module
    # events is a queue used to get the correct signal events in the correct order
    events = deque(("broadcaster", 0, dest) for dest in broadcaster)
    while len(events) > 0:
        source_str, signal, dest_str = events.popleft()
        if signal == 0:
            low_pulses += 1
        else:
            high_pulses += 1
        if dest_str not in modules:
            # We found an untyped output module
            continue
        else:
            for next_event in modules[dest_str].send_signals(source_str, signal):
                events.append(next_event)

print(f"Part 1's resulting product: {low_pulses*high_pulses}")

# Part 2 Solution:
# Let's first make an adjacency matrix to visualize the modules in a graph
"""
u = graphviz.Digraph('Modules', filename='modules.gv', node_attr={'color': 'yellow', 'style': 'filled'})
u.edge('button', 'broadcaster')
u.attr('node', color='lightblue2')
for next_mod in broadcaster:
    u.edge('broadcaster', next_mod)
for source_name, module in modules.items():
    if isinstance(module, Conjunction):
        u.attr('node', color='red')
        u.node(source_name)
        u.attr('node', color='lightblue2')
    else:
        u.node(source_name)
for source_name, module in modules.items():
    for dest in module.destinations:
        u.edge(source_name, dest)
print(u.source)
u.render()
for _ in range(20000):
    # events is a queue used to get the correct signal events in the correct order
    events = deque(("broadcaster", 0, dest) for dest in broadcaster)
    while len(events) > 0:
        source_str, signal, dest_str = events.popleft()
        if dest_str == 'dg' and signal == 1:
            print(source_str, _)
        if dest_str not in modules:
            # We found an untyped output module
            continue
        else:
            for next_event in modules[dest_str].send_signals(source_str, signal):
                events.append(next_event)

"""

xt = (2766, 6533)
lk = (2822, 3823)
sp = (2928, 6857)
zv = (3050, 4051)
conjunctions = (xt, lk, sp, zv)

i = 2766
while True:
    i += 1
    found = True
    for start, increment in conjunctions:
        if (i - start) % increment != 0:
            found = False
            break
        else:
            print(i, start)
    if found:
        print(i)
        break
