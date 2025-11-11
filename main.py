"""
main.py
--------------------------------------------------------------------
QMS_ice — Quadrupole Mass Spectrometry Analysis Tool

Analiza señales del cuadrupolo de masas (QMS) obtenidas en experimentos
de hielos astrofísicos. Puede operar en dos modos:
  - 'temperature': análisis de TPD (vs temperatura)
  - 'time': evolución temporal (vs tiempo)

--------------------------------------------------------------------
Author: Joaquín Delgado Amar
Affiliation: [Centro de Astrobiología (CAB), CSIC-INTA, Spain]
Date: 2025-11-07
--------------------------------------------------------------------
"""

import os
from src.qms_io import read_qms_file
from src.qms_integrate import (
    integrate_multiple_masses
)
from src.qms_plots import (
    plot_multiple_masses,
    plot_multiple_masses_time,
)
from src.qms_config import QMS_CONFIG


def main(cfg: dict):
    """
    Flujo principal del análisis QMS.
    """
    qms_path = cfg["QMS_PATH"]
    print(f"📂 Cargando datos QMS desde: {qms_path}")

    if not os.path.isfile(qms_path):
        raise FileNotFoundError(f"No se encontró el archivo: {qms_path}")

    # --- Leer datos ---
    headers, data = read_qms_file(qms_path)
    print(f"✅ Archivo leído correctamente ({len(headers)} columnas).")

    # === Determinar modo de análisis ===
    mode = cfg.get("ANALYSIS_MODE", "time").lower()
    if mode not in ["time", "temperature"]:
        raise ValueError("ANALYSIS_MODE debe ser 'time' o 'temperature'.")

    print(f"\n🔧 Modo de análisis seleccionado: {mode.upper()}")

    # ===============================================================
    # === PLOTEO DE SEÑALES ===
    # ===============================================================
    if cfg.get("PLOT_SIGNALS", True):
        print("\n📊 Generando gráficos de las masas seleccionadas...")
        if mode == "time":
            plot_multiple_masses_time(
                data,
                time_key=cfg["TIME_KEY"],
                masses=cfg["MASSES"],
                figsize=cfg["FIGSIZE"],
                linewidth=cfg["LINEWIDTH"],
                save_path=cfg["PLOT_OUTPUT_FILE"] if cfg.get("SAVE_PLOTS") else None,
                show=cfg.get("SHOW_PLOTS", True),
                title=cfg["TITLE_TIME"]
            )
        else:
            plot_multiple_masses(
                data,
                temp_key=cfg["TEMP_KEY"],
                masses=cfg["MASSES"],
                figsize=cfg["FIGSIZE"],
                linewidth=cfg["LINEWIDTH"],
                save_path=cfg["PLOT_OUTPUT_FILE"] if cfg.get("SAVE_PLOTS") else None,
                show=cfg.get("SHOW_PLOTS", True),
                title=cfg["TITLE_TEMP"]
            )

    # ===============================================================
    # === INTEGRACIÓN ===
    # ===============================================================

    if cfg.get("INTEGRATE_SIGNALS", True):
        start, end = cfg["INTEGRATION_RANGE"]
        print(f"\n🧮 Integrando señales entre {start} y {end} ({'s' if mode=='time' else 'K'})")

        x_key = cfg["TIME_KEY"] if mode == "time" else cfg["TEMP_KEY"]

        results = integrate_multiple_masses(
            data,
            x_key=x_key,
            mass_keys=cfg["MASSES"],
            integration_range=(start, end),
            save_dir="results/integrations",
            correct_baseline=True,
            show_plots=cfg.get("SHOW_PLOTS", False),
            save_plots=cfg.get("SAVE_PLOTS", True),
            xlabel="Tiempo (s)" if mode == "time" else "Temperatura (K)",
            ylabel="Intensidad (a.u.)"
        )

        print("\nResultados de integración (área bajo la curva):")
        for m, area in results.items():
            print(f"  • Masa {m}: {area:.4e}")

# ===============================================================
#  EJECUCIÓN PRINCIPAL
# ===============================================================
if __name__ == "__main__":
    main(QMS_CONFIG)
