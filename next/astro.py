# -*- coding: iso_8859-15 -*-

# Constantes
SOLAR_ABSMAG  = 4.83
LN_MAG        = 1.085736
LY_PER_PARSEC = 3.26167
KM_PER_LY     = 9466411842000.000
KM_PER_AU     = 149597870.7
AU_PER_LY     = (KM_PER_LY / KM_PER_AU)

Mean_sidereal_day = 86164.09054 # s (= 23:56:04.09054)
Sidereal_year     = 365.25636   # d
G = 6.67259e-11 # N m^2 / kg^2 (Gravitational_constant)
c = 299792.458 # km/s (Speed of light)
J2000 = 2451545.0   # epoch J2000: 12    UT on  1 Jan 2000
B1950 = 2433282.423 # epoch B1950: 22:09 UT on 21 Dec 1949

def lightYears2Parsecs(ly):
	return ly / LY_PER_PARSEC

def parsecs2LightYears(pc):
	return pc * LY_PER_PARSEC

def lightYears2Kilometers(ly):
	return ly * KM_PER_LY

def kilometers2LightYears(km):
	return km / KM_PER_LY

def lightYears2AU(ly):
	return ly * AU_PER_LY

def AU2LightYears(au):
	return au / AU_PER_LY

def AU2Kilometers(au):
	return au * KM_PER_AU

def kilometers2AU(km):
	return km / KM_PER_AU

