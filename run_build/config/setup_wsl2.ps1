# Script de configuração WSL2 para build móvel
# Versão: 1.0
# Autor: Platform Game Build System

param(
    [switch]$InstallWSL,
    [switch]$SetupEnv,
    [switch]$BuildProject,
    [switch]$Help
)

# Função para exibir ajuda
function Show-Help {
    Write-Host "=== Setup WSL2 para Build Móvel ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\setup_wsl2.ps1 [opções]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opções:" -ForegroundColor Green
    Write-Host "  -InstallWSL     Instala e configura o WSL2 com Ubuntu"
    Write-Host "  -SetupEnv       Configura o ambiente de desenvolvimento no WSL2"
    Write-Host "  -BuildProject   Executa o build do projeto no WSL2"
    Write-Host "  -Help           Exibe esta ajuda"
    Write-Host ""
    Write-Host "Exemplos:" -ForegroundColor Magenta
    Write-Host "  .\setup_wsl2.ps1 -InstallWSL"
    Write-Host "  .\setup_wsl2.ps1 -SetupEnv"
    Write-Host "  .\setup_wsl2.ps1 -BuildProject"
    Write-Host ""
}

# Função para verificar se está executando como administrador
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Função para instalar WSL2
function Install-WSL2 {
    Write-Host "[INFO] Iniciando instalação do WSL2..." -ForegroundColor Green
    
    if (-not (Test-Administrator)) {
        Write-Host "[ERRO] Este script precisa ser executado como Administrador para instalar o WSL2" -ForegroundColor Red
        Write-Host "[INFO] Clique com o botão direito no PowerShell e selecione 'Executar como administrador'" -ForegroundColor Yellow
        return $false
    }
    
    try {
        # Verificar se WSL já está instalado
        $wslStatus = wsl --status 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[INFO] WSL2 já está instalado" -ForegroundColor Yellow
            
            # Verificar se Ubuntu está instalado
            $distros = wsl --list --quiet
            if ($distros -match "Ubuntu") {
                Write-Host "[INFO] Ubuntu já está instalado no WSL2" -ForegroundColor Green
                return $true
            }
        }
        
        Write-Host "[INFO] Habilitando recursos do Windows..." -ForegroundColor Cyan
        
        # Habilitar WSL
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
        
        # Habilitar Virtual Machine Platform
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
        
        Write-Host "[INFO] Instalando Ubuntu 22.04..." -ForegroundColor Cyan
        wsl --install -d Ubuntu-22.04
        
        Write-Host "[SUCESSO] WSL2 instalado com sucesso!" -ForegroundColor Green
        Write-Host "[INFO] Reinicie o computador e execute novamente com -SetupEnv" -ForegroundColor Yellow
        
        return $true
    }
    catch {
        Write-Host "[ERRO] Falha ao instalar WSL2: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Função para configurar ambiente no WSL2
function Setup-Environment {
    Write-Host "[INFO] Configurando ambiente de desenvolvimento no WSL2..." -ForegroundColor Green
    
    # Verificar se WSL2 está disponível
    try {
        $wslTest = wsl --list --quiet 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERRO] WSL2 não está instalado. Execute com -InstallWSL primeiro" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "[ERRO] WSL2 não está disponível" -ForegroundColor Red
        return $false
    }
    
    Write-Host "[INFO] Atualizando sistema Ubuntu..." -ForegroundColor Cyan
    wsl -- sudo apt update
    wsl -- sudo apt upgrade -y
    
    Write-Host "[INFO] Instalando dependências Python..." -ForegroundColor Cyan
    wsl -- sudo apt install -y python3 python3-pip python3-venv
    
    Write-Host "[INFO] Instalando dependências Android..." -ForegroundColor Cyan
    wsl -- sudo apt install -y openjdk-17-jdk unzip wget curl
    
    Write-Host "[INFO] Instalando Buildozer..." -ForegroundColor Cyan
    wsl -- pip3 install --user buildozer cython
    
    Write-Host "[INFO] Configurando Android SDK..." -ForegroundColor Cyan
    $androidSetup = @"
export ANDROID_HOME=`$HOME/android-sdk
export PATH=`$PATH:`$ANDROID_HOME/cmdline-tools/latest/bin:`$ANDROID_HOME/platform-tools
"@
    
    $androidSetup | wsl -- tee -a ~/.bashrc
    
    Write-Host "[SUCESSO] Ambiente configurado com sucesso!" -ForegroundColor Green
    return $true
}

