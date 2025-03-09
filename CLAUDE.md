# CLAUDE.md - EEG Seizure Detection Project Guide

## Commands
- **Run main script**: `python3 eeg-seizure-detection.py`
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

## Latest Model Improvements (2025-03-09)
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
   - Reduced window size to 128 samples for memory efficiency

3. **Model Architecture**:
   - Created a CNN with three convolutional layers
   - Implemented dynamic model initialization that adapts to input dimensions
   - Added dropout for improved generalization
   - Used class-weighted loss to handle imbalanced data

4. **Training Process**:
   - Added early stopping based on F1 score
   - Added event-based metrics for realistic evaluation
   - Implemented model checkpointing based on event F1 score
   - Added Docker support for model deployment

The latest model is saved as `seizure_model_event_metrics.pth`.

## Docker Deployment
To deploy the seizure detection model:
1. Copy your trained model to the Docker directory as 'model.pth'
2. Build the Docker image: `docker build -t seizure-detection .`
3. Test the Docker image on a sample EEG file:
   ```
   docker run --rm -v /path/to/eeg:/data -v /path/to/output:/output -e INPUT=sample.edf -e OUTPUT=prediction.tsv seizure-detection
   ```
4. Submit the Docker image to the competition