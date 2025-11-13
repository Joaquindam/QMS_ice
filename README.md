# QMS_ice — Quadrupole Mass Spectrometry Analysis Tool

### Analysis of gas-phase desorption and temporal evolution in astrophysical ice experiments.

---

## Overview

**QMS_ice** is a modular Python package designed to process and analyze **Quadrupole Mass Spectrometry (QMS)** data obtained from astrophysical ice experiments.  
It supports both **temperature-programmed desorption (TPD)** and **time-resolved** experiments, allowing you to visualize and quantify mass signals (m/z) and correlate them with photon flux measurements.

The tool can:
- Read `.dat` QMS files directly from laboratory instruments.
- Plot one or multiple **mass channels** versus time or temperature.
- Integrate selected **mass peaks** with baseline correction.
- Compute the **photon fluence** over a defined interval.
- Automatically save plots and results in organized output folders.

---

## Installation

1. **Clone the repository**
   
   - git clone https://github.com/Joaquindam/QMS_ice.git
   - cd qms_ice

2. **(Optional) Create a virtual environment**

    - python -m venv venv
    - source venv/bin/activate   # macOS / Linux
    - venv\Scripts\activate      # Windows

3. **Install dependencies**

    pip install -r requirements.txt

---

## Features

- Read QMS data from ASCII-formatted `.dat` files  
- Flexible selection of **time** or **temperature** as the main axis  
- Integration of mass signals over a specified range (in minutes)  
- Automatic baseline correction for accurate peak area calculation  
- Photon flux conversion from current (A) to photons·cm⁻²·s⁻¹  
- Integrated photon fluence calculation with shaded visualization  
- Logarithmic-scale plotting for signals across several orders of magnitude  
- Automatic saving of plots and `.txt` summary tables  

---

## Repository structure

    QMS_ice/
    │
    ├── main.py # Main entry point              
    │
    ├── src/
    │   ├── qms_io.py              
    │   ├── qms_plots.py            
    │   ├── qms_integrate.py        
    │   ├── qms_config.py         
    │   └── __init__.py
    │
    ├── results/# (Optional) Output folder for plots
    ├── requirements.txt
    └── README.md


---

## Configuration

All analysis parameters can be adjusted in **`src/qms_config.py`**.

### Main configuration options

    | Key | Description |
    |-----|--------------|
    | `QMS_PATH` | Path to the `.dat` QMS data file. |
    | `ANALYSIS_MODE` | `"time"` for time-based analysis or `"temperature"` for TPD. |
    | `MASSES` | List of mass channels (m/z) to analyze. |
    | `INTEGRATION_RANGE` | Tuple specifying start and end time in **minutes**. |
    | `PHOTON_KEY` | Column name containing photon current (A). |
    | `PHOTON_SCALE` | Conversion factor from A to photons·cm⁻²·s⁻¹. |
    | `SAVE_PLOTS` / `SHOW_PLOTS` | Control whether plots are displayed or saved. |
    | `INTEGRATION_RESULTS_FILE` | Output file for the integrated areas. |

Example (inside `src/qms_config.py`):

    QMS_CONFIG = {
        "QMS_PATH": r"C:\Data\20251022_prueba-Synchro_QMS_ASPER.dat",
        "MASSES": ["17.72", "27.84", "31.81", "43.94"],
        "ANALYSIS_MODE": "time",
        "INTEGRATION_RANGE": (1490, 1500),  # minutes
        "INTEGRATE_SIGNALS": True,
        "SAVE_PLOTS": True,
        "SHOW_PLOTS": False,
        "PHOTON_KEY": "PhCurrentA",
        "PHOTON_SCALE": 1.924e22,
        "INTEGRATION_RESULTS_FILE": "results/qms_integration_results.txt",
    }


## Usage

1. Configure the analysis. 

Edit src/qms_config.py to set:

- The data file path (QMS_PATH)
- The list of masses to analyze (MASSES)
- The analysis mode (time or temperature)
- The integration range (in minutes)
- Whether to display or save plots

2. Run the program

From the repository root, execute:

    python main.py


3. Outputs

All results are automatically generated inside the /results directory.

- QMS signal plots (linear and log-scale options)
- Photon flux plots (photon_flux.png)
- Individual integration figures for each mass and for photon fluence
- Text file with integrated results

## Notes

- Time values are automatically converted from seconds to minutes for visualization.
- Integration is always performed with respect to time in seconds, ensuring correct numerical results.
- Photon flux is calculated from the column PhCurrentA (in A), scaled by 1.924e22 to photons·cm⁻²·s⁻¹.
- All figures are saved with 300 dpi resolution for publication-quality output.

## Requirements

Install dependencies using:

    pip install -r requirements.txt

## Relation to FTIR_ice

QMS_ice is the companion analysis tool to FTIR_ice.Both repositories share a modular design and are intended to work together for the combined analysis of infrared spectra (solid phase) and QMS data (gas phase) from astrophysical ice experiments.

## Author

Joaquín Delgado Amar
Centro de Astrobiología (CAB), CSIC-INTA, Spain
2025