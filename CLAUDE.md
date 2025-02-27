# CLAUDE.md - EEG Seizure Detection Project Guide

## Commands
- **Run main script**: `python eeg-seizure-detection.py`
- **Run Jupyter notebook**: `jupyter notebook eegSeizureDetection.ipynb`
- **Install dependencies**: `pip install -r requirements.txt`
- **Create environment**: `conda create -n eeg python=3.9 && conda activate eeg`

## Code Style Guidelines
- **Naming**: snake_case for functions/variables, CamelCase for classes
- **Imports**: Group as (1) standard lib, (2) third-party, (3) local modules
- **Type hints**: Use throughout for function parameters and return values
- **Docstrings**: Use Google style docstrings with Args/Returns sections
- **Error handling**: Use try/except with specific exceptions and detailed logging
- **Formatting**: Follow PEP 8 conventions
- **Logging**: Use Python's logging module with appropriate levels
- **Libraries**: Prefer NumPy/Pandas for data processing, PyTorch for models, MNE for EEG-specific operations

## Project Structure
- Core functionality in `eeg-seizure-detection.py`
- Notebooks for exploration and visualization
- BIDS-formatted dataset organized by subjects/sessions