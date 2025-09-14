#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar e executar o jogo no emulador Android
Requer Android Studio instalado com SDK e emulador configurado
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def find_android_sdk():
    """Encontrar o caminho do Android SDK"""
    possible_paths = [
        os.path.expanduser("~/AppData/Local/Android/Sdk"),
        "C:/Users/%s/AppData/Local/Android/Sdk" % os.getenv('USERNAME'),
        "C:/Android/Sdk",
        "C:/Program Files/Android/Sdk",
        "C:/Program Files (x86)/Android/Sdk"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def setup_android_env():
    """Configurar variáveis de ambiente do Android"""
    sdk_path = find_android_sdk()
    if not sdk_path:
        print("❌ Android SDK não encontrado!")
        print("📱 Instale o Android Studio e configure o SDK")
        return False
    
    print(f"✅ Android SDK encontrado: {sdk_path}")
    
    # Adicionar ao PATH
    platform_tools = os.path.join(sdk_path, "platform-tools")
    tools = os.path.join(sdk_path, "tools")
    emulator_path = os.path.join(sdk_path, "emulator")
    cmdline_tools = os.path.join(sdk_path, "cmdline-tools", "latest", "bin")
    
    paths_to_add = [platform_tools, tools, emulator_path, cmdline_tools]
    current_path = os.environ.get('PATH', '')
    
    for path in paths_to_add:
        if os.path.exists(path) and path not in current_path:
            os.environ['PATH'] = f"{path};{current_path}"
            current_path = os.environ['PATH']
    
    os.environ['ANDROID_HOME'] = sdk_path
    os.environ['ANDROID_SDK_ROOT'] = sdk_path
    
    print(f"✅ PATH atualizado com ferramentas Android")
    return True

def check_emulator():
    """Verificar se há emulador rodando"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # Pular cabeçalho
        devices = [line for line in lines if line.strip() and 'device' in line]
        
        if devices:
            print(f"✅ Emulador encontrado: {len(devices)} dispositivo(s)")
            return True
        else:
            print("❌ Nenhum emulador rodando")
            return False
    except FileNotFoundError:
        print("❌ ADB não encontrado no PATH")
        return False

def start_emulator():
    """Tentar iniciar um emulador"""
    try:
        # Listar AVDs disponíveis
        result = subprocess.run(['emulator', '-list-avds'], capture_output=True, text=True)
        avds = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        
        if not avds:
            print("❌ Nenhum AVD encontrado")
            print("📱 Crie um emulador no Android Studio primeiro")
            return False
        
        print(f"📱 AVDs disponíveis: {', '.join(avds)}")
        avd_name = avds[0]  # Usar o primeiro AVD
        
        print(f"🚀 Iniciando emulador: {avd_name}")
        subprocess.Popen(['emulator', '-avd', avd_name], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Aguardar emulador inicializar
        print("⏳ Aguardando emulador inicializar...")
        for i in range(60):  # Aguardar até 60 segundos
            time.sleep(1)
            if check_emulator():
                print("✅ Emulador iniciado com sucesso!")
                return True
            if i % 10 == 0:
                print(f"⏳ Aguardando... ({i}s)")
        
        print("❌ Timeout ao iniciar emulador")
        return False
        
    except FileNotFoundError:
        print("❌ Comando 'emulator' não encontrado")
        return False

def adapt_game_for_android():
    """Adaptar o jogo para controles touch Android"""
    print("🎮 Adaptando jogo para controles touch...")
    
    # Ler o jogo original
    with open('main.py', 'r', encoding='utf-8') as f:
        game_code = f.read()
    
    # Adaptações para Android
    android_adaptations = '''
# Adaptações para Android Touch
import pygame.locals as pg_locals

# Configurações touch
TOUCH_BUTTON_SIZE = 80
TOUCH_BUTTON_ALPHA = 128
TOUCH_MARGIN = 20

class TouchControls:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Posições dos botões touch
        self.left_btn = pygame.Rect(TOUCH_MARGIN, screen_height - TOUCH_BUTTON_SIZE - TOUCH_MARGIN, TOUCH_BUTTON_SIZE, TOUCH_BUTTON_SIZE)
        self.right_btn = pygame.Rect(TOUCH_MARGIN + TOUCH_BUTTON_SIZE + 10, screen_height - TOUCH_BUTTON_SIZE - TOUCH_MARGIN, TOUCH_BUTTON_SIZE, TOUCH_BUTTON_SIZE)
        self.jump_btn = pygame.Rect(screen_width - TOUCH_BUTTON_SIZE - TOUCH_MARGIN, screen_height - TOUCH_BUTTON_SIZE - TOUCH_MARGIN, TOUCH_BUTTON_SIZE, TOUCH_BUTTON_SIZE)
        self.shoot_btn = pygame.Rect(screen_width - TOUCH_BUTTON_SIZE*2 - TOUCH_MARGIN - 10, screen_height - TOUCH_BUTTON_SIZE - TOUCH_MARGIN, TOUCH_BUTTON_SIZE, TOUCH_BUTTON_SIZE)
        
        # Estados dos botões
        self.left_pressed = False
        self.right_pressed = False
        self.jump_pressed = False
        self.shoot_pressed = False
        
    def handle_touch(self, pos, pressed):
        """Processar eventos de toque"""
        if self.left_btn.collidepoint(pos):
            self.left_pressed = pressed
        elif self.right_btn.collidepoint(pos):
            self.right_pressed = pressed
        elif self.jump_btn.collidepoint(pos):
            self.jump_pressed = pressed
        elif self.shoot_btn.collidepoint(pos):
            self.shoot_pressed = pressed
    
    def draw(self, screen):
        """Desenhar controles touch"""
        # Superfície semi-transparente para botões
        button_surface = pygame.Surface((TOUCH_BUTTON_SIZE, TOUCH_BUTTON_SIZE))
        button_surface.set_alpha(TOUCH_BUTTON_ALPHA)
        
        # Botão esquerda
        color = (100, 100, 255) if self.left_pressed else (200, 200, 200)
        button_surface.fill(color)
        screen.blit(button_surface, self.left_btn)
        font = pygame.font.Font(None, 36)
        text = font.render("◀", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.left_btn.center)
        screen.blit(text, text_rect)
        
        # Botão direita
        color = (100, 100, 255) if self.right_pressed else (200, 200, 200)
        button_surface.fill(color)
        screen.blit(button_surface, self.right_btn)
        text = font.render("▶", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.right_btn.center)
        screen.blit(text, text_rect)
        
        # Botão pulo
        color = (100, 255, 100) if self.jump_pressed else (200, 200, 200)
        button_surface.fill(color)
        screen.blit(button_surface, self.jump_btn)
        text = font.render("↑", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.jump_btn.center)
        screen.blit(text, text_rect)
        
        # Botão tiro
        color = (255, 100, 100) if self.shoot_pressed else (200, 200, 200)
        button_surface.fill(color)
        screen.blit(button_surface, self.shoot_btn)
        text = font.render("●", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.shoot_btn.center)
        screen.blit(text, text_rect)

'''
    
    # Inserir adaptações no início do código
    adapted_code = android_adaptations + "\n" + game_code
    
    # Modificar a classe Game para incluir controles touch
    # Procurar pela inicialização da classe Game
    if "def __init__(self):" in adapted_code:
        adapted_code = adapted_code.replace(
            "def __init__(self):",
            "def __init__(self):\n        # Controles touch para Android\n        self.touch_controls = TouchControls(WIDTH, HEIGHT)"
        )
    
    # Modificar o loop de eventos para incluir touch
    if "for event in pygame.event.get():" in adapted_code:
        touch_event_code = '''
            # Eventos touch para Android
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo (touch)
                    self.touch_controls.handle_touch(event.pos, True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Soltar touch
                    self.touch_controls.handle_touch(event.pos, False)
'''
        
        # Encontrar onde inserir o código touch
        lines = adapted_code.split('\n')
        for i, line in enumerate(lines):
            if "elif event.type == pygame.QUIT:" in line:
                lines.insert(i, touch_event_code)
                break
        adapted_code = '\n'.join(lines)
    
    # Modificar controles do jogador para usar touch
    player_control_code = '''
        # Controles touch
        if self.touch_controls.left_pressed:
            keys_pressed[pygame.K_LEFT] = True
        if self.touch_controls.right_pressed:
            keys_pressed[pygame.K_RIGHT] = True
        if self.touch_controls.jump_pressed:
            keys_pressed[pygame.K_SPACE] = True
        if self.touch_controls.shoot_pressed:
            keys_pressed[pygame.K_LCTRL] = True
'''
    
    # Inserir controles touch antes da atualização do jogador
    if "keys_pressed = pygame.key.get_pressed()" in adapted_code:
        adapted_code = adapted_code.replace(
            "keys_pressed = pygame.key.get_pressed()",
            "keys_pressed = pygame.key.get_pressed()\n" + player_control_code
        )
    
    # Adicionar desenho dos controles touch
    if "pygame.display.flip()" in adapted_code:
        adapted_code = adapted_code.replace(
            "pygame.display.flip()",
            "# Desenhar controles touch\n        self.touch_controls.draw(self.screen)\n        pygame.display.flip()"
        )
    
    # Salvar versão adaptada
    with open('main_android.py', 'w', encoding='utf-8') as f:
        f.write(adapted_code)
    
    print("✅ Jogo adaptado salvo como main_android.py")
    return True

def build_apk():
    """Compilar APK usando buildozer"""
    print("📦 Compilando APK...")
    
    try:
        # Usar main_android.py como main
        if os.path.exists('main_android.py'):
            if os.path.exists('main.py.backup'):
                os.remove('main.py.backup')
            os.rename('main.py', 'main.py.backup')
            os.rename('main_android.py', 'main.py')
        
        # Compilar APK
        result = subprocess.run(['buildozer', 'android', 'debug'], 
                              capture_output=True, text=True)
        
        # Restaurar main.py original
        if os.path.exists('main.py.backup'):
            os.remove('main.py')
            os.rename('main.py.backup', 'main.py')
        
        if result.returncode == 0:
            print("✅ APK compilado com sucesso!")
            return True
        else:
            print(f"❌ Erro na compilação: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao compilar: {e}")
        return False

def install_apk():
    """Instalar APK no emulador"""
    print("📱 Instalando APK no emulador...")
    
    # Encontrar APK gerado
    apk_path = None
    bin_dir = Path('bin')
    if bin_dir.exists():
        apk_files = list(bin_dir.glob('*.apk'))
        if apk_files:
            apk_path = apk_files[0]
    
    if not apk_path:
        print("❌ APK não encontrado")
        return False
    
    try:
        result = subprocess.run(['adb', 'install', '-r', str(apk_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ APK instalado com sucesso!")
            return True
        else:
            print(f"❌ Erro na instalação: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao instalar: {e}")
        return False

def launch_app():
    """Iniciar o app no emulador"""
    print("🚀 Iniciando jogo no emulador...")
    
    try:
        # Ler package name do buildozer.spec
    package_name = "org.example.platformgame"  # default
    
    buildozer_path = os.path.join('run_build', 'config', 'buildozer.spec')
    if os.path.exists(buildozer_path):
        with open(buildozer_path, 'r') as f:
                for line in f:
                    if line.startswith('package.domain'):
                        domain = line.split('=')[1].strip()
                    elif line.startswith('package.name'):
                        name = line.split('=')[1].strip()
                        package_name = f"{domain}.{name}"
                        break
        
        result = subprocess.run([
            'adb', 'shell', 'am', 'start', 
            '-n', f"{package_name}/org.kivy.android.PythonActivity"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Jogo iniciado no emulador!")
            return True
        else:
            print(f"❌ Erro ao iniciar: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        return False

def main():
    """Função principal"""
    print("🎮 PLATFORM GAME - ANDROID EMULATOR")
    print("====================================")
    
    # 1. Configurar ambiente Android
    if not setup_android_env():
        return False
    
    # 2. Verificar/iniciar emulador
    if not check_emulator():
        print("📱 Tentando iniciar emulador...")
        if not start_emulator():
            print("❌ Falha ao iniciar emulador")
            print("📱 Inicie manualmente o emulador no Android Studio")
            return False
    
    # 3. Adaptar jogo para Android
    if not adapt_game_for_android():
        return False
    
    # 4. Compilar APK
    if not build_apk():
        return False
    
    # 5. Instalar no emulador
    if not install_apk():
        return False
    
    # 6. Iniciar jogo
    if not launch_app():
        return False
    
    print("\n🎉 Sucesso! Jogo rodando no emulador Android!")
    print("📱 Controles touch disponíveis na tela")
    return True

if __name__ == "__main__":
    main()