# -*- coding: iso_8859-15 -*-

from math import pi, cos, sin

J2000 = 2451545			# epoch J2000: 12 UT on 1 Jan 2000

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
		self.Inclination = inclination
		self.AscendingNode = ascendingNode
		self.argOfPeriapsis = argOfPeriapsis
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
	if orbitData.has_key('Epoch'):
		epoch = orbitData.['Epoch']
	else:
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


