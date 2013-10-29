#!/usr/bin/env python
# -*- coding: iso_8859-15 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, os
from math import cos, sin, radians, sqrt
from time import time, sleep

ESCAPE = '\033'

class System:
	def __init__(self, lum, etoile):
		self.DISTANCE_MAX = 1000000
		self.b_gauche = self.b_droit = self.b_milieu = 0
		self.lastx = self.lasty = 0
		self.theta, self.phi, self.R = -42, 21, 200
		self.drawOrbit, self.drawAxe = 0, 0
		self.lumieres = lum
		self.etoile = etoile

		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutInitWindowSize(400, 400)
		glutCreateWindow(os.path.basename(sys.argv[0]))


		glClearColor(0.0, 0.0, 0.0, 0.0)
		glColor3f(1.0, 1.0, 1.0)
		glEnable(GL_DEPTH_TEST)

		glShadeModel(GL_SMOOTH)
		glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
		glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
		glEnable(GL_LIGHTING)
		for lumiere in self.lumieres:
			glEnable(lumiere['nom'])
			for parametre in lumiere['parametres'].keys():
				glLightfv(lumiere['nom'], parametre, lumiere['parametres'][parametre])

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, 1.0, 0.1, self.DISTANCE_MAX)
		glMatrixMode(GL_MODELVIEW)

		self._callbacks()

	def _callbacks(self):
		"""Affectation des fonctions de rappel"""
		glutDisplayFunc(self._on_display)
		glutIdleFunc(self._on_idle)
		glutReshapeFunc(self._on_reshape)
		glutKeyboardFunc(self._on_keyboard)
		glutMouseFunc(self._on_mouse)
		glutMotionFunc(self._on_mousemotion)
#		glutPassiveMotionFunc(self._on_motion)

	def _on_reshape(self, largeur, hauteur):
		if hauteur == 0: hauteur = 1
		glViewport(0, 0, largeur, hauteur)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(largeur)/float(hauteur), 0.1, self.DISTANCE_MAX)
		glMatrixMode(GL_MODELVIEW)

	def _on_mouse(self, bouton, etat, x , y):
		if bouton == GLUT_LEFT_BUTTON and etat == GLUT_UP:
			self.b_gauche = 0
		elif bouton == GLUT_LEFT_BUTTON and etat == GLUT_DOWN:
			self.b_gauche = 1
			self.lastx, self.lasty = x, y
		
		if bouton == GLUT_RIGHT_BUTTON and etat == GLUT_UP:
			self.b_droit = 0
		elif bouton == GLUT_RIGHT_BUTTON and etat == GLUT_DOWN:
			self.b_droit = 1
			self.lastx, self.lasty = x, y
		
		if bouton == GLUT_MIDDLE_BUTTON and etat == GLUT_UP:
			self.b_milieu = 0
		elif bouton == GLUT_MIDDLE_BUTTON and etat == GLUT_DOWN:
			self.b_milieu = 1
			self.lastx, self.lasty = x, y

	def _on_mousemotion(self, x, y):
		if self.b_gauche:
			self.theta = (self.theta + (x - self.lastx)) % 360
	#	elif self.b_milieu:
			self.phi = (self.phi + (y - self.lasty)) % 360
		glutPostRedisplay()
		self.lastx, self.lasty = x, y

	def _on_keyboard(self, *args):
		if args[0] == ESCAPE or args[0] == "q": sys.exit()
		if args[0] == "z": self.R -= 5
		if args[0] == "s": self.R += 5
		if args[0] == "o": self.drawOrbit = (self.drawOrbit + 1) % 2
		if args[0] == "a": self.drawAxe = (self.drawAxe + 1) % 2
		glutPostRedisplay()

	def _on_display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		
		gluLookAt(0, 0, self.R,
				self.tx, self.ty, self.tz, 0.0, 1.0, 0.0)
		
		glRotatef(self.phi, 1.0, 0.0, 0.0)
		glRotatef(self.theta, 0.0, 1.0, 0.0)

		for lumiere in self.lumieres:
			glLightfv(lumiere['nom'], GL_POSITION, lumiere['parametres'][GL_POSITION])



		glutSwapBuffers()

if __name__ == '__main__':
	from optparse import OptionParser
	usage = "usage: %prog [options]"
	parser = OptionParser(usage, version="%prog 0.2")
	(options, args) = parser.parse_args()
	glutInit(sys.argv)

