# src/qms_config.py
"""
General configuration for the Quadrupole Mass Spectrometry (QMS) analysis.
Defines file paths, target masses, visualization parameters, and integration settings.
"""

QMS_CONFIG = {
    # === INPUT SETTINGS ===
        # Path to the QMS data file (ASCII format).
        "QMS_PATH": r"C:\Users\Usuario\Documents\CAB\20251023_CO_irr_TPD\20251022_prueba-Synchro_QMS_ASPER.dat",

        # Column identifiers
        "TIME_KEY": "TimesExp",         # Experimental time (s)
        "TEMP_KEY": "TempAK",           # Temperature (K)

    # === PHOTON FLUX SETTINGS ===
        "PHOTON_KEY": "PhCurrentA",     # Column name for photon current (A)
        "PHOTON_SCALE": 1.924e22,       # Conversion factor from A to photons·cm⁻²·s⁻¹


    # === MASSES OF INTEREST ===
        # Define which masses (m/z) to analyze. If None, all available masses will be processed.
        # Typical masses detected:
        # 0.91, 1.91, 11.80, 12.78, 13.77, 14.76, 15.75, 16.74, 17.72, 18.73, 19.74,
        # 23.79, 24.80, 27.84, 28.84, 29.83, 30.82, 31.81, 32.82, 33.83, 34.84, 35.85,
        # 39.89, 43.94, 44.94, 45.94, 46.94, 47.94, 48.94, 49.94, 59.94, 62.94, 63.94,
        # 64.95, 66.00, 76.00, 77.00, 78.00, 80.00, 81.00, 82.00, 96.00, 128.00, 150.00
        "MASSES": ["11.80", "12.78", "15.75", "27.84"],

    # === ANALYSIS MODE ===
        # Choose between:
        #   "temperature": TPD-type experiments (signal vs Temperature)
        #   "time": Temporal evolution (signal vs Time)
        "ANALYSIS_MODE": "time",

    # === INTEGRATION RANGE ===
        # Integration interval [start, end] in minutes or Kelvin,
        # depending on the selected ANALYSIS_MODE.
        "INTEGRATION_RANGE": (1370.4, 1376.8),

    # === INTEGRATION OPTIONS ===
        "INTEGRATE_SIGNALS": True,                       # Perform integration
        "SAVE_INTEGRATION_RESULTS": True,                # Save integrated areas to file
        "INTEGRATION_RESULTS_FILE": "results/qms_integration_results.txt",

    # === PLOTTING OPTIONS ===
        "PLOT_SIGNALS": True,                            # Plot all selected mass signals
        "SHOW_PLOTS": True,                              # Display plots interactively
        "SAVE_PLOTS": True,                              # Save plots to disk
        "PLOT_OUTPUT_FILE_QMS": "results/qms_signals.png",
        "PLOT_OUTPUT_FILE_PHOTON": "results/photon_flux.png",
        "FIGSIZE": (8, 5),

    # === STYLE SETTINGS ===
        "LINEWIDTH": 1.2,
        "TITLE_TIME": "QMS Signals (m/z vs Time)",
        "TITLE_TEMP": "QMS Signals (m/z vs Temperature)",
}