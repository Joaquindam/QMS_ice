# src/qms_plots.py
"""
Visualization of Quadrupole Mass Spectrometry (QMS) signals.
Allows plotting one or multiple mass channels against temperature or time.
"""

import os
import matplotlib.pyplot as plt
import numpy as np


# ===============================================================
# PLOTTING MASS SIGNALS VS TEMPERATURE
# ===============================================================

def plot_mass_signal(temp: np.ndarray, signal: np.ndarray, mass: str,
                     ax=None, label=None, linewidth=1.2, color=None):
    """
    Plot a single QMS mass signal versus temperature.

    Parameters
    ----------
    temp : np.ndarray
        Temperature values (K).
    signal : np.ndarray
        Signal intensity corresponding to the selected mass.
    mass : str
        Mass label or value (e.g., '28.00').
    ax : matplotlib.axes.Axes, optional
        Axis object to plot on. If not provided, a new one is created.
    label : str, optional
        Label for the legend. Defaults to "Mass XX".
    linewidth : float, optional
        Line thickness.
    color : str, optional
        Line color.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))

    label = label or f"Mass {mass}"
    ax.plot(temp, signal, label=label, lw=linewidth, color=color)
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_title("QMS Signal vs Temperature")
    return ax


def plot_multiple_masses(data: dict, temp_key: str = "TempAK",
                         masses=None, figsize=(8, 5),
                         linewidth=1.2, save_path=None, show=True,
                         title="QMS Signals (m/z vs Temperature)"):
    """
    Plot multiple QMS mass signals in a single figure versus temperature.

    Parameters
    ----------
    data : dict
        Dictionary containing {column_name: np.ndarray}.
    temp_key : str
        Name of the temperature column.
    masses : list[str], optional
        List of mass channels (columns) to plot. 
        If None, all numeric-like columns will be plotted.
    figsize : tuple, optional
        Figure size.
    linewidth : float, optional
        Line width.
    save_path : str, optional
        File path to save the figure (e.g., "results/qms_plot.png").
    show : bool, optional
        If True, display the figure interactively.
    title : str, optional
        Plot title.
    """
    if temp_key not in data:
        raise KeyError(f"Temperature column '{temp_key}' not found in the data.")

    temp = data[temp_key]

    if masses is None:
        # Automatically detect numeric-like column names (mass channels)
        masses = [k for k in data.keys() if k.replace('.', '', 1).isdigit()]

    fig, ax = plt.subplots(figsize=figsize)
    for m in masses:
        if m in data:
            ax.plot(temp, data[m], label=f"Mass {m}", lw=linewidth)
        else:
            print(f"[WARN] Mass {m} not found in the data.")

    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    # Save or show figure
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Figure saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)


# ===============================================================
# PLOTTING MASS SIGNALS VS TIME
# ===============================================================

def plot_mass_signal_time(time: np.ndarray, signal: np.ndarray, mass: str,
                          ax=None, label=None, linewidth=1.2, color=None):
    """
    Plot a single QMS mass signal versus time.

    Parameters
    ----------
    time : np.ndarray
        Time values (s).
    signal : np.ndarray
        Signal intensity for the selected mass.
    mass : str
        Mass label or value (e.g., '28.00').
    ax : matplotlib.axes.Axes, optional
        Axis object to plot on. If not provided, a new one is created.
    label : str, optional
        Label for the legend. Defaults to "Mass XX".
    linewidth : float, optional
        Line thickness.
    color : str, optional
        Line color.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))

    label = label or f"Mass {mass}"
    ax.plot(time, signal, label=label, lw=linewidth, color=color)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_title("QMS Signal vs Time")
    return ax


def plot_multiple_masses_time(data: dict, time_key: str = "TimesExp",
                              masses=None, figsize=(8, 5),
                              linewidth=1.2, save_path=None, show=True,
                              title="QMS Signals (m/z vs Time)"):
    """
    Plot multiple QMS mass signals in a single figure versus time.
    """
    if time_key not in data:
        raise KeyError(f"Time column '{time_key}' not found in the data.")

    time = data[time_key] / 60.0  # Convert seconds → minutes

    if masses is None:
        masses = [k for k in data.keys() if k.replace('.', '', 1).isdigit()]

    fig, ax = plt.subplots(figsize=figsize)
    for m in masses:
        if m in data:
            ax.plot(time, data[m], label=f"{m}", lw=linewidth)
        else:
            print(f"[WARN] Mass {m} not found in the data.")

    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Intensity (A)")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.legend(title="m/z", frameon=False)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Figure saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

