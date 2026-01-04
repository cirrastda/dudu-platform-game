# Guia de Build - Jump and Hit

## Visão Geral

O jogo pode ser compilado em um **executável único** que funciona independentemente em qualquer PC Windows, Linux ou MacOS, sem necessidade de dependências externas pré-configuradas.

## Pré-requisitos

- Python 3.8+
- Todas as dependências instaladas

Para instalar as dependências:

```bash
pip install -r requirements.txt
```

## Como Compilar para Desktop

### Windows (Executável .exe único)

Execute o script de build:

```bash
python run_build\build.py
```

O executável será gerado em:
```
dist\JumpandHit-0.0.3-alpha.1-win64.exe
```

Para rodar o jogo:

```bash
.\dist\JumpandHit-0.0.3-alpha.1-win64.exe
```

### Linux / MacOS (Executável único)

```bash
python run_build/build.py
```

O executável será gerado em:
```
dist/JumpandHit-0.0.3-alpha.1-linux64   (Linux)
dist/JumpandHit-0.0.3-alpha.1-macos     (MacOS)
```

## Opções do Script de Build

```bash
# Verificar dependências
python run_build/build.py --check

# Instalar dependências
python run_build/build.py --install

# Limpar builds anteriores
python run_build/build.py --clean

# Mostrar ajuda
python run_build/build.py --help
```

## Características do Executável

✅ **Executável Único**: Um arquivo .exe (ou similar) que contém tudo  
✅ **Sem Dependências Externas**: Funciona em qualquer PC  
✅ **Modo Production**: O executável sempre roda em modo production  
✅ **Com Recursos Inclusos**: Imagens, áudios e vídeos inclusos  
✅ **Logs de Debug**: Cria arquivo `runtime.log` para diagnosticar problemas  

## Comportamento do Jogo

O comportamento do jogo é idêntico ao original (desenvolvimento):

- Mesma dificuldade padrão (Normal)
- Mesmos níveis, inimigos e mecânicas
- Suporte a joystick
- Sistema de ranking

**Diferença**: No executável compilado, o modo development (.env) é ignorado e o jogo sempre roda em modo **production**.

## Tamanho do Executável

- **Windows**: ~295 MB (inclui ffmpeg, pygame, moviepy, numpy e todas as dependências)
- **Linux/MacOS**: Similar

Este tamanho é normal pois inclui:
- Interpretador Python
- Todas as bibliotecas necessárias (pygame, moviepy, ffmpeg, numpy, etc.)
- Todos os recursos do jogo (imagens, sons, vídeos)

## Distribução

Para distribuir o jogo:

1. Compile o executável com `python run_build/build.py`
2. Copie o arquivo .exe/linux64/macos para um pendrive ou repositório
3. Distribua para outros PCs
4. Execute o arquivo de forma direta (sem necessidade de instalação)

## Troubleshooting

### O executável não inicia

Verifique o arquivo `runtime.log` no mesmo diretório do executável para erros de inicialização.

### Erro: "PyInstaller not found"

Instale as dependências:
```bash
python run_build/build.py --install
```

### Erro de recursos não encontrados

Certifique-se de executar o build a partir da raiz do projeto:
```bash
cd c:\caminho\para\dudu-platform-game
python run_build\build.py
```

## Estrutura do Projeto

O script de build (`run_build/build.py`) automaticamente:

1. ✓ Verifica as dependências necessárias
2. ✓ Limpa builds anteriores
3. ✓ Coleta todos os módulos Python necessários
4. ✓ Inclui todos os recursos (imagens, sons, vídeos)
5. ✓ Compila para um executável único
6. ✓ Valida o resultado

## Informações Técnicas

- **Compilador**: PyInstaller 6.3.0+
- **Python**: 3.8 a 3.13
- **Modo**: Onefile (executável único)
- **Configuração**: bootstrap.py + runtime_hook_logging.py

O executável usa a função `resource_path()` no `internal/utils/functions.py` para localizar recursos de forma automática:

- Em desenvolvimento: usa diretório do projeto
- Em executável: usa `sys._MEIPASS` (PyInstaller onefile)

---

**Data**: 31 de Dezembro de 2025  
**Versão**: 0.0.3-alpha.1
