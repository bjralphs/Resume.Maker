$ErrorActionPreference = "Stop"

$gtk="D:\Applications\GTK3\GTK3-Runtime Win64\bin"
$msys="D:\Applications\msys2\ucrt64\bin"

.\.venv\Scripts\Activate.ps1

$env:WEASYPRINT_DLL_DIRECTORIES=$gtk
$paths = $env:PATH -split ';' | Where-Object { $_ -and ($_ -ne $msys) }
$env:PATH = ($gtk + ';' + ($paths -join ';'))

python main.py
