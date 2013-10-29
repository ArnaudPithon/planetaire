# -*- coding: iso_8859-15 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from orbit import CreateEllipticalOrbit

class Lumiere(dict):
	_numero = 0
	def __init__(self):
		# tester que numéro est compris entre 0 et GL_MAX_LIGHTS (au moins 8).
		self['nom'] = eval("GL_LIGHT" + str(Lumiere._numero))
		Lumiere._numero += 1

class Body:
	def __init__(self, donnees):
		self.color = donnees['color']
		self.radius = donnees['radius']
	def _set_materiau(self):
		for parametre in self.materiau.keys():
			glMaterialfv(GL_FRONT, parametre, self.materiau[parametre])
	def _drawAxe(self):
		glDisable(GL_LIGHTING)
		glLineWidth(1.0)
		glEnable(GL_LINE_STIPPLE), glLineStipple(1, 0x1C47)
		glBegin(GL_LINES)
		glColor3f(0.0, 0.5, 0.0)
		glVertex3f(0.0, -self.radius*1.5, 0.0)
		glVertex3f(0.0, self.radius*1.5, 0.0)
		glEnd()
		glDisable(GL_LINE_STIPPLE)
		glEnable(GL_LIGHTING)

class Satellite(Body):
	def __init__(self, donnees):
		Body.__init__(self, donnees)
		self.orbite = CreateEllipticalOrbit(donnees['orbitData'], 0)
		self.rotationData = donnees['rotationData']
	def __call__(self, date, drawAxe):
		self._set_materiau()
		# Positionnement par rapport à la planète
		glRotate(self.orbite.AscendingNode, 0.0, 1.0, 0.0)
		glRotate(self.orbite.Inclination, 1.0, 0.0, 0.0)
		glRotate(self.orbite.argOfPeriapsis, 0.0, 1.0, 0.0)
		position = self.orbite.positionAtTime(date)
		glTranslatef(position[0], 0.0, 0.0)
		glTranslatef(0.0, 0.0, position[1])
		# Inclinaison de l'axe des pôles
		glRotate(self.rotationData['obliquity'], 0.0, 0.0, 1.0)
		# 
		glutSolidSphere(self.radius, 16, 16)
		if drawAxe == 1: self._drawAxe()

class Planet(Body):
	def __init__(self, donnees):
		Body.__init__(self, donnees)
		self.orbite = CreateEllipticalOrbit(donnees['orbitData'], 1)
		self.rotationData = donnees['rotationData']
		if donnees.has_key('rings'):
			self.rings = donnees['rings']
			self.orb = gluNewQuadric()
		if donnees.has_key('moons'):
			self.moons = []
			for d in donnees['moons']:
				self.moons.append(Moon(d))
	def __call__(self, date, drawOrbit, drawAxe):
		self._set_materiau()
		# Positionnement par rapport à l'étoile
		glRotate(self.orbite.AscendingNode, 0.0, 1.0, 0.0)
		glRotate(self.orbite.Inclination, 1.0, 0.0, 0.0)
		glRotate(self.orbite.argOfPeriapsis, 0.0, 1.0, 0.0)
		position = self.orbite.positionAtTime(date)
		glTranslatef(position[0], 0.0, position[1])
		# Inclinaison de l'axe des pôles
		glRotate(self.rotationData['obliquity'], 0.0, 0.0, 1.0)
		# 
		glutSolidSphere(self.radius, 16, 16)
		if drawAxe == 1: self._drawAxe()
		if hasattr(self, 'rings'):
			self._drawRings()
		if hasattr(self, 'moons'):
			for moon in self.moons:
				glPushMatrix()
				moon(date, drawOrbit, drawAxe)
				glPopMatrix()
	def _drawRings(self):
		glPushMatrix()
		glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.rings['color'])
		glRotated(90, -1, 0, 0)
		gluQuadricDrawStyle(self.orb, GLU_FILL)
		gluDisk(self.orb, self.rings['inner'], self.rings['outer'], 64, 16)
		glPopMatrix()

class Star(Body):
	def __init__(self, donnees):
		Body.__init__(self, donnees)
		self.materiau = {GL_DIFFUSE: self.color}
		if donnees.has_key('planetes'):
			self.planets = []
			for d in donnees['planetes']:
				self.planets.append(Planet(d))
	def __call__(self, date, drawOrbit, drawAxe):
		if hasattr(self, 'planets'):
			for planet in self.planets:
				glPushMatrix()
				planet(date, drawOrbit, drawAxe)
				glPopMatrix()
