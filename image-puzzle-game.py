import pygame
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Initialize Pygame and Tkinter
pygame.init()
root = tk.Tk()
root.withdraw()  # Hide the Tkinter main window

# Screen size and colors
SCREEN_SIZE = 300
TILE_SIZE = SCREEN_SIZE // 3
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("8-Puzzle Game with Image Selector")

# Tile variables
tiles = []
tile_images = []
original_image = None

# Helper functions
def choose_image():
    global original_image, tile_images, tiles
    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if file_path:
        # Load, resize, and slice the image
        original_image = pygame.image.load(file_path)
        original_image = pygame.transform.scale(original_image, (SCREEN_SIZE, SCREEN_SIZE))
        
        # Slice image into tiles
        tile_images.clear()
        tiles = []
        for row in range(3):
            row_tiles = []
            for col in range(3):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if row == 2 and col == 2:
                    row_tiles.append(0)  # Empty tile
                    tile_images.append(None)
                else:
                    row_tiles.append(len(tile_images) + 1)
                    tile_images.append(original_image.subsurface(rect))
            tiles.append(row_tiles)

        # Shuffle tiles while keeping the empty space last
        flattened_tiles = [tile for row in tiles for tile in row if tile != 0]
        random.shuffle(flattened_tiles)
        flattened_tiles.append(0)
        tiles = [flattened_tiles[i:i + 3] for i in range(0, len(flattened_tiles), 3)]
        
        # Redraw grid with the new image
        draw_grid()

def draw_grid():
    if not tiles or len(tiles) != 3 or any(len(row) != 3 for row in tiles):
        print("Tiles array is not correctly initialized.")
        return
    
    screen.fill(WHITE)
    for row in range(3):
        for col in range(3):
            tile_num = tiles[row][col]
            if tile_num != 0:
                # Draw the tile image
                image = tile_images[tile_num - 1]
                screen.blit(image, (col * TILE_SIZE, row * TILE_SIZE))
                pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    pygame.display.flip()


def find_empty():
    for row in range(3):
        for col in range(3):
            if tiles[row][col] == 0:
                return row, col

def is_solved():
    return tiles == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def move_tile(direction):
    empty_row, empty_col = find_empty()
    if direction == "UP" and empty_row < 2:
        tiles[empty_row][empty_col], tiles[empty_row + 1][empty_col] = tiles[empty_row + 1][empty_col], tiles[empty_row][empty_col]
    elif direction == "DOWN" and empty_row > 0:
        tiles[empty_row][empty_col], tiles[empty_row - 1][empty_col] = tiles[empty_row - 1][empty_col], tiles[empty_row][empty_col]
    elif direction == "LEFT" and empty_col < 2:
        tiles[empty_row][empty_col], tiles[empty_row][empty_col + 1] = tiles[empty_row][empty_col + 1], tiles[empty_row][empty_col]
    elif direction == "RIGHT" and empty_col > 0:
        tiles[empty_row][empty_col], tiles[empty_row][empty_col - 1] = tiles[empty_row][empty_col - 1], tiles[empty_row][empty_col]

# Game loop
running = True
while running:
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_tile("UP")
            elif event.key == pygame.K_DOWN:
                move_tile("DOWN")
            elif event.key == pygame.K_LEFT:
                move_tile("LEFT")
            elif event.key == pygame.K_RIGHT:
                move_tile("RIGHT")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within a small top-left "button" area for image selection
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < 100 and mouse_y < 50:
                choose_image()

    # Draw the "Choose Image" button
    pygame.draw.rect(screen, (100, 100, 250), (10, 10, 80, 30))  # Button rectangle
    text = FONT.render("Choose Image", True, WHITE)
    screen.blit(text, (12, 12))
    
    pygame.display.flip()

pygame.quit()
