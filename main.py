"""
main.py
--------------------------------------------------------------------
QMS Analysis — Mass Spectrometry (Quadrupole) Visualization & Integration Tool

Este script lee archivos del cuadrupolo de masas (QMS), representa las señales
de las masas seleccionadas frente a la temperatura y calcula el área integrada
bajo las curvas de desorción (TPD).

Desarrollado para el laboratorio de Astrofísica y Ciencias Planetarias.
--------------------------------------------------------------------
Author: Joaquín Delgado Amar
Affiliation: Centro de Astrobiología (CAB), CSIC-INTA, España
Date: 2025-11-03
--------------------------------------------------------------------
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from src.qms_io import read_qms_file
from src.qms_integrate import integrate_multiple_masses
from src.qms_plots import plot_multiple_masses
from src.qms_config import QMS_CONFIG


def main(cfg: dict):
    """
    Flujo principal del análisis QMS.
    1. Lee los datos desde archivo.
    2. Grafica las masas seleccionadas.
    3. Integra las áreas bajo las curvas de desorción.
    4. Guarda los resultados si se indica.
    """

    qms_path = cfg["QMS_PATH"]
    print(f"📂 Cargando datos QMS desde: {qms_path}")

    if not os.path.isfile(qms_path):
        raise FileNotFoundError(f"No se encontró el archivo: {qms_path}")

    # --- Leer datos ---
    headers, data = read_qms_file(qms_path)
    print(f"✅ Archivo leído correctamente ({len(headers)} columnas).")

    # --- Graficar ---
    if cfg.get("PLOT_SIGNALS", True):
        print("\n📊 Generando gráficos de las masas seleccionadas...")
        plot_multiple_masses(
            data,
            temp_key=cfg["TEMP_KEY"],
            masses=cfg["MASSES"],
            figsize=cfg["FIGSIZE"],
            linewidth=cfg["LINEWIDTH"],
            save_path=cfg["PLOT_OUTPUT_FILE"] if cfg.get("SAVE_PLOTS") else None,
            show=cfg.get("SHOW_PLOTS", True),
            title=cfg["TITLE"]
        )

    # --- Integrar ---
    if cfg.get("INTEGRATE_SIGNALS", True):
        print("\n🧮 Calculando integrales de desorción...")
        results = integrate_multiple_masses(
            data,
            temp_key=cfg["TEMP_KEY"],
            mass_keys=cfg["MASSES"]
        )

        print("\nResultados de integración (área bajo la curva):")
        for m, area in results.items():
            print(f"  • Masa {m}: {area:.4e}")

        # --- Guardar resultados ---
        if cfg.get("SAVE_INTEGRATION_RESULTS", True):
            out_path = cfg["INTEGRATION_RESULTS_FILE"]
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("Masa\tÁrea_integrada\n")
                for m, area in results.items():
                    f.write(f"{m}\t{area:.6e}\n")
            print(f"\n💾 Resultados guardados en: {out_path}")


# ===============================================================
#  EJECUCIÓN PRINCIPAL
# ===============================================================
if __name__ == "__main__":
    main(QMS_CONFIG)
