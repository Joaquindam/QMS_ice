# src/qms_integrate.py
"""
Integration of Quadrupole Mass Spectrometry (QMS) signals with baseline correction.
Allows integration with respect to time or temperature and generates 
figures highlighting the integrated region.
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
    xlabel="Time (min)",
    ylabel="Intensity (A)",
    title="Integration"
):
    """
    Integrate a QMS signal between x_min and x_max (given in SECONDS),
    but plot the x-axis in MINUTES.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.integrate import simpson
    import os

    x = np.asarray(x)
    y = np.asarray(y)

    mask = (x >= x_min) & (x <= x_max)
    if np.sum(mask) < 3:
        raise ValueError(f"Integration region [{x_min}, {x_max}] outside data range.")

    x_region = x[mask]
    y_region = y[mask]

    # Baseline correction
    if correct_baseline:
        slope = (y_region[-1] - y_region[0]) / (x_region[-1] - x_region[0])
        intercept = y_region[0] - slope * x_region[0]
        baseline = slope * x_region + intercept
        y_corrected = y_region - baseline
    else:
        baseline = np.zeros_like(y_region)
        y_corrected = y_region

    # Integration
    area = simpson(y_corrected, x_region)

    # Plot
    if show_plot or save_plot:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x / 60.0, y, "k-", lw=1.2, label="Signal")
        ax.plot(x_region / 60.0, baseline, "r--", lw=1.2, label="Baseline")
        ax.fill_between(x_region / 60.0, y_region, baseline, color="tab:blue", alpha=0.3)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_yscale('log')
        ax.set_xlim(x_min / 60.0, x_max / 60.0)
        ax.set_ylim(min(y_region.min(), baseline.min())*0.9, max(y_region.max(), baseline.max())*1.1)
        ax.set_title(title)
        ax.legend(frameon=False)
        plt.tight_layout()

        if save_plot and save_path and filename:
            os.makedirs(save_path, exist_ok=True)
            full_path = os.path.join(save_path, filename)
            plt.savefig(full_path, dpi=300)
            plt.close()
            print(f"Integration plot saved to: {full_path}")
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
    xlabel="Time (min)",
    ylabel="Intensity (A)"
):
    """
    Integrate multiple QMS mass channels over a defined range (in MINUTES),
    applying baseline correction and generating figures for each integrated region.

    Parameters
    ----------
    data : dict
        Dictionary containing data columns {column_name: np.ndarray}.
    x_key : str
        Key corresponding to the x-axis variable (time or temperature).
    mass_keys : list[str]
        List of mass channels (m/z values) to integrate.
    integration_range : tuple[float, float]
        Start and end points of the integration range (in minutes).
    save_dir : str, optional
        Directory to save integration figures.
    correct_baseline : bool, optional
        Apply baseline correction between the interval edges.
    show_plots : bool, optional
        If True, display plots for each mass.
    save_plots : bool, optional
        If True, save the generated plots.
    xlabel, ylabel : str, optional
        Axis labels for the plots.

    Returns
    -------
    results : dict
        Dictionary {mass: integrated_area}.
    """
    import numpy as np
    from .qms_integrate import integrate_signal  # asegúrate de tener esta importación si está en otro archivo

    x = np.asarray(data[x_key])  # en segundos
    x_min_min, x_max_min = integration_range

    # Convert minutes → seconds for integration math
    x_min = x_min_min * 60
    x_max = x_max_min * 60

    results = {}

    for m in mass_keys:
        try:
            y = np.asarray(data[m])
            filename = f"integrated_mass_{m.replace('.', '_')}.png"
            area, _, _ = integrate_signal(
                x, y, x_min, x_max,
                correct_baseline=correct_baseline,
                show_plot=show_plots,
                save_plot=save_plots,
                save_path=save_dir,
                filename=filename,
                xlabel=xlabel,  # Time (min)
                ylabel=ylabel,
                title=f"{m} — Integration ({x_min_min:.1f}–{x_max_min:.1f} min)"
            )
            results[m] = area
        except Exception as e:
            results[m] = np.nan
            print(f"[WARN] Could not integrate mass {m}: {e}")

    return results


def integrate_photon_flux(data: dict,
                          time_key: str = "TimesExp",
                          photon_key: str = "PhCurrentA",
                          photon_scale: float = 1.924e22,
                          integration_range=None,
                          show_plot=False,
                          save_plot=False,
                          save_path=None,
                          filename="photon_flux_integration.png"):
    """
    Integrate the photon flux over a specified time range (in minutes) and optionally
    plot the integrated region with a shaded band.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.integrate import simpson
    import os

    if time_key not in data or photon_key not in data:
        raise KeyError(f"Missing column: '{time_key}' or '{photon_key}' not found in data.")

    time = np.asarray(data[time_key])  # in seconds
    photon_flux = np.asarray(data[photon_key]) * photon_scale

    if integration_range is not None:
        # Convert input range (minutes) → seconds
        t_min, t_max = integration_range
        t_min *= 60
        t_max *= 60
        mask = (time >= t_min) & (time <= t_max)
        time_region = time[mask]
        flux_region = photon_flux[mask]
    else:
        time_region = time
        flux_region = photon_flux

    if len(time_region) < 2:
        raise ValueError("Integration range is too narrow or outside data limits.")

    photon_area = simpson(flux_region, time_region)

    # --- Plot shaded integration region ---
    if show_plot or save_plot:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(time / 60.0, photon_flux, color="tab:orange", lw=1.2, label="Photon flux")
        ax.fill_between(time_region / 60.0, flux_region, color="tab:orange", alpha=0.3,
                        label="Integrated area")
        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Photon Flux (photons·cm⁻²·s⁻¹)")
        ax.set_title(f"Photon Flux Integration ({t_min/60:.1f}–{t_max/60:.1f} min)")
        ax.set_xlim(time_region.min() / 60.0, time_region.max() / 60.0)
        ax.legend(frameon=False)
        plt.tight_layout()

        if save_plot and save_path is not None and filename is not None:
            os.makedirs(save_path, exist_ok=True)
            full_path = os.path.join(save_path, filename)
            plt.savefig(full_path, dpi=300)
            plt.close()
            print(f"Integration plot saved to: {full_path}")
        elif show_plot:
            plt.show()

    return photon_area

