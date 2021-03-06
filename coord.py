"""class MapCoord(Coord):
	#
class RectMapCoord(MapCoord):
	#members x and y as int
	@property
	def rect(self):
		return self
	def __add__(self, other):
		return Coord(x=self.x+other.x,y=self.y+other.y)
	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		return self
	def __sub__(self, other):
		return Coord(x=self.x-other.x,y=self.y-other.y)
	def __isub__(self, other):
		self.x -= other.x
		self.y -= other.y
		return self
#class AxialMapCoord(MapCoord)
	# members a,b,c as int, a+b+c=0
	
class GLCoord(Coord):
	# members x and y in [0.0,1.0]
	
	def __mul__(self, other):
		if type(other) is Coord:
			return Coord(x=self.x*other.x,y=self.y*other.y)
		else:
			return Coord(x=self.x*other,y=self.y*other)
	def __imul__(self, other):
		if type(other) is Coord:
			self.x *= other.x
			self.y *= other.y
		else:
			self.x *= other
			self.y *= other
		return self
class PixelCoord(Coord):
	# members x and y as int in [0,W],[0,H], should not be stored.
"""

class Coord:
	def __init__(self, **kargs):
		self.x = kargs["x"]
		self.y = kargs["y"]
		
	@property
	def rect(self):
		return self

	def __add__(self, other):
		return Coord(x=self.x+other.x,y=self.y+other.y)
	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		return self
	def __sub__(self, other):
		return Coord(x=self.x-other.x,y=self.y-other.y)
	def __isub__(self, other):
		self.x -= other.x
		self.y -= other.y
		return self
	def __mul__(self, other):
		if type(other) is Coord:
			return Coord(x=self.x*other.x,y=self.y*other.y)
		else:
			return Coord(x=self.x*other,y=self.y*other)
	def __imul__(self, other):
		if type(other) is Coord:
			self.x *= other.x
			self.y *= other.y
		else:
			self.x *= other
			self.y *= other
		return self
	def __round__(self):
		return Coord(x=round(self.x),y=round(self.y))
	def __repr__(self):
		return "(%s,%s)"%(repr(self.x),repr(self.y))
	def __eq__(self, other):
		if type(other) is type(None): return False
		return self.x == other.x and self.y == other.y
	def __ne__(self, other):
		if type(other) is type(None): return False
		return self.x != other.x or self.y != other.y
	def __hash__(self):
		return hash((self.x, self.y))
	def __truediv__(self, other):
		if type(other) is Coord:
			return Coord(x=self.x/other.x,y=self.y/other.y)
		else:
			return Coord(x=self.x/other,y=self.y/other)
	def __itruediv__(self, other):
		if type(other) is Coord:
			self.x /= other.x
			self.y /= other.y
		else:
			self.x /= other
			self.y /= other
		return self

		
class RectCoordBound:
	def __init__(self, min_coord, max_coord):
		self.min_coord, self.max_coord = min_coord, max_coord
	def within(self, coord):
		return coord.x >= self.min_coord.x and coord.x <= max_coord.x and coord.y >= self.min_coord.y and coord.y <= self.max_coord.y
	def normalize(self, origin_bound, coord):
		return None