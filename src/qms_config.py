"""
Configuración general para el análisis de datos del cuadrupolo de masas (QMS).
Define rutas, masas de interés, parámetros de visualización e integración.
"""

QMS_CONFIG = {
    # === Entrada de datos ===
    "QMS_PATH": r"C:\Users\Usuario\Documents\CAB\20251023_CO_irr_TPD\20251022_prueba-Synchro_QMS_ASPER.dat",

    # Claves de columnas
    "TIME_KEY": "TimesExp",
    "TEMP_KEY": "TempAK",

    # Masas de interés (None para todas)
    "MASSES": ["17.72", "27.84", "31.81", "43.94"],

    # === Tipo de análisis ===
    # Puede ser "temperature" (TPD) o "time" (experimento temporal)
    "ANALYSIS_MODE": "time",

    # === Rango de integración ===
    # Intervalo [inicio, fin] en segundos o Kelvin, según ANALYSIS_MODE
    "INTEGRATION_RANGE": (85000, 90000),

    # === Opciones de integración ===
    "INTEGRATE_SIGNALS": True,
    "SAVE_INTEGRATION_RESULTS": True,
    "INTEGRATION_RESULTS_FILE": "results/qms_integration_results.txt",

    # === Opciones de ploteo ===
    "PLOT_SIGNALS": True,
    "SHOW_PLOTS": True,
    "SAVE_PLOTS": True,
    "PLOT_OUTPUT_FILE": "results/qms_signals.png",
    "FIGSIZE": (8, 5),

    # === Estilo ===
    "LINEWIDTH": 1.2,
    "TITLE_TIME": "Señales QMS (m/z vs Tiempo)",
    "TITLE_TEMP": "Señales QMS (m/z vs Temperatura)",
}
