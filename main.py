import math

import pygame
import var
import unit


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((var.screen_width, var.screen_height), pygame.NOFRAME)
        pygame.display.set_caption('Rock Paper Scissor')

        self.clock = pygame.time.Clock()

        self.screen.fill((150, 150, 150))

        self.sprite_group = pygame.sprite.RenderPlain()

        for x in range(int(var.number_of_units / 3)):
            rock = unit.Unit('rock')
            paper = unit.Unit('paper')
            scissor = unit.Unit('scissor')
            self.sprite_group.add(rock)
            self.sprite_group.add(paper)
            self.sprite_group.add(scissor)

    def run(self):
        while True:
            pygame.display.flip()
            self.screen.fill((150, 150, 150))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit(0)

            unit_types = set(sprite.unit_type for sprite in self.sprite_group)
            if len(unit_types) <= 1:
                return

            for item in self.sprite_group:
                item.draw(self.screen)
                item.move()
                # pygame.draw.rect(screen, (255, 0, 0), item.rect)
                # pygame.draw.rect(item.image, (255,0,0), [0, 0, item.rect.width, item.rect.height], 1)

            collided_items = []
            for item1 in self.sprite_group:
                for item2 in self.sprite_group:
                    if item1 is item2:
                        continue
                    # if item1 == item2:
                    # continue
                    if item1.unit_type == item2.unit_type:
                        continue
                    if not pygame.Rect.colliderect(item1.rect, item2.rect):
                        continue
                    if (item1, item2) in collided_items:
                        continue

                    collided_items.append((item1, item2))

                    # Collision logic
                    x1 = item2.rect.x
                    y1 = item2.rect.y

                    x2 = item1.rect.x
                    y2 = item1.rect.y

                    dx = x2 - x1
                    dy = y2 - y1

                    angle_rad = math.atan2(dy, dx)

                    # if angle_rad < 0:
                    # angle_rad += 2 * math.pi

                    # angle_rad = math.pi / 2 - angle_rad
                    # print(angle_rad)

                    item1.collide_wall(angle_rad)
                    item2.collide_wall(angle_rad)

                    if item1.unit_type == "rock" and item2.unit_type == "paper":
                        item1.join_group("paper")
                    elif item1.unit_type == "paper" and item2.unit_type == "scissor":
                        item1.join_group("scissor")
                    elif item1.unit_type == "scissor" and item2.unit_type == "rock":
                        item1.join_group("rock")
                    elif item2.unit_type == "rock" and item1.unit_type == "paper":
                        item2.join_group("paper")
                    elif item2.unit_type == "paper" and item1.unit_type == "scissor":
                        item2.join_group("scissor")
                    elif item2.unit_type == "scissor" and item1.unit_type == "rock":
                        item2.join_group("rock")

                    item1.move()
                    item2.move()

            pygame.display.update()
            self.clock.tick(240)


if __name__ == '__main__':
    while True:
        main = Main()
        main.run()

