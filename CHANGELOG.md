# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Planejado
- Sistema de power-ups
- Mais tipos de inimigos
- Editor de níveis
- Modo multiplayer local
- Suporte a mods

## [0.0.1-alpha.1] - 2024-01-15

### 🎉 Primeira Versão Alpha

Esta é a primeira versão alpha do **Jogo de Plataforma - Vista do Mar**, criada para testes e feedback da comunidade.

### ✨ Adicionado

#### 🎮 Recursos do Jogo
- **5 níveis completos** com dificuldade progressiva (20-40 plataformas por nível)
- **Sistema de física realista** com gravidade e mecânicas de pulo
- **Sistema de vidas** (3 vidas por jogo)
- **Sistema de pontuação** (10 pontos por plataforma alcançada)
- **Câmera dinâmica** que segue o jogador suavemente
- **Múltiplos fundos** com gradientes céu-mar e elementos animados

#### 🕹️ Controles e Input
- **Controles de teclado completos**:
  - Movimento: Setas ← → ou A/D
  - Pulo: Espaço, Seta ↑ ou W
  - Agachar: Seta ↓ ou S
  - Atirar: Ctrl ou X
  - Reiniciar: R (após Game Over)
  - Sair: ESC
- **Suporte completo a joystick/gamepad**:
  - Detecção automática de controles
  - Mapeamento para Xbox e PlayStation
  - Suporte a analógico e D-pad
- **Utilitários de debug** para joystick (`debug_joystick.py`, `test_joystick.py`)

#### 👾 Inimigos e Combat
- **Pássaros voadores** com animação e movimento horizontal
- **Tartarugas patrulheiras** que caminham nas plataformas
- **Sistema de tiro** para eliminar inimigos
- **Animações de explosão** quando inimigos são eliminados
- **Detecção de colisão** precisa entre jogador e inimigos

#### 🎨 Elementos Visuais
- **Sprites animados do jogador** com diferentes estados:
  - Parado, correndo, pulando, agachado
  - Animações suaves de transição
- **Texturas variadas** para plataformas
- **Bandeira animada** no final de cada nível
- **Interface HUD completa**:
  - Contador de vidas com ícones
  - Pontuação em tempo real
  - Indicador de nível atual
- **Efeitos visuais** (explosões, partículas)

#### 🎵 Áudio
- **Múltiplas trilhas sonoras**:
  - Música de introdução
  - 4 músicas de fundo diferentes para os níveis
- **Efeitos sonoros completos**:
  - Som de pulo
  - Som de tiro
  - Som de explosão
  - Som de vida extra
- **Sistema de cache de áudio** para performance otimizada

#### 🖥️ Interface e Menus
- **Tela de splash** com logos
- **Menu principal** navegável
- **Tela de game over** com opção de reiniciar
- **Tela de vitória** com troféu
- **Sistema de ranking** persistente:
  - Entrada de nome do jogador
  - Salvamento de recordes
  - Exibição de top scores
- **Tela de créditos**
- **Tela de recordes**

#### 🏗️ Arquitetura e Código
- **Arquitetura orientada a objetos** bem estruturada
- **Sistema de estados** para gerenciar diferentes telas
- **Cache de recursos** para otimização de performance:
  - Cache de imagens com redimensionamento
  - Cache de sons
  - Estatísticas de cache
- **Gerador procedural de níveis** com múltiplos padrões:
  - Padrão escada
  - Padrão onda
  - Padrão zigue-zague
  - Padrão espiral
  - Clusters aleatórios
  - Padrão labirinto
  - Padrão ponte
  - Padrão torre
- **Sistema de configuração** via arquivo `.env`
- **Gerenciamento de ranking** com persistência em JSON

#### 🔧 Sistema de Build
- **Build multiplataforma** com suporte completo para:
  - Windows (x64) - Executável .exe
  - Linux (x64) - Binário nativo
  - macOS (x64/ARM64) - Binário universal
- **Script de build avançado** (`build.py`) com:
  - Detecção automática de plataforma
  - Verificação de dependências
  - Limpeza automática de arquivos temporários
  - Inclusão automática de recursos (imagens, sons, músicas)
  - Nomeação inteligente de executáveis com versão
  - Criação de pacotes de release
