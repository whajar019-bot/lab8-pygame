import pygame
import random
import math
import logging
from typing import List

WIDTH, HEIGHT = 800, 600
FPS = 60
GLOBAL_MAX_SPEED = 50.0 
FLEE_RADIUS = 150
CHASE_RADIUS = 200
FLEE_FORCE = 12.0
CHASE_FORCE = 6.0
JITTER_STRENGTH = 2.0
TEST_MODE_ON: bool = False 

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
    def __init__(self, size: int) -> None:
        self.original_size = size # Store for respawning[cite: 1]
        self.size = size
        self.target_size = size # Goal for animation[cite: 1]
        self.growth_timer = 0.0 # Timer for animation[cite: 1]
        
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
        
        self.lifetime = random.uniform(30.0, 180.0)
        self.age = 0.0
        self.is_dead = False
        self.trail: List[pygame.Vector2] = []

    def grow(self, prey_size: int) -> None:
        # Ex 9: Set target instead of immediate change[cite: 1]
        self.target_size += int(prey_size * 0.2)
        self.growth_timer = 0.0 

    def apply_jitter(self, dt: float) -> None:
        angle = math.atan2(self.vy, self.vx)
        speed = math.hypot(self.vx, self.vy)
        angle += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH) * dt
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def apply_behaviors(self, others: List['Square'], dt: float) -> None:
        fx, fy = 0.0, 0.0
        for other in others:
            if other is self: continue
            
            dx = other.rect.centerx - self.rect.centerx
            dy = other.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist == 0: continue

            if dist < FLEE_RADIUS and other.size > self.size:
                strength = (FLEE_RADIUS - dist) / FLEE_RADIUS
                fx -= (dx / dist) * strength * FLEE_FORCE
                fy -= (dy / dist) * strength * FLEE_FORCE
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
        self.trail.append(pygame.Vector2(self.rect.center))
        if len(self.trail) > 30:
            self.trail.pop(0)

        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        
        self.age += dt
        if self.age >= self.lifetime:
            self.is_dead = True

    def wrap(self) -> None:
        wrapped = False
        if self.rect.right < 0:
            self.rect.left = WIDTH
            wrapped = True
        elif self.rect.left > WIDTH:
            self.rect.right = 0
            wrapped = True
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
            wrapped = True
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
            wrapped = True

        if wrapped:
            self.trail.clear()

    def update(self, others: List['Square'], logger: logging.Logger, dt: float) -> None:
        # Ex 9: Animated Growth Logic[cite: 1]
        if self.size < self.target_size:
            self.growth_timer += dt
            progress = min(self.growth_timer / 0.5, 1.0) # 0.5s duration[cite: 1]
            self.size = int(self.size + (self.target_size - self.size) * progress)
            self.rect.width = self.rect.height = self.size
            self.max_speed = GLOBAL_MAX_SPEED * (25 / self.size)

        self.apply_behaviors(others, dt)
        self.apply_jitter(dt)
        self.limit_speed()
        self.move(dt)
        self.wrap()

    def draw(self, screen: pygame.Surface) -> None:
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color, False, self.trail, 2)
        pygame.draw.rect(screen, self.color, self.rect)

def check_collision(a: Square, b: Square) -> bool:
    return a.rect.colliderect(b.rect) 

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 10: Steering and Rebirth")
    
    font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()
    logger = setup_logger()

    squares = []
    for _ in range(5): squares.append(Square(25))
    for _ in range(10): squares.append(Square(10))
    for _ in range(30): squares.append(Square(4))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0 
        screen.fill((25, 25, 35))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares[:]:
            square.update(squares, logger, dt)

            for other in squares:
                if other is square: continue
                if check_collision(square, other):
                    if square.size > other.size:
                        square.grow(other.size) # Ex 6 & 9[cite: 1]
                        other.is_dead = True
            
            if square.is_dead:
                squares.remove(square)
                # Ex 2 & 5: Respawn with ORIGINAL size[cite: 1]
                squares.append(Square(square.original_size))
            else:
                square.draw(screen)

        fps_text = font.render(f"FPS: {clock.get_fps():.1f} | Active: {len(squares)}", True, (200, 200, 200))
        screen.blit(fps_text, (10, 10))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()