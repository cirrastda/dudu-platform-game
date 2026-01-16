# Guia da Versão Demo - Jump and Hit

## O que é a Versão Demo?

A versão Demo do Jump and Hit é uma versão de demonstração gratuita do jogo que permite aos jogadores experimentarem as **10 primeiras fases** do jogo completo.

## Características da Versão Demo

### ✅ O que está incluído:
- **10 fases jogáveis** - Todas as mecânicas e recursos das primeiras 10 fases
- **Sistema completo de pontuação** - Acumule pontos normalmente
- **Todos os power-ups** - Experimente todos os power-ups disponíveis nas fases iniciais
- **Ranking local** - Compete com suas próprias pontuações
- **Todas as configurações** - Ajuste controles, áudio, vídeo e acessibilidade
- **Sistema de save** - Salva seu progresso dentro das 10 fases

### ❌ Limitações:
- **Apenas 10 fases** - Fases 11 em diante não estão disponíveis
- **Mensagem ao completar fase 10** - Ao completar a décima fase, uma mensagem informará sobre a versão completa
- **Retorno automático ao menu** - Após ver a mensagem, o jogo volta ao menu principal

## Como Compilar a Versão Demo

### Passo 1: Preparar o Ambiente

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

### Passo 2: Executar o Builder da Demo

Na raiz do projeto, execute:

```bash
# Windows
python run_build\build_demo.py

# Linux/Mac
python run_build/build_demo.py
```

### Passo 3: Localizar o Executável

O executável será criado em:
```
dist\JumpandHit-0.0.3-alpha.1-Demo-win64.exe
```

O tamanho deve ser aproximadamente o mesmo da versão completa (~295 MB).

## Mensagem ao Fim da Demo

Quando o jogador completa a fase 10, a seguinte mensagem é exibida:

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

Após pressionar Enter (ou botão A no controle), o jogador retorna ao menu principal.

## Distribuição da Versão Demo

### Plataformas de Distribuição Recomendadas:

1. **Site Oficial**
   - Hospede o executável no seu site
   - Link: https://v0-cirrastec.vercel.app/jogos/jump-and-hit

2. **Plataformas de Jogos Indie**
   - itch.io (recomendado para demos gratuitas)
   - GameJolt
   - IndieDB

3. **Mídia Social**
   - Compartilhe em redes sociais
   - Grupos de jogos indie
   - Fóruns de desenvolvimento de jogos

4. **Steam (quando disponível)**
   - Steam permite demos gratuitas
   - Vinculada à página do jogo completo

### Tamanho e Requisitos

- **Tamanho**: ~295 MB (igual à versão completa, pois contém todos os assets)
- **Sistema Operacional**: Windows 7 ou superior
- **Processador**: Qualquer processador moderno
- **Memória**: 512 MB RAM (mínimo), 1 GB (recomendado)
- **Espaço em Disco**: 350 MB

## Detalhes Técnicos

### Como Funciona Internamente

A versão Demo utiliza um sistema de detecção automática:

1. **Nome do Executável**: Se o executável contém "Demo" no nome, ativa modo demo
2. **Variável de Ambiente**: `PLATFORM_GAME_DEMO=1` força modo demo
3. **Módulo `edition.py`**: Gerencia todas as verificações e limitações

### Arquivos Modificados

- `internal/utils/edition.py` - Sistema de detecção de edição
- `internal/engine/state.py` - Novo estado DEMO_END_MESSAGE
- `internal/engine/game.py` - Usa GameEdition.get_max_levels()
- `internal/engine/game_modules/update.py` - Verifica fim da demo
- `internal/engine/game_modules/draw.py` - Desenha mensagem da demo
- `internal/engine/game_modules/events.py` - Trata eventos da mensagem
- `run_build/build_demo.py` - Script de build para demo

### Desenvolvimento e Testes

Para testar o modo Demo durante o desenvolvimento:

```bash
# Windows PowerShell
$env:PLATFORM_GAME_DEMO="1"
python main.py

# Linux/Mac
export PLATFORM_GAME_DEMO=1
python main.py
```

## Atualização da Versão Demo

Quando lançar uma nova versão do jogo completo, compile uma nova versão Demo com:

```bash
python run_build\build_demo.py
```

Isso garantirá que a demo tenha as mesmas correções e melhorias da versão completa.

## Conversão de Demo para Completo

### Estratégia de Monetização

A versão Demo serve como "funil de vendas":

1. **Jogador baixa Demo** - Sem custo, sem barreiras
2. **Joga as 10 primeiras fases** - Experimenta a jogabilidade
3. **Vê mensagem de compra** - Link claro para compra
4. **Compra versão completa** - Acesso às 51 fases

### Dados que NÃO são Transferidos

Por questões técnicas, o progresso da Demo não é transferido para a versão completa. Os jogadores devem:
- Recomeçar do início
- Manter saves separados

**Nota**: Em futuras versões, pode-se implementar um sistema de transferência de save, mas isso requer:
- Sistema de validação de save
- Detecção de versão instalada
- Migração de dados

## Suporte

### FAQ - Versão Demo

**P: O save da Demo funciona na versão completa?**
R: Não, são versões separadas. O jogador deve recomeçar na versão completa.

**P: Posso modificar o número de fases da Demo?**
R: Sim, edite `internal/utils/edition.py` e altere `_max_demo_levels = 10` para o valor desejado.

**P: A mensagem pode ser personalizada?**
R: Sim, edite o método `get_demo_message()` em `internal/utils/edition.py`.

**P: Como desativar o modo Demo?**
R: O modo Demo é detectado automaticamente pelo nome do executável. Se o nome não contém "Demo", será versão completa.

---

**Versão do Documento**: 1.0  
**Data**: 04 de Janeiro de 2026  
**Autor**: CirrasTec
