import pygame as p

WIDTH, aspect, zoom = 1280, 1.8, 64
MAX_FPS = 12
SQ_SIZE = WIDTH//zoom

def updatestate(state):
    newstate = {}
    borders = {}
    for cell in list(state):
        x,y = cell[0], cell[1]
        neighbors = [(x,y+1),(x,y-1),(x+1,y),(x-1,y),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]
        score = 0
        for neighbor in neighbors:
            if neighbor in state:
                score += 1
            elif neighbor not in borders:
                borders[neighbor] = 1
        if score == 2 or score == 3:
            newstate[cell] = 1
    for cell in list(borders):
        x, y = cell[0], cell[1]
        neighbors = [(x,y+1),(x,y-1),(x+1,y),(x-1,y),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]
        if sum(1 for c in neighbors if c in state) == 3:
            newstate[cell] = 1
    return newstate

def drawBoard(screen,state,view,zoom,aspect):
    x,y = view[0], view[1]
    screen.fill(p.Color('white'))
    for r in range(round(zoom/aspect)):
        rSq = r*SQ_SIZE
        for c in range(zoom):
            if (c-x,r-y) in state:
                p.draw.rect(screen, p.Color("black"), p.Rect(c * SQ_SIZE, rSq, SQ_SIZE, SQ_SIZE))
        p.draw.line(screen, p.Color("grey"), (0, rSq), (WIDTH, rSq))
    for c in range(zoom):
        cSq = c * SQ_SIZE
        p.draw.line(screen, p.Color("grey"), (cSq, 0), (cSq, WIDTH // aspect))

clock = p.time.Clock()
p.init()
screen = p.display.set_mode((WIDTH, WIDTH//aspect))

current_state = {}
save = current_state
view = (0,0)
editing = True
painting_mode = 0
while True:
    if not editing and painting_mode == 0:
        current_state = updatestate(current_state)
    drawBoard(screen, current_state,view,zoom,aspect)
    clock.tick(MAX_FPS)
    p.display.set_caption(f'Conway\'s Game of Life {clock.get_fps() :.2f}')
    p.display.flip()
    for e in p.event.get():
        if e.type == p.KEYDOWN:
            if e.key == p.K_e:
                if editing:
                    save = current_state
                editing = not editing
            elif e.key == p.K_c:
                current_state = {}
            elif e.key == p.K_r:
                editing = True
                current_state = save
            elif e.key == p.K_p:
                painting_mode = (painting_mode+1)%3
            elif e.key == p.K_KP_PLUS:
                MAX_FPS += 2
            elif e.key == p.K_KP_MINUS:
                MAX_FPS -= 2
            elif e.key == p.K_i:
                print(f"Max FPS: {MAX_FPS}\nEditing: {editing}\nPainting mode: {painting_mode}\nZoom: {zoom}\n==========================")
        elif e.type == p.MOUSEBUTTONDOWN:
            if e.button == 1 and painting_mode == 0:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE - view[0]
                row = location[1] // SQ_SIZE - view[1]
                if editing:
                    if (col,row) in current_state:
                        del current_state[(col,row)]
                    else:
                        current_state[(col,row)] = 1
            if e.button == 3:
                location0 = p.mouse.get_pos()
                view0 = view
        if e.type == p.MOUSEWHEEL:
            if (e.y > 0 and zoom > 10) or (e.y < 0 and zoom < 400):
                zoom -= e.y*2
            SQ_SIZE = WIDTH // zoom + 1
    mouse_state = p.mouse.get_pressed()
    if mouse_state[2]:
        location = p.mouse.get_pos()
        view = ((location[0] - location0[0]) // SQ_SIZE + view0[0], (location[1] - location0[1]) // SQ_SIZE + view0[1])
    elif mouse_state[0] and painting_mode != 0:
        location = p.mouse.get_pos()
        col = location[0] // SQ_SIZE - view[0]
        row = location[1] // SQ_SIZE - view[1]
        if painting_mode == 1:
            current_state[(col,row)] = 1
        elif (col,row) in current_state:
            del current_state[(col,row)]
