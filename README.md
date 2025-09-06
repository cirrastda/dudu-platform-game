# 🎮 Jogo de Plataforma - Vista do Mar

Um jogo de plataforma em Python com 5 níveis de dificuldade crescente, ambientado com uma vista do mar.

## 🌊 Características do Jogo

- **5 níveis** com dificuldade progressiva
- **Fundo do mar** com ondas animadas
- **Plataformas espalhadas** sem chão contínuo
- **Bandeira no final** de cada fase (estilo Super Mario)
- **Física realista** com gravidade e pulo
- **Controles simples** e responsivos

## 🎯 Objetivo

Navegue pelas plataformas saltando de uma para outra até alcançar a bandeira no final de cada nível. Cuidado para não cair no mar!

## 🕹️ Controles

- **Movimento**: Setas ← → ou A/D
- **Pulo**: Espaço, Seta ↑ ou W
- **Reiniciar** (após Game Over): R
- **Sair**: ESC

## 🚀 Como Executar

### Opção 1: Executar diretamente com Python

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o jogo:
```bash
python main.py
```

### Opção 2: Criar executável

1. Execute o script de build:
```bash
python build.py
```

2. O executável será criado na pasta `dist/`:
   - **macOS/Linux**: `./dist/JogoPlataforma`
   - **Windows**: `dist\JogoPlataforma.exe`

## 📋 Requisitos

- Python 3.7+
- pygame 2.5.2+
- pyinstaller 6.3.0+ (apenas para criar executável)

## 🎮 Níveis

1. **Nível 1**: Introdução - Plataformas grandes e bem espaçadas
2. **Nível 2**: Básico - Plataformas menores com mais variação de altura
3. **Nível 3**: Intermediário - Saltos mais desafiadores
4. **Nível 4**: Avançado - Plataformas pequenas em alturas extremas
5. **Nível 5**: Expert - Máxima dificuldade com precisão necessária

## 🏗️ Estrutura do Projeto

```
plataforma/
├── main.py          # Arquivo principal do jogo
├── build.py         # Script para criar executável
├── requirements.txt # Dependências do projeto
└── README.md       # Este arquivo
```

## 🎨 Elementos Visuais

- **Jogador**: Retângulo azul com cabeça branca
- **Plataformas**: Retângulos marrons com bordas pretas
- **Bandeira**: Mastro marrom com bandeira vermelha
- **Fundo**: Gradiente do céu para o mar com ondas animadas

## 🐛 Solução de Problemas

### Erro ao instalar pygame
```bash
# No macOS, pode ser necessário:
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame
```

### Erro ao criar executável
- Certifique-se de que o PyInstaller está instalado: `pip install pyinstaller`
- Execute o build.py no diretório do jogo

## 🎉 Parabéns!

Se você conseguir completar todos os 5 níveis, você é um verdadeiro mestre das plataformas! 🏆