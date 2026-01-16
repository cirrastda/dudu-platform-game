# Scripts de Build - Jump and Hit

## Builders Disponíveis

### 1. Build Versão Completa - `build.py`
Cria executável da versão completa do jogo (51 fases).

```bash
# Build completo do jogo em um executável único
python run_build\build.py

# Verificar dependências
python run_build\build.py --check

# Instalar dependências
python run_build\build.py --install

# Limpar builds anteriores
python run_build\build.py --clean

# Ajuda
python run_build\build.py --help
```

**Saída**: `dist\JumpandHit-0.0.3-alpha.1-win64.exe` (~295 MB)

### 2. Build Versão Demo - `build_demo.py` ⭐ NOVO
Cria executável da versão de demonstração (10 fases).

```bash
# Build da versão Demo
python run_build\build_demo.py
```

**Saída**: `dist\JumpandHit-0.0.3-alpha.1-Demo-win64.exe` (~295 MB)

**Características da Demo**:
- ✅ Apenas 10 primeiras fases
- ✅ Pop-up ao completar fase 10 com mensagem de compra
- ✅ Retorna ao menu automaticamente
- ✅ Ideal para distribuição gratuita
- 📖 Veja [DEMO_GUIDE.md](../DEMO_GUIDE.md) para mais detalhes

---

## O que é criado?

Um executável único que:
- ✅ Contém todo o jogo
- ✅ Inclui todas as dependências (pygame, moviepy, ffmpeg, etc)
- ✅ Funciona em qualquer PC Windows/Linux/MacOS
- ✅ Sempre roda em modo production
- ✅ ~295 MB de tamanho

## Exemplo de Build

```bash
C:\projetos\dudu-platform-game> python run_build\build.py
============================================================
[BUILD] Jump and Hit
   Versao: 0.0.3-alpha.1
   Plataforma: WINDOWS
   Executavel: JumpandHit-0.0.3-alpha.1-win64.exe
============================================================

[CLEAN] Limpando diretorios de build...
[CHECK] Verificando dependencias...
[BUILD] Compilando executavel...
[OK] SUCESSO! Executavel criado:
   C:\projetos\dudu-platform-game\dist\JumpandHit-0.0.3-alpha.1-win64.exe
   Tamanho: 294.66 MB

[OK] Para executar o jogo:
   .\dist\JumpandHit-0.0.3-alpha.1-win64.exe
```

## Arquivos Importantes

- `build.py` - Script principal de build
- `runtime_hook_logging.py` - Hook para logging em tempo de execução
- `bootstrap.py` - Bootstrap do jogo (raiz do projeto)

## Para Mais Informações

Veja `BUILD_GUIDE.md` na raiz do projeto.
