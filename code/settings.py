from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15),
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'ground plant': 4,
	'main': 5,
}



GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}


