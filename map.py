from numpy import full

class Map:
	"""
	Map class.

	Represents a map.
	"""
	def __init__(self, size):
		self.data = full(size, -1)
		self.width = size[0]
		self.height = size[1]
	def get_at(self, col, row):
		return self.data[row][col]
	def set_at(self, col, row, value):
		self.data[row][col] = value
