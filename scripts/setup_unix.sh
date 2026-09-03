#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Instalando TensorFlow CPU (recomendado)..."
pip install tensorflow-cpu
echo "Setup concluído. Ative o ambiente com: source .venv/bin/activate"