# Função para fazer build do projeto
function Build-Project {
    Write-Host "[INFO] Iniciando build do projeto no WSL2..." -ForegroundColor Green
    
    # Verificar se WSL2 está disponível
    try {
        $wslTest = wsl --list --quiet 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERRO] WSL2 não está instalado ou configurado" -ForegroundColor Red
            Write-Host "[SOLUÇÃO] Execute os seguintes passos:" -ForegroundColor Yellow
            Write-Host "  1. Abra PowerShell como Administrador" -ForegroundColor Cyan
            Write-Host "  2. Execute: .\setup_wsl2.ps1 -InstallWSL" -ForegroundColor Cyan
            Write-Host "  3. Reinicie o computador" -ForegroundColor Cyan
            Write-Host "  4. Configure usuário/senha do Ubuntu" -ForegroundColor Cyan
            Write-Host "  5. Execute: .\setup_wsl2.ps1 -SetupEnv" -ForegroundColor Cyan
            return $false
        }
    }
    catch {
        Write-Host "[ERRO] WSL2 não está disponível" -ForegroundColor Red
        -ForegroundColor Yellow
        return $false
    }
    
    # Obter caminho atual do Windows e converter para WSL
    $currentPath = Get-Location
    $wslPath = $currentPath.Path -replace '^([A-Z]):', '/mnt/$1' -replace '\\', '/'
    $wslPath = $wslPath.ToLower()
    
    Write-Host "[INFO] Caminho do projeto: $wslPath" -ForegroundColor Cyan
    
    # Navegar para o diretório do projeto no WSL
    Write-Host "[INFO] Configurando ambiente virtual Python..." -ForegroundColor Cyan
    
    # Criar ambiente virtual se não existir
    wsl -- bash -c "cd '$wslPath' && if [ ! -d 'venv' ]; then python3 -m venv venv; fi"
    
    # Ativar ambiente virtual e instalar dependências
    wsl -- bash -c "cd '$wslPath' && source venv/bin/activate && python -m pip install --upgrade pip"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao atualizar pip" -ForegroundColor Red
        return $false
    }
    
    # Instalar setuptools (necessário para Python 3.12+)
    wsl -- bash -c "cd '$wslPath' && source venv/bin/activate && python -m pip install setuptools"
    
    # Instalar buildozer e cython
    wsl -- bash -c "cd '$wslPath' && source venv/bin/activate && python -m pip install buildozer cython"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao instalar buildozer/cython" -ForegroundColor Red
        return $false
    }
    
    # Instalar dependências do projeto
    wsl -- bash -c "cd '$wslPath' && source venv/bin/activate && python -m pip install -r requirements-mobile.txt"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[AVISO] Falha ao instalar requirements-mobile.txt, tentando requirements.txt" -ForegroundColor Yellow
        wsl -- bash -c "cd '$wslPath' && source venv/bin/activate && python -m pip install -r requirements.txt"
    }
    
    # Verificar se Java está instalado
    $javaCheck = wsl -- bash -c "which javac"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[INFO] Instalando OpenJDK..." -ForegroundColor Cyan
        wsl -- bash -c "sudo apt update && sudo apt install -y openjdk-17-jdk"
    }
    
    Write-Host "[INFO] Executando build Android..." -ForegroundColor Cyan
    
    # Verificar se buildozer.spec existe, se não, inicializar
    wsl -- bash -c "cd '$wslPath' && if [ ! -f 'run_build/config/buildozer.spec' ]; then source venv/bin/activate && buildozer init && mv buildozer.spec run_build/config/; fi"
    
    # Executar build com tratamento de erro
    wsl -- bash -c "cd '$wslPath' && source venv/bin/activate && buildozer android debug"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[SUCESSO] Build concluído com sucesso!" -ForegroundColor Green
        
        # Listar APKs gerados
        Write-Host "[INFO] Procurando APKs gerados..." -ForegroundColor Cyan
        wsl -- bash -c "cd '$wslPath' && find . -name '*.apk' -type f 2>/dev/null || echo 'Nenhum APK encontrado'"
        
        # Verificar se há APKs no diretório bin
        $apkCheck = wsl -- bash -c "cd '$wslPath' && ls bin/*.apk 2>/dev/null"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[INFO] APKs encontrados no diretório bin/" -ForegroundColor Green
            Write-Host "[INFO] Copiando APKs para o Windows..." -ForegroundColor Cyan
            
            # Criar diretório de saída se não existir
            if (-not (Test-Path "dist")) {
                New-Item -ItemType Directory -Path "dist" -Force | Out-Null
            }
            
            # Copiar APKs (WSL para Windows)
            wsl -- bash -c "cd '$wslPath' && cp bin/*.apk dist/ 2>/dev/null || echo 'Falha ao copiar APKs'"
            
            Write-Host "[SUCESSO] APKs copiados para o diretório dist/" -ForegroundColor Green
        }
        
        return $true
    }
    else {
        Write-Host "[ERRO] Falha no build do projeto" -ForegroundColor Red
        Write-Host "[INFO] Possíveis causas:" -ForegroundColor Yellow
        Write-Host "  - Dependências Android não instaladas" -ForegroundColor Cyan
        Write-Host "  - Configuração run_build/config/buildozer.spec incorreta" -ForegroundColor Cyan
        Write-Host "  - Problemas de permissão" -ForegroundColor Cyan
        Write-Host "[SOLUÇÃO] Execute: .\setup_wsl2.ps1 -SetupEnv" -ForegroundColor Yellow
        return $false
    }
}