- **Script de release automatizado** (`build_release.py`) com:
  - Criação de pacotes ZIP
  - Instruções específicas por plataforma
  - Documentação incluída
  - Timestamp nos releases
- **Configuração de versão centralizada** (`version.py`)

#### 📚 Documentação
- **README.md completo** com:
  - Instruções detalhadas de instalação
  - Guia de build multiplataforma
  - Solução de problemas comuns
  - Documentação de controles
  - Estrutura do projeto
- **CHANGELOG.md** para rastreamento de mudanças
- **Instruções de execução** específicas por plataforma

#### 🛠️ Ferramentas de Desenvolvimento
- **Utilitários de debug**:
  - Debug de joystick
  - Teste de joystick
  - Logs detalhados
- **Sistema de configuração** flexível
- **Gerenciamento de dependências** com `requirements.txt`

### 🔧 Técnico

#### Dependências
- **pygame 2.5.2** - Engine principal do jogo
- **pyinstaller 6.3.0** - Para criação de executáveis
- **Python 3.8+** - Versão mínima suportada

#### Arquivos Principais
- `main.py` - Arquivo principal do jogo (3820+ linhas)
- `version.py` - Configuração de versão
- `build.py` - Sistema de build multiplataforma
- `build_release.py` - Automação de releases
- `debug_joystick.py` - Utilitário de debug
- `test_joystick.py` - Teste de joystick

#### Estrutura de Recursos
- `imagens/` - Sprites, texturas, fundos, logos
- `musicas/` - Trilha sonora (5 arquivos MP3)
- `sounds/` - Efeitos sonoros (4 arquivos MP3)

### 🐛 Problemas Conhecidos

#### Limitações da Versão Alpha
- **Performance**: Pode haver quedas de FPS em sistemas mais antigos
- **Compatibilidade**: Testado principalmente em Windows 10/11
- **Balanceamento**: Dificuldade dos níveis pode precisar de ajustes
- **Audio**: Alguns efeitos sonoros podem não tocar em certas configurações

#### Issues Técnicos
- Build para macOS pode requerer assinatura de código
- Alguns joysticks podem não ser detectados corretamente
- Cache de recursos pode consumir muita memória em sessões longas

### 📋 Requisitos do Sistema

#### Mínimos
- **SO**: Windows 10, Linux (Ubuntu 20.04+), macOS 10.14+
- **RAM**: 512 MB
- **Espaço**: 100 MB livres
- **GPU**: Suporte básico a OpenGL

#### Recomendados
- **SO**: Windows 11, Linux (Ubuntu 22.04+), macOS 12+
- **RAM**: 1 GB
- **Espaço**: 200 MB livres
- **GPU**: Placa dedicada com drivers atualizados

### 🎯 Objetivos da Versão Alpha

1. **Validar conceito** do jogo de plataforma
2. **Testar sistema de build** multiplataforma
3. **Coletar feedback** da comunidade
4. **Identificar bugs** e problemas de performance
5. **Avaliar jogabilidade** e balanceamento

### 🚀 Próximos Passos

Para a próxima versão (0.0.2-alpha.2), planejamos:
- Correção de bugs reportados
- Otimizações de performance
- Melhorias na compatibilidade
- Novos recursos baseados no feedback

---

## Formato das Versões

- **MAJOR.MINOR.PATCH-STAGE.BUILD**
- **Exemplo**: 0.0.1-alpha.1

### Estágios de Desenvolvimento
- **alpha**: Versão inicial para testes internos
- **beta**: Versão para testes públicos
- **rc**: Release Candidate (candidato a lançamento)
- **stable**: Versão estável para produção

### Tipos de Mudanças
- **Adicionado**: Novos recursos
- **Alterado**: Mudanças em recursos existentes
- **Depreciado**: Recursos que serão removidos
- **Removido**: Recursos removidos
- **Corrigido**: Correções de bugs
- **Segurança**: Correções de vulnerabilidades

---

**Nota**: Esta é uma versão alpha destinada a testes. Feedback e relatórios de bugs são muito bem-vindos!