import json   # Used when TRACE=jsonp
import os     # Used to get the TRACE environment variable
import re     # Used when TRACE=jsonp
import sys    # Used to smooth over the range / xrange issue.
from red_black_tree import *

if sys.version_info >= (3,):
    xrange = range

class Wire(object):

  def __init__(self, name, x1, y1, x2, y2):
    if x1 > x2:
      x1, x2 = x2, x1
    if y1 > y2:
      y1, y2 = y2, y1
    
    self.name = name
    self.x1, self.y1 = x1, y1
    self.x2, self.y2 = x2, y2
    self.object_id = Wire.next_object_id()
    
    if not (self.is_horizontal() or self.is_vertical()):
      raise ValueError(str(self) + ' is neither horizontal nor vertical')
  
  def is_horizontal(self):
    return self.y1 == self.y2
  
  def is_vertical(self):
    return self.x1 == self.x2
  
  def intersects(self, other_wire):
    if self.is_horizontal() == other_wire.is_horizontal():
      return False 
    
    if self.is_horizontal():
      h = self
      v = other_wire
    else:
      h = other_wire
      v = self
    return v.y1 <= h.y1 and h.y1 <= v.y2 and h.x1 <= v.x1 and v.x1 <= h.x2
  
  def __repr__(self):

    # :nodoc: nicer formatting to help with debugging
    return('<wire ' + self.name + ' (' + str(self.x1) + ',' + str(self.y1) + 
           ')-(' + str(self.x2) + ',' + str(self.y2) + ')>')
  
  def as_json(self):
    """Dict that obeys the JSON format restrictions, representing the wire."""
    return {'id': self.name, 'x': [self.x1, self.x2], 'y': [self.y1, self.y2]}

  # Next number handed out by Wire.next_object_id()
  _next_id = 0
  
  @staticmethod
  def next_object_id():
    """Returns a unique numerical ID to be used as a Wire's object_id."""
    id = Wire._next_id
    Wire._next_id += 1
    return id

class WireLayer(object):  
  def __init__(self):
    self.wires = {}
  
  def wires(self):
    self.wires.values()
  
  def add_wire(self, name, x1, y1, x2, y2):
    if name in self.wires:
        raise ValueError('Wire name ' + name + ' not unique')
    self.wires[name] = Wire(name, x1, y1, x2, y2)
  
  def as_json(self):
    """Dict that obeys the JSON format restrictions, representing the layout."""
    return { 'wires': [wire.as_json() for wire in self.wires.values()] }
  
  @staticmethod
  def from_file(file):
    """Builds a wire layer layout by reading a textual description from a file.
    
    Args:
      file: a File object supplying the input
    
    Returns a new Simulation instance."""

    layer = WireLayer()
    
    while True:
      command = file.readline().split()
      if command[0] == 'wire':
        coordinates = [float(token) for token in command[2:6]]
        layer.add_wire(command[1], *coordinates)
      elif command[0] == 'done':
        break
      
    return layer

class ResultSet(object):
  """Records the result of the circuit verifier (pairs of crossing wires)."""
  
  def __init__(self):
    """Creates an empty result set."""
    self.crossings = []
  
  def add_crossing(self, wire1, wire2):
    """Records the fact that two wires are crossing."""
    self.crossings.append(sorted([wire1.name, wire2.name]))
  
  def write_to_file(self, file):
    """Write the result to a file."""
    for crossing in self.crossings:
      file.write(' '.join(crossing))
      file.write('\n')

class TracedResultSet(ResultSet):
  """Augments ResultSet to build a trace for the visualizer."""
  
  def __init__(self, trace):
    """Sets the object receiving tracing info."""
    ResultSet.__init__(self)
    self.trace = trace
    
  def add_crossing(self, wire1, wire2):
    self.trace.append({'type': 'crossing', 'id1': wire1.name,
                       'id2': wire2.name})
    ResultSet.add_crossing(self, wire1, wire2)

class CrossVerifier(object):
	def __init__(self, layer):
		self.events = []
		self.events_from_layer(layer)
		self.events.sort()
		self.tree_y = RedBlackTree()
		self.tree_x = RedBlackTree()

		self.result = ResultSet()
		self.performed = False

	def count_crossings(self):
		if self.performed:
			raise
		self.performed = True
		return self.compute_crossing(True)

	def wire_crossings(self):
		if self.performed:
			raise
		self.performed = True
		return self.compute_crossing(False)

	def events_from_layer(self, layer):
		for wire in layer.wires.values():
			if wire.is_horizontal():
				self.events.append([wire.x1, 'horizontal', wire])
			else:
				self.events.append([wire.x1, 'vertical', wire])

	def compute_crossing(self, count_only):
		start_add = 0
		start_del = 0
		end_add = 0
		end_del = 0

		if count_only:
			result = 0
		else:
			result = ResultSet()

		for event in self.events:
			event_type, wire = event[1], event[2]
			end_add += 1
			if event_type is 'vertical':
				temp = wire.x2
				i = start_add
				while i < end_add - 1:
					if self.events[i][2].x2 > temp:
						self.tree_y.insert(Node(self.events[i][2].y1, self.events[i][2]))
					i += 1

				k = start_del
				while k < end_del - 1:
					if self.events[k][2].x2 < temp:
						self.tree_y.delete(self.tree_y.search(self.events[k][2].y1))
					k += 1

				start_del = end_del
				start_add = end_add
				end_del = start_add

				if count_only:
					result += self.tree_y.count(wire.y1, wire.y2)
				else:
					node_list = self.tree_y.list(wire.y1, wire.y2)
					for node in node_list:
						result.add_crossing(node.wire, wire)
		return result	

	def trace_sweep_line(self, x):
		pass

class TracedCrossVerifier(CrossVerifier):
	"""Augments CrossVerifier to build a trace for the visualizer."""
	def __init__(self, layer):
		CrossVerifier.__init__(self, layer)
		self.trace = []
		self.index = TracedRangeIndex(self.trace)
		self.result_set = TracedResultSet(self.trace)

	def trace_sweep_line(self, x):
		self.trace.append({'type': 'sweep', 'x': x})

	def trace_as_json(self):
		"""List that obeys the JSON format restrictions with the verifier trace."""
		return self.trace

# Command-line controller.
if __name__ == '__main__':
		import sys
		layer = WireLayer.from_file(sys.stdin)
		verifier = CrossVerifier(layer)

		if os.environ.get('TRACE') == 'jsonp':
			verifier = TracedCrossVerifier(layer)
			result = verifier.wire_crossings()
			json_obj = {'layer': layer.as_json(), 'trace': verifier.trace_as_json()}
			sys.stdout.write('onJsonp(')
			json.dump(json_obj, sys.stdout)
			sys.stdout.write(');\n')
		elif os.environ.get('TRACE') == 'list':
			verifier.wire_crossings().write_to_file(sys.stdout)
		else:
			sys.stdout.write(str(verifier.count_crossings()) + "\n")