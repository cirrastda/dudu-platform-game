#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar e instalar o jogo no emulador Android
Configura automaticamente o ambiente Android
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def find_android_sdk():
    """Encontrar o caminho do Android SDK"""
    username = os.getenv("USERNAME", "user")
    possible_paths = [
        f"C:/Users/{username}/AppData/Local/Android/Sdk",
        os.path.expanduser("~/AppData/Local/Android/Sdk"),
        "C:/Android/Sdk",
        "C:/Program Files/Android/Sdk",
        "C:/Program Files (x86)/Android/Sdk",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Android SDK encontrado: {path}")
            return path

    print("❌ Android SDK não encontrado!")
    return None


def setup_android_env():
    """Configurar ambiente Android (SDK, ADB, etc.)"""
    print("🔧 Configurando ambiente Android...")

    sdk_path = find_android_sdk()
    if not sdk_path:
        return False

    # Caminhos importantes
    platform_tools = os.path.join(sdk_path, "platform-tools")
    emulator_path = os.path.join(sdk_path, "emulator")
    cmdline_tools = os.path.join(sdk_path, "cmdline-tools", "latest", "bin")

    # Adicionar ao PATH
    paths_to_add = [platform_tools, emulator_path, cmdline_tools]
    current_path = os.environ.get("PATH", "")

    for path in paths_to_add:
        if os.path.exists(path) and path not in current_path:
            os.environ["PATH"] = f"{path};{current_path}"
            current_path = os.environ["PATH"]

    print("✅ PATH atualizado com ferramentas Android")
    return True


def check_emulator_advanced():
    """Verificar emulador com múltiplas tentativas"""
    print("📱 Verificando emuladores Android...")

    # Tentar diferentes comandos ADB
    adb_commands = ["adb", "adb.exe"]

    for adb_cmd in adb_commands:
        try:
            # Primeiro, matar servidor ADB e reiniciar
            subprocess.run([adb_cmd, "kill-server"], capture_output=True)
            time.sleep(1)
            subprocess.run([adb_cmd, "start-server"], capture_output=True)
            time.sleep(2)

            # Verificar dispositivos
            result = subprocess.run(
                [adb_cmd, "devices"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                print(f"📋 Saída do ADB devices:")
                for line in lines:
                    print(f"   {line}")

                # Procurar por dispositivos online
                devices = []
                for line in lines[1:]:  # Pular cabeçalho
                    if line.strip() and "\t" in line:
                        device_id, status = line.split("\t", 1)
                        if "device" in status and "offline" not in status:
                            devices.append(device_id.strip())

                if devices:
                    print(f"✅ Emulador(es) encontrado(s): {', '.join(devices)}")
                    return True, devices[0]
                else:
                    print("⚠️ Nenhum emulador online encontrado")
                    return False, None

        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"⚠️ Erro com {adb_cmd}: {e}")
            continue

    print("❌ ADB não encontrado ou não funcional")
    return False, None


def list_available_emulators():
    """Listar emuladores disponíveis"""
    try:
        result = subprocess.run(
            ["emulator", "-list-avds"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            avds = result.stdout.strip().split("\n")
            print(f"📱 Emuladores disponíveis: {', '.join(avds)}")
            return avds
        else:
            print("⚠️ Nenhum emulador configurado")
            return []
    except Exception as e:
        print(f"⚠️ Erro ao listar emuladores: {e}")
        return []


def start_emulator_if_needed():
    """Tentar iniciar um emulador se nenhum estiver rodando"""
    print("🚀 Tentando iniciar emulador...")

    avds = list_available_emulators()
    if not avds:
        print("❌ Nenhum emulador configurado no Android Studio")
        return False

    # Usar o primeiro emulador disponível
    emulator_name = avds[0]
    print(f"🎯 Iniciando emulador: {emulator_name}")

    try:
        # Iniciar emulador em background
        subprocess.Popen(
            ["emulator", "-avd", emulator_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print("⏳ Aguardando emulador inicializar (30 segundos)...")

        # Aguardar até 60 segundos para o emulador aparecer
        for i in range(12):  # 12 * 5 = 60 segundos
            time.sleep(5)
            found, device_id = check_emulator_advanced()
            if found:
                print(f"✅ Emulador {device_id} iniciado com sucesso!")
                return True
            print(f"⏳ Tentativa {i+1}/12...")

        print("❌ Timeout: emulador não iniciou a tempo")
        return False

    except Exception as e:
        print(f"❌ Erro ao iniciar emulador: {e}")
        return False


def create_android_version():
    """Criar versão do jogo adaptada para Android com controles touch"""
    print("🎮 Criando versão Android com controles touch...")

    # Ler o jogo original
    with open("main.py", "r", encoding="utf-8") as f:
        original_code = f.read()

    # Código de controles touch para inserir
    touch_controls_code = '''
# === CONFIGURAÇÕES ANDROID ===
import os
if 'ANDROID_ARGUMENT' in os.environ:
    # Forçar orientação landscape no Android
    os.environ['KIVY_ORIENTATION'] = 'landscape'
    
# === CONTROLES TOUCH PARA ANDROID ===
class TouchButton:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.pressed_color = (color[0] - 50, color[1] - 50, color[2] - 50)
        self.pressed = False
        self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.pressed = False
                return False
        return None
    
    def draw(self, screen):
        color = self.pressed_color if self.pressed else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class TouchControls:
    def __init__(self, screen_width, screen_height):
        button_size = 80
        margin = 20
        
        # Botões de movimento (esquerda)
        self.left_btn = TouchButton(margin, screen_height - button_size - margin, 
                                   button_size, button_size, "◀", (100, 150, 255))
        self.right_btn = TouchButton(margin + button_size + 10, screen_height - button_size - margin, 
                                    button_size, button_size, "▶", (100, 150, 255))
        
        # Botões de ação (direita)
        self.jump_btn = TouchButton(screen_width - button_size - margin, screen_height - button_size - margin, 
                                   button_size, button_size, "↑", (100, 255, 100))
        self.shoot_btn = TouchButton(screen_width - button_size*2 - margin - 10, screen_height - button_size - margin, 
                                    button_size, button_size, "●", (255, 100, 100))
        
        self.buttons = [self.left_btn, self.right_btn, self.jump_btn, self.shoot_btn]
        
        # Estados dos controles
        self.left_pressed = False
        self.right_pressed = False
        self.jump_pressed = False
        self.shoot_pressed = False
    
    def handle_event(self, event):
        for button in self.buttons:
            result = button.handle_event(event)
            if result is not None:
                if button == self.left_btn:
                    self.left_pressed = result
                elif button == self.right_btn:
                    self.right_pressed = result
                elif button == self.jump_btn:
                    self.jump_pressed = result
                elif button == self.shoot_btn:
                    self.shoot_pressed = result
    
    def get_keys_state(self):
        """Retorna estado das teclas simuladas"""
        keys = {}
        keys[pygame.K_LEFT] = self.left_pressed
        keys[pygame.K_RIGHT] = self.right_pressed
        keys[pygame.K_SPACE] = self.jump_pressed
        keys[pygame.K_LCTRL] = self.shoot_pressed
        return keys
    
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

'''

    # Inserir controles touch no início do código
    lines = original_code.split("\n")

    # Encontrar onde inserir (após os imports)
    insert_index = 0
    for i, line in enumerate(lines):
        if line.startswith("# Cores") or line.startswith("WHITE ="):
            insert_index = i
            break

    # Inserir código de controles touch
    lines.insert(insert_index, touch_controls_code)

    # Modificar a classe Game para incluir controles touch
    modified_lines = []
    in_game_init = False
    game_init_found = False

    for line in lines:
        if "class Game:" in line:
            modified_lines.append(line)
        elif "def __init__(self):" in line and not game_init_found:
            modified_lines.append(line)
            modified_lines.append("        # Controles touch para Android")
            modified_lines.append(
                "        self.touch_controls = TouchControls(WIDTH, HEIGHT)"
            )
            game_init_found = True
        elif "for event in pygame.event.get():" in line:
            modified_lines.append(line)
            modified_lines.append("            # Processar eventos touch")
            modified_lines.append("            self.touch_controls.handle_event(event)")
        elif "keys_pressed = pygame.key.get_pressed()" in line:
            modified_lines.append(line)
            modified_lines.append("            # Adicionar controles touch")
            modified_lines.append(
                "            touch_keys = self.touch_controls.get_keys_state()"
            )
            modified_lines.append("            keys_pressed = dict(keys_pressed)")
            modified_lines.append("            for key, pressed in touch_keys.items():")
            modified_lines.append("                if pressed:")
            modified_lines.append("                    keys_pressed[key] = True")
        elif (
            "pygame.display.set_mode" in line
            or "screen = pygame.display.set_mode" in line
        ):
            modified_lines.append("        # Configuração para Android landscape")
            modified_lines.append('        if "ANDROID_ARGUMENT" in os.environ:')
            modified_lines.append(
                "            # Forçar fullscreen landscape no Android"
            )
            modified_lines.append("            info = pygame.display.Info()")
            modified_lines.append(
                "            width, height = info.current_w, info.current_h"
            )
            modified_lines.append(
                "            if width < height:  # Se estiver em portrait, trocar"
            )
            modified_lines.append("                width, height = height, width")
            modified_lines.append(
                "            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)"
            )
            modified_lines.append("        else:")
            modified_lines.append("            " + line)
        elif "pygame.display.flip()" in line:
            modified_lines.append("        # Desenhar controles touch")
            modified_lines.append("        self.touch_controls.draw(self.screen)")
            modified_lines.append(line)
        else:
            modified_lines.append(line)

    # Salvar versão Android
    android_code = "\n".join(modified_lines)
    with open("main_android.py", "w", encoding="utf-8") as f:
        f.write(android_code)

    print("✅ Versão Android criada: main_android.py")
    return True


def build_apk():
    """Compilar APK usando buildozer"""
    print("📦 Compilando APK (isso pode demorar alguns minutos...)")

    try:
        # Backup do main.py original
        if os.path.exists("main_android.py"):
            if os.path.exists("main.py.backup"):
                os.remove("main.py.backup")
            os.rename("main.py", "main.py.backup")
            os.rename("main_android.py", "main.py")

        # Compilar APK
        print("⏳ Iniciando compilação...")
        result = subprocess.run(
            ["buildozer", "android", "debug"], capture_output=False, text=True
        )

        # Restaurar main.py original
        if os.path.exists("main.py.backup"):
            os.remove("main.py")
            os.rename("main.py.backup", "main.py")

        if result.returncode == 0:
            print("✅ APK compilado com sucesso!")
            return True
        else:
            print("❌ Erro na compilação")
            return False

    except Exception as e:
        print(f"❌ Erro ao compilar: {e}")
        # Restaurar main.py em caso de erro
        if os.path.exists("main.py.backup"):
            if os.path.exists("main.py"):
                os.remove("main.py")
            os.rename("main.py.backup", "main.py")
        return False


def install_apk(device_id):
    """Instalar APK no emulador"""
    print(f"📱 Instalando APK no emulador {device_id}...")

    # Encontrar APK gerado
    apk_path = None
    bin_dir = Path("bin")
    if bin_dir.exists():
        apk_files = list(bin_dir.glob("*.apk"))
        if apk_files:
            apk_path = apk_files[-1]  # Pegar o mais recente

    if not apk_path:
        print("❌ APK não encontrado na pasta bin/")
        return False

    print(f"📦 Instalando: {apk_path.name}")

    try:
        result = subprocess.run(
            ["adb", "-s", device_id, "install", "-r", str(apk_path)],
            capture_output=True,
            text=True,
        )

        if "Success" in result.stdout:
            print("✅ APK instalado com sucesso!")
            return True
        else:
            print(f"❌ Erro na instalação: {result.stdout}")
            return False

    except Exception as e:
        print(f"❌ Erro ao instalar: {e}")
        return False


def launch_app(device_id):
    """Iniciar o app no emulador"""
    print(f"🚀 Iniciando jogo no emulador {device_id}...")

    try:
        package_name = "org.example.platformgame"

        result = subprocess.run(
            [
                "adb",
                "-s",
                device_id,
                "shell",
                "am",
                "start",
                "-n",
                f"{package_name}/org.kivy.android.PythonActivity",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Jogo iniciado no emulador!")
            print("🎮 Use os controles touch na tela:")
            print("   ◀ ▶ - Movimento")
            print("   ↑ - Pulo")
            print("   ● - Atirar")
            print("📱 Jogo forçado em orientação LANDSCAPE")
            return True
        else:
            print(f"❌ Erro ao iniciar: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        return False


def main():
    """Função principal"""
    print("🎮 PLATFORM GAME - BUILD ANDROID")
    print("==================================")
    print("")

    # 1. Configurar ambiente Android
    if not setup_android_env():
        print("❌ Falha ao configurar ambiente Android")
        return False

    # 2. Verificar emulador
    found, device_id = check_emulator_advanced()

    if not found:
        print("📱 Nenhum emulador rodando. Tentando iniciar automaticamente...")
        if not start_emulator_if_needed():
            print("")
            print("❌ EMULADOR NÃO ENCONTRADO!")
            print("")
            print("📱 INSTRUÇÕES MANUAIS:")
            print("1. Abra o Android Studio")
            print("2. Vá em Tools > AVD Manager")
            print("3. Inicie um emulador Android")
            print("4. Aguarde carregar completamente")
            print("5. Execute este script novamente")
            print("")
            input("Pressione ENTER após iniciar o emulador...")

            # Tentar novamente após instrução manual
            found, device_id = check_emulator_advanced()
            if not found:
                print("❌ Ainda não foi possível detectar o emulador")
                return False

    print(f"✅ Usando emulador: {device_id}")

    # 3. Criar versão Android
    if not create_android_version():
        return False

    # 4. Compilar APK
    if not build_apk():
        return False

    # 5. Instalar no emulador
    if not install_apk(device_id):
        return False

    # 6. Iniciar jogo
    if not launch_app(device_id):
        return False

    print("\n🎉 SUCESSO!")
    print("🎮 Seu jogo está rodando no emulador Android!")
    print("📱 Controles touch estão disponíveis na tela")
    print("🌊 Divirta-se com o Platform Game - Vista do Mar!")
    print("📐 Orientação forçada: LANDSCAPE")
    return True


if __name__ == "__main__":
    main()
