<#
Setup script for Windows (PowerShell).
Creates a virtual environment, activates it, upgrades pip and installs
project dependencies including CPU-only TensorFlow by default.
#>

python -m venv .venv
Write-Host "Ativando ambiente virtual..."
. .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
Write-Host "Instalando dependências básicas..."
pip install -r requirements.txt
Write-Host "Instalando TensorFlow CPU (recomendado para a maioria dos usuários)..."
pip install tensorflow-cpu
Write-Host "Setup concluído. Para usar o ambiente: . .venv\Scripts\Activate.ps1"
