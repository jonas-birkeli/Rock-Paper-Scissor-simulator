import math
import random
import var
import pygame


class Unit(pygame.sprite.Sprite):
	def __init__(self, unit_type: str):
		super(Unit, self).__init__()
		self.unit_type = unit_type
		self.speed = 1 / 2
		self.size = 1 / 5

		self.surf = pygame.image.load(f'images/{self.unit_type}.png')
		self.image = pygame.image.load(f'images/{self.unit_type}.png')
		image_size = self.image.get_size()
		new_x_size = image_size[0] * self.size
		new_y_size = image_size[1] * self.size

		self.image = pygame.transform.scale(self.image, (new_x_size, new_y_size))

		self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)

		self.rect = self.surf.get_rect(
			center=(
				random.randint(0, var.screen_width),
				random.randint(0, var.screen_height)
			)
		).inflate(-300, -300)
		self.dir = random.uniform(0, 2 * math.pi)

	def move(self):
		self.rect.x += math.cos(self.dir)
		self.rect.y += math.sin(self.dir)

		# Limit
		if self.rect.x > var.screen_width - 250 * self.size:
			self.collide_wall(math.pi)
			self.rect.x = var.screen_width - 250 * self.size
		if self.rect.x < 50 / 20:
			self.collide_wall(math.pi)
			self.rect.x = 50 / 20 + 1

		# Screen limit
		if self.rect.y > var.screen_height - 250 * self.size:
			self.collide_wall(1 / 2 * math.pi)
			self.rect.y = var.screen_height - 250 * self.size
		if self.rect.y < 50 / 20:
			self.collide_wall(1 / 2 * math.pi)
			self.rect.y = 50 / 20 + 1

		self.rect.x += math.cos(self.dir) * self.speed
		self.rect.y += math.sin(self.dir) * self.speed

	def join_group(self, unit_type):
		self.unit_type = unit_type
		self.image = pygame.image.load(f'images/{self.unit_type}.png')

		image_size = self.image.get_size()
		new_x_size = image_size[0] * self.size
		new_y_size = image_size[1] * self.size

		self.image = pygame.transform.scale(self.image, (new_x_size, new_y_size))

	def draw(self, screen):
		screen.blit(self.image, (self.rect.x, self.rect.y))

	def collide_wall(self, wallnormal):
		dy = math.sin(self.dir)
		dx = math.cos(self.dir)
		ny = math.sin(wallnormal)
		nx = math.cos(wallnormal)

		rx = dx - 2 * (dx * nx + dy * ny) * nx
		ry = dy - 2 * (dx * nx + dy * ny) * ny

		self.dir = math.atan2(ry, rx)
