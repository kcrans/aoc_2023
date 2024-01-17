from collections import deque
from math import lcm
from itertools import count

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
    def is_default(self):
        return self.on == False
    def send_signals(self, source, signal):
        if signal == 1:
            return ()
        else:
            if self.on:
                self.on = False
                return ((self.name, 0, dest) for dest in self.destinations)
            else:
                self.on = True
                return ((self.name, 1, dest) for dest in self.destinations)

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
    def is_default(self):
        return all(signal == 0 for source, signal in self.states.items())
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
button_pushes = 1000 # For part 1 we will push the button 1000 times
low_pulses = 0
high_pulses = 0
for _ in range(button_pushes):
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

# Clear all states from part 1 and set them back to the default values
with open("day20.txt", "r") as file:
    modules = {}
    file_text = file.readlines()
    for line in file_text:
        source, dest_string = line.strip('\n').split(' -> ')
        destinations = dest_string.split(', ')
        if source == "broadcaster":
            broadcaster = destinations
            continue
        mod_type, name = source[0], source[1:]
        if mod_type == "%":
            # Flip-flop module
            modules[name] = FlipFlop(name, destinations)
        elif mod_type == "&":
            # Conjunction module
            modules[name] = Conjunction(name, destinations) 
for source_name, module in modules.items():
    for dest in module.destinations:
        if dest in modules and isinstance(modules[dest], Conjunction):
            modules[dest].states[source_name] = 0

# Find all modules that feed into the terminal 'rx' modules
parents = [module for module in modules.keys() if 'rx' in modules[module].destinations]
# Note that there is only one and it is a conjunction
assert len(parents) == 1
assert isinstance(modules[parents[0]], Conjunction)
# Find all modules which feed into the above module
grandparents = set(module for module in modules.keys() if parents[0] in modules[module].destinations)
# There are 4 of them and all are conjunctions
assert len(grandparents) == 4
assert all(isinstance(modules[mod], Conjunction) for mod in grandparents)
# If you look at the dependancy graph, you'll notice that these 4 conjunctions are paired up with another 4 conjunctions
# which provide the only input into them. We want rx to receive a low signal, so its parent must receive/remember all high signals.
# In order for each conjunction to send a high signal, one of their inputs must be a low signal. They only have one input, so we just
# need to find the first time each of these 4 conjunctions is sent a low signal during the phase after a button press.
# It's going to take to long simulate all the button pushes it takes to reach this event, so let's instead look at how
# many button pushes it takes for each of the grandparent modules to receive a low pulse. If the state of the whole system is periodic
# (i.e. it reaches the default state and then restarts in a cycle) then each of the times until a low pulse will cycle for however
# many button pushes and we can just find the lcm of them to get our answer. I'm not sure how to prove this, but looking at the ouput
# we see that low pulses are sent to the grandparent modules in repeated cycles.

reached_default = False
cycle_lengths = []

for button_push in count(start = 1, step = 1):
    if len(grandparents) == 0:
        break
    events = deque(("broadcaster", 0, dest) for dest in broadcaster)
    while len(events) > 0:
        source_str, signal, dest_str = events.popleft()
        if dest_str not in modules:
            # We found an untyped output module
            continue
        elif dest_str in grandparents and signal == 0:
            cycle_lengths.append(button_push)
            grandparents.remove(dest_str)
        else:
            new_events = []
            for next_event in modules[dest_str].send_signals(source_str, signal):
                events.append(next_event)
                new_events.append(next_event)

print(f'Part 2 number of button pushes needed to send a low pulse to "rx": {lcm(*cycle_lengths)}')
