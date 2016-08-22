class Node(object):
	def __init__(self, key):
		self.left = None
		self.right = None
		self.parent = None

		self.key = key
		self.color =  None
		self.nums_child = 0

class RedBlackTree(object):
	def __init__(self):
		self.nil = Node(None)
		self.root = Node(None)
	def nums_child_update(self, x):
		"""Update number of children node for node x"""
		if x.left is None:
			if x.right is None:
				x.nums_child = 0
			else:
				x.nums_child = x.right.nums_child + 1
		else:
			if x.right is None:
				x.nums_child = x.left.nums_child + 1
			else:
				x.nums_child = x.left.nums_child + x.right.nums_child  + 2

	def left_rotate(self, x):
		""" Modify the change of number of children when left_rotate"""
		y = x.right
		x.right = y.left
		if y.left is not None:
			y.left.parent = x
		y.parent = x.parent
		if x is self.root:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.left = x
		x.parent = y
		self.nums_child_update(x)	
		self.nums_child_update(y)

	def right_rotate(self, y):
		""" Modify the change of number of children when right_rotate"""
		x = y.left
		y.left = x.right
		if x.right is not None:
			x.right.parent = y
		x.parent = y.parent
		if y.parent is self.root:
			self.root = x
		elif y is y.parent.right:
			y.parent.right = x
		else:
			y.parent.left = x
		x.right = y
		y.parent = x
		self.nums_child_update(x)	
		self.nums_child_update(y)

	def insert(self, key):
		z = Node(key)
		if self.root.key is None:
			self.root = z
			self.root.color = 'BLACK'
			self.nil.color = 'BLACK'
			self.root.parent = self.nil
			return
		x = self.root
		while x != None:
			y = x
			if z.key < x.key:
				x = x.left
			else:
				x = x.right
		z.parent = y
		if z.key < y.key:
			y.left = z
		else:
			y.right = z
		z.color = 'RED'
		node = z
		while node is not self.root:
			node.parent.nums_child = node.parent.nums_child + 1
			node = node.parent
		self.insert_fix_up(z)

	def insert_fix_up(self, z):
		while z.parent.color is 'RED':
			if z.parent is z.parent.parent.left:
				y = z.parent.parent.right
				if y is not None and y.color is 'RED':
					z.parent.color = 'BLACK'
					y.color = 'BLACK'
					z.parent.parent.color = 'RED'
					z = z.parent.parent
				elif z is z.parent.right:
					z = z.parent
					self.left_rotate(z)
					z.parent.color = 'BLACK'
					z.parent.parent.color = 'RED'
					self.right_rotate(z.parent.parent)
				elif z is z.parent.left:
					z.parent.color = 'BLACK'
					z.parent.parent.color = 'RED'
					self.right_rotate(z.parent.parent)
			else:
				y = z.parent.parent.left
				if y is not None and y.color is 'RED':
					z.parent.color = 'BLACK'
					y.color = 'BLACK'
					z.parent.parent.color = 'RED'
					z = z.parent.parent
				elif z is z.parent.left:
					z = z.parent
					self.right_rotate(z)
					z.parent.color = 'BLACK'
					z.parent.parent.color = 'RED'
					self.left_rotate(z.parent.parent)
				elif z is z.parent.right:
					z.parent.color = 'BLACK'
					z.parent.parent.color = 'RED'
					self.left_rotate(z.parent.parent)
		self.root.color = 'BLACK'

	def transplant(self, u, v):
		""" Replace subtree rooted at node u with that of node v"""
		if u.parent is self.nil:
			self.root = v
		elif u is u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v
		v.parent = u.parent

	def search(self, key):
		"""Return node with the specified key"""
		x = self.root
		while x is not self.nil:
			y = x
			if x.key > key:
				x = x.left
			elif x.key < key:
				x = x.right
			elif x.key == key:
				return x
			else:
				return None

	def delete(self, key):
		z = self.search(key)
		if z is None:
			return
		y = z
		y_origin_color = y.color
		if z.left is self.nil:
			x = z.right
			self.transplant(z, z.right)
		elif z.right is self.nil:
			x = z.left
			self.transplant(z, z.left)
		else:
			y = self.min(z.right)
			y_origin_color = y.color
			x = y.right
			if y.parent is z:
				x.parent = y
			else:
				self.transplant(y, y.right)
				y.right = z.right
				y.right.parent = y
			self.transplant(z, y)
			y.left = z.left
			y.left.parent = y
			y.color = z.color
		if y_origin_color is 'BLACK':
			self.delete_fix_up(x)

	def min(self, x):
	  """Return the node with minumin key given subtree rooted at node x"""
	  while x.left is not None:
	  	x = x.left
	  return x

	def max(self, x):
		"""Return the node with maximum key given subtree rooted at node x"""
		while x.right is not self.nil:
			x = x.right
		return x

	def delete_fix_up(self, x):
		while x is not self.root and x.color is 'BLACK':
			if x is x.parent.left:
				w = x.parent.right
				if w.color is 'RED':
					w.color == 'BLACK'
					w.parent.color = 'RED'
					self.left_rotate(x.parent)
					w = x.parent.right
				if w.left.color is 'BLACK' and w.right.color is 'BLACK':
					w.color = 'RED'
					x = x.parent
				elif w.right.color is 'BLACK':
					w.left.color = 'BLACK'
					w.color = 'RED'
					self.right_rotate(w)
					w = x.parent.right
				w.color = x.parent.color
				x.parent.color = 'BLACK'
				w.right.color = 'BLACK'
				self.left_rotate(x.parent)
				x = self.root
			else:
				w = x.parent.left
				if w.color is 'RED':
					w.color == 'BLACK'
					w.parent.color = 'RED'
					self.right_rotate(x.parent)
	  			w = x.parent.left
				if w.right.color is 'BLACK' and w.left.color is 'BLACK':
					w.color = 'RED'
					x = x.parent
				elif w.left.color is 'BLACK':
					w.right.color = 'BLACK'
					w.color = 'RED'
					self.left_rotate(w)
					w = x.parent.left
				w.color = x.parent.color
				x.parent.color = 'BLACK'
				w.left.color = 'BLACK'
				self.right_rotate(x.parent)
				x = self.root

	def rank(self, key):
		number = 0
		x = self.root
		while x is not None:
			if x.key <= key:
				number = number + 2 + x.left.nums_child
				x = x.right
			else:
				x = x.left
		return number

	def count(self, start, end):
		"""Return number of nodes with key that are smmaller than or equal 'end' and greater or equal than 'start'"""
		if self.search(start) is not None:
			return self.rank(end) - self.rank(start) + 1
		else:
			return self.rank(end) - self.rank(start)

	def lca(self, low, high):
		"""Lowest Common Ancestor"""
		x = self.root
		while x is not self.nil or (low <= x.key and h >= x.key):
			if low < x.ley:
				x = x.left
			else:
				x = x.right
		return x

	def node_list(node, low, high):
		result = []
		if node is self.nil:
			return result
		if low <= node.key and node.key <= high:
			result.append(node)
		if low < node.key:
			self.node_list(node.right, low, high)
		if node.key <= high:
			self.node_list(node.left, low, high)
		return result

	def list(self, start, end):
		"""Return a list of nodes with key that are smmaller than or equal 'end' and greater or equal than 'start'"""
		node = self.lca(start, end) 
		result = self.node_list(node, start, end)
		return result

class TraceRedBlackTree(RedBlackTree):
	"""Augments RedBlackTree to build a trace for the visualizer"""
	def __init__(self, trace):
		RedBlackTree.__init__(self)
		self.trace = trace

	def insert(self, node):
		self.trace.append({'type': 'add', 'id' : node.wire.name})
		RedBlackTree.insert(self, node)

	def delete(self, node):
		self.trace.append({'type': 'delete', 'id': node.wire.name})
		RedBlackTree.remove(self, node)

	def list(self, start, end):
		result = RedBlackTree.list(self, start, end)
		self.trace.append({'type': 'list', 'from': start, 'to': end, 'ids': restul})
		return result

	def count(self, start, end):
		result = RedBlackTree.count(self, start, end)
		self.trace.append({'type': 'count', 'from': start, 'to': end, 'id': result})
		return result