# Windows Setup Guide

This guide sets up the photonics project on native Windows using **uv** (no WSL needed).
Only **legume** notebooks are supported on Windows. MEEP notebooks require Linux.

---

## 1. Install uv

Open PowerShell and run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Close and reopen your terminal so `uv` is on your PATH.

## 2. Get the project files

**Option A — Clone from GitHub:**
```
git clone https://github.com/Luxchen77/legume-l3-cavity-sim.git
cd legume-l3-cavity-sim
```

**Option B — Copy from WSL:**
1. Open Windows Explorer
2. Navigate to `\\wsl$\Ubuntu\home\jonah\photonics`
3. Copy the entire folder to e.g. `C:\Users\jonah\photonics`

## 3. Install Python & dependencies

Open a terminal in the project folder:

```
cd C:\Users\jonah\photonics
uv sync
```

That's it. `uv sync` reads `pyproject.toml` and automatically:
- Downloads Python 3.12 if you don't have it
- Creates a `.venv` virtual environment
- Installs all dependencies

## 4. Run notebooks

### In VS Code (recommended):
1. Open the project folder in VS Code
2. Install the "Python" and "Jupyter" extensions if not already installed
3. Select the `.venv` interpreter: press `Ctrl+Shift+P` → type "Python: Select Interpreter" → choose `.venv`
4. Open any legume notebook (e.g. `legume_L3_oxidized.ipynb`) and run it

### In browser (alternative):
```
uv run jupyter notebook
```

## 5. Verify it works

```
uv run python -c "import legume; print('legume OK')"
uv run python -c "import numpy; print('numpy OK')"
uv run python -c "import matplotlib; print('matplotlib OK')"
```

## Notebooks that work on Windows

All legume notebooks:
- `legume_L3_conical.ipynb`
- `legume_L3_optimization.ipynb.ipynb`
- `legume_L3_oxidized.ipynb`
- `legume_PhC_Wg.ipynb`
- `legume_examplePhC.ipynb`
- `legume_examplePhC_edittoL3.ipynb`
- `Legume_test_phc_cavity.ipynb`
- `Legumes_test_L3_cavity.ipynb`
- `L3_cavity_fixed.ipynb`

## Notebooks that require Linux (won't work on Windows)

These import `meep`, which has no Windows build:
- `L3_Cavity_MEEP_Full.ipynb`
- `L3_Cavity_MEEP_QuickStart.ipynb`
- `Meep_L3_cavity.ipynb`
- `meep_test_L3.ipynb`
