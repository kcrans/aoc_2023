# Code for generating a graph visualization of the modules and their connections
from collections import deque
import graphviz

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

# Using the graphviz library we can generate a visualization of the relationships between the modules
# The broadcaster module will be yellow, conjunctions red, and flip-flops light blue
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
