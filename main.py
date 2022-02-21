import pygame as pg
import numpy as np

# To slow down the visualization a time.sleep() statement can be added 
# where the input is in seconds.
# import time
# time.sleep() 

TYPES = ["spiral","grid"]

GRID_SIZE = int(input("Input a gride size. > "))
TYPE = str(input("Visualization as grid or spiral? > "))
if TYPE.lower().strip() not in TYPES:
    TYPE = "spiral"
    print("Unrecognised input, visualization set to default(spiral).")

WHITE = (244, 243, 239)
BLACK = (16, 16, 16)

SCREEN_SIZE = 600
WIDTH = SCREEN_SIZE
HEIGHT = SCREEN_SIZE

RESOLUTION = (WIDTH,HEIGHT)
SCREEN = pg.display.set_mode(RESOLUTION)
SCREEN.fill(BLACK)

FPS = 60

pg.display.set_caption(f"Prime{TYPE.title().strip()}")


def primesfrom2to(n):
    sieve = np.ones(n//3 + (n%6==2), dtype=bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0][1:]+1)|1)]


def genPrimeGrid(size: int):
    if size % 2 == 0:
        size += 1
    
    grid = np.zeros(shape=(size,size))

    center = (size//2, size//2)
    
    current_x = center[0]
    current_y = center[1]
    current_number = 1

    pattern_direction = ["right","down","left","up"]
    pattern_steps = []
    pattern_draw = []
    pattern_prime = []

    primes = primesfrom2to(int(size**2))

    for i in range(1, 2*size):
        if i == 1:
            steps = 0
        if i % 2 == 1:
            steps += 1  
        pattern_steps.append(steps)

    for index, amount_of_steps in enumerate(pattern_steps):
        direction = pattern_direction[index%4]
        for i in range(amount_of_steps):
            
            grid[current_y][current_x] = current_number
            
            pattern_draw.append((current_x,current_y))
            
            if current_number in primes:
                pattern_prime.append(True)
            else:
                pattern_prime.append(False)

            if direction == "left":
                current_x -= 1
            elif direction == "right":
                current_x += 1
            elif direction == "up":
                current_y -= 1
            elif direction == "down":
                current_y += 1
            
            current_number += 1

    return pattern_draw, pattern_prime


def drawPrimeGrid(current_node, prime_state, grid_size):
    scale = SCREEN_SIZE // grid_size
    current_x = current_node[0] * scale
    current_y = current_node[1] * scale
    
    if prime_state:
        pg.draw.circle(SCREEN, WHITE, (current_x, current_y), scale // 4)  
    pg.display.flip()


def drawPrimeSpiral(previous_node, current_node, prime_state, grid_size):
    scale = SCREEN_SIZE // grid_size
    previous_x = previous_node[0] *  scale
    previous_y = previous_node[1] * scale
    current_x = current_node[0] * scale
    current_y = current_node[1] * scale
    
    pg.draw.line(SCREEN, WHITE, (previous_x, previous_y), (current_x, current_y), width=scale//8)
    if prime_state:
        pg.draw.circle(SCREEN, WHITE, (current_x, current_y), scale // 4)  
    pg.display.flip()


def exit(run_state = True):
    """Exit pygame using esc or the close button"""
    pg.event.pump()
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            run_state = False
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        run_state = False
    return run_state
    

def main():
    pg.init()

    run_state = True
    clock = pg.time.Clock()

    draw_coordinates, prime = genPrimeGrid(GRID_SIZE)

    while run_state:
        clock.tick(FPS)
        
        # -- main --

        for index in range(1,len(draw_coordinates)):
            
            run_state = exit()
            if not run_state:
                break
            
            if TYPE.lower().strip() == "grid":
                drawPrimeGrid(draw_coordinates[index], prime[index], GRID_SIZE)
            elif TYPE.lower().strip() == "spiral":
                drawPrimeSpiral(draw_coordinates[index-1], draw_coordinates[index], prime[index], GRID_SIZE)

        if run_state:
            run_state = exit()
    
    pg.quit()

if __name__ == "__main__":
    main()