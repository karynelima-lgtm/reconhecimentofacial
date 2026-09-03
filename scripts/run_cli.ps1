param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $RemainingArgs
)

if (Test-Path .venv) {
    . .venv\Scripts\Activate.ps1
}

# Forward any CLI args to main.py
python main.py @RemainingArgs
