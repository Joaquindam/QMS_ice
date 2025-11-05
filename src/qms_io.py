import numpy as np

def read_qms_file(file_path: str):
    """
    Lee un archivo QMS y devuelve:
        - headers: lista con los nombres de las columnas
        - data: diccionario {columna: np.array}

    El separador se detecta automáticamente (tabulación o espacio múltiple).
    Las columnas no numéricas al final o vacías son ignoradas.
    """

    # --- Leer líneas del archivo ---
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f if line.strip()]

    # --- Determinar el separador ---
    first_line = lines[0]
    if '\t' in first_line:
        sep = '\t'
    else:
        sep = None  # espacios múltiples

    # --- Extraer cabecera ---
    headers = lines[0].split(sep) if sep else first_line.split()
    n_cols = len(headers)

    # --- Cargar los datos numéricos ---
    try:
        data_array = np.genfromtxt(
            file_path,
            delimiter=sep,
            skip_header=1,
            autostrip=True,
            invalid_raise=False
        )
    except Exception as e:
        raise ValueError(f"Error al leer datos numéricos en {file_path}: {e}")

    # --- Si solo hay una columna, asegurar 2D ---
    if data_array.ndim == 1:
        data_array = data_array[:, np.newaxis]

    # --- Ajustar columnas si hay descuadre ---
    n_data_cols = data_array.shape[1]
    if n_data_cols < n_cols:
        headers = headers[:n_data_cols]
    elif n_data_cols > n_cols:
        headers += [f"col_{i}" for i in range(n_cols, n_data_cols)]

    # --- Crear diccionario de resultados ---
    data = {headers[i]: data_array[:, i] for i in range(len(headers))}

    return headers, data