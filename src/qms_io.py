# src/qms_io.py
"""
Reads raw Quadrupole Mass Spectrometry (QMS) files and converts them into
NumPy arrays for analysis. Automatically detects separators (tabs or spaces)
and returns both the column headers and data as a dictionary.
"""

import numpy as np


def read_qms_file(file_path: str):
    """
    Read a QMS data file and return:
        - headers: list of column names
        - data: dictionary {column_name: np.ndarray}

    The column separator is automatically detected (tab or multiple spaces).
    Non-numeric or empty trailing columns are ignored.

    Parameters
    ----------
    file_path : str
        Path to the QMS data file (.txt, .dat, or .csv).

    Returns
    -------
    headers : list[str]
        List of column names extracted from the header line.
    data : dict[str, np.ndarray]
        Dictionary where each key is a column name and each value is a NumPy array
        containing the column data.
    """

    # --- Read all non-empty lines ---
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError(f"The file '{file_path}' is empty or unreadable.")

    # --- Detect column separator ---
    first_line = lines[0]
    if '\t' in first_line:
        sep = '\t'
    else:
        sep = None  # interpret multiple spaces as separator

    # --- Extract header names ---
    headers = first_line.split(sep) if sep else first_line.split()
    n_cols = len(headers)

    # --- Load numeric data ---
    try:
        data_array = np.genfromtxt(
            file_path,
            delimiter=sep,
            skip_header=1,
            autostrip=True,
            invalid_raise=False
        )
    except Exception as e:
        raise ValueError(f"Error reading numeric data from {file_path}: {e}")

    # --- Ensure 2D shape even if single column ---
    if data_array.ndim == 1:
        data_array = data_array[:, np.newaxis]

    # --- Adjust header count if mismatch occurs ---
    n_data_cols = data_array.shape[1]
    if n_data_cols < n_cols:
        headers = headers[:n_data_cols]
    elif n_data_cols > n_cols:
        headers += [f"col_{i}" for i in range(n_cols, n_data_cols)]

    # --- Create output dictionary ---
    data = {headers[i]: data_array[:, i] for i in range(len(headers))}

    return headers, data