def plot_qms_and_photon_flux_time(data: dict,
                                  time_key: str = "TimesExp",
                                  photon_key: str = "PhCurrentA",
                                  masses=None,
                                  figsize=(8, 5),
                                  linewidth=1.2,
                                  photon_scale=1.924e22,
                                  save_path=None,
                                  show=True,
                                  title="QMS Signals and Photon Flux vs Time"):
    """
    Plot QMS mass signals and photon flux (converted from current) versus time.

    Parameters
    ----------
    data : dict
        Dictionary containing {column_name: np.ndarray}.
    time_key : str
        Name of the time column.
    photon_key : str
        Name of the photon current column (in Amperes).
    masses : list[str], optional
        List of mass channels (columns) to plot. 
        If None, all numeric-like columns are used.
    figsize : tuple, optional
        Figure size.
    linewidth : float, optional
        Line width for the plots.
    photon_scale : float, optional
        Conversion factor from A to photons·cm⁻²·s⁻¹.
    save_path : str, optional
        File path to save the figure (e.g., "results/qms_photon_flux.png").
    show : bool, optional
        If True, display the figure.
    title : str, optional
        Title of the figure.
    """
    if time_key not in data:
        raise KeyError(f"Time column '{time_key}' not found in data.")

    if photon_key not in data:
        raise KeyError(f"Photon current column '{photon_key}' not found in data.")

    time = data[time_key] / 60.0  # convert seconds → minutes
    photon_flux = data[photon_key] * photon_scale

    if masses is None:
        masses = [k for k in data.keys() if k.replace('.', '', 1).isdigit()]

    fig, ax1 = plt.subplots(figsize=figsize)

    # --- Left axis: QMS signals ---
    for m in masses:
        if m in data:
            ax1.plot(time, data[m], lw=linewidth, label=f"Mass {m}")
        else:
            print(f"[WARN] Mass {m} not found in data.")
    ax1.set_xlabel("Time (min)")
    ax1.set_ylabel("QMS Signal (a.u.)")
    ax1.set_yscale("log")

    # --- Right axis: Photon flux ---
    ax2 = ax1.twinx()
    ax2.plot(time, photon_flux, color="tab:orange", lw=1.5, label="Photon flux")
    ax2.set_ylabel("Photon Flux (photons·cm⁻²·s⁻¹)", color="tab:orange")
    ax2.tick_params(axis="y", labelcolor="tab:orange")

    # --- Combine legends ---
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left", frameon=False)

    ax1.set_title(title)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Figure saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

def plot_photon_flux_time(data: dict,
                          time_key: str = "TimesExp",
                          photon_key: str = "PhCurrentA",
                          photon_scale: float = 1.924e22,
                          figsize=(8, 4),
                          linewidth=1.5,
                          color="tab:orange",
                          save_path=None,
                          show=True,
                          title="Photon Flux vs Time"):
    """
    Plot the photon flux versus time (converted from current in Amperes).

    Parameters
    ----------
    data : dict
        Data dictionary containing the photon current column.
    time_key : str
        Column name for experimental time (s).
    photon_key : str
        Column name for photon current (A).
    photon_scale : float
        Conversion factor from A to photons·cm⁻²·s⁻¹.
    figsize : tuple
        Figure size.
    linewidth : float
        Line width.
    color : str
        Line color for the photon flux.
    save_path : str, optional
        File path to save the figure.
    show : bool, optional
        Whether to display the figure.
    title : str
        Figure title.
    """
    if time_key not in data or photon_key not in data:
        raise KeyError(f"Missing column: '{time_key}' or '{photon_key}' not found in data.")

    time = data[time_key] / 60.0  # Convert to minutes
    photon_flux = data[photon_key] * photon_scale

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time, photon_flux, color=color, lw=linewidth)
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Photon Flux (photons·cm⁻²·s⁻¹)")
    ax.set_title(title)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Figure saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)
