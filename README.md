# Sk-thetaBXpi-AI

Autonomous AI Terminal Agent built by Stratigickhaos.
Executes command logic via neural pathways and trigonometric reasoning.

## Core Components

- `core.py` — main loop
- `fix_all_and_run.ps1` — installer/runner
- `deploy/deploy_repo.ps1` — GitHub auto-pusher

## Safety & Verification

This repository includes comprehensive safety verification tools for local AI models:

- **[MODEL_SAFETY.md](MODEL_SAFETY.md)** — 100 ways to verify your local AI model is safe and secure
- **[tools/](tools/)** — Automated verification scripts for model inspection, network isolation, and safety validation

### Quick Safety Check

```bash
cd tools
python run_all_checks.py
```

For detailed information, see [MODEL_SAFETY.md](MODEL_SAFETY.md)

## Usage

Run the main agent:
```bash
python core.py
```

## Installation

Use the provided PowerShell script:
```powershell
.\fix_all_and_run.ps1
```

## Requirements

See `requirements.txt` for Python dependencies:
```bash
pip install -r requirements.txt
```

## License

See [LICENSE](LICENSE) for details.
