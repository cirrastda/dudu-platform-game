# 🎮 Jogo de Plataforma - Vista do Mar

**Versão 0.0.1-alpha.1** - Um jogo de plataforma em Python com 5 níveis de dificuldade crescente, ambientado com uma vista do mar.

> ⚠️ **VERSÃO ALPHA**: Esta é uma versão de teste em desenvolvimento. Podem ocorrer bugs e instabilidades.

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
- **Suporte a joystick/gamepad**
- **Sistema de ranking** com recordes
- **Múltiplas telas** (menu, créditos, game over)

## 🎯 Objetivo

Navegue pelas plataformas saltando de uma para outra até alcançar a bandeira no final de cada nível. Cuidado para não cair no mar!

## 🕹️ Controles

### Teclado
- **Movimento**: Setas ← → ou A/D
- **Pulo**: Espaço, Seta ↑ ou W
- **Agachar**: Seta ↓ ou S (reduz altura do personagem)
- **Atirar**: Ctrl ou X
- **Reiniciar** (após Game Over): R
- **Sair**: ESC

### Joystick/Gamepad
- **Movimento**: Analógico esquerdo ou D-pad
- **Pulo**: Botão A (Xbox) / X (PlayStation)
- **Atirar**: Botão X (Xbox) / Quadrado (PlayStation)
- **Menu**: Botão Start/Options

## 🚀 Como Executar

### 🚀 Execução Rápida (VS Code)
Se você está usando VS Code, pressione **F5** e escolha uma das opções:
- **🎮 Jogo - Windows (Run)** - Execução normal
- **🎮 Jogo - Windows (Debug)** - Com debug ativo
- **📱 Build e Teste Android (Debug)** - Para dispositivos móveis
- **🐧 Jogo - Linux (via WSL2)** - Para Linux

### Opção 1: Executar diretamente com Python

1. **Instale o Python 3.8+** (se não tiver)

2. **Clone ou baixe o projeto**

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Execute o jogo**:
```bash
python main.py
```

### 📱 Build para Android
Para compilar para Android:
```bash
python run_build/build_apk_only.py
```
O APK será gerado na pasta `bin/`

### 📁 Scripts de Build
Todos os scripts de build e execução estão organizados na pasta `run_build/`:
- `build_apk_only.py` - Build básico do APK
- `build_apk_direct.py` - Build direto com instalação
- `build_and_run_android.py` - Build e execução automática
- `run_android.py` - Execução otimizada para Android
- `run_linux.py` - Execução via WSL2

### Opção 2: Usar executável pré-compilado

1. **Baixe o executável** para sua plataforma:
   - Windows: `JogoPlataforma-0.0.1-alpha.1-win64.exe`
   - Linux: `JogoPlataforma-0.0.1-alpha.1-linux64`
   - macOS: `JogoPlataforma-0.0.1-alpha.1-macos`

2. **Execute diretamente** (no Linux/macOS, pode ser necessário dar permissão de execução)

### Opção 3: Compilar seu próprio executável

#### Build Simples (Plataforma Atual)
```bash
# Instalar dependências de build
python build.py --install-deps

# Verificar dependências
python build.py --check

# Executar build
python build.py
```

#### Build de Release (Recomendado)
```bash
# Criar pacote completo de release
python build_release.py
```

#### Opções Avançadas de Build
```bash
# Limpar arquivos de build anteriores
python build.py --clean

# Ver ajuda
python build.py --help
python build_release.py --help
```

## 🖥️ Suporte Multiplataforma

### Windows
- **Requisitos**: Windows 10+ (x64)
- **Executável**: `.exe` de arquivo único
- **Testado em**: Windows 10, Windows 11

### Linux
- **Requisitos**: Linux com X11 (x64)
- **Executável**: Binário nativo
- **Testado em**: Ubuntu 20.04+, Fedora 35+

### macOS
- **Requisitos**: macOS 10.14+ (x64/ARM64)
- **Executável**: Binário universal
- **Testado em**: macOS Big Sur, Monterey, Ventura

## 📋 Requisitos do Sistema

### Para Executar
- **Python**: 3.8+ (apenas se executar via código fonte)
- **RAM**: 512 MB mínimo
- **Espaço**: 100 MB livres
- **Placa de vídeo**: Suporte básico a OpenGL

### Para Desenvolvimento
- **Python**: 3.8+
- **pygame**: 2.5.2+
- **pyinstaller**: 6.3.0+ (para builds)

### Dependências (requirements.txt)
```
pygame==2.5.2
pyinstaller==6.3.0
```

## 🎮 Níveis

