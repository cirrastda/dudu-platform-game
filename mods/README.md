# 📦 Sistema de MODs - Jump and Hit

## 🎯 O que são MODs?

MODs (modificações) são arquivos Python que podem alterar o comportamento do jogo.
Eles são carregados automaticamente quando o jogo inicia.

## 📍 Como usar MODs

### Na versão compilada (.exe):
1. Crie uma pasta chamada `mods` no mesmo local do executável
2. Coloque seus arquivos `.py` dentro dessa pasta
3. Execute o jogo normalmente

### Durante desenvolvimento:
1. Crie arquivos `.py` nesta pasta (`mods/`)
2. Execute `python main.py` normalmente

## 📝 Como criar um MOD

Crie um arquivo `.py` com uma função `init_mod(game)`:

```python
def init_mod(game):
    """
    Função chamada quando o MOD é carregado
    
    Args:
        game: Objeto Game com acesso completo ao jogo
    """
    # Seu código aqui
    game.lives += 10
```

## 🔧 Exemplos

### Dar vidas extras
```python
def init_mod(game):
    game.lives = min(game.lives + 10, 99)
    print(f"Vidas: {game.lives}")
```

### Dar pontos iniciais
```python
def init_mod(game):
    game.score += 10000
    print(f"Pontuação: {game.score}")
```

### Ativar power-ups
```python
def init_mod(game):
    game.player.is_invulnerable = True
    game.player.invulnerability_timer = 3000
    game.shield_active = True
    print("Power-ups ativados!")
```

### Modo Deus
```python
def init_mod(game):
    game.lives = 99
    game.player.is_invulnerable = True
    game.player.invulnerability_timer = 999999
    game.shield_active = True
    print("GOD MODE ativado!")
```

### Iniciar em nível específico
```python
def init_mod(game):
    game.current_level = 25
    print(f"Iniciando no nível {game.current_level}")
```

### Ajustar dificuldade
```python
def init_mod(game):
    from internal.engine.difficulty import Difficulty
    game.difficulty = Difficulty.EASY
    print("Dificuldade: Fácil")
```

## 🎮 API Disponível

### Gameplay
- `game.score` - Pontuação
- `game.lives` - Vidas restantes
- `game.current_level` - Nível atual (1-51)
- `game.difficulty` - Dificuldade (Difficulty.EASY/NORMAL/HARD)
- `game.state` - Estado do jogo (GameState.*)

### Player
- `game.player.x, game.player.y` - Posição
- `game.player.vel_x, game.player.vel_y` - Velocidade
- `game.player.is_invulnerable` - Invulnerabilidade
- `game.player.invulnerability_timer` - Timer de invulnerabilidade
- `game.player.double_jump_enabled` - Pulo duplo
- `game.player.double_jump_timer` - Timer de pulo duplo

### Power-ups
- `game.shield_active` - Escudo ativo
- `game.tempo_active` - Lentidão ativa
- `game.tempo_timer` - Timer de lentidão
- `game.super_shot_active` - Super tiro ativo
- `game.super_shot_timer` - Timer de super tiro
- `game.invincibility_active` - Invencibilidade ativa

### Outros
- `game.platforms` - Lista de plataformas do nível
- `game.powerups` - Lista de power-ups disponíveis
- `game.extra_lives` - Lista de vidas extras
- `game.enemies` - Vários tipos (birds, bats, spiders, etc.)

## ⚠️ Avisos

- MODs podem quebrar o jogo se mal programados
- Não há sandbox de segurança - MODs têm acesso total ao jogo
- Use apenas MODs de fontes confiáveis
- MODs são executados na ordem alfabética dos nomes de arquivo
- Se um MOD causar erro, ele será ignorado e o jogo continuará
- Remova MODs problemáticos e reinicie o jogo

## 🐛 Problemas?

- Veja as mensagens no console/terminal para erros
- Remova todos os MODs para isolar o problema
- Verifique se a função `init_mod(game)` existe no seu MOD
- Certifique-se de que o arquivo está com extensão `.py`

## 📖 Mais Informações

Para mais detalhes sobre a API do jogo, consulte o código fonte em:
- `internal/engine/game.py` - Classe principal Game
- `internal/resources/player.py` - Classe Player
- `internal/engine/state.py` - Estados do jogo
- `internal/engine/difficulty.py` - Níveis de dificuldade
