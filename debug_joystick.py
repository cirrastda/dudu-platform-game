import pygame
import sys

pygame.init()
pygame.joystick.init()

# Verificar se há joysticks conectados
if pygame.joystick.get_count() == 0:
    print("Nenhum joystick conectado!")
    sys.exit()

# Inicializar o primeiro joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick conectado: {joystick.get_name()}")
print(f"Número de botões: {joystick.get_numbuttons()}")
print(f"Número de eixos: {joystick.get_numaxes()}")
print(f"Número de hats: {joystick.get_numhats()}")
print("\nPressione os botões do joystick para ver seus números...")
print("Pressione ESC para sair\n")

# Criar uma tela pequena
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Debug Joystick")
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
        elif event.type == pygame.JOYHATMOTION:
            print(f"Hat {event.hat} movido para: {event.value}")
        elif event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.1:  # Só mostrar movimentos significativos
                direction = ""
                if event.axis == 7:  # D-pad vertical
                    if event.value < -0.5:
                        direction = " (D-pad UP)"
                    elif event.value > 0.5:
                        direction = " (D-pad DOWN)"
                elif event.axis == 6:  # D-pad horizontal
                    if event.value < -0.5:
                        direction = " (D-pad LEFT)"
                    elif event.value > 0.5:
                        direction = " (D-pad RIGHT)"
                print(f"Eixo {event.axis} movido para: {event.value:.2f}{direction}")
    
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()