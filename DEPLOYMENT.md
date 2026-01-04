# Instruções de Deployment - Jump and Hit

## Para Distribuir o Jogo

### Passo 1: Criar o Executável

Na máquina de desenvolvimento:

```bash
cd c:\projetos\dudu-platform-game
python run_build\build.py
```

Isso gera: `dist\JumpandHit-0.0.3-alpha.1-win64.exe` (~295 MB)

### Passo 2: Distribuir

Opções:

#### A) Copiar direto
```bash
# Copiar o .exe para:
- USB
- Rede compartilhada
- Email (talvez seja muito pesado)
- Google Drive / OneDrive
```

#### B) Compactar (opcional)
```bash
# Comprimir o .exe para reduzir tamanho (~40-50% da original)
7z a JumpandHit.7z dist\JumpandHit-0.0.3-alpha.1-win64.exe
# ou
Compress-Archive -Path dist\JumpandHit-0.0.3-alpha.1-win64.exe -DestinationPath JumpandHit.zip
```

### Passo 3: Usuário Final - Executar

Simplesmente:

```bash
# Windows
JumpandHit-0.0.3-alpha.1-win64.exe

# Duplo clique no arquivo
```

Pronto! Sem instalação, sem Python, sem dependências.

---

## Troubleshooting

### Problema: "runtime.log mostra erros"

1. Abra o arquivo `runtime.log` ao lado do .exe
2. Procure por `[EXCEPTION]` ou `[BOOT]` para erros
3. Se tiver problema com vídeo/áudio:
   ```bash
   # Testar em modo headless
   set SDL_VIDEODRIVER=dummy
   JumpandHit-0.0.3-alpha.1-win64.exe
   ```

### Problema: "Game runs but graphics are weird"

Pode ser problema com driver de vídeo. Tente:
```bash
# Usar renderizador diferente
set SDL_VIDEODRIVER=windib
JumpandHit-0.0.3-alpha.1-win64.exe
```

### Problema: "No audio"

```bash
# Testar áudio
set SDL_AUDIODRIVER=directsound
JumpandHit-0.0.3-alpha.1-win64.exe
```

---

## Requisitos Mínimos do Sistema

- **Windows**: XP SP3 ou superior (tecnicamente, mas recomenda-se Windows 7+)
- **Processador**: Qualquer coisa que rode Python 3.x
- **Memória**: 512 MB RAM (mínimo), 1 GB (recomendado)
- **Disco**: 350 MB espaço livre (para o executável + recursos)
- **Tela**: Resolução mínima 800x600

---

## Distribuição para Múltiplas Plataformas

### Windows (Feito ✅)
```bash
python run_build\build.py
# Gera: JumpandHit-0.0.3-alpha.1-win64.exe
```

### Linux (Compilar em Linux)
```bash
python run_build/build.py
# Gera: JumpandHit-0.0.3-alpha.1-linux64
```

### MacOS (Compilar em MacOS)
```bash
python run_build/build.py
# Gera: JumpandHit-0.0.3-alpha.1-macos
```

---

## Changelog do Build

### v0.0.3-alpha.1
- ✅ Executável único compilado
- ✅ Todas as dependências incluídas
- ✅ Modo production ativado por padrão
- ✅ 294.7 MB (Windows)
- ✅ Testado e funcionando

---

## Suporte

Se alguém tiver problemas:

1. Peça para enviar o arquivo `runtime.log` (criado ao lado do .exe)
2. Ele terá informações de debug
3. Exemplo de log:
```
[BOOT] App iniciado
[BOOT] Python: C:\...\pythonXX.dll
[BOOT] Frozen: True
[BOOT] Criando Game...
[BOOT] Iniciando loop do jogo...
```

---

**Versão**: 0.0.3-alpha.1  
**Data**: 31 de Dezembro de 2025  
**Status**: Pronto para Distribuição ✅
