# -*- coding: iso_8859-15 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from bodyStelar import *

class Sun(Star):
	def __init__(self):
		Star.__init__(self)
		self.materiau[GL_EMISSION] = (1.0, 1.0, 0.5)
		self.distance = 0
		self.mass = 1.989e30
		self.temperature = 5780.0
		self.radius = 696000

class Mercury(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.84, 0.71, 0.52)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 2#2440				# km
		self.ellipticalOrbit = {
			'Period': 0.2408,				# Année (* 365.25 jours)
			'SemiMajorAxis': 0.3871,		# AU
			'Eccentricity': 0.2056,			# AU
			'Inclination': 7.0049,			# degrees
			'AscendingNode': 48.33167,		# degrees
			'LongOfPericenter': 77.456,
			'MeanLongitude': 252.251}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 1407.509405	# heures (/ 24.0 heures)
		self.obliquity = 7.01

class Venus(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.62, 0.33, 0.07)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 4#6052
		self.ellipticalOrbit = {
			'Period': 0.6152,
			'SemiMajorAxis': 0.7233,
			'Eccentricity': 0.0068,
			'Inclination': 3.3947,
			'AscendingNode': 76.681,
			'LongOfPericenter': 131.533,
			'MeanLongitude': 181.979}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 5832.479839
		self.obliquity = 178.78

class Earth(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.17, 0.22, 0.29)
		self.materiau[GL_DIFFUSE]= self.couleur
		self.mass = 5.976e24
		self.radius = 5#6378

		self.ellipticalOrbit = {
			'Period': 1.0,	#
			'SemiMajorAxis': 1.0,	#
			'Eccentricity': 0.0167,
			'Inclination': 0.0001,	#
			'AscendingNode': 348.739,	#
			'LongOfPericenter': 102.947,
			'MeanLongitude': 100.464}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 23.9344694
		self.obliquity = -23.45

class Lune(Moon):
	def __init__(self):
		Moon.__init__(self)
		self.materiau[GL_DIFFUSE]= (0.5, 0.5, 0.5)
		self.mass = 7.354e22
		self.radius = 1.7#1737.53
		
		self.ellipticalOrbit = {
			'Period': 27.321661,		# jours
			'SemiMajorAxis': 384400,	# km
			'Eccentricity': 0.054900,
			'Inclination': 5.15}
		self._calcRevolutionOffset()
		self.distance = 10.0

		self.obliquity = 23.45

class Mars(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.83, 0.45, 0.21)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 3#3394
		self.ellipticalOrbit = {
			'Period': 1.8809,
			'SemiMajorAxis': 1.5237,
			'Eccentricity': 0.0934,
			'Inclination': 1.8506,
			'AscendingNode': 49.479,
			'LongOfPericenter': 336.041,
			'MeanLongitude': 355.453}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 24.622962
		self.obliquity = 26.72

class Jupiter(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.64, 0.60, 0.57)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 9#71398
		self.ellipticalOrbit = {
			'Period': 11.8622,
			'SemiMajorAxis': 5.2034,
			'Eccentricity': 0.0484,
			'Inclination': 1.3053,
			'AscendingNode': 100.556,
			'LongOfPericenter': 14.7539,
			'MeanLongitude': 34.404}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 9.927953
		self.obliquity = 2.222461

class Io(Moon):
	def __init__(self):
		Moon.__init__(self)
		self.materiau[GL_DIFFUSE]= (0.5, 0.5, 0.5)
		self.distance = 12.0
		self.radius = 1.8#1821.6
		self.ellipticalOrbit = {'Epoch': 2443000.00038375,
			'Period': 1.769138,
			'SemiMajorAxis': 421600,
			'Eccentricity': 0.0041,
			'Inclination': 0.040,
			'AscendingNode': 312.981,
			'LongOfPericenter': 97.735,
			'MeanLongitude': 106.724}
		self._calcRevolutionOffset()
		self.obliquity = 0.0
