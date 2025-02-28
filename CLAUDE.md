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

## Latest Model Improvements (2025-02-27)
The seizure detection model was enhanced with the following improvements:

1. **EEG Preprocessing**:
   - Applied bandpass filtering (1-40 Hz) to focus on relevant frequency bands
   - Added notch filtering for 50/60 Hz to remove line noise
   - Implemented common average referencing to improve signal quality
   - Added signal standardization (zero mean, unit variance)

2. **Data Handling**:
   - Increased window overlap to 75% for better temporal resolution
   - Added support for multi-subject training
   - Implemented data augmentation for seizure windows
   - Added class balancing through weighted sampling

3. **Model Architecture**:
   - Created a more efficient CNN with three convolutional layers
   - Reduced model parameters for faster training and inference
   - Added dropout for improved generalization
   - Implemented class-weighted loss to handle imbalanced data

4. **Training Process**:
   - Added early stopping based on F1 score
   - Added detailed evaluation metrics (precision, recall, F1, specificity)
   - Implemented model checkpointing based on F1 score
   - Added final training on full dataset for optimal performance

The latest model is saved as `improved_seizure_model_new.pth`.