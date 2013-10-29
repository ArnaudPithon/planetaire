# -*- coding: iso_8859-15 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pi
from fonctions import *

speedOfLight = 299792.458	# km/s
J2000 = 2451545.0			# epoch J2000: 12 UT on 1 Jan 2000
G = 6.672e-11				# N meters^2 / kg^2

epoch = J2000

# Body
# Star; Planet; Moon; Comet; Asteroid; Spacecraft

class EllipticalOrbit:
	def __init__(self,
			pericenterDistance,
			eccentricity,
			inclination,
			ascendingNode,
			argOfPeriapsis,
			meanAnomalyAtEpoch,
			period,
			epoch):
		self.pericenterDistance = pericenterDistance
		self.eccentricity = eccentricity
		self.meanAnomalyAtEpoch = meanAnomalyAtEpoch
		self.period = period
		self.epoch = epoch
	def _solve_iteration_fixed(self, f, x0, maxIter):
		"""Solve using iteration method and a fixed number of steps."""
		x = 0
		x2 = x0
		M = x0	#
		for i in range(0, maxIter):
			x = x2
			x2 = f(self.eccentricity, M, x)
		return x2, x2 - x
	def _eccentricAnomaly(self, M):
		if self.eccentricity == 0.0: # Circular orbit
			return M
		elif self.eccentricity < 0.2: # Low eccentricity, so use the standard iteration technique
			sol = self._solve_iteration_fixed(SolveKeplerFunc1, M, 5)
			return sol[0]
		elif self.eccentricity < 0.9:
			sol = self._solve_iteration_fixed(SolveKeplerFunc2, M, 6)
			return sol[0]
	def _positionAtE(self, E):
		if self.eccentricity < 1.0:
			a = self.pericenterDistance / (1.0 - self.eccentricity)
			x = a * (cos(E) - self.eccentricity)
			z = a * sqrt(1 - self.eccentricity**2) * -sin(E)
		elif self.eccentricity > 1.0:
			a = self.pericenterDistance / (1.0 - self.eccentricity)
			x = -a * (self.eccentricity - cosh(E))
			z = -a * sqrt(self.eccentricity**2 - 1) * -sinh(E)
		else:
			x, z = 0.0, 0.0
		return x, z
	def positionAtTime(self, t):
		"""Return the offset from the center"""
		t = t - self.epoch
		meanMotion = 2.0 * pi / self.period
		meanAnomaly = (self.meanAnomalyAtEpoch + t * meanMotion) % (2*pi)
		E = self._eccentricAnomaly(meanAnomaly)
		print meanMotion, self.meanAnomalyAtEpoch, E
		return self._positionAtE(E)

class Repere:
	def __init__(self):
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
	def __call__(self, taille=1.0):
		glPushMatrix()
		glScalef(taille, taille, taille)
		glCallList(self.repere)
		glPopMatrix()
axes = Repere()

class Body:
	def __init__(self):
		self.materiau = {
			GL_AMBIENT: (0.2, 0.2, 0.2, 1.0),
			GL_DIFFUSE: (0.8, 0.8, 0.8, 1.0),
			GL_SPECULAR: (0, 0, 0, 1),
			GL_EMISSION: (0, 0, 0, 1),
			GL_SHININESS: 0}
	def _set_materiau(self):
		for parametre in self.materiau.keys():
			glMaterialfv(GL_FRONT, parametre, self.materiau[parametre])
	def CreateEllipticalOrbit(self, orbitData, usePlanetUnits):
		period = orbitData['Period']
		semiMajorAxis = orbitData['SemiMajorAxis']
		eccentricity  = orbitData['Eccentricity']
		inclination = orbitData['Inclination']
		longOfPericenter = orbitData['LongOfPericenter']
		ascendingNode = orbitData['AscendingNode']
		if orbitData.has_key('ArgOfPericenter'):
			argOfPericenter = orbitData['ArgOfPericenter']
		else:
			argOfPericenter = longOfPericenter - ascendingNode
		longAtEpoch = orbitData['MeanLongitude']
		if orbitData.has_key('MeanAnomaly'):
			anomalyAtEpoch = orbitData['MeanAnomaly']
		else:
			anomalyAtEpoch = longAtEpoch - (argOfPericenter + ascendingNode)
		pericenterDistance = semiMajorAxis * (1.0 - eccentricity)
		epoch = J2000
		if usePlanetUnits:
			semiMajorAxis = AUtoKilometers(semiMajorAxis)
			pericenterDistance = AUtoKilometers(pericenterDistance)
			period = period * 365.25
		return EllipticalOrbit(\
				pericenterDistance,
				eccentricity,
				radians(inclination),
				radians(ascendingNode),
				radians(argOfPericenter),
				radians(anomalyAtEpoch),
				period,
				epoch)

