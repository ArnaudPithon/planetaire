#!/usr/bin/env python2
# -*- coding: iso_8859-15 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, os
from math import cos, sin, radians, sqrt
from time import time, sleep
from ssolar import *

ESCAPE = '\033'

Cos = [cos(radians(angle)) for angle in range(0, 360)]
Sin = [sin(radians(angle)) for angle in range(0, 360)]

class Lumiere(dict):
	_numero = 0
	def __init__(self):
		# tester que numéro est compris entre 0 et GL_MAX_LIGHTS (au moins 8).
		self['nom'] = eval("GL_LIGHT" + str(Lumiere._numero))
		Lumiere._numero += 1

class Ssolar:
	def __init__(self, lum, etoile):
		self.DISTANCE_MAX = 1000000
		self.b_gauche = self.b_droit = self.b_milieu = 0
		self.lastx = self.lasty = 0
		self.theta, self.phi, self.R = -42, 21, 200
		self.tx, self.ty, self.tz = 0.0, 0.0, 0.0	# coordonées ciblée par la caméra
		self.camtarget = soleil
		self.drawOrbit, self.drawAxe = 0, 0

		self.lumieres = lum
		self.etoile = etoile

		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
#		glutInitWindowPosition(200, 200)
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

		def creeRepere():
			self.repere = glGenLists(1)
			glNewList(self.repere, GL_COMPILE)
			glDisable(GL_LIGHTING)
			glLineWidth(1.0)
			glBegin(GL_LINES)
			glColor3f(1.0, 0.0, 0.0)
			glVertex3f(0.0, 0.0, 0.0)
			glVertex3f(1.0, 0.0, 0.0)
			glColor3f(0.0, 1.0, 0.0)
			glVertex3f(0.0, 0.0, 0.0)
			glVertex3f(0.0, 1.0, 0.0)
			glColor3f(0.0, 0.0, 1.0)
			glVertex3f(0.0, 0.0, 0.0)
			glVertex3f(0.0, 0.0, 1.0)
			glEnd()
			glEnable(GL_LIGHTING)
			glEndList()
		creeRepere()

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
		if args[0] == "1":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "2":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "3":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "4":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "5":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "6":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "7":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "8":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "9":
			self.camtarget = self.etoile.planetes[int(args[0]) -1]
			print self.camtarget
		if args[0] == "0":
			self.camtarget = soleil
		glutPostRedisplay()

	def _on_idle(self):
		for planete in self.etoile.planetes:
			planete.updatePosition()
		glutPostRedisplay()
		sleep(1e-4)
	
	def _on_display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		
		gluLookAt(0, 0, self.R,
				self.tx, self.ty, self.tz, 0.0, 1.0, 0.0)
		
		glRotatef(self.phi, 1.0, 0.0, 0.0)
		glRotatef(self.theta, 0.0, 1.0, 0.0)

		for lumiere in self.lumieres:
			glLightfv(lumiere['nom'], GL_POSITION, lumiere['parametres'][GL_POSITION])
		
	#	glPushMatrix()
	#	glScalef(40.0, 40.0, 40.0)
	#	glCallList(self.repere)
	#	glPopMatrix()
		self.etoile()
		for planete in self.etoile.planetes:
			glPushMatrix()
			planete(self.drawOrbit, self.drawAxe)
			glPopMatrix()

		glutSwapBuffers()

if __name__ == '__main__':
	from optparse import OptionParser
	usage = "usage: %prog [options]"
	parser = OptionParser(usage, version="%prog 0.2")
	(options, args) = parser.parse_args()
	glutInit(sys.argv)
	
	lumiere0 = Lumiere()
	lumiere0['parametres'] = {GL_POSITION: (0.0, 0.0, 0.0, 1),
		GL_DIFFUSE: (1.0, 1.0, 1.0, 1.0),
		GL_SPECULAR: (1.0, 1.0, 1.0)}
	lumieres = [lumiere0]
	
	soleil = Sun()
	mercure = Mercury()
	venus = Venus()
	terre = Earth()
	lune = Lune()
	terre.moons = (lune, )
	mars = Mars()
	jupiter = Jupiter()
	io = Io()
	europa = Europa()
	ganymede = Ganymede()
	callisto = Callisto()
	jupiter.moons = (io, europa, ganymede, callisto)
	saturne = Saturn()
	uranus = Uranus()
	neptune = Neptune()
	pluton = Pluto()
	soleil.planetes = (mercure, venus, terre, mars,
			jupiter, saturne, uranus, neptune, pluton)

	teapot = Ssolar(lumieres, soleil)
	
	glutMainLoop()