1. **Nível 1**: Introdução - 20 plataformas grandes e bem espaçadas
2. **Nível 2**: Básico - 30 plataformas menores com mais variação de altura
3. **Nível 3**: Intermediário - 35 plataformas com saltos mais desafiadores
4. **Nível 4**: Avançado - 40 plataformas pequenas em alturas extremas
5. **Nível 5**: Expert - 40 plataformas com máxima dificuldade e precisão necessária

## 🎯 Sistema de Jogo

- **Vidas**: 3 vidas por jogo
- **Pontuação**: 10 pontos por cada nova plataforma alcançada
- **Inimigos**: Pássaros e tartarugas que causam dano
- **Armas**: Sistema de tiro para eliminar inimigos
- **Morte**: Cair no mar ou colidir com inimigos remove uma vida
- **Vitória**: Complete todos os 5 níveis para ver a tela de vitória 🏆
- **Ranking**: Sistema de recordes com nome do jogador

## 🏗️ Estrutura do Projeto

```
platform-game/
├── main.py              # Arquivo principal do jogo
├── version.py           # Configurações de versão
├── build.py             # Script de build multiplataforma
├── build_release.py     # Script de release automatizado
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
├── CHANGELOG.md        # Histórico de mudanças
├── .gitignore          # Arquivos ignorados pelo Git
├── debug_joystick.py   # Utilitário para debug de joystick
├── test_joystick.py    # Teste de joystick
├── imagens/            # Recursos visuais
│   ├── fundo*.jpg      # Imagens de fundo
│   ├── personagem/     # Sprites do personagem
│   ├── inimigos/       # Sprites dos inimigos
│   ├── elementos/      # Elementos do jogo (bandeira, tiro, etc.)
│   ├── texturas/       # Texturas das plataformas
│   └── logos/          # Logos e ícones
├── musicas/            # Trilha sonora
│   ├── fundo*.mp3      # Músicas de fundo
│   └── intro.mp3       # Música de introdução
├── sounds/             # Efeitos sonoros
│   ├── jump.mp3        # Som de pulo
│   ├── shot.mp3        # Som de tiro
│   ├── explosion.mp3   # Som de explosão
│   └── new-life.mp3    # Som de vida extra
├── dist/               # Executáveis compilados (gerado)
├── build/              # Arquivos temporários de build (gerado)
└── releases/           # Pacotes de release (gerado)
```

## 🎨 Elementos Visuais

- **Jogador**: Sprites animados com diferentes estados (parado, correndo, pulando, agachado)
- **Plataformas**: Texturas variadas carregadas de imagens
- **Bandeira**: Mastro amarelo com bandeira vermelha triangular animada
- **Inimigos**: 
  - **Pássaros**: Voam horizontalmente com animação de voo
  - **Tartarugas**: Caminham nas plataformas com patrulhamento
- **Projéteis**: Sistema de tiro com animações de explosão
- **Fundo**: Múltiplos fundos com gradientes e elementos animados
- **Interface**: HUD completo com vidas, pontuação, nível e mini-mapa
- **Câmera**: Sistema avançado que segue o jogador suavemente

## 🔧 Desenvolvimento

### Estrutura de Código
- **Orientado a objetos** com classes bem definidas
- **Sistema de estados** para diferentes telas do jogo
- **Cache de recursos** para otimização de performance
- **Gerador de níveis** procedural com padrões variados
- **Sistema de configuração** via arquivos .env

### Recursos Avançados
- **Detecção automática de joystick**
- **Sistema de ranking persistente**
- **Múltiplas trilhas sonoras**
- **Efeitos visuais** (explosões, partículas)
- **Sistema de debug** integrado

## 🐛 Solução de Problemas

### Problemas Comuns

#### Erro ao instalar pygame
```bash
# Windows
pip install --upgrade pip
pip install pygame

# macOS
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame

# Linux (Ubuntu/Debian)
sudo apt-get install python3-pygame
# ou
pip install pygame
```

#### Erro ao criar executável
```bash
# Verificar instalação do PyInstaller
pip install --upgrade pyinstaller

# Limpar cache e tentar novamente
python build.py --clean
python build.py
```

#### Problemas de Performance
- Feche outros programas que usam muito CPU/GPU
- Verifique se os drivers de vídeo estão atualizados
- Execute em resolução menor se necessário

#### Joystick não funciona
```bash
# Testar detecção de joystick
python debug_joystick.py
python test_joystick.py
```

### Logs e Debug
- Logs são salvos automaticamente durante a execução
- Use a variável de ambiente `DEBUG=1` para mais informações
- Verifique o console para mensagens de erro

## 📝 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico completo de mudanças.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎉 Parabéns!

Se você conseguir completar todos os 5 níveis, você é um verdadeiro mestre das plataformas! 🏆

---

**Versão Alpha 0.0.1** - Esta é uma versão de desenvolvimento. Feedback e relatórios de bugs são muito bem-vindos!