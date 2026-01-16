# Como Testar a Versão Demo Localmente

## Durante o Desenvolvimento

Para testar a funcionalidade da versão Demo sem compilar:

### Windows PowerShell

```powershell
# Definir modo Demo
$env:PLATFORM_GAME_DEMO = "1"

# Executar o jogo
python main.py

# Para desativar o modo Demo
Remove-Item Env:\PLATFORM_GAME_DEMO
```

### Windows CMD

```cmd
# Definir modo Demo
set PLATFORM_GAME_DEMO=1

# Executar o jogo
python main.py

# Para desativar o modo Demo
set PLATFORM_GAME_DEMO=
```

### Linux/Mac

```bash
# Definir modo Demo
export PLATFORM_GAME_DEMO=1

# Executar o jogo
python main.py

# Para desativar o modo Demo
unset PLATFORM_GAME_DEMO
```

## Comportamento Esperado

Quando em modo Demo:

1. **Fase 1-9**: Jogo funciona normalmente
2. **Fase 10**: Ao completar, aparece mensagem de Demo
3. **Após mensagem**: Retorna ao menu principal automaticamente
4. **Limite**: Não é possível acessar fase 11 ou superior

## Teste Rápido

Para testar rapidamente, você pode iniciar direto na fase 10:

### Criar arquivo `.env`

```env
environment=development
initial-stage=10
PLATFORM_GAME_DEMO=1
```

Depois execute:

```bash
python main.py
```

Agora o jogo iniciará na fase 10 em modo Demo. Complete a fase e veja a mensagem.

## Compilando a Demo para Testes

Para testar a versão compilada:

```bash
# Compilar versão Demo
python run_build\build_demo.py

# Executar a Demo compilada
.\dist\JumpandHit-0.0.3-alpha.1-Demo-win64.exe
```

## Verificações Importantes

### 1. Nome do Executável
O executável compilado deve conter "Demo" no nome para ativar o modo automaticamente.

### 2. Mensagem de Demo
Ao completar a fase 10, deve aparecer:

```
╔════════════════════════════════════════════════════════════╗
║                     Versão Demo                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Esta é uma versão de Demonstração do jogo.               ║
║                                                            ║
║  Para jogar o game completo, você deve comprá-lo,         ║
║  no site https://v0-cirrastec.vercel.app/jogos/jump-and-hit
║  ou na página do jogo na Steam.                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

              [Enter: Voltar ao Menu]
```

### 3. Retorno ao Menu
Após pressionar Enter (ou botão A do controle), o jogo deve:
- Voltar ao menu principal
- Resetar pontuação
- Resetar vidas
- Limpar save automático

## Troubleshooting

### Problema: Jogo não entra em modo Demo

**Solução 1**: Verificar variável de ambiente
```bash
# Windows PowerShell
$env:PLATFORM_GAME_DEMO

# Linux/Mac
echo $PLATFORM_GAME_DEMO
```

Deve retornar "1".

**Solução 2**: Verificar no código
Adicione print em `internal/utils/edition.py`:

```python
@classmethod
def is_demo(cls):
    print(f"[DEBUG] Demo Mode Check: {cls._is_demo}")
    # resto do código...
```

### Problema: Mensagem não aparece ao completar fase 10

**Verificação**: 
1. Confirme que está em modo Demo
2. Verifique se completou realmente a fase (pegou a bandeira/foi abduzido)
3. Veja os logs no console

### Problema: Executável compilado não está em modo Demo

**Causa**: O nome do executável não contém "Demo"

**Solução**: Certifique-se de usar `build_demo.py` em vez de `build.py`

## Alterando Configurações da Demo

Para mudar o número de fases ou a mensagem, edite `internal/utils/edition.py`:

```python
class GameEdition:
    # Mudar número de fases da demo
    _max_demo_levels = 10  # Altere aqui
    
    # Mudar URLs
    _demo_url = "https://v0-cirrastec.vercel.app/jogos/jump-and-hit"
    _demo_steam_url = "Steam"
    
    @classmethod
    def get_demo_message(cls):
        # Personalize a mensagem aqui
        return (
            "Esta é uma versão de Demonstração do jogo.\n\n"
            f"Para jogar o game completo, você deve comprá-lo,\n"
            f"no site {cls._demo_url}\n"
            f"ou na página do jogo na {cls._demo_steam_url}."
        )
```

## Testes Automatizados

TODO: Criar testes unitários para versão Demo
- Teste de limite de fases
- Teste de mensagem ao completar fase 10
- Teste de reset ao voltar ao menu

---

**Última atualização**: 04/01/2026
