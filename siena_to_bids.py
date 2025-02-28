#!/usr/bin/env python
"""
Script to convert Siena Scalp EEG dataset to BIDS format using epilepsy2bids

Requirements:
- mne
- mne-bids
- pandas
- numpy
- epilepsy2bids
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import logging
import re
import datetime
import json
import mne
from dateutil.parser import parse as dateparse
from mne_bids import (BIDSPath, make_dataset_description)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def convert_siena_to_bids():
    try:
        # Import epilepsy2bids (will raise ImportError if not installed)
        from epilepsy2bids.datasets import SeizureDetectionDataset
        from epilepsy2bids.configs import SienaScalpEEGConfig
        from epilepsy2bids.utils import read_annotations
    except ImportError:
        logger.error("epilepsy2bids is not installed. Install it with: pip install epilepsy2bids")
        return
    
    # Define paths (use Path objects for cross-platform compatibility)
    siena_root = Path("/mnt/c/Users/user/Documents/eeg_data_challenge/physionet.org/files/siena-scalp-eeg/1.0.0")
    bids_output = Path("/mnt/c/Users/user/Documents/eeg_data_challenge/BIDS_Siena_Converted")
    
    # Check if siena_root exists
    if not siena_root.exists():
        logger.error(f"Source directory not found: {siena_root}")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(bids_output, exist_ok=True)
    
    # Load subject info if available
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
    
    # Process each subject with epilepsy2bids
    for subject_dir in subject_dirs:
        subject_id = subject_dir.name  # PN00, PN01, etc.
        subject_num = subject_id.replace("PN", "")
        logger.info(f"Processing subject: {subject_id}")
        
        # Create a SienaScalpEEGConfig for this subject
        config = SienaScalpEEGConfig(
            subject_id=subject_num,
            session_id="01",
            task_name="szMonitoring",
            # Set the channel renaming appropriately for Siena dataset
            rename_channels=True
        )
        
        # Find all EDF files for this subject
        edf_files = list(subject_dir.glob("*.edf"))
        if not edf_files:
            logger.warning(f"No EDF files found for {subject_id}, skipping")
            continue
        
        logger.info(f"Found {len(edf_files)} EDF files for {subject_id}")
        
        # Get seizure information
        seizure_list_file = subject_dir / f"Seizures-list-{subject_id}.txt"
        if not seizure_list_file.exists():
            logger.warning(f"Seizure list file not found for {subject_id}")
            seizure_events = []
        else:
            logger.info(f"Parsing seizure annotations from {seizure_list_file}")
            seizure_events = parse_siena_seizure_annotations(seizure_list_file)
        
        # Process each EDF file
        for run_idx, edf_file in enumerate(edf_files):
            run_id = f"{run_idx:02d}"
            logger.info(f"Processing run {run_id}: {edf_file.name}")
            
            # Get seizure events for this file
            current_seizures = [event for event in seizure_events if event['file_name'] == edf_file.name]
            
            try:
                # Create dataset
                dataset = SeizureDetectionDataset(
                    data_path=str(edf_file),
                    bids_path=str(bids_output),
                    config=config,
                    run=run_id
                )
                
                # Add seizure annotations if available
                if current_seizures:
                    logger.info(f"Adding {len(current_seizures)} seizure annotations to {edf_file.name}")
                    
                    # Convert to epilepsy2bids annotation format
                    annotations = []
                    for seizure in current_seizures:
                        annotations.append({
                            'onset': seizure['onset_sec'],
                            'duration': seizure['duration_sec'],
                            'description': 'Seizure'
                        })
                    
                    # Add annotations to dataset
                    dataset.add_annotations(annotations)
                
                # Write to BIDS
                logger.info(f"Converting {edf_file.name} to BIDS format")
                dataset.write_dataset(overwrite=True)
                logger.info(f"Successfully converted {edf_file.name}")
                
            except Exception as e:
                logger.error(f"Error converting {edf_file.name}: {str(e)}")
                continue
    
    # Create dataset_description.json
    create_dataset_description(bids_output)
    
    # Create participants.tsv and other metadata
    create_participants_tsv(bids_output, subject_info)
    
    logger.info("Conversion to BIDS format completed!")

def parse_siena_seizure_annotations(seizure_file):
    """
    Parse the Siena Seizures-list-PNxx.txt file to extract seizure annotations
    with proper time conversion
    """
    annotations = []
    
    with open(seizure_file, 'r') as f:
        content = f.read()
    
    # Extract patient ID
    patient_id = re.search(r'PN\d+', content).group(0) if re.search(r'PN\d+', content) else None
    
    # Find all seizure blocks
    seizure_blocks = re.findall(r'Seizure n \d+.*?(?=Seizure n \d+|\Z)', content, re.DOTALL)
    
    for block in seizure_blocks:
        try:
            # Extract filename
            file_match = re.search(r'File name: (.*\.edf)', block)
            if not file_match:
                continue
            filename = file_match.group(1)
            
            # Extract registration times
            reg_start = re.search(r'Registration start time: (\d+\.\d+\.\d+)', block)
            reg_end = re.search(r'Registration end time: *(\d+\.\d+\.\d+)', block)
            
            # Extract seizure times
            seizure_start = re.search(r'Seizure start time: (\d+\.\d+\.\d+)', block)
            seizure_end = re.search(r'Seizure end time: (\d+\.\d+\.\d+)', block)
            
            if not (reg_start and seizure_start and seizure_end):
                logger.warning(f"Could not parse all required times from seizure block: {block}")
                continue
                
            # Parse the times (format: HH.MM.SS)
            reg_start_time = parse_time(reg_start.group(1))
            seizure_start_time = parse_time(seizure_start.group(1))
            seizure_end_time = parse_time(seizure_end.group(1))
            
            # Calculate onset in seconds from recording start
            onset_sec = (seizure_start_time - reg_start_time).total_seconds()
            duration_sec = (seizure_end_time - seizure_start_time).total_seconds()
            
            # Ensure positive values
            if onset_sec < 0:
                logger.warning(f"Negative onset time calculated: {onset_sec}s, adjusting to 0")
                onset_sec = 0
                
            if duration_sec <= 0:
                logger.warning(f"Invalid duration: {duration_sec}s, skipping annotation")
                continue
            
            annotations.append({
                'file_name': filename,
                'onset_sec': onset_sec,
                'duration_sec': duration_sec
            })
            
            logger.info(f"Added seizure annotation for {filename}: onset={onset_sec}s, duration={duration_sec}s")
            
        except Exception as e:
            logger.error(f"Error parsing seizure block: {str(e)}")
    
    return annotations

def parse_time(time_str):
    """Parse time string in format HH.MM.SS to datetime object"""
    hours, minutes, seconds = map(int, time_str.split('.'))
    return datetime.datetime(1900, 1, 1, hours, minutes, seconds)

def create_dataset_description(bids_path):
    """Create a dataset_description.json file"""
    description = {
        "Name": "Siena Scalp EEG Dataset",
        "BIDSVersion": "1.8.0",
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
    
    logger.info(f"Created dataset_description.json at {bids_path}")

def create_participants_tsv(bids_path, subject_info=None):
    """Create participants.tsv and participants.json files"""
    # Get list of subjects from directory structure
    subjects = sorted([d.name.replace('sub-', '') for d in Path(bids_path).glob('sub-*')])
    
    # Create minimal participants dataframe
    participants_df = pd.DataFrame({
        'participant_id': [f'sub-{s}' for s in subjects]
    })
    
    # Add subject info if available
    if subject_info is not None:
        # Map subject IDs and merge additional info
        # This would need to be customized based on the actual structure of subject_info.csv
        pass
    
    # Save to TSV
    participants_df.to_csv(os.path.join(bids_path, 'participants.tsv'), sep='\t', index=False)
    logger.info(f"Created participants.tsv with {len(participants_df)} subjects")
    
    # Create participants.json schema
    participants_json = {
        "participant_id": {
            "Description": "Unique participant identifier"
        }
    }
    
    # Add additional field descriptions if subject_info is available
    
    # Save to JSON
    with open(os.path.join(bids_path, 'participants.json'), 'w') as f:
        json.dump(participants_json, f, indent=4)
    
    # Create events.json for seizure annotations
    events_json = {
        "Seizure": {
            "Description": "Epileptic seizure",
            "HED": "Event/Category/Experimental-stimulus, Sensory-event"
        }
    }
    
    with open(os.path.join(bids_path, 'events.json'), 'w') as f:
        json.dump(events_json, f, indent=4)
        
    logger.info("Created BIDS metadata files")

if __name__ == "__main__":
    convert_siena_to_bids()