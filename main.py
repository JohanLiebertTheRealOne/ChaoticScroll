import pygame
import math
import os

def get_image_paths(directory="."):
    """Get full paths to all image files in a directory

    Args:
        directory: Path to directory (default is current directory)

    Returns:
        List of full image paths
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff')

    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(image_extensions):
            full_path = os.path.join(directory, filename)
            images.append(full_path)

    return images

# Usage:
image_paths = get_image_paths()
print(image_paths)

pygame.init()

clock = pygame.time.Clock()

s_w = 1920 // 2  # Use integer division
s_h = 1080 // 2

screen = pygame.display.set_mode((s_w, s_h))
pygame.display.set_caption("Chaotic Scroll")

def_bg = pygame.image.load('./tibo1.jpeg').convert()  # Add convert back for performance
current_bg = def_bg
current_bg = pygame.transform.scale(current_bg, (int(s_w / 1.5), s_h))  # Convert to int

bg_w = current_bg.get_width()
bg_h = current_bg.get_height()

# game variables
scroll = 0
tiles = math.ceil(s_w / bg_w) + 1  # Add 1 extra tile for seamless scrolling
print(f"Tiles needed: {tiles}")

run = True

while run:
    clock.tick(60)
    
    # Draw tiled background with scroll offset
    for i in range(0, tiles):
        screen.blit(current_bg, (i * bg_w + scroll, 0))  # Fixed: single tuple for position
    
    # Move scroll left
    scroll -= 5
    
    # Reset scroll when one tile width has passed (infinite scroll effect)
    if abs(scroll) > bg_w:
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
