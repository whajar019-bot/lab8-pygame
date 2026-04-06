import pygame
import random
import math
import logging

# Configuration
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_SQUARES = 10
GLOBAL_MAX_SPEED = 5.0


def setup_journal_logger():
    logger = logging.getLogger("journal")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        file_handler = logging.FileHandler("journal.log", mode="w", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(file_handler)

    return logger

def create_square():
    size = random.randint(20, 60)
    # REQUIREMENT: Speed is a function of size (Larger = Slower)
    max_speed = GLOBAL_MAX_SPEED * (20 / size) 
    
    return {
        "rect": pygame.Rect(random.randint(0, WIDTH-size), random.randint(0, HEIGHT-size), size, size),
        "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
        "vx": random.uniform(-max_speed, max_speed),
        "vy": random.uniform(-max_speed, max_speed),
        "max_speed": max_speed
    }

def apply_jitter(square):
    """
    Requirement: Small rotation of the speed vector.
    This changes direction without necessarily changing speed magnitude.
    """
    vx, vy = square["vx"], square["vy"]
    
    # 1. Get current magnitude (speed) and direction (angle)
    current_speed = math.hypot(vx, vy)
    angle = math.atan2(vy, vx)
    
    # 2. Rotate slightly (jitter) - occurring every frame
    angle += random.uniform(-0.05, 0.05)
    
    # 3. Convert back to Cartesian (x, y) coordinates
    new_vx = math.cos(angle) * current_speed
    new_vy = math.sin(angle) * current_speed
    
    # 4. Defensive guard: clamp speed to the square's max_speed
    if current_speed > square["max_speed"]:
        scale = square["max_speed"] / current_speed
        new_vx *= scale
        new_vy *= scale
        
    return new_vx, new_vy

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 8: Moving Squares Part I")
    clock = pygame.time.Clock()
    journal_logger = setup_journal_logger()
    journal_logger.info("Journal logger activated")
    
    squares = [create_square() for _ in range(NUM_SQUARES)]
    
    running = True
    while running:
        screen.fill((20, 20, 20)) # Background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for s in squares:
            # Apply the jitter/rotation
            s["vx"], s["vy"] = apply_jitter(s)
            
            # Update position
            s["rect"].x += s["vx"]
            s["rect"].y += s["vy"]
            
            # Collision with window boundaries (Bounce)
            if s["rect"].left <= 0 or s["rect"].right >= WIDTH:
                s["vx"] *= -1
                journal_logger.info("Horizontal bounce at x=%s", s["rect"].x)
            if s["rect"].top <= 0 or s["rect"].bottom >= HEIGHT:
                s["vy"] *= -1
                journal_logger.info("Vertical bounce at y=%s", s["rect"].y)
                
            # Draw the square
            pygame.draw.rect(screen, s["color"], s["rect"])
            
        pygame.display.flip()
        clock.tick(FPS)

    journal_logger.info("Journal logger shutting down")
    pygame.quit()

if __name__ == "__main__":
    main()