
from math import cos, sin

def AUtoKilometers(au):
	KM_PER_AU = 149597870.7
	return au * KM_PER_AU

def SolveKeplerFunc1(ecc, M, x):
	"""Standard iteration for solving Kepler's Equation"""
	return M + ecc * sin(x)

def SolveKeplerFunc2(ecc, M, x):
	"""Faster converging iteration for Kepler's Equation; more efficient\n
than above for orbits with eccentricities greater than 0.3."""
	return x + (M + ecc * sin(x) - x) / (1 - ecc * cos(x))


