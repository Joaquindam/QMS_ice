"""
QMS_ice — Quadrupole Mass Spectrometry Analysis Tool

This script analyzes Quadrupole Mass Spectrometry (QMS) signals obtained
from astrophysical ice experiments. It supports two analysis modes:
  - 'temperature': TPD-type experiments (signal vs Temperature)
  - 'time': Temporal evolution experiments (signal vs Time)

--------------------------------------------------------------------
Author: Joaquín Delgado Amar
Affiliation: Centro de Astrobiología (CAB), CSIC-INTA, Spain
Date: 2025-11-11
--------------------------------------------------------------------
"""

import os
from src.qms_io import read_qms_file
from src.qms_integrate import integrate_multiple_masses, integrate_photon_flux
from src.qms_plots import plot_multiple_masses, plot_multiple_masses_time, plot_photon_flux_time

from src.qms_config import QMS_CONFIG


def main(cfg: dict):
    """
    Main execution flow for QMS analysis.
    """
    qms_path = cfg["QMS_PATH"]
    print(f"Loading QMS data from: {qms_path}")

    if not os.path.isfile(qms_path):
        raise FileNotFoundError(f"❌ File not found: {qms_path}")

    # --- Read QMS data ---
    headers, data = read_qms_file(qms_path)
    print(f"✅ File successfully read ({len(headers)} columns detected).")

    # === Determine analysis mode ===
    mode = cfg.get("ANALYSIS_MODE", "time").lower()
    if mode not in ["time", "temperature"]:
        raise ValueError("ANALYSIS_MODE must be 'time' or 'temperature'.")

    print(f"\nSelected analysis mode: {mode.upper()}")

    # ===============================================================
    # === SIGNAL PLOTTING ===
    # ===============================================================
    if cfg.get("PLOT_SIGNALS", True):
        print("Generating signal plots for selected masses...")
        if mode == "time":
            plot_multiple_masses_time(
                data,
                time_key=cfg["TIME_KEY"],
                masses=cfg["MASSES"],
                figsize=cfg["FIGSIZE"],
                linewidth=cfg["LINEWIDTH"],
                save_path=cfg["PLOT_OUTPUT_FILE_QMS"] if cfg.get("SAVE_PLOTS") else None,
                show=cfg.get("SHOW_PLOTS", True,),
                title="QMS Signals vs Time"
            )

            plot_photon_flux_time(
                data,
                time_key=cfg["TIME_KEY"],
                photon_key=cfg["PHOTON_KEY"],
                photon_scale=cfg["PHOTON_SCALE"],
                save_path=cfg["PLOT_OUTPUT_FILE_PHOTON"] if cfg.get("SAVE_PLOTS") else None,
                show=cfg.get("SHOW_PLOTS", True)
            )

        else:
            plot_multiple_masses(
                data,
                temp_key=cfg["TEMP_KEY"],
                masses=cfg["MASSES"],
                figsize=cfg["FIGSIZE"],
                linewidth=cfg["LINEWIDTH"],
                save_path=cfg["PLOT_OUTPUT_FILE"] if cfg.get("SAVE_PLOTS") else None,
                show=cfg.get("SHOW_PLOTS", False),
                title=cfg["TITLE_TEMP"]
            )

    # ===============================================================
    # === SIGNAL INTEGRATION ===
    # ===============================================================
    if cfg.get("INTEGRATE_SIGNALS", True):
        start_min, end_min = cfg["INTEGRATION_RANGE"]
        print(f"\nIntegrating signals between {start_min:.1f} and {end_min:.1f} min")

        x_key = cfg["TIME_KEY"] if mode == "time" else cfg["TEMP_KEY"]

        # --- QMS mass integration ---
        results = integrate_multiple_masses(
            data,
            x_key=x_key,
            mass_keys=cfg["MASSES"],
            integration_range=(start_min, end_min),  # minutes (no conversion here)
            save_dir="results/integrations",
            correct_baseline=True,
            show_plots=cfg.get("SHOW_PLOTS", False),
            save_plots=cfg.get("SAVE_PLOTS", True),
            xlabel="Time (min)" if mode == "time" else "Temperature (K)",
            ylabel="Intensity (A)"
        )

        print("\nIntegration results (area under the curve):")
        for m, area in results.items():
            print(f"  • Mass {m}: {area:.4e}")

        # --- Photon flux integration ---
        photon_area = integrate_photon_flux(
            data,
            time_key=cfg["TIME_KEY"],
            photon_key=cfg["PHOTON_KEY"],
            photon_scale=cfg["PHOTON_SCALE"],
            integration_range=(start_min, end_min),  # minutes (no conversion here)
            show_plot=cfg.get("SHOW_PLOTS", False),
            save_plot=cfg.get("SAVE_PLOTS", True),
            save_path="results/integrations",
            filename="photon_flux_integration.png"
        )

        print(f"\nIntegrated photon flux: {photon_area:.6e} photons·cm⁻²")


    # ===============================================================
    # === SAVE RESULTS TO TXT FILE ===
    # ===============================================================
    if cfg.get("SAVE_INTEGRATION_RESULTS", True):
        out_path = cfg["INTEGRATION_RESULTS_FILE"]
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("Mass\tIntegrated_Area\n")
            for m, area in results.items():
                f.write(f"{m}\t{area:.6e}\n")

            # Add integrated photon flux at the end of the file
            f.write("\nPhoton_Flux\t{:.6e}\n".format(photon_area))

        print(f"\nIntegration results (including photon flux) saved to: {out_path}")


# ===============================================================
#  EXECUTION ENTRY POINT
# ===============================================================
if __name__ == "__main__":
    main(QMS_CONFIG)
