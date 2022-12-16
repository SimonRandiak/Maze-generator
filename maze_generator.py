import pygame 
import random

WIDTH, HEIGHT = 640, 480 

ZOOM = 2

OFFSET_X = 0 
OFFSET_Y = 0 

BLOCK_THICK = 2 
BLOCK_COUNT = 50 

BLOCK_WIDTH = (WIDTH // BLOCK_COUNT)
BLOCK_HEIGHT = (HEIGHT // BLOCK_COUNT)

BLOCK_UNVISITED_COLOR = (0,0,255)
BLOCK_VISITED_COLOR = (0,0,0)

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

class Cell:
    def __init__(self, x, y) -> None:
        self.top = True
        self.left = True 
        self.right = True 
        self.bottom = True 
        self.x = x 
        self.y = y
        self.color = BLOCK_UNVISITED_COLOR

def drawCell(c: Cell):
    dx = ((c.x * BLOCK_WIDTH) + OFFSET_X)
    dy = ((c.y * BLOCK_HEIGHT) + OFFSET_Y)

    if c.top:
        pygame.draw.line(screen, c.color, (dx, dy), (dx+BLOCK_WIDTH, dy), width=BLOCK_THICK)
    if c.left:
        pygame.draw.line(screen, c.color, (dx+BLOCK_WIDTH, dy), (dx+BLOCK_WIDTH, dy+BLOCK_HEIGHT), width=BLOCK_THICK)
    if c.bottom:
        pygame.draw.line(screen, c.color, (dx, dy+BLOCK_HEIGHT), (dx+BLOCK_WIDTH, dy+BLOCK_HEIGHT), width=BLOCK_THICK)
    if c.right:
        pygame.draw.line(screen, c.color, (dx, dy), (dx, dy+BLOCK_HEIGHT), width=BLOCK_THICK)

def getFreeNodes(x, y):
    nodes = []
    if x+1 in range(BLOCK_COUNT) and y in range(BLOCK_COUNT) and cells[y][x+1].color == BLOCK_UNVISITED_COLOR:
        nodes.append((x+1, y))
    if x-1 in range(BLOCK_COUNT) and y in range(BLOCK_COUNT) and cells[y][x-1].color == BLOCK_UNVISITED_COLOR:
        nodes.append((x-1, y))
    if x in range(BLOCK_COUNT) and y+1 in range(BLOCK_COUNT) and cells[y+1][x].color == BLOCK_UNVISITED_COLOR:
        nodes.append((x, y+1))
    if x in range(BLOCK_COUNT) and y-1 in range(BLOCK_COUNT) and cells[y-1][x].color == BLOCK_UNVISITED_COLOR:
        nodes.append((x,y-1))

    return nodes


def removeBorders(x,y, x1, y1):
    if x1 - 1 == x:
        cells[y][x].left = False
        cells[y][x1].right= False
    if x1 + 1 == x:
        cells[y][x].right = False
        cells[y][x1].left = False
    if y1 - 1 == y:
        cells[y][x].bottom = False
        cells[y1][x1].top = False
    if y1 + 1 == y:
        cells[y][x].top = False
        cells[y1][x].bottom = False

def dfs(x, y):
    stack = [(x,y)]
    cur = (x, y)


    while len(stack) != 0:
        free_nodes = getFreeNodes(cur[0], cur[1])
        if len(free_nodes) == 0: #dead end 
            cur = stack.pop()
            continue

        stack.append(cur)
        #cells[cur[1]][cur[0]].color = BLOCK_VISITED_COLOR
        free_node = random.choice(free_nodes)
        removeBorders(cur[0], cur[1], free_node[0], free_node[1])
        cur = free_node
        cells[cur[1]][cur[0]].color = BLOCK_VISITED_COLOR


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

cells = []

for _ in range(BLOCK_COUNT):
    rows = []
    for __ in range(BLOCK_COUNT):
        c = Cell(__, _)
        rows.append(c)
        
    cells.append(rows)


dfs(0, 0)
running = True 

prev_mouse = tuple()

dragged = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT:
            prev_mouse = pygame.mouse.get_pos()
            dragged = True
        if event.type == pygame.MOUSEBUTTONUP:
            dragged = False

    if dragged and pygame.MOUSEBUTTONDOWN:
        OFFSET_X += pygame.mouse.get_pos()[0] - prev_mouse[0]
        OFFSET_Y += pygame.mouse.get_pos()[1] - prev_mouse[1]

        prev_mouse = pygame.mouse.get_pos()


    screen.fill((255,255,255))
    for row in cells:
        for cell in row:
            drawCell(cell)

    pygame.display.update()

        