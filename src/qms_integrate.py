import numpy as np
from scipy.integrate import simpson

def integrate_signal(temp: np.ndarray, signal: np.ndarray) -> float:
    """
    Integra una señal del QMS (por ejemplo, intensidad de masa 28) 
    frente a la temperatura usando la regla de Simpson.

    Parámetros
    ----------
    temp : np.ndarray
        Temperaturas (en K).
    signal : np.ndarray
        Intensidad de la señal para una masa concreta.
    
    Devuelve
    --------
    area : float
        Área integrada bajo la curva (en unidades arbitrarias).
    """
    if temp.size != signal.size:
        raise ValueError("Las arrays de temperatura y señal deben tener la misma longitud.")

    if len(temp) < 2:
        raise ValueError("No hay suficientes puntos para integrar.")

    # Eliminar valores NaN si los hay
    mask = np.isfinite(temp) & np.isfinite(signal)
    temp_clean = temp[mask]
    signal_clean = signal[mask]

    if len(temp_clean) < 2:
        raise ValueError("Demasiados NaN o datos no válidos en la señal.")

    # Asegurar que esté ordenado por temperatura
    idx = np.argsort(temp_clean)
    temp_sorted = temp_clean[idx]
    signal_sorted = signal_clean[idx]

    # Integración numérica
    area = simpson(signal_sorted, temp_sorted)
    return area


def integrate_multiple_masses(data: dict, temp_key: str = "TempAK", mass_keys=None):
    """
    Calcula el área integrada para varias masas a la vez.

    Parámetros
    ----------
    data : dict
        Diccionario con los arrays de datos {columna: np.ndarray}.
    temp_key : str
        Nombre de la columna de temperatura.
    mass_keys : list[str]
        Lista de columnas (masas) a integrar.

    Devuelve
    --------
    results : dict
        Diccionario {masa: área_integrada}.
    """
    if temp_key not in data:
        raise KeyError(f"No se encontró la columna de temperatura '{temp_key}'.")

    temp = data[temp_key]
    results = {}

    if mass_keys is None:
        # Detectar columnas que parezcan masas numéricas
        mass_keys = [k for k in data.keys() if k.replace('.', '', 1).isdigit()]

    for m in mass_keys:
        try:
            results[m] = integrate_signal(temp, data[m])
        except Exception as e:
            results[m] = np.nan
            print(f"[WARN] No se pudo integrar masa {m}: {e}")

    return results