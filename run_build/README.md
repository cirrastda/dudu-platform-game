# Script de Build - Jump and Hit

## Uso Rápido

```bash
# Build completo do jogo em um executável único
python build.py

# Verificar dependências
python build.py --check

# Instalar dependências
python build.py --install

# Limpar builds anteriores
python build.py --clean

# Ajuda
python build.py --help
```

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
