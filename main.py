import pygame
import random
import math

# Setup
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_SQUARES = 10

def create_square():
    size = random.randint(20, 60)
    # Rule: Larger squares move slower
    max_speed = 5.0 * (20 / size) 
    return {
        "rect": pygame.Rect(random.randint(0, WIDTH-size), random.randint(0, HEIGHT-size), size, size),
        "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
        "vx": random.uniform(-max_speed, max_speed),
        "vy": random.uniform(-max_speed, max_speed),
        "max_speed": max_speed
    }

def update_square(s):
    # Jitter: Small rotation of the speed vector
    speed = math.hypot(s["vx"], s["vy"])
    angle = math.atan2(s["vy"], s["vx"]) + random.uniform(-0.1, 0.1)
    
    s["vx"] = math.cos(angle) * speed
    s["vy"] = math.sin(angle) * speed

    # Movement & Bouncing
    s["rect"].x += s["vx"]
    s["rect"].y += s["vy"]
    if s["rect"].left <= 0 or s["rect"].right >= WIDTH: s["vx"] *= -1
    if s["rect"].top <= 0 or s["rect"].bottom >= HEIGHT: s["vy"] *= -1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    squares = [create_square() for _ in range(NUM_SQUARES)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
        
        screen.fill((30, 30, 30))
        for s in squares:
            update_square(s)
            pygame.draw.rect(screen, s["color"], s["rect"])
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()