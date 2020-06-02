import sys
import math
import pygame

# AP Physics C Final Project
# Universal Gravitation Simulation
# Jules Goduco-Bunting


# Universal Gravitational Constant (m^3/(kg*s^2))
G = 6.67408 * (10 ** -11)

# Astronomical Unit (meters)
AU = 1.495978707 * (10 ** 11)
SCALE = 300 / AU


class Mass:
	def __init__(self, name, m, x, y, vx, vy, r):
		self.name = name
		self.mass = m
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.radius = r

	def net_force(self, other):
		dx = self.x - other.x
		dy = self.y - other.y
		d = math.sqrt(dx**2 + dy**2)

		# Check for collisions
		if d == 0:
			raise Exception('Collision between {} and {},'.format(self.name, other.name))

		f = G * self.mass * other.mass / (d ** 2)  # Universal Force of Gravity: F = (G * m1 * m2) / (r^2)
		theta = math.atan2(dy, dx)  # Calculate angle of force to get component vectors
		fx = f * math.cos(theta)
		fy = f * math.sin(theta)

		return -fx, -fy


class Simulation:
	def __init__(self, spf, masses, size=(1280,720), fps=60, scale=SCALE):
		self.spf    = spf   # seconds per frame
		self.masses = masses
		self.size   = size  # window size
		self.fps    = fps   # frames per second

		# PyGame Setup

		pygame.init()
		
		black =   0,   0,   0
		white = 255, 255, 255

		screen = pygame.display.set_mode(self.size)
		clock = pygame.time.Clock()
		pygame.display.set_caption('AP Physics C Final Project- Universal Gravitation')

		# Game Loop

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			screen.fill(black)  # Wipe screen clear

			forces = {}
			for mass in self.masses:
				# Calculate net force acting on body given gravitational pull from other masses
				net_fx, net_fy = 0, 0
				for other in self.masses:
					if mass is not other:
						fx, fy = mass.net_force(other)
						net_fx += fx
						net_fy += fy

				forces[mass] = net_fx, net_fy

			for mass in self.masses:
				# Apply forces (update velocities)
				fx, fy = forces[mass]
				mass.vx += fx / mass.mass * self.spf
				mass.vy += fy / mass.mass * self.spf

				# Update position based on velocities
				mass.x += mass.vx * self.spf
				mass.y += mass.vy * self.spf

				# Draw mass on screen, adjust origin to center of screen
				# Radius not drawn to scale for visibility
				pygame.draw.circle(screen, white, (int(mass.x * scale + 640), int(mass.y * scale + 360)), int(mass.radius))

			pygame.display.flip()
			clock.tick(self.fps)

# Demos

# Orbit via calculation
# When one mass is significantly larger than another:
# v0 = sqrt(G * M / r)
# v0 is orbit velocity
# M is the mass of the object being orbitted
# r is orbit radius

# m1 = 10,000 kg
# m2 = 25 kg
# r = 50 m

# v0 = sqrt(G * (10000kg) / (50 m)) = 1.155 * 10^-4 m/s

Simulation(3600,
	[Mass('1', 10**7, 0, 0, 0, 0, 50),
	Mass('2', 100, 100, 0, 0, math.sqrt(G * 10**7 / 100), 10)],
	scale=1)

# Planetary Data gathered from https://nssdc.gsfc.nasa.gov/planetary/planetfact.html
# Given only mass, distance from sun (semimajor axis), and avg velocity
earth = Mass('Earth', 5.9724 * 10**24, -1*AU, 0, 0, 29.78 * 1000, 5)
sun = Mass('Sun', 1988500 * 10**24, 0, 0, 0, 0, 15)
mercury = Mass('Mercury', 0.3301 * 10**24, -0.3871*AU, 0, 0, 47360, 3)
venus = Mass('Venus', 4.8675 * 10**24, -0.7233*AU, 0, 0, 35020, 3)

Simulation(3600 * 24, [earth, sun, mercury, venus])

Simulation(3600 * 24,
	[Mass('1', 500, 100, 0, 0, 0, 5),
	Mass('2', 400, -100, 0, 0, 0, 2),
	Mass('3', 700, 0, 100, 0, -0.000001, 7)],
	scale=1)

Simulation(3600 * 12,
	[Mass('1', 5, 0, 10, 0.00001, 0, 5),
	Mass('2', 10, 3, 5, 0, -0.00001, 10),
	Mass('3', 7, 4, 0, 0.00001, 0, 7),
	Mass('4', 3, -5, -2, 0, 0, 3)],
	scale=5)