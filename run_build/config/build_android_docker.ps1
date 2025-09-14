#!/usr/bin/env pwsh
# Build Android via Docker - Script PowerShell
# Facilita o uso do Docker para build Android no Windows

# Configurações
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Função para verificar se Docker está instalado
function Test-Docker {
    try {
        docker --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Função para verificar se Docker Compose está instalado
function Test-DockerCompose {
    try {
        docker-compose --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Função para executar Docker Compose
function Invoke-DockerCompose {
    param(
        [string[]]$Arguments
    )
    
    Write-Host "Executando: docker-compose $($Arguments -join ' ')" -ForegroundColor Gray
    & docker-compose @Arguments
}

# Função para verificar dependências
function Test-Dependencies {
    Write-Host "=== VERIFICANDO DEPENDENCIAS ===" -ForegroundColor Cyan
    
    $dockerOk = Test-Docker
    $composeOk = Test-DockerCompose
    
    if ($dockerOk) {
        Write-Host "[OK] Docker encontrado" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Docker nao encontrado" -ForegroundColor Red
        Write-Host "Instale o Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    }
    
    if ($composeOk) {
        Write-Host "[OK] Docker Compose encontrado" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Docker Compose nao encontrado" -ForegroundColor Red
        Write-Host "Docker Compose geralmente vem com Docker Desktop" -ForegroundColor Yellow
    }
    
    if (-not ($dockerOk -and $composeOk)) {
        Write-Host "\nPor favor, instale as dependencias necessarias antes de continuar." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "\nTodas as dependencias estao OK!" -ForegroundColor Green
}

# Função para build debug
function Build-AndroidDebug {
    Write-Host "=== BUILD ANDROID DEBUG ===" -ForegroundColor Cyan
    Write-Host "Iniciando build debug via Docker..." -ForegroundColor Yellow
    
    try {
        Invoke-DockerCompose -Arguments @("-f", "docker-compose.android.yml", "up", "--build", "android-builder")
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Build debug concluido com sucesso!" -ForegroundColor Green
            Write-Host "APK gerado em: .\bin\" -ForegroundColor Green
            
            # Listar APKs gerados
            if (Test-Path ".\bin\*.apk") {
                Write-Host "\nAPKs encontrados:" -ForegroundColor Green
                Get-ChildItem ".\bin\*.apk" | ForEach-Object {
                    $size = [math]::Round($_.Length / 1MB, 2)
                    Write-Host "  $($_.Name) ($size MB)" -ForegroundColor White
                }
            }
        }
        else {
            Write-Host "[ERRO] Erro no build debug" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "[ERRO] Erro ao executar Docker: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Função para build release
function Build-AndroidRelease {
    Write-Host "=== BUILD ANDROID RELEASE ===" -ForegroundColor Cyan
    Write-Host "Iniciando build release via Docker..." -ForegroundColor Yellow
    
    try {
        Invoke-DockerCompose -Arguments @("-f", "docker-compose.android.yml", "up", "--build", "android-builder-release")
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Build release concluido com sucesso!" -ForegroundColor Green
            Write-Host "APK gerado em: .\bin\" -ForegroundColor Green
            Write-Host "\nNota: Para publicar na Play Store, voce precisa assinar o APK." -ForegroundColor Yellow
            
            # Listar APKs gerados
            if (Test-Path ".\bin\*.apk") {
                Write-Host "\nAPKs encontrados:" -ForegroundColor Green
                Get-ChildItem ".\bin\*.apk" | ForEach-Object {
                    $size = [math]::Round($_.Length / 1MB, 2)
                    Write-Host "  $($_.Name) ($size MB)" -ForegroundColor White
                }
            }
        }
        else {
            Write-Host "[ERRO] Erro no build release" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "[ERRO] Erro ao executar Docker: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Função para abrir shell interativo
function Open-AndroidShell {
    Write-Host "=== SHELL ANDROID INTERATIVO ===" -ForegroundColor Cyan
    Write-Host "Abrindo shell interativo no container..." -ForegroundColor Yellow
    Write-Host "Use 'exit' para sair do container." -ForegroundColor Gray
    
    try {
        Invoke-DockerCompose -Arguments @("-f", "docker-compose.android.yml", "run", "--rm", "android-shell")
    }
    catch {
        Write-Host "[ERRO] Erro ao abrir shell: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Função para limpeza
function Clear-AndroidBuild {
    Write-Host "=== LIMPEZA DE BUILD ===" -ForegroundColor Cyan
    Write-Host "Removendo containers e volumes..." -ForegroundColor Yellow
    
    try {
        # Parar e remover containers
        Invoke-DockerCompose -Arguments @("-f", "docker-compose.android.yml", "down", "-v")
        
        # Remover imagens relacionadas
        $images = docker images --filter "reference=platform-game*" -q
        if ($images) {
            Write-Host "Removendo imagens Docker..." -ForegroundColor Yellow
            docker rmi $images -f
        }
        
        # Limpar cache do buildozer se existir
        if (Test-Path ".buildozer") {
            Write-Host "Removendo cache do buildozer..." -ForegroundColor Yellow
            Remove-Item ".buildozer" -Recurse -Force
        }
        
        Write-Host "[OK] Limpeza concluida!" -ForegroundColor Green
    }
    catch {
        Write-Host "[ERRO] Erro na limpeza: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Função para mostrar ajuda
function Show-Help {
    Write-Host "=== BUILD ANDROID VIA DOCKER ===" -ForegroundColor Cyan
    Write-Host "Script para facilitar builds Android no Windows usando Docker\n" -ForegroundColor White
    
    Write-Host "USO:" -ForegroundColor Yellow
    Write-Host "  .\build_android_docker.ps1 [comando]\n" -ForegroundColor White
    
    Write-Host "COMANDOS:" -ForegroundColor Yellow
    Write-Host "  debug     - Build APK debug" -ForegroundColor White
    Write-Host "  release   - Build APK release (para producao)" -ForegroundColor White
    Write-Host "  shell     - Abrir shell interativo no container" -ForegroundColor White
    Write-Host "  clean     - Limpar containers, volumes e cache" -ForegroundColor White
    Write-Host "  check     - Verificar dependencias (Docker)" -ForegroundColor White
    Write-Host "  help      - Mostrar esta ajuda\n" -ForegroundColor White
    
    Write-Host "EXEMPLOS:" -ForegroundColor Yellow
    Write-Host "  .\build_android_docker.ps1 debug" -ForegroundColor Gray
    Write-Host "  .\build_android_docker.ps1 release" -ForegroundColor Gray
    Write-Host "  .\build_android_docker.ps1 shell" -ForegroundColor Gray
}

# Função principal
function Main {
    param(
        [string]$Command = "help"
    )
    
    switch ($Command.ToLower()) {
        "debug" {
            Test-Dependencies
            Build-AndroidDebug
        }
        "release" {
            Test-Dependencies
            Build-AndroidRelease
        }
        "shell" {
            Test-Dependencies
            Open-AndroidShell
        }
        "clean" {
            Clear-AndroidBuild
        }
        "check" {
            Test-Dependencies
        }
        "help" {
            Show-Help
        }
        default {
            Write-Host "Comando desconhecido: $Command" -ForegroundColor Red
            Show-Help
            exit 1
        }
    }
}

# Executar função principal com argumentos
if ($args.Count -gt 0) {
    Main -Command $args[0]
} else {
    Main
}