import pygame
import random
import math
import logging
from typing import List

# =========================================================================
# CONSTANTS
# =========================================================================
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_SQUARES = 25

GLOBAL_MAX_SPEED = 150.0 
FLEE_RADIUS = 150
CHASE_RADIUS = 200
FLEE_FORCE = 12.0
CHASE_FORCE = 6.0
JITTER_STRENGTH = 2.0

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("journal")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        file_handler = logging.FileHandler("journal.log", mode="w", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(file_handler)
    return logger

class Square:
    def __init__(self) -> None:
        self.size = random.randint(20, 60)
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size),
            random.randint(0, HEIGHT - self.size),
            self.size,
            self.size
        )
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
        self.max_speed = GLOBAL_MAX_SPEED * (25 / self.size)
        self.vx = random.uniform(-self.max_speed, self.max_speed)
        self.vy = random.uniform(-self.max_speed, self.max_speed)
        
        # LAB 10: Life Span & Rebirth
        self.lifetime = random.uniform(30.0, 180.0)
        self.age = 0.0
        self.is_dead = False

    def apply_jitter(self, dt: float) -> None:
        angle = math.atan2(self.vy, self.vx)
        speed = math.hypot(self.vx, self.vy)
        angle += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH) * dt
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def apply_behaviors(self, others: List['Square'], dt: float) -> None:
        fx, fy = 0.0, 0.0
        for other in others:
            if other is self:
                continue
            
            dx = other.rect.centerx - self.rect.centerx
            dy = other.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            
            if dist == 0: continue

            # Fleeing (Small dodges Big)
            if dist < FLEE_RADIUS and other.size > self.size:
                strength = (FLEE_RADIUS - dist) / FLEE_RADIUS
                fx -= (dx / dist) * strength * FLEE_FORCE
                fy -= (dy / dist) * strength * FLEE_FORCE
            
            # Chasing (Big hunts Small)
            elif dist < CHASE_RADIUS and other.size < self.size:
                strength = (CHASE_RADIUS - dist) / CHASE_RADIUS
                fx += (dx / dist) * strength * CHASE_FORCE
                fy += (dy / dist) * strength * CHASE_FORCE

        self.vx += fx * dt * 100 
        self.vy += fy * dt * 100

    def limit_speed(self) -> None:
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def move(self, dt: float) -> None:
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        
        self.age += dt
        if self.age >= self.lifetime:
            self.is_dead = True

    def bounce(self, logger: logging.Logger) -> None:
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx *= -1
            logger.info("Bounce Left")
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.vx *= -1
            logger.info("Bounce Right")
            
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
            logger.info("Bounce Top")
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy *= -1
            logger.info("Bounce Bottom")

    def update(self, others: List['Square'], logger: logging.Logger, dt: float) -> None:
        self.apply_behaviors(others, dt)
        self.apply_jitter(dt)
        self.limit_speed()
        self.move(dt)
        self.bounce(logger)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 10: Steering and Rebirth")
    
    font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()
    logger = setup_logger()

    squares = [Square() for _ in range(NUM_SQUARES)]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0 
        screen.fill((25, 25, 35))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares[:]:
            square.update(squares, logger, dt)
            if square.is_dead:
                squares.remove(square)
                squares.append(Square())
            else:
                square.draw(screen)

        fps_text = font.render(f"FPS: {clock.get_fps():.1f} | Active Squares: {len(squares)}", True, (200, 200, 200))
        screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()