import pygame


class Joystick:

    def init(self):
        pygame.joystick.init()
        self.joystick = None
        self.joystick_connected = False

        # Verificar se há joystick conectado
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.joystick_connected = True
            print(f"Joystick conectado: {self.joystick.get_name()}")
            return self.joystick
        else:
            print("Nenhum joystick detectado. Usando controles do teclado.")
            return None
