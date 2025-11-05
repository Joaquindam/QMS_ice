"""
Configuración general para el análisis de datos del cuadrupolo de masas (QMS).
Define rutas, masas de interés y parámetros de visualización.
"""

# === CONFIGURACIÓN PRINCIPAL ===
QMS_CONFIG = {
    # Ruta al archivo o carpeta con los datos QMS
    "QMS_PATH": r"C:\Users\Usuario\Documents\CAB\20251023_CO_irr_TPD\20251023_CO_irr_TPD_QMS.txt",

    # Columna de temperatura
    "TEMP_KEY": "TempAK",

    # Masas que queremos analizar (None para todas)
    "MASSES": ["18.00", "28.00", "32.00", "44.00"],

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
    "TITLE": "Señales QMS (m/z vs Temperatura)"
}
