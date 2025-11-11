"""
Integración de señales del cuadrupolo de masas (QMS) con corrección de línea base,
idéntica al método usado en FTIR_ice. Permite integrar respecto al tiempo o temperatura
y genera figuras con la región integrada sombreada.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson


def integrate_signal(
    x, y,
    x_min, x_max,
    correct_baseline=True,
    ax=None,
    show_plot=False,
    save_plot=False,
    save_path=None,
    filename=None,
    xlabel="Tiempo (s)",
    ylabel="Intensidad (a.u.)",
    title="Integración de señal QMS"
):
    """
    Integra una señal del QMS entre x_min y x_max, corrigiendo la línea base
    (recta entre los bordes del intervalo) y opcionalmente mostrando/guardando
    la región integrada sombreada.

    Parámetros
    ----------
    x, y : np.ndarray
        Eje (tiempo o temperatura) y señal de intensidad.
    x_min, x_max : float
        Límites del intervalo de integración.
    correct_baseline : bool, opcional
        Si True, resta una línea base lineal entre los extremos.
    show_plot : bool, opcional
        Muestra la figura de la integración.
    save_plot : bool, opcional
        Guarda la figura en disco.
    save_path : str, opcional
        Carpeta donde guardar la figura.
    filename : str, opcional
        Nombre del archivo de salida.
    xlabel, ylabel, title : str, opcional
        Etiquetas del gráfico.

    Devuelve
    --------
    area : float
        Área integrada (respecto a la línea base).
    baseline : np.ndarray
        Línea base en la región integrada.
    mask : np.ndarray
        Máscara booleana usada para seleccionar el intervalo.
    """

    x = np.asarray(x)
    y = np.asarray(y)

    # --- Seleccionar el intervalo de integración ---
    if x[0] > x[-1]:
        mask = (x <= x_min) & (x >= x_max)
    else:
        mask = (x >= x_min) & (x <= x_max)

    if np.sum(mask) < 3:
        raise ValueError(
            f"Región de integración [{x_min}, {x_max}] fuera de rango "
            f"({x.min():.1f}–{x.max():.1f}) o demasiado estrecha."
        )

    x_region = x[mask]
    y_region = y[mask]

    # --- Calcular línea base entre los extremos ---
    if correct_baseline:
        slope = (y_region[-1] - y_region[0]) / (x_region[-1] - x_region[0])
        intercept = y_region[0] - slope * x_region[0]
        baseline = slope * x_region + intercept
        y_corrected = y_region - baseline
    else:
        baseline = np.zeros_like(y_region)
        y_corrected = y_region

    # --- Integrar respecto a la línea base ---
    if x_region[0] > x_region[-1]:
        area = simpson(y_corrected[::-1], x_region[::-1])
    else:
        area = simpson(y_corrected, x_region)

    # --- Visualización de la región integrada ---
    if show_plot or save_plot:
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, "k-", lw=1.2, label="Señal QMS")
        ax.plot(x_region, baseline, "r--", lw=1.2, label="Línea base")
        ax.fill_between(x_region, y_region, baseline, color="tab:blue", alpha=0.3, label="Área integrada")
        ax.legend(frameon=False)
        ax.set_xlim(x_min, x_max)
        y_min, y_max = min(y_region.min(), baseline.min()), max(y_region.max(), baseline.max())
        margin = 0.2 * (y_max - y_min)
        ax.set_ylim(y_min - margin, y_max + margin)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        plt.tight_layout()

        # Mostrar o guardar
        if save_plot and save_path and filename:
            os.makedirs(save_path, exist_ok=True)
            full_path = os.path.join(save_path, filename)
            plt.savefig(full_path, dpi=300)
            plt.close()
            print(f"💾 Saved integration plot: {full_path}")
        elif show_plot:
            plt.show()

    return area, baseline, mask


def integrate_multiple_masses(
    data: dict,
    x_key: str,
    mass_keys,
    integration_range,
    save_dir="results/integrations",
    correct_baseline=True,
    show_plots=False,
    save_plots=True,
    xlabel="Tiempo (s)",
    ylabel="Intensidad (a.u.)"
):
    """
    Integra varias masas dentro de un rango definido, aplicando corrección
    de línea base y generando figuras con la región integrada.
    """
    x = data[x_key]
    x_min, x_max = integration_range
    results = {}

    for m in mass_keys:
        try:
            y = data[m]
            filename = f"integrated_mass_{m.replace('.', '_')}.png"
            area, _, _ = integrate_signal(
                x, y, x_min, x_max,
                correct_baseline=correct_baseline,
                show_plot=show_plots,
                save_plot=save_plots,
                save_path=save_dir,
                filename=filename,
                xlabel=xlabel,
                ylabel=ylabel,
                title=f"Masa {m} — Integración ({x_min}–{x_max})"
            )
            results[m] = area
        except Exception as e:
            results[m] = np.nan
            print(f"[WARN] No se pudo integrar masa {m}: {e}")

    return results
