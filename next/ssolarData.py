# -*- coding: iso_8859-15 -*-

# = {\
#		'color': ,
#		'radius': , # km
#		'mass': ,   # * 1e23 kg
#		'orbitData': {\
#				'Period': , # Années
#				'SemiMajorAxis': ,
#				'Eccentricity': ,
#				'Inclination': ,
#				'AscendingNode': ,
#				'LongOfPericenter': ,
#				'MeanLongitude': }
#		'rotationData': {\
#				'Period': , # heures
#				'obliquity': }
#}

mercury = {\
		'name': "Mercury",
		'color': (0.84, 0.71, 0.52),
		'radius': 2440,
		'mass': 3.302e23,
		'orbitData': {\
				'Period'           : 0.2408,
				'SemiMajorAxis'    : 0.3871,
				'Eccentricity'     : 0.2056,
				'Inclination'      : 7.0049,
				'AscendingNode'    : 48.33167,
				'LongOfPericenter' : 77.456,
				'MeanLongitude'    : 252.251},
		'rotationData': {\
				'Period': 1407.509405,
				'obliquity': 7.01},
		'mythology': "Dieu des commerçants, des voyageurs et des voleurs, \
il est l'équivalent Romain du dieu Grecque Hermes, le messager des dieus.",
		'otherNames': (("Apollo", "as morning star"),
				("Hermes", "as evening star"))
}

venus = {\
		'name': "Venus",
		'color': (0.62, 0.33, 0.07),
		'radius': 6051.84,
		'mass': 48.685e23,
		'orbitData': {\
				'Period': 0.6152,
				'SemiMajorAxis': 0.7233,
				'Eccentricity': 0.0068,
				'Inclination': 3.3947,
				'AscendingNode': 76.681,
				'LongOfPericenter': 131.533,
				'MeanLongitude': 181.979},
		'rotationData': {\
				'Period': 5832.479839,
				'obliquity': 178.78},
		'mythology': "Déesse de l'amour et de la beauté",
		'otherNames': (("Aphrodite", "by Greek"),
				("Ishtar", "by Babylonian"),
				("Eosphorus", "as morning star"),
				("Hesperus", "as evening star"))
}

moon = {\
		'name': 'Moon',
		'color': (0.5, 0.5, 0.5),
		'radius': 1737.53,
		'mass': 7.354e22,
		'orbitData': {\
				'Period': 27.321661,
				'SemiMajorAxis': 384400,
				'Eccentricity': 0.054900,
				'Inclination': 5.15},
		'rotationData': {\
				'obliquity': 23.45}
}

earth = {\
		'name': "Earth",
		'color': (0.17, 0.22, 0.29),
		'radius': 6378,	# 6371.01
		'mass': 5.976e24,	# 59.736e23
		'orbitData': {\
				'Period'           : 1.0,
				'SemiMajorAxis'    : 1.0,
				'Eccentricity'     : 0.0167,
				'Inclination'      : 0.0001,
				'AscendingNode'    : 348.739,
				'LongOfPericenter' : 102.947,
				'MeanLongitude'    : 100.464},
		'rotationData': {\
				'Period': 23.9344694,
				'obliquity': -23.45},
		'moons': (moon, )
}

mars = {\
		'name': "Mars",
		'color': (0.83, 0.45, 0.21),
		'radius': 3394,	# 3389.92
		'mass': 6.4185e23,
		'orbitData': {\
				'Period': 1.8809,
				'SemiMajorAxis': 1.5237,
				'Eccentricity': 0.0934,
				'Inclination': 1.8506,
				'AscendingNode': 49.479,
				'LongOfPericenter': 336.041,
				'MeanLongitude': 355.453},
		'rotationData': {\
				'Period': 24.622962,
				'obliquity': 26.72}
}

