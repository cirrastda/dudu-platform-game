import pygame
import sys

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Nenhum joystick conectado!")
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick conectado: {joystick.get_name()}")
print(f"Número de botões: {joystick.get_numbuttons()}")
print("\nPressione botões para ver seus números (ESC para sair):")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Botão pressionado: {event.button}")
    
    clock.tick(60)

pygame.quit()