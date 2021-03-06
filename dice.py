from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy

import coord
import dieentity
import time
import math

WINDOW_IDX = 0
WINDOW_SIZE = coord.Coord(x=640, y=480)
FULLSCREEN = False
SHOWFPS=True
GUI_LAYER=0
GEO_LAYER=1
USE_DRAG_MOVE = True
USE_DRAG_ROTATE = False

def refresh2d(vw, vh, width, height):
	glViewport(0, 0, width, height)
	glClearColor(0, 0, 0, 0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, vw, 0.0, vh, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()

class mygame:
	def __init__(self):
		self.window_size = WINDOW_SIZE
		self.window_bound = coord.RectCoordBound (coord.Coord(x=0.0,y=0.0), coord.Coord(x=1.0,y=1.0))
		
		self.init_window()
		self.init_callback()
		
		self.mouseloc = None
		self.wmouseloc = None
		self.mouse_coord = None
		
		self.objects = [dieentity.DieEntity(3, coord.Coord(x=0.5,y=0.5), 0.1, 0.0, GEO_LAYER)]
		if not USE_DRAG_ROTATE:
			self.objects[0].set_update ( lambda obj: obj.rotate(0.025) )
		self.mouse_callbacks = []
		
		self.lasttime = time.time()
		self.elapsedtime = 0.0
		self.tick = 0
		
	def update(self):
		for obj in self.objects: obj.update(obj)
		
	def time(self):
		thistime = time.time()
		d = thistime - self.lasttime
		self.lasttime = thistime
		self.elapsedtime += d
		
		if self.elapsedtime >= 0.01:
			self.elapsedtime -= 0.01
			self.update()
		self.draw()
	def init_window(self):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.window_size.x, self.window_size.y)
		glutInitWindowPosition(0, 0)
		self.window = glutCreateWindow(b'Dice Roller')
		if FULLSCREEN: glutFullScreen()
		
	def init_callback(self):
		glutDisplayFunc(lambda: self.draw())
		glutIdleFunc(lambda: self.time())
		glutMouseFunc(lambda button, state, x, y: self.mouse(button, state, x, y))
		glutPassiveMotionFunc(lambda x, y: self.mouse_motion(x, y))
		glutMotionFunc(lambda x, y: self.mouse_motion(x, y))
		glutKeyboardFunc(lambda key, x, y: self.keyboard(key, x, y))
		glutReshapeFunc(lambda w, h: self.reshape(w, h))
		
	def reshape(self, w, h):
		self.window_size.x = w
		self.window_size.y = h
	
	def mouse_motion(self, x, y):
		mouse_last_coord = self.mouse_coord if self.mouse_coord else None
		
		self.mouse_coord = coord.Coord(x=x,y=y)
		self.mouse_coord *= coord.Coord(x=1.0,y=-1.0)
		self.mouse_coord += coord.Coord(x=0,y=self.window_size.y-1)
		self.mouse_coord /= self.window_size # mouse_coord is the pixel position on screen normalized into game-space
		
		if mouse_last_coord and USE_DRAG_MOVE:
			for func in self.mouse_callbacks:
				func(self.mouse_coord - mouse_last_coord)
	
		if self.objects[0].contains(self.mouse_coord):
			self.objects[0].hover = True
		else:
			self.objects[0].hover = False
			self.objects[0].deselect()
			
	def mouse(self, button, state, x, y):
		if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
			print("mouse: right press")
		elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			print("mouse: left press")
			if self.objects[0].contains(self.mouse_coord):
				self.objects[0].select(self.mouse_coord)
				self.mouse_callbacks.append(lambda vec: self.objects[0].move(vec))
				
		elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
			print("mouse: left release")
			#if self.objects[0].contains(self.mouse_coord):
			self.objects[0].deselect()
			if len(self.mouse_callbacks) > 0:
				self.mouse_callbacks.pop()
			
	def keyboard(self, key, x, y):
		#print("key %x pressed" % key)
		if key == b'\x1b':
			print("keyboard: escape detected: exiting program")
			exit()
			
	def draw(self):
		refresh2d(1, 1, self.window_size.x, self.window_size.y)
		self.objects.sort(key=lambda obj:obj.layer)
		for obj in self.objects: obj.draw()
		glutSwapBuffers()
		
# initialization
m = mygame()
glutMainLoop() # start everything