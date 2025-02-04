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

In this machine learning challenge, I leveraged the standardization proposed by SzCORE. Participants are invited to build models on any combination of standardized publicly available datasets or private datasets. The model should perform a segmentation task by identifying the onset and duration of all epileptic seizures given a long-term, continuous EEG as input. Models will then be evaluated on a large hold-out dataset using the event-based F1 score as the evaluation metric.

---

### Objective

This challenge aimed to build a seizure detection model that accurately detected the onset and duration of all epileptic seizures in a recording from long-term EEG data collected in an epilepsy monitoring unit.

---

### Installation

pip install -r requirements.txt

---

### Usage

*Explain how to run or use the project.*

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