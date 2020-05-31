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


class Mass:
	def __init__(self, m, x, y, vx, vy, r):
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

		f = G * self.mass * other.mass / (d ** 2)  # Universal Force of Gravity: F = (G * m1 * m2) / (r^2)
		theta = math.atan2(dy, dx)  # Calculate angle of force to get component vectors
		fx = f * math.cos(theta)
		fy = f * math.sin(theta)

		return fx, fy


class Simulation:
	def __init__(self, spf, masses, size=(1280,720), fps=60):
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

				# Draw mass on screen
				pygame.draw.circle(screen, white, (mass.x, mass.y), mass.radius)

			pygame.display.flip()
			clock.tick(self.fps)