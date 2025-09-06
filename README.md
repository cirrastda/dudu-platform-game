# 🎮 Jogo de Plataforma - Vista do Mar

Um jogo de plataforma em Python com 5 níveis de dificuldade crescente, ambientado com uma vista do mar.

## 🌊 Características do Jogo

- **5 níveis** com dificuldade progressiva (20-40 plataformas por nível)
- **Fundo do mar** com ondas animadas e gradiente céu-mar
- **Plataformas espalhadas** sem chão contínuo
- **Bandeira no final** de cada fase (estilo Super Mario)
- **Física realista** com gravidade e pulo
- **Sistema de vidas** (3 vidas por jogo)
- **Sistema de pontuação** (10 pontos por plataforma alcançada)
- **Pássaros inimigos** que voam pela tela
- **Câmera dinâmica** que segue o jogador
- **Agachamento** para passar por obstáculos baixos
- **Controles simples** e responsivos

## 🎯 Objetivo

Navegue pelas plataformas saltando de uma para outra até alcançar a bandeira no final de cada nível. Cuidado para não cair no mar!

## 🕹️ Controles

- **Movimento**: Setas ← → ou A/D
- **Pulo**: Espaço, Seta ↑ ou W
- **Agachar**: Seta ↓ ou S (reduz altura do personagem)
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

1. **Nível 1**: Introdução - 20 plataformas grandes e bem espaçadas
2. **Nível 2**: Básico - 30 plataformas menores com mais variação de altura
3. **Nível 3**: Intermediário - 35 plataformas com saltos mais desafiadores
4. **Nível 4**: Avançado - 40 plataformas pequenas em alturas extremas
5. **Nível 5**: Expert - 40 plataformas com máxima dificuldade e precisão necessária

## 🎯 Sistema de Jogo

- **Vidas**: 3 vidas por jogo
- **Pontuação**: 10 pontos por cada nova plataforma alcançada
- **Inimigos**: Pássaros que voam horizontalmente e causam dano
- **Morte**: Cair no mar ou colidir com pássaros remove uma vida
- **Vitória**: Complete todos os 5 níveis para ver a tela de vitória 🏆

## 🏗️ Estrutura do Projeto

```
plataforma/
├── main.py          # Arquivo principal do jogo
├── build.py         # Script para criar executável
├── requirements.txt # Dependências do projeto
├── README.md       # Este arquivo
└── imagens/         # Pasta com recursos visuais
    ├── fundo.jpg    # Imagem de fundo alternativa
    ├── fundo2.jpg   # Imagem de fundo principal
    ├── objetos.jpg  # Texturas de plataformas
    ├── personagem.jpg # Imagem do personagem
    ├── texturas.png # Texturas adicionais
    └── personagem/  # Sprites do personagem
        ├── 1.png, 2.png, 3.png, 4.png # Animações
        ├── d1.png   # Sprite agachado
        └── j1.png-j5.png # Sprites de pulo
```

## 🎨 Elementos Visuais

- **Jogador**: Retângulo azul com cabeça branca (pode agachar)
- **Plataformas**: Texturas carregadas de imagens ou retângulos marrons
- **Bandeira**: Mastro amarelo com bandeira vermelha triangular
- **Pássaros**: Inimigos voadores que se movem horizontalmente
- **Fundo**: Gradiente do céu para o mar com ondas animadas
- **Interface**: Contador de vidas, pontuação e nível atual
- **Câmera**: Segue o jogador mantendo-o no terço esquerda da tela

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