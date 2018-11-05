import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

SHIP_WIDTH = 40
SHIP_HEIGHT = 120
SHIP_PNG = 'spaceship.red.png'

GRAVITY = 1
FRICTION_DX = 4
FRICTION_DY = 1

FRICTION_GROUND_DX = 2
FRICTION_GROUND_DY = 1

x = WINDOW_WIDTH * 0.5
y = WINDOW_HEIGHT * 0.5

def main():
    # vectors for the forces
    acceleration = pygame.math.Vector2(0, 0)
    velocity = pygame.math.Vector2(0, 0)
    position = pygame.math.Vector2(x, y)
    gravity = pygame.math.Vector2(0, GRAVITY)

    pygame.init()
    mainDisplay = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame practice")

    gameClock = pygame.time.Clock()

    crashed = False
    image = pygame.image.load(SHIP_PNG)
    image = pygame.transform.scale(image,(SHIP_WIDTH, SHIP_HEIGHT))

    while not crashed:
        gameClock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        #check for key presses
        pressed = pygame.key.get_pressed()
        move_left = pressed[pygame.K_a] or pressed[pygame.K_LEFT]
        move_right = pressed[pygame.K_d] or pressed[pygame.K_RIGHT]
        move_up = pressed[pygame.K_w] or pressed[pygame.K_UP]

        # calculate acceleration vector based on key presses
        acceleration.x = (move_right - move_left ) / FRICTION_DX
        acceleration.y = - move_up / FRICTION_DY

        # the physics stuff (I had to tweak some numbers to make it playable)
        velocity += acceleration * 0.5
        velocity += gravity * 0.1
        position += velocity + 0.5 * acceleration

        # reset acceleration
        acceleration *= 0

        # restrict ship to the game window
        position.x = max(0, min(position.x, WINDOW_WIDTH - SHIP_WIDTH))
        position.y = max(0, min(position.y, WINDOW_HEIGHT - SHIP_HEIGHT))

        # apply friction if ship is on the surface edges
        if position.y == WINDOW_HEIGHT - SHIP_HEIGHT:
            velocity.x /= FRICTION_GROUND_DX
            velocity.y = 0

        if position.x == 0 or position.x == WINDOW_WIDTH - SHIP_WIDTH:
            velocity.x = 0
            velocity.y /= FRICTION_GROUND_DY

        mainDisplay.fill((0,0,0))
        createShipImage(mainDisplay,image,position.x,position.y)

        pygame.display.update()

    pygame.quit()

def createShipImage(display,image,x,y):
    display.blit(image,(x,y))

if __name__ == '__main__':
    main()
