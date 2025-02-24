# SzCORE - Epilepsy Benchmarks

## Seizure Detection Challenge (2025)

In partnership with The International Conference on Artificial Intelligence in Epilepsy and Other Neurological Disorders (2025), EPFL, ETH, and partners.

---

### Table of Contents

- [Background and Impact](#background-and-impact)
- [Objective](#objective)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Citations](#Citations)

---
### Background and Impact

Epilepsy is the most common chronic brain disease and affects people of all ages. More than 50 million people worldwide have epilepsy. Scalp EEG-based seizure detection algorithms can optimize and facilitate the diagnostic workup performed on people with epilepsy to improve patients’ care and quality of life [1].

EEG-based seizure detection aims to detect the onset and duration of all seizures in an EEG recording. The task has benefited from advances in machine learning. However, a relative scarcity of public datasets and a lack of standardization hinder progress in the field. This likely explains the lack of adoption of state-of-the-art algorithms in clinical practices. Recently, SzCORE has proposed a method to standardize dataset formats, evaluation methodology, and performance metrics.

---

### Objective

This challenge aimed to build a seizure detection model that accurately detected the onset and duration of all epileptic seizures in a recording from long-term EEG data collected in an epilepsy monitoring unit.

---

### Installation

#### Prerequisites
- Python 3.9 or higher
- BIDS-formatted EEG dataset

#### Create a virtual environment
```
conda create -n eeg python=3.9
conda activate eeg
```
#### Install dependencies
```
pip install -r requirements.txt
```
---

### Usage

#### EEG Seizure Detection Pipeline
A deep learning-based pipeline for detecting seizures in EEG data using BIDS-formatted datasets.

#### Data Preparation

Ensure your EEG data is organized in BIDS format. The structure should look like:
```
BIDS_Siena/
└── BIDS_Siena/
    ├── sub-00/
    │   └── ses-01/
    │       └── eeg/
    │           ├── sub-00_ses-01_task-szMonitoring_run-00_eeg.edf
    │           ├── sub-00_ses-01_task-szMonitoring_run-00_events.tsv
    │           └── ...
    ├── sub-01/
    └── ...
```

### Running the Pipeline

#### Option 1: Jupyter Notebook (Recommended for Exploration)

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `seizure_detection.ipynb` and run the cells sequentially to:
   - Load and preprocess EEG data
   - Train the seizure detection model
   - Visualize results
   - Evaluate model performance

#### Option 2: Python Script

1. Update the path to your BIDS dataset in the script:
```python
# In seizure_detection.py
initial_path = Path(r"path/to/your/BIDS_dataset")
```

2. Run the script:
```bash
python seizure_detection.py
```

3. The script will:
   - Load and process the EEG data
   - Train a CNN model on the data
   - Output metrics and visualizations
   - Save the best model to `best_model.pth`

### Customizing the Pipeline

- **Adjust hyperparameters** in `main()`:
```python
# Change learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)

# Adjust batch size
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Change training epochs
n_epochs = 20
```

- **Modify model architecture** in `SeizureDetectionModel` class
- **Change data preprocessing** in `load_single_recording` function

### Using the Trained Model for Inference

```python
# Load the best model
checkpoint = torch.load('best_model.pth')
model = SeizureDetectionModel(n_channels=19)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Process new EEG data
# ... [code to load and preprocess new EEG data] ...

# Make predictions
with torch.no_grad():
    predictions = model(new_data)
    predictions = (torch.sigmoid(predictions.squeeze()) > 0.5).float()
```

---

### Contributing

*Outline guidelines for contributing to the project.*

---

### License

This project is licensed under the [Open Data Commons Attribution License v1.0](LICENSE).

---

### Citations

- **Beniczky, S., et al. (2013).** *Standardized computer‐based organized reporting of EEG: SCORE.* Epilepsia, 54(6), 1112-1124.  
- **Beniczky, S., et al. (2017).** *Standardized computer-based organized reporting of EEG: SCORE–second version.* Clinical Neurophysiology, 128(11), 2334-2346.  
- **Dan, J., & Detti, P. (2024).** *BIDS Siena Scalp EEG Database (v1.0.0)* [Data set]. EPFL. [https://doi.org/10.5281/zenodo.10640762](https://doi.org/10.5281/zenodo.10640762).  
- **Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000).** *PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals.* Circulation [Online], 101(23), e215–e220.  
- **Guttag, J. (2010).** *CHB-MIT Scalp EEG Database (version 1.0.0).* PhysioNet. [https://doi.org/10.13026/C2K01R](https://doi.org/10.13026/C2K01R).  
- **Shoeb, A. (2009).** *Application of Machine Learning to Epileptic Seizure Onset Detection and Treatment.* PhD Thesis, Massachusetts Institute of Technology.  
- **Tal Pal Attia, et al. (in prep).** *Hierarchical Event Descriptor library schema for clinical EEG data annotation.* [https://arxiv.org/abs/2310.15173](https://arxiv.org/abs/2310.15173).  


In partnership with The International Conference on Artificial Intelligence in Epilepsy and Other Neurological Disorders (2025), EPFL, ETH, and partners.