io = {\
		'name': 'Io',
		'color': (0.5, 0.5, 0.5),
		'radius': 1821.6,
		'orbitData': {\
				'Epoch': 2443000.00038375,
				'Period': 1.769138,
				'SemiMajorAxis': 421600,
				'Eccentricity': 0.0041,
				'Inclination': 0.040,
				'AscendingNode': 312.981,
				'LongOfPericenter': 97.735,
				'MeanLongitude': 106.724},
		'rotationData': {\
				'obliquity': 0.0}
}

jupiter = {\
		'name': "Jupiter",
		'color': (0.64, 0.60, 0.57),
		'radius': 71398,	# 69911
		'mass': 18986e23,
		'orbitData': {\
				'Period': 11.8622,
				'SemiMajorAxis': 5.2034,
				'Eccentricity': 0.0484,
				'Inclination': 1.3053,
				'AscendingNode': 100.556,
				'LongOfPericenter': 14.7539,
				'MeanLongitude': 34.404},
		'rotationData': {\
				'Period': 9.927953,
				'obliquity': 2.222461},
		'moons': (io, )#'europa', 'ganymede', 'callisto')
}

saturn = {\
		'name': "Saturn",
		'color': (0.95, 0.77, 0.52),
		'radius': 60330,	# 58232
		'mass': 5684.6e23,
		'orbitData': {\
				'Period': 29.4577,
				'SemiMajorAxis': 9.5371,
				'Eccentricity': 0.0542,
				'Inclination': 2.4845,
				'AscendingNode': 113.715,
				'LongOfPericenter': 92.432,
				'MeanLongitude': 49.944},
		'rotationData': {\
				'Period': 10.65622,
				'obliquity': 28.049},
		'rings': {\
				"inner": 74658,
				"outer": 140000,
				"color": (1.0, 0.88, 0.82)}
}

uranus = {\
		'name': "Uranus",
		'color': (0.61, 0.73, 0.77),
		'radius': 26200,	# 25362
		'mass': 868.32e23,
		'orbitData': {\
				'Period': 84.0139,
				'SemiMajorAxis': 19.1913,
				'Eccentricity': 0.0472,
				'Inclination': 0.7699,
				'AscendingNode': 74.230,
				'LongOfPericenter': 170.964,
				'MeanLongitude': 313.232},
		'rotationData': {\
				'Period': 17.24,
				'obliquity': 97.81},
		'rings': {\
				'inner': 41800,
				'outer': 51149}
}

neptune = {\
		'name': "Neptune",
		'color': (0.375, 0.53, 0.91),
		'radius': 25225,	# 24624
		'mass': 1024.3e23,
		'orbitData': {\
				'Period': 164.793,
				'SemiMajorAxis': 30.0690,
				'Eccentricity': 0.0086,
				'Inclination': 1.7692,
				'AscendingNode': 131.722,
				'LongOfPericenter': 44.971,
				'MeanLongitude': 304.880},
		'rotationData': {\
				'Period': 16.11,
				'obliquity': 28.03}
}

pluto = {\
		'name': "Pluto",
		'color': (0.46, 0.5, 0.57),
		'radius': 1137,	# 1151
		'mass': .1314e23,
		'orbitData': {\
				'Period': 248.54,
				'SemiMajorAxis': 39.48168677,
				'Eccentricity': 0.24880766,
				'Inclination': 17.14175,
				'AscendingNode': 110.30347,
				'LongOfPericenter': 224.06776,
				'MeanLongitude': 238.92881},
		'rotationData': {\
				'Period': 153.293904,
				'obliquity': 115.60}
}

sun = {\
		'name': "Sun",
		'color': (1.0, 1.0, 0.5),
		'radius': 696000,
		'mass': 1.989e30,
		'temperature': (5780, 15600000),	# ° Kelvin
		'otherNames': (("Helios", "by Greeks"),
				("sol", "by Romans")),
		'planetes': (\
				mercury,
				venus,
				earth,
				mars,
				jupiter,
				saturn,
				uranus,
				neptune,
				pluto)
}
