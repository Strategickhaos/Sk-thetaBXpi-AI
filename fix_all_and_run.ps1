\ = 'C:\Users\Junior.JUNIOR-LAPTOP\OneDrive\Desktop\Sk-thetaBXpi-AI'
\ = Join-Path \ 'venv'
\ = Join-Path \ 'Scripts\Activate.ps1'
if (-not (Test-Path \)) { python -m venv \ }
& \
pip install -r (Join-Path \ 'requirements.txt')
python (Join-Path \ 'core.py')