# Função principal
function Main {
    Write-Host "=== Setup WSL2 para Build Móvel ===" -ForegroundColor Cyan
    Write-Host ""
    
    if ($Help) {
        Show-Help
        return
    }
    
    if ($InstallWSL) {
        $result = Install-WSL2
        if ($result) {
            Write-Host "[INFO] Próximo passo: Execute '.\setup_wsl2.ps1 -SetupEnv' após reiniciar" -ForegroundColor Yellow
        }
        return
    }
    
    if ($SetupEnv) {
        $result = Setup-Environment
        if ($result) {
            Write-Host "[INFO] Próximo passo: Execute '.\setup_wsl2.ps1 -BuildProject' para fazer o build" -ForegroundColor Yellow
        }
        return
    }
    
    if ($BuildProject) {
        $result = Build-Project
        return
    }
    
    # Se nenhuma opção foi especificada, mostrar menu interativo
    Write-Host "Escolha uma opção:" -ForegroundColor Yellow
    Write-Host "1. Instalar WSL2"
    Write-Host "2. Configurar ambiente"
    Write-Host "3. Build do projeto"
    Write-Host "4. Ajuda"
    Write-Host "5. Sair"
    Write-Host ""
    
    do {
        $choice = Read-Host "Digite sua escolha (1-5)"
        
        switch ($choice) {
            "1" { 
                $result = Install-WSL2
                if ($result) {
                    Write-Host "[INFO] Próximo passo: Execute '.\setup_wsl2.ps1 -SetupEnv' após reiniciar" -ForegroundColor Yellow
                }
                break 
            }
            "2" { 
                $result = Setup-Environment
                if ($result) {
                    Write-Host "[INFO] Próximo passo: Execute '.\setup_wsl2.ps1 -BuildProject' para fazer o build" -ForegroundColor Yellow
                }
                break 
            }
            "3" { 
                $result = Build-Project
                break 
            }
            "4" { 
                Show-Help
                break 
            }
            "5" { 
                Write-Host "Saindo..." -ForegroundColor Gray
                return 
            }
            default { 
                Write-Host "Opção inválida. Digite um número de 1 a 5." -ForegroundColor Red 
            }
        }
    } while ($choice -notin @("1", "2", "3", "4", "5"))
}

# Executar função principal
Main