"""
Visualización de señales del cuadrupolo de masas (QMS).
Permite graficar una o varias masas frente a la temperatura.
"""

import os
import matplotlib.pyplot as plt
import numpy as np


def plot_mass_signal(temp: np.ndarray, signal: np.ndarray, mass: str,
                     ax=None, label=None, linewidth=1.2, color=None):
    """
    Dibuja una sola señal de masa frente a la temperatura.

    Parámetros
    ----------
    temp : np.ndarray
        Temperaturas (en K).
    signal : np.ndarray
        Intensidad de la masa correspondiente.
    mass : str
        Nombre o valor de la masa (p.ej. '28.00').
    ax : matplotlib.axes.Axes, opcional
        Ejes donde dibujar. Si no se pasa, crea uno nuevo.
    label : str, opcional
        Etiqueta para la leyenda. Por defecto, 'Masa XX'.
    linewidth : float, opcional
        Grosor de línea.
    color : str, opcional
        Color de la curva.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))

    label = label or f"Masa {mass}"
    ax.plot(temp, signal, label=label, lw=linewidth, color=color)
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Intensidad (a.u.)")
    ax.set_title("Señal QMS vs Temperatura")
    return ax


def plot_multiple_masses(data: dict, temp_key: str = "TempAK",
                         masses=None, figsize=(8, 5),
                         linewidth=1.2, save_path=None, show=True,
                         title="Señales QMS (m/z vs Temperatura)"):
    """
    Grafica múltiples masas en una sola figura.

    Parámetros
    ----------
    data : dict
        Diccionario con los arrays de datos {columna: np.ndarray}.
    temp_key : str
        Nombre de la columna de temperatura.
    masses : list[str], opcional
        Lista de masas (columnas) a graficar. Si no se indica, detecta las numéricas.
    figsize : tuple, opcional
        Tamaño de la figura.
    linewidth : float, opcional
        Grosor de las líneas.
    save_path : str, opcional
        Ruta para guardar la figura (e.g. "results/qms_plot.png").
    show : bool, opcional
        Si True, muestra la figura al final.
    title : str, opcional
        Título de la figura.
    """
    if temp_key not in data:
        raise KeyError(f"No se encontró la columna de temperatura '{temp_key}' en los datos.")

    temp = data[temp_key]

    if masses is None:
        # Detecta las columnas que parezcan masas (numéricas)
        masses = [k for k in data.keys() if k.replace('.', '', 1).isdigit()]

    fig, ax = plt.subplots(figsize=figsize)
    for m in masses:
        if m in data:
            ax.plot(temp, data[m], label=f"Masa {m}", lw=linewidth)
        else:
            print(f"[WARN] Masa {m} no encontrada en los datos.")

    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Intensidad (a.u.)")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    # Guardar o mostrar
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Figura guardada en: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

# ===============================================================
# VISUALIZACIÓN EN FUNCIÓN DEL TIEMPO
# ===============================================================

def plot_mass_signal_time(time: np.ndarray, signal: np.ndarray, mass: str,
                          ax=None, label=None, linewidth=1.2, color=None):
    """
    Dibuja una sola señal de masa frente al tiempo.

    Parámetros
    ----------
    time : np.ndarray
        Tiempo (s).
    signal : np.ndarray
        Intensidad de la señal para una masa concreta.
    mass : str
        Nombre o valor de la masa (p.ej. '28.00').
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))

    label = label or f"Masa {mass}"
    ax.plot(time, signal, label=label, lw=linewidth, color=color)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Intensidad (a.u.)")
    ax.set_title("Señal QMS vs Tiempo")
    return ax


def plot_multiple_masses_time(data: dict, time_key: str = "TimesExp",
                              masses=None, figsize=(8, 5),
                              linewidth=1.2, save_path=None, show=True,
                              title="Señales QMS (m/z vs Tiempo)"):
    """
    Grafica múltiples masas en una sola figura frente al tiempo.
    """
    if time_key not in data:
        raise KeyError(f"No se encontró la columna de tiempo '{time_key}' en los datos.")

    time = data[time_key]

    if masses is None:
        masses = [k for k in data.keys() if k.replace('.', '', 1).isdigit()]

    fig, ax = plt.subplots(figsize=figsize)
    for m in masses:
        if m in data:
            ax.plot(time, data[m], label=f"Masa {m}", lw=linewidth)
        else:
            print(f"[WARN] Masa {m} no encontrada en los datos.")

    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Intensidad (a.u.)")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Figura guardada en: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)
