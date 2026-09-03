<#
Activate venv and run the Tkinter GUI (Windows PowerShell)
#>

if (Test-Path .venv) {
    . .venv\Scripts\Activate.ps1
}

python interface.py
