#!/usr/bin/env python
"""
Script to convert Siena Scalp EEG dataset to BIDS format using MNE-BIDS directly
since epilepsy2bids is having compatibility issues

Requirements:
- mne
- mne-bids
- pandas
- numpy
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import logging
import datetime
import json
import mne
from mne_bids import (write_raw_bids, BIDSPath, update_sidecar_json, 
                     write_anat, make_dataset_description)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def convert_siena_to_bids():
    # Define paths
    siena_root = Path("C:/Users/user/Documents/eeg_data_challenge/physionet.org/files/siena-scalp-eeg/1.0.0")
    bids_output = Path("C:/Users/user/Documents/eeg_data_challenge/BIDS_Siena_Converted")
    
    # Check if siena_root exists
    if not siena_root.exists():
        logger.error(f"Source directory not found: {siena_root}")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(bids_output, exist_ok=True)
    
    # Load subject info
    subject_info_path = siena_root / "subject_info.csv"
    if subject_info_path.exists():
        subject_info = pd.read_csv(subject_info_path)
        logger.info(f"Loaded subject info for {len(subject_info)} subjects")
    else:
        logger.warning("Subject info file not found, proceeding without demographic data")
        subject_info = None
    
    # Get list of subject directories (PN*)
    subject_dirs = [d for d in siena_root.glob("PN*") if d.is_dir()]
    logger.info(f"Found {len(subject_dirs)} subject directories")
    
    # Process each subject
    for subject_dir in subject_dirs:
        subject_id = subject_dir.name  # PN00, PN01, etc.
        logger.info(f"Processing subject: {subject_id}")
        
        # Map subject IDs: PN00 -> sub-00
        bids_subject_id = subject_id.replace("PN", "")
        
        # Get seizure annotations
        seizure_list_file = subject_dir / f"Seizures-list-{subject_id}.txt"
        if not seizure_list_file.exists():
            logger.warning(f"Seizure list file not found for {subject_id}")
            seizure_annotations = None
        else:
            try:
                seizure_annotations = parse_seizure_list(seizure_list_file)
                logger.info(f"Found {len(seizure_annotations)} seizure annotations")
            except Exception as e:
                logger.error(f"Error parsing seizure annotations: {str(e)}")
                seizure_annotations = None
        
        # Find all EDF files for this subject
        edf_files = list(subject_dir.glob("*.edf"))
        logger.info(f"Found {len(edf_files)} EDF files for {subject_id}")
        
        for i, edf_file in enumerate(edf_files):
            try:
                # Create a unique run identifier (00, 01, etc.)
                run_id = f"{i+1:02d}"
                
                # Read the EDF file using MNE
                logger.info(f"Reading {edf_file.name} with MNE")
                raw = mne.io.read_raw_edf(edf_file, preload=True, verbose=False)
                
                # Set channel types to EEG if not specified
                for ch_name in raw.ch_names:
                    if raw.get_channel_types([ch_name])[0] == 'misc':
                        raw.set_channel_types({ch_name: 'eeg'})
                
                # Add standard montage if not present
                if raw.get_montage() is None:
                    try:
                        montage = mne.channels.make_standard_montage('standard_1020')
                        raw.set_montage(montage, match_case=False, on_missing='warn')
                    except Exception as e:
                        logger.warning(f"Could not set montage: {str(e)}")
                
                # Add seizure annotations if available
                if seizure_annotations and edf_file.name in seizure_annotations:
                    logger.info(f"Adding seizure annotations for {edf_file.name}")
                    seizures = seizure_annotations[edf_file.name]
                    
                    # Create MNE Annotations
                    onset = []
                    duration = []
                    description = []
                    
                    for seizure in seizures:
                        onset.append(seizure['onset'])
                        duration.append(seizure['duration'])
                        description.append('Seizure')
                    
                    if onset:  # Only add annotations if there are seizures
                        annotations = mne.Annotations(onset=onset, duration=duration, 
                                                     description=description)
                        raw.set_annotations(annotations)
                
                # Prepare BIDS path
                bids_path = BIDSPath(
                    subject=bids_subject_id,
                    session='01',
                    task='seizuremonitoring',
                    run=run_id,
                    root=bids_output
                )
                
                # Write to BIDS format
                logger.info(f"Writing {edf_file.name} to BIDS format")
                write_raw_bids(raw, bids_path, overwrite=True)
                
                # Update the sidecar JSON with additional info
                events_json_path = bids_path.copy().update(suffix='events').fpath.with_suffix('.json')
                if os.path.exists(events_json_path):
                    with open(events_json_path, 'r') as f:
                        events_json = json.load(f)
                    
                    # Add information about the seizure annotation
                    events_json.update({
                        "Seizure": {
                            "Description": "Epileptic seizure",
                            "HED": "Event/Category/Experimental-stimulus, Sensory-event"
                        }
                    })
                    
                    with open(events_json_path, 'w') as f:
                        json.dump(events_json, f, indent=4)
                
                logger.info(f"Successfully converted {edf_file.name}")
                
            except Exception as e:
                logger.error(f"Error converting {edf_file.name}: {str(e)}")
                continue
    
    # Create dataset_description.json
    create_dataset_description(bids_output)
    
    logger.info("Conversion to BIDS format completed!")

def parse_seizure_list(seizure_file):
    """Parse the Seizures-list-PNxx.txt file to extract seizure annotations"""
    annotations = {}
    
    with open(seizure_file, 'r') as f:
        lines = f.readlines()
    
    current_file = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        if line.endswith(".edf"):
            # New file section
            current_file = line
            annotations[current_file] = []
        elif current_file and "," in line:
            # Format: start_time, end_time
            try:
                parts = line.split(",")
                if len(parts) >= 2:  # Ensure we have at least start and end
                    start = float(parts[0].strip())
                    end = float(parts[1].strip())
                    annotations[current_file].append({
                        'onset': start,
                        'duration': end - start
                    })
            except Exception as e:
                logger.error(f"Error parsing seizure time: {line}, {str(e)}")
    
    return annotations

def create_dataset_description(bids_path):
    """Create a dataset_description.json file"""
    try:
        make_dataset_description(
            path=bids_path,
            name="Siena Scalp EEG Dataset",
            data_type="EEG",
            authors=["Dan, J.", "Detti, P."],
            acknowledgements="We thank the contributors to the Siena Scalp EEG dataset",
            how_to_acknowledge="Cite DOI: 10.5281/zenodo.10640762",
            funding=[""],
            references_and_links=["https://doi.org/10.5281/zenodo.10640762"],
            doi="10.5281/zenodo.10640762",
            license="ODC-BY 1.0",
            overwrite=True
        )
    except Exception as e:
        logger.error(f"Error creating dataset description with mne-bids: {str(e)}")
        # Fallback to manual creation
        import json
        
        description = {
            "Name": "Siena Scalp EEG Dataset",
            "BIDSVersion": "1.6.0",
            "DatasetType": "raw",
            "Authors": ["Dan, J.", "Detti, P."],
            "Acknowledgements": "We thank the contributors to the Siena Scalp EEG dataset",
            "HowToAcknowledge": "Cite DOI: 10.5281/zenodo.10640762",
            "ReferencesAndLinks": ["https://doi.org/10.5281/zenodo.10640762"],
            "DatasetDOI": "10.5281/zenodo.10640762",
            "License": "ODC-BY 1.0"
        }
        
        # Write the file
        with open(os.path.join(bids_path, "dataset_description.json"), "w") as f:
            json.dump(description, f, indent=4)

if __name__ == "__main__":
    convert_siena_to_bids()