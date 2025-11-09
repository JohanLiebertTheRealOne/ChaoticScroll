import pygame
import math
import os
import sys
import random

def get_resource_path(relative_path):
    """Obtient le chemin correct pour les ressources, compatible PyInstaller"""
    try:
        # PyInstaller crée un dossier temp et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
        print(f"Running from PyInstaller bundle: {base_path}")
    except Exception:
        base_path = os.path.abspath(".")
        print(f"Running from script directory: {base_path}")
    
    return os.path.join(base_path, relative_path)

def get_image_paths(directory="."):
    """Get full paths to all image files in a directory"""
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff')
    
    # Utilise le chemin des ressources
    actual_directory = get_resource_path(directory)
    print(f"Looking for images in: {actual_directory}")
    
    images = []
    try:
        files = os.listdir(actual_directory)
        print(f"Files found: {files}")
        
        for filename in files:
            if filename.lower().endswith(image_extensions):
                full_path = os.path.join(actual_directory, filename)
                images.append(full_path)
                print(f"Found image: {filename}")
    except Exception as e:
        print(f"Error reading directory: {e}")
    
    return images

# Usage:
image_paths = get_image_paths()
print(f"Total images loaded: {len(image_paths)}")

pygame.init()

clock = pygame.time.Clock()

s_w = 1920 // 2
s_h = 1080 // 2

screen = pygame.display.set_mode((s_w, s_h))
pygame.display.set_caption("Chaotic Scroll")

# Pre-load all backgrounds
loaded_backgrounds = []
target_size = (int(s_w / 1.5), s_h)

for path in image_paths:
    try:
        bg = pygame.image.load(path).convert()
        bg = pygame.transform.scale(bg, target_size)
        loaded_backgrounds.append(bg)
        print(f"Loaded: {os.path.basename(path)}")
    except pygame.error as e:
        print(f"Could not load {path}: {e}")

# Fallback if no images found
if not loaded_backgrounds:
    print("WARNING: No images loaded! Creating default colored surfaces.")
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
    for color in colors:
        default_surf = pygame.Surface(target_size)
        default_surf.fill(color)
        loaded_backgrounds.append(default_surf)

print(f"Total backgrounds ready: {len(loaded_backgrounds)}")

bg_w = loaded_backgrounds[0].get_width()
bg_h = loaded_backgrounds[0].get_height()

# game variables
scroll = 0
tiles = math.ceil(s_w / bg_w) + 1
tile_strip = [random.choice(loaded_backgrounds) for _ in range(tiles)]

run = True

while run:
    clock.tick(60)
    
    # Draw each tile with its own background
    for i in range(tiles):
        screen.blit(tile_strip[i], (i * bg_w + scroll, 0))
    
    # Move scroll left
    scroll -= 5
    
    # When first tile goes off screen, cycle the strip
    if abs(scroll) >= bg_w:
        scroll += bg_w
        tile_strip.pop(0)
        tile_strip.append(random.choice(loaded_backgrounds))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