class Star(Body):
	def __init__(self):
		Body.__init__(self)
		self.materiau[GL_DIFFUSE]= (0, 0, 0)
	def __call__(self):
		self._set_materiau()
		glutSolidSphere(2.0, 32, 32)

class Planet(Body):
	def __init__(self):
		Body.__init__(self)
		self.moons = ()
		self.theta = 0
		self.orb = gluNewQuadric()
	def __call__(self, drawOrbit, drawAxe):
		self._set_materiau()
		# Positionnement par rapport à l'étoile
		glRotate(self.ellipticalOrbit['AscendingNode'], 0.0, 1.0, 0.0)
		glRotate(self.ellipticalOrbit['Inclination'], 1.0, 0.0, 0.0)
		glRotate(self.theta, 0.0, 1.0, 0.0)
		if drawOrbit == 1: self._drawOrbit()
		glTranslatef(self.distance, 0.0, 0.0)
		# Inclinaison de l'axe des pôles
		glRotate(self.obliquity, 0.0, 0.0, 1.0)
		# 
		glutSolidSphere(self.radius, 16, 16)
		if hasattr(self, "rings"):
			self._drawRings()
		for moon in self.moons:
			glPushMatrix()
			moon()
			glPopMatrix()
		if drawAxe == 1: self._drawAxe()
	def updatePosition(self):
		self.theta = (self.theta + self.revolutionOffset) % 360
		for moon in self.moons:
			moon.updatePosition()
	def _calcDistance(self):
		self.distance = 40.0 * self.ellipticalOrbit['SemiMajorAxis']
	def _calcRevolutionOffset(self):
		period = self.ellipticalOrbit['Period'] * 365.25
		self.revolutionOffset = 2*pi / period
	def _drawOrbit(self):
		glPushMatrix()
		glDisable(GL_LIGHTING)
		glColor3fv(self.couleur)
		glRotated(90, -1, 0, 0)
		gluQuadricDrawStyle(self.orb, GLU_SILHOUETTE)
		gluDisk(self.orb, self.distance, self.distance, 64, 1)
		glEnable(GL_LIGHTING)
		glPopMatrix()
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
	def _drawRings(self):
		glPushMatrix()
		if self.rings.has_key('color'):
			glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.rings['color'])
		glRotated(90, -1, 0, 0)
		gluQuadricDrawStyle(self.orb, GLU_FILL)
	#	gluDisk(self.orb, self.rings['inner'], self.rings['outer'], 64, 16)
		gluDisk(self.orb, self.radius*1.5, self.radius*2.5, 64, 1)
		glPopMatrix()


class Moon(Body):
	def __init__(self):
		Body.__init__(self)
		self.theta = 0
	def __call__(self):
		self._set_materiau()
		# 
		glRotate(self.ellipticalOrbit['Inclination'], 0.0, 0.0, 1.0)
		glRotate(self.theta, 0.0, 1.0, 0.0)
		glTranslatef(self.distance, 0.0, 0.0)
		# 
		glRotate(self.obliquity, 0.0, 0.0, 1.0)
		# 
		glutSolidSphere(0.5, 12, 12)
	def _calcRevolutionOffset(self):
		period = self.ellipticalOrbit['Period']
		self.revolutionOffset = 2*pi / period
	def updatePosition(self):
		self.theta = (self.theta + self.revolutionOffset) % 360

