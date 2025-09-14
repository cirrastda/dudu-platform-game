#!/usr/bin/env python3
"""
Script simples para instalar APK no emulador quando estiver disponível
"""

import subprocess
import time
import os


def find_android_sdk():
    """Encontra o Android SDK"""
    possible_paths = [
        os.path.expanduser("~/AppData/Local/Android/Sdk"),
        "C:/Android/Sdk",
        "C:/Users/ANDERSON MATUCHENKO/AppData/Local/Android/Sdk",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def wait_for_emulator():
    """Aguarda um emulador estar disponível"""
    android_sdk = find_android_sdk()
    if not android_sdk:
        print("❌ Android SDK não encontrado")
        return None

    adb_path = os.path.join(android_sdk, "platform-tools", "adb.exe")
    if not os.path.exists(adb_path):
        adb_path = os.path.join(android_sdk, "platform-tools", "adb")

    if not os.path.exists(adb_path):
        print("❌ ADB não encontrado")
        return None

    print("🔍 Aguardando emulador estar disponível...")

    for attempt in range(60):  # 5 minutos
        try:
            result = subprocess.run(
                [adb_path, "devices"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines[
                    1:
                ]:  # Pula a primeira linha "List of devices attached"
                    if line.strip() and "\t" in line:
                        device_id, status = line.split("\t")
                        if "emulator" in device_id:
                            print(f"🔍 Emulador encontrado: {device_id} ({status})")
                            if status == "device":
                                print(f"✅ Emulador {device_id} está online!")
                                return device_id, adb_path
                            elif status == "offline":
                                print(
                                    f"⚠️ Emulador {device_id} ainda está offline, aguardando..."
                                )
                                # Não retorna, continua aguardando

            print(f"⏳ Tentativa {attempt + 1}/60 - Nenhum emulador encontrado")
            time.sleep(5)

        except Exception as e:
            print(f"⚠️ Erro na tentativa {attempt + 1}: {e}")
            time.sleep(5)

    print("❌ Timeout: Nenhum emulador encontrado em 5 minutos")
    return None


def install_apk(device_id, adb_path, apk_path):
    """Instala o APK no dispositivo"""
    print(f"📱 Instalando APK {apk_path} no dispositivo {device_id}...")

    for attempt in range(3):
        try:
            print(f"📦 Tentativa de instalação {attempt + 1}/3...")

            # Habilita fontes desconhecidas
            try:
                subprocess.run(
                    [
                        adb_path,
                        "-s",
                        device_id,
                        "shell",
                        "settings",
                        "put",
                        "global",
                        "install_non_market_apps",
                        "1",
                    ],
                    capture_output=True,
                    timeout=10,
                )
                subprocess.run(
                    [
                        adb_path,
                        "-s",
                        device_id,
                        "shell",
                        "settings",
                        "put",
                        "secure",
                        "install_non_market_apps",
                        "1",
                    ],
                    capture_output=True,
                    timeout=10,
                )
            except:
                pass

            # Instala o APK
            result = subprocess.run(
                [adb_path, "-s", device_id, "install", "-r", "-t", "-g", apk_path],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                print("✅ APK instalado com sucesso!")

                # Tenta executar a aplicação
                time.sleep(3)

                commands = [
                    [
                        adb_path,
                        "-s",
                        device_id,
                        "shell",
                        "am",
                        "start",
                        "-n",
                        "com.platformgame.app/.MainActivity",
                    ],
                    [
                        adb_path,
                        "-s",
                        device_id,
                        "shell",
                        "am",
                        "start",
                        "-a",
                        "android.intent.action.MAIN",
                        "-n",
                        "com.platformgame.app/.MainActivity",
                    ],
                    [
                        adb_path,
                        "-s",
                        device_id,
                        "shell",
                        "monkey",
                        "-p",
                        "com.platformgame.app",
                        "1",
                    ],
                ]

                for cmd in commands:
                    try:
                        exec_result = subprocess.run(
                            cmd, capture_output=True, text=True, timeout=15
                        )
                        print(f"🚀 Comando: {' '.join(cmd[2:])}")
                        if exec_result.returncode == 0:
                            print("🎮 Aplicação iniciada com sucesso!")

                            # Verifica se está rodando
                            time.sleep(2)
                            check_result = subprocess.run(
                                [adb_path, "-s", device_id, "shell", "ps"],
                                capture_output=True,
                                text=True,
                                timeout=10,
                            )

                            if (
                                "platformgame" in check_result.stdout
                                or "com.platformgame.app" in check_result.stdout
                            ):
                                print("✅ SUCESSO! Aplicação está rodando no emulador!")
                                return True
                        else:
                            print(f"⚠️ Comando falhou: {exec_result.stderr}")
                    except Exception as e:
                        print(f"⚠️ Erro executando comando: {e}")

                print("⚠️ APK instalado mas aplicação pode não ter iniciado")
                return True

            else:
                print(f"⚠️ Tentativa {attempt + 1} falhou: {result.stderr}")
                time.sleep(3)

        except Exception as e:
            print(f"❌ Erro na tentativa {attempt + 1}: {e}")
            time.sleep(3)

    print("❌ Todas as tentativas de instalação falharam")
    return False


def main():
    print("🎮 INSTALADOR APK PLATFORM GAME")
    print("================================")

    # Verifica se o APK existe
    # Caminho do APK na pasta dist/android
    dist_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "dist", "android"
    )
    apk_path = os.path.join(dist_dir, "platform_game_unsigned.apk")
    if not os.path.exists(apk_path):
        print(f"❌ APK não encontrado: {apk_path}")
        print("Execute primeiro o build_apk_direct.py para criar o APK")
        return

    # Aguarda emulador
    emulator_info = wait_for_emulator()
    if not emulator_info:
        print("❌ Nenhum emulador disponível")
        return

    device_id, adb_path = emulator_info

    # Instala o APK
    success = install_apk(device_id, adb_path, apk_path)

    if success:
        print("\n🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"📱 O jogo foi instalado no emulador {device_id}")
        print("🎮 Verifique o emulador para jogar!")
    else:
        print("\n❌ FALHA NA INSTALAÇÃO")
        print("Verifique se o emulador está funcionando corretamente")


if __name__ == "__main__":
    main()
