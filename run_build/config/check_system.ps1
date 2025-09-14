# Script de Verificacao do Sistema para Build Movel
# Diagnostica o estado atual e fornece instrucoes especificas

Write-Host "=== Diagnostico do Sistema para Build Movel ===" -ForegroundColor Cyan
Write-Host ""

# Função para verificar se está executando como administrador
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Verificar privilégios
Write-Host "[1] Verificando privilégios..." -ForegroundColor Yellow
if (Test-Administrator) {
    Write-Host "    ✅ Executando como Administrador" -ForegroundColor Green
}
else {
    Write-Host "    [!] Nao esta executando como Administrador" -ForegroundColor Yellow
    Write-Host "    [INFO] Para instalar WSL2, execute como Administrador" -ForegroundColor Cyan
}

# Verificar WSL
Write-Host "\n[2] Verificando WSL2..." -ForegroundColor Yellow
try {
    $wslStatus = wsl --status 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✅ WSL2 está instalado" -ForegroundColor Green
        
        # Verificar distribuições
        Write-Host "\n[3] Verificando distribuições..." -ForegroundColor Yellow
        $distros = wsl --list --quiet 2>$null
        if ($LASTEXITCODE -eq 0 -and $distros) {
            Write-Host "    ✅ Distribuições encontradas:" -ForegroundColor Green
            $distros | ForEach-Object {
                if ($_ -and $_.Trim()) {
                    Write-Host "      - $_" -ForegroundColor White
                }
            }
        }
        else {
            Write-Host "    ❌ Nenhuma distribuição instalada" -ForegroundColor Red
        }
    }
    else {
        Write-Host "    ❌ WSL2 não está instalado" -ForegroundColor Red
    }
}
catch {
    Write-Host "    ❌ WSL2 não está disponível" -ForegroundColor Red
}

# Verificar Docker
Write-Host "\n[4] Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✅ Docker está instalado: $dockerVersion" -ForegroundColor Green
    }
    else {
        Write-Host "    ❌ Docker não está instalado" -ForegroundColor Red
    }
}
catch {
    Write-Host "    ❌ Docker não está disponível" -ForegroundColor Red
}

# Verificar Python
Write-Host "\n[5] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✅ Python está instalado: $pythonVersion" -ForegroundColor Green
    }
    else {
        Write-Host "    ❌ Python não está instalado" -ForegroundColor Red
    }
}
catch {
    Write-Host "    ❌ Python não está disponível" -ForegroundColor Red
}

# Verificar arquivos do projeto
Write-Host "`n[6] Verificando arquivos do projeto..." -ForegroundColor Yellow
$requiredFiles = @(
    "main.py",
    "requirements.txt",
    "requirements-mobile.txt",
    "setup_wsl2.ps1",
    "build_mobile.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "    ✅ $file" -ForegroundColor Green
    }
    else {
        Write-Host "    ❌ $file (não encontrado)" -ForegroundColor Red
    }
}

# Recomendações
Write-Host "`n=== Recomendacoes ===" -ForegroundColor Cyan

# Verificar se WSL2 precisa ser instalado
try {
    $wslTest = wsl --list --quiet 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[PROXIMOS PASSOS PARA WSL2]:" -ForegroundColor Yellow
        Write-Host "   1. Abra PowerShell como Administrador" -ForegroundColor White
        Write-Host "   2. Execute: .\setup_wsl2.ps1 -InstallWSL" -ForegroundColor Cyan
        Write-Host "   3. Reinicie o computador" -ForegroundColor White
        Write-Host "   4. Configure usuário/senha do Ubuntu" -ForegroundColor White
        Write-Host "   5. Execute: .\setup_wsl2.ps1 -SetupEnv" -ForegroundColor Cyan
        Write-Host "   6. Execute: .\setup_wsl2.ps1 -BuildProject" -ForegroundColor Cyan
    }
    else {
        Write-Host "`n[WSL2 PRONTO] Voce pode executar:" -ForegroundColor Green
        Write-Host "   .\setup_wsl2.ps1 -BuildProject" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "`n[INSTALE O WSL2 PRIMEIRO]:" -ForegroundColor Yellow
    Write-Host "   .\setup_wsl2.ps1 -InstallWSL" -ForegroundColor Cyan
}

# Verificar se Docker está disponível como alternativa
try {
    $dockerTest = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[ALTERNATIVA DOCKER DISPONIVEL]:" -ForegroundColor Blue
        Write-Host "   .\build_android_docker.ps1 debug" -ForegroundColor Cyan
    }
}
catch {
    # Docker não disponível
}

Write-Host "`n[DOCUMENTACAO] Para mais informacoes, consulte:" -ForegroundColor Magenta
Write-Host "   - README.md (visao geral dos metodos)" -ForegroundColor White

Write-Host "`n=== Diagnostico Concluido ===" -ForegroundColor Cyan