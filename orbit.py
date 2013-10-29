def positionAtTime(t):
	t = t - epoch
	meanMotion = 2.0 * pi / period
	meanAnomaly = meanAnomalyAtEpoch + t * meanMotion
	E = eccentricAnomaly(meanAnomaly)

	return positionAtE(E)
