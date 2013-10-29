#!/usr/bin/env python

from math import pi, cos, sin, sqrt, radians, degrees, acos, asin, cosh, sinh
from time import time, sleep

J2000 = 2451545.0

def AUtoKilometers(au):
	KM_PER_AU = 149597870.7
	return au * KM_PER_AU

Mercure_orbitData = {\
		'Period'           : 0.2408,
		'SemiMajorAxis'    : 0.3871,
		'Eccentricity'     : 0.2056,
		'Inclination'      : 7.0049,
		'AscendingNode'    : 48.33167,
		'LongOfPericenter' : 77.456,
		'MeanLongitude'    : 252.251}

Earth_orbitData = {\
		'Period'           : 1.0,
		'SemiMajorAxis'    : 1.0,
		'Eccentricity'     : 0.0167,
		'Inclination'      : 0.0001,
		'AscendingNode'    : 348.739,
		'LongOfPericenter' : 102.947,
		'MeanLongitude'    : 100.464}

def CreateEllipticalOrbit(orbitData, usePlanetUnits):
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



def SolveKeplerFunc1(ecc, M, x):
	"""Standard iteration for solving Kepler's Equation"""
	return M + ecc * sin(x)

def SolveKeplerFunc2(ecc, M, x):
	"""Faster converging iteration for Kepler's Equation; more efficient\n
than above for orbits with eccentricities greater than 0.3."""
	return x + (M + ecc * sin(x) - x) / (1 - ecc * cos(x))

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
		self.BoundingRadius = pericenterDistance * ((1.0 + eccentricity) / (1.0 - eccentricity))
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
	#	R = sqrt(x**2 + z**2)
	#	A = degrees(asin(x/R))
	#	if acos(z/R) < -1: A *= -1
	#	return R, A
	##	R = (yrotation(ascendingNode) *
	##			xrotation(inclination) *
	##			yrotation(argOfPeriapsis))
	##	return R * Point3d(x, 0, z)
	def positionAtTime(self, t):
		"""Return the offset from the center"""
		t = t - self.epoch
		meanMotion = 2.0 * pi / self.period
		meanAnomaly = (self.meanAnomalyAtEpoch + t * meanMotion) % (2*pi)
		E = self._eccentricAnomaly(meanAnomaly)
		print meanMotion, self.meanAnomalyAtEpoch, E
		return self._positionAtE(E)

def testonrange(donnees):
	a = CreateEllipticalOrbit(donnees, 1)
	Rmin, Rmax = 10e12, 0
	Amin, Amax = 360, 0
	for t in range(2451545, 2451545+365):
		rayon, angle = a.positionAtTime(t)
		if rayon < Rmin: Rmin = rayon
		if rayon > Rmax: Rmax = rayon
		if angle < Amin: Amin = angle
		if angle > Amax: Amax = angle
	#	print "%d : %f | %f" % (t, rayon, angle)
	print "min : %f | %f\nmax : %f | %f" % (Rmin, Amin, Rmax, Amax)

def test(donnees):
	a = CreateEllipticalOrbit(donnees, 1)
	t = time() / 86400
	rayon, angle = a.positionAtTime(t)
	print t, rayon, angle

#test(Mercure_orbitData)
testonrange(Earth_orbitData)

def oldtest():
	Rmin, Rmax = 4096, -4096
	Amin, Amax = 360, 0
	t0 = time() / 86400
	for t in range(0, 365):
		x, z = positionAtTime(t)
		R = sqrt(x**2 + z**2)
		A = degrees(acos(x))
		if   R < Rmin: Rmin = R
		elif R > Rmax: Rmax = R
		if   A < Amin: Amin = A
		elif A > Amax: Amax = A
	print "%f - %f | %f - %f" % (Rmin, Rmax, Amin, Amax)