class Europa(Moon):
	def __init__(self):
		Moon.__init__(self)
		self.materiau[GL_DIFFUSE]= (0.5, 0.5, 0.5)
		self.distance = 12.0
		self.radius = 1.5#1560.8
		self.ellipticalOrbit = {'Epoch': 2443000.00038375,
			'Period': 3.551810,
			'SemiMajorAxis': 670900,
			'Eccentricity': 0.0101,
			'Inclination': 0.470,
			'AscendingNode': 101.087,
			'LongOfPericenter': 155.512,
			'MeanLongitude': 176.377}
		self._calcRevolutionOffset()
		self.obliquity = 0.0
class Ganymede(Moon):
	def __init__(self):
		Moon.__init__(self)
		self.materiau[GL_DIFFUSE]= (0.5, 0.5, 0.5)
		self.distance = 12.0
		self.radius = 2.6#2631.2
		self.ellipticalOrbit = {'Epoch': 2443000.00038375,
			'Period': 7.154553,
			'SemiMajorAxis': 1070000,
			'Eccentricity': 0.0015,
			'Inclination': 0.195,
			'AscendingNode': 119.841,
			'LongOfPericenter': 188.831,
			'MeanLongitude': 121.206}
		self._calcRevolutionOffset()
		self.obliquity = 0.1
class Callisto(Moon):
	def __init__(self):
		Moon.__init__(self)
		self.materiau[GL_DIFFUSE]= (0.5, 0.5, 0.5)
		self.distance = 12.0
		self.radius = 2.4#2410.3
		self.ellipticalOrbit = {'Epoch': 2443000.00038375,
			'Period': 16.689018,
			'SemiMajorAxis': 1883000,
			'Eccentricity': 0.007,
			'Inclination': 0.281,
			'AscendingNode': 323.265,
			'LongOfPericenter': 335.933,
			'MeanLongitude': 85.091}
		self._calcRevolutionOffset()
		self.obliquity = 0.4

class Saturn(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.95, 0.77, 0.52)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 8#60330
		self.ellipticalOrbit = {
			'Period': 29.4577,
			'SemiMajorAxis': 9.5371,
			'Eccentricity': 0.0542,
			'Inclination': 2.4845,
			'AscendingNode': 113.715,
			'LongOfPericenter': 92.432,
			'MeanLongitude': 49.944}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 10.65622
		self.obliquity = 28.049
		self.rings = {
			"inner": 74658,
			"outer": 140000,
			"color": (1.0, 0.88, 0.82)}

class Uranus(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.61, 0.73, 0.77)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 7#26200
		self.ellipticalOrbit = {
			'Period': 84.0139,
			'SemiMajorAxis': 19.1913,
			'Eccentricity': 0.0472,
			'Inclination': 0.7699,
			'AscendingNode': 74.230,
			'LongOfPericenter': 170.964,
			'MeanLongitude': 313.232}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 17.24
		self.obliquity = 97.81
		self.rings = {
			"inner": 41800,
			"outer": 51149}

class Neptune(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.375, 0.53, 0.91)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 6#25225
		self.ellipticalOrbit = {
			'Period': 164.793,
			'SemiMajorAxis': 30.0690,
			'Eccentricity': 0.0086,
			'Inclination': 1.7692,
			'AscendingNode': 131.722,
			'LongOfPericenter': 44.971,
			'MeanLongitude': 304.880}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 16.11
		self.obliquity = 28.03

class Pluto(Planet):
	def __init__(self):
		Planet.__init__(self)
		self.couleur = (0.46, 0.5, 0.57)
		self.materiau[GL_DIFFUSE]= self.couleur
		
		self.radius = 1#1137
		self.ellipticalOrbit = {
			'Period': 248.54,
			'SemiMajorAxis': 39.48168677,
			'Eccentricity': 0.24880766,
			'Inclination': 17.14175,
			'AscendingNode': 110.30347,
			'LongOfPericenter': 224.06776,
			'MeanLongitude': 238.92881}
		self._calcRevolutionOffset()
		self._calcDistance()
		
		self.rotationPeriod = 153.293904
		self.obliquity = 115.60
