"""
Generate summary plots for every data directory in data/.
Each plot is saved as summary_plot.png in the corresponding directory.
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import ScalarFormatter

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DPI = 150
FIG_LINE = (8, 5)
FIG_HEAT = (7, 6)
CMAP = "plasma"


# ── helpers ──────────────────────────────────────────────────────────

def _savefig(fig, dirpath):
    out = os.path.join(dirpath, "summary_plot.png")
    fig.savefig(out, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → saved {out}")


def _load(dirpath, name):
    return np.load(os.path.join(dirpath, name))


def _npy_list(dirpath, prefix):
    """Return sorted list of (label, filepath) matching prefix*.npy"""
    files = sorted(f for f in os.listdir(dirpath)
                   if f.startswith(prefix) and f.endswith(".npy"))
    out = []
    for f in files:
        # extract the parameter value from filename like Qs_cr0.40.npy → 0.40
        m = re.search(rf"{prefix}(.+)\.npy", f)
        if m:
            out.append((m.group(1), os.path.join(dirpath, f)))
    return out


def _colors(n, cmap=CMAP):
    return [cm.get_cmap(cmap)(i / max(n - 1, 1)) for i in range(n)]


def _get_sweep_type(dirpath):
    info = os.path.join(dirpath, "info.txt")
    if not os.path.exists(info):
        return None
    with open(info) as f:
        for line in f:
            if line.startswith("Sweep:"):
                return line.split(":", 1)[1].strip()
    return None


def _title_from_dir(dirname):
    """Make a readable title from directory name."""
    # Strip date prefix
    parts = dirname.split("_", 3)
    if len(parts) >= 4:
        return parts[3].replace("_", " ").title()
    return dirname


def _freq_to_lam(freq, a_nm=250):
    return a_nm / freq


# ── plot functions ───────────────────────────────────────────────────

def plot_optimization(dirpath, dirname):
    """Plot Q trajectory over optimization epochs."""
    ofs = _load(dirpath, "ofs.npy")
    Q = _load(dirpath, "Q.npy")

    fig, ax = plt.subplots(figsize=FIG_LINE)
    epochs = np.arange(len(ofs))
    ax.plot(epochs, ofs, color=cm.get_cmap(CMAP)(0.3), linewidth=1.5)
    ax.set_xlabel("Epoch", fontsize=12)
    ax.set_ylabel("Objective (1/Q)", fontsize=12)
    ax.set_title(f"Optimization Trajectory — final Q = {Q[0]:,.0f}", fontsize=13)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_taper_single(dirpath, dirname):
    """Q vs taper angle, single radius."""
    angles = _load(dirpath, "taper_angles.npy")
    Qs = _load(dirpath, "Qs.npy")
    freqs = _load(dirpath, "freqs.npy")
    lam = _freq_to_lam(freqs)

    fig, ax1 = plt.subplots(figsize=FIG_LINE)
    c1, c2 = cm.get_cmap(CMAP)(0.2), cm.get_cmap(CMAP)(0.7)
    ax1.plot(angles, Qs, "o-", color=c1, markersize=4, linewidth=1.5)
    ax1.set_xlabel("Taper angle (°)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12, color=c1)
    ax1.tick_params(axis="y", labelcolor=c1, labelsize=10)
    ax1.tick_params(axis="x", labelsize=10)
    ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax1.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    ax2 = ax1.twinx()
    ax2.plot(angles, lam, "s-", color=c2, markersize=3, linewidth=1.5)
    ax2.set_ylabel("Wavelength (nm)", fontsize=12, color=c2)
    ax2.tick_params(axis="y", labelcolor=c2, labelsize=10)

    ax1.set_title(_title_from_dir(dirname), fontsize=13)
    ax1.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_radius_taper(dirpath, dirname):
    """Multi-radius Q vs taper angle."""
    angles = _load(dirpath, "taper_angles.npy")
    radii_files = sorted(f for f in os.listdir(dirpath) if f.startswith("Qs_r") and f.endswith(".npy"))
    radii = sorted(set(int(re.search(r"r(\d+)", f).group(1)) for f in radii_files))
    colors = _colors(len(radii))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for r, c in zip(radii, colors):
        Qs = _load(dirpath, f"Qs_r{r}.npy")
        ax.plot(angles, Qs, "o-", color=c, markersize=3, linewidth=1.5, label=f"r = {r} nm")
    ax.set_xlabel("Taper angle (°)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_piecewise_heatmap(dirpath, dirname):
    """2D heatmap: top angle vs bottom angle."""
    Q_mat = _load(dirpath, "Q_matrix.npy")
    angles = _load(dirpath, "angles.npy")

    fig, ax = plt.subplots(figsize=FIG_HEAT)
    im = ax.imshow(Q_mat, origin="lower", cmap=CMAP, aspect="auto",
                   extent=[angles[0], angles[-1], angles[0], angles[-1]])
    ax.set_xlabel("Bottom taper angle (°)", fontsize=12)
    ax.set_ylabel("Top taper angle (°)", fontsize=12)
    ax.set_title(f"{_title_from_dir(dirname)} — Q", fontsize=13)
    ax.tick_params(labelsize=10)
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("Quality factor Q", fontsize=11)
    cb.ax.tick_params(labelsize=10)
    _savefig(fig, dirpath)


def plot_oxide_thickness(dirpath, dirname):
    """Q vs oxide thickness, single curve."""
    t_ox = _load(dirpath, "t_ox_nm.npy")
    Qs = _load(dirpath, "Qs.npy")
    freqs = _load(dirpath, "freqs.npy")
    lam = _freq_to_lam(freqs)

    fig, ax1 = plt.subplots(figsize=FIG_LINE)
    c1, c2 = cm.get_cmap(CMAP)(0.2), cm.get_cmap(CMAP)(0.7)
    ax1.plot(t_ox, Qs, "o-", color=c1, markersize=4, linewidth=1.5)
    ax1.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12, color=c1)
    ax1.tick_params(axis="y", labelcolor=c1, labelsize=10)
    ax1.tick_params(axis="x", labelsize=10)
    ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax1.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    ax2 = ax1.twinx()
    ax2.plot(t_ox, lam, "s-", color=c2, markersize=3, linewidth=1.5)
    ax2.set_ylabel("Wavelength (nm)", fontsize=12, color=c2)
    ax2.tick_params(axis="y", labelcolor=c2, labelsize=10)

    ax1.set_title(_title_from_dir(dirname), fontsize=13)
    ax1.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_consume_ratio_oxide(dirpath, dirname):
    """Multi-cr Q vs oxide thickness."""
    t_ox = _load(dirpath, "t_ox_nm.npy")
    cr_files = sorted(f for f in os.listdir(dirpath) if f.startswith("Qs_cr") and f.endswith(".npy"))
    # Extract cr value: strip prefix and .npy suffix first
    cr_vals = sorted(float(f.replace("Qs_cr", "").replace(".npy", "")) for f in cr_files)
    colors = _colors(len(cr_vals))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for cr, c in zip(cr_vals, colors):
        Qs = _load(dirpath, f"Qs_cr{cr:.2f}.npy")
        ax.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.5, label=f"$c_r$ = {cr:.1f}")
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_radius_oxide(dirpath, dirname):
    """Multi-radius Q vs oxide thickness."""
    t_ox = _load(dirpath, "t_ox_nm.npy")
    r_files = sorted(f for f in os.listdir(dirpath) if f.startswith("Qs_r") and f.endswith(".npy"))
    radii = sorted(int(re.search(r"r(\d+)", f).group(1)) for f in r_files)
    colors = _colors(len(radii))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for r, c in zip(radii, colors):
        Qs = _load(dirpath, f"Qs_r{r}.npy")
        ax.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.5, label=f"r = {r} nm")
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_dx_shift_oxide(dirpath, dirname):
    """Multi-dx Q vs oxide thickness."""
    t_ox = _load(dirpath, "t_ox_nm.npy")
    dx_files = sorted(f for f in os.listdir(dirpath) if f.startswith("Qs_dx") and f.endswith(".npy"))
    # Extract dx value: strip prefix and .npy suffix
    dx_vals = sorted(float(f.replace("Qs_dx", "").replace(".npy", "")) for f in dx_files)
    colors = _colors(len(dx_vals))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for dx, c in zip(dx_vals, colors):
        Qs = _load(dirpath, f"Qs_dx{dx:.4f}.npy")
        ax.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.5, label=f"dx = {dx:.3f}a")
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_ellipticity(dirpath, dirname):
    """Q vs ellipticity, single curve."""
    e = _load(dirpath, "ellipticities.npy")
    Qs = _load(dirpath, "Qs.npy")
    freqs = _load(dirpath, "freqs.npy")
    lam = _freq_to_lam(freqs)

    fig, ax1 = plt.subplots(figsize=FIG_LINE)
    c1, c2 = cm.get_cmap(CMAP)(0.2), cm.get_cmap(CMAP)(0.7)
    ax1.plot(e, Qs, "o-", color=c1, markersize=4, linewidth=1.5)
    ax1.set_xlabel("Ellipticity", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12, color=c1)
    ax1.tick_params(axis="y", labelcolor=c1, labelsize=10)
    ax1.tick_params(axis="x", labelsize=10)
    ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax1.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    ax2 = ax1.twinx()
    ax2.plot(e, lam, "s-", color=c2, markersize=3, linewidth=1.5)
    ax2.set_ylabel("Wavelength (nm)", fontsize=12, color=c2)
    ax2.tick_params(axis="y", labelcolor=c2, labelsize=10)

    ax1.set_title(_title_from_dir(dirname), fontsize=13)
    ax1.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_ellipticity_rotation(dirpath, dirname):
    """2D heatmap: ellipticity vs rotation angle."""
    Q_map = _load(dirpath, "Q_map.npy")
    ells = _load(dirpath, "ellipticities.npy")
    phis = _load(dirpath, "phi_degs.npy")

    fig, ax = plt.subplots(figsize=FIG_HEAT)
    im = ax.imshow(Q_map, origin="lower", cmap=CMAP, aspect="auto",
                   extent=[phis[0], phis[-1], ells[0], ells[-1]])
    ax.set_xlabel("Rotation angle (°)", fontsize=12)
    ax.set_ylabel("Ellipticity", fontsize=12)
    ax.set_title(f"{_title_from_dir(dirname)} — Q", fontsize=13)
    ax.tick_params(labelsize=10)
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("Quality factor Q", fontsize=11)
    cb.ax.tick_params(labelsize=10)
    _savefig(fig, dirpath)


def plot_wg_consume_ratio(dirpath, dirname):
    """Multi-cr wavelength vs oxide thickness (waveguide)."""
    t_ox = _load(dirpath, "t_ox_nm.npy")
    cr_list = _load(dirpath, "cr_list.npy")
    colors = _colors(len(cr_list))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for cr, c in zip(cr_list, colors):
        lam = _load(dirpath, f"lam_cr{cr:.2f}.npy")
        ax.plot(t_ox, lam * 1e3, "o-", color=c, markersize=3, linewidth=1.5,
                label=f"$c_r$ = {cr:.1f}")
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Wavelength (nm)", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_lattice_constant(dirpath, dirname):
    """Q and wavelength vs lattice constant."""
    a_nm = _load(dirpath, "a_nm.npy")
    Qs = _load(dirpath, "Qs.npy")
    lam = _load(dirpath, "lambdas_nm.npy")

    fig, ax1 = plt.subplots(figsize=FIG_LINE)
    c1, c2 = cm.get_cmap(CMAP)(0.2), cm.get_cmap(CMAP)(0.7)
    ax1.plot(a_nm, Qs, "o-", color=c1, markersize=5, linewidth=1.5)
    ax1.set_xlabel("Lattice constant a (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12, color=c1)
    ax1.tick_params(axis="y", labelcolor=c1, labelsize=10)
    ax1.tick_params(axis="x", labelsize=10)
    ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax1.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

    ax2 = ax1.twinx()
    ax2.plot(a_nm, lam, "s-", color=c2, markersize=4, linewidth=1.5)
    ax2.set_ylabel("Wavelength (nm)", fontsize=12, color=c2)
    ax2.tick_params(axis="y", labelcolor=c2, labelsize=10)

    ax1.set_title(_title_from_dir(dirname), fontsize=13)
    ax1.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_conical_oxide_sweep(dirpath, dirname):
    """Multi-oxide-thickness Q vs taper angle."""
    angles = _load(dirpath, "taper_angles.npy")
    tox_files = sorted(f for f in os.listdir(dirpath) if f.startswith("Qs_tox") and f.endswith(".npy"))
    tox_vals = sorted(int(re.search(r"tox(\d+)", f).group(1)) for f in tox_files)
    colors = _colors(len(tox_vals))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for tox, c in zip(tox_vals, colors):
        Qs = _load(dirpath, f"Qs_tox{tox}.npy")
        ax.plot(angles, Qs, "o-", color=c, markersize=3, linewidth=1.5,
                    label=f"$t_{{ox}}$ = {tox} nm")
    ax.set_xlabel("Taper angle (°)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_random_oxide_sigma(dirpath, dirname):
    """Q mean ± std vs sigma."""
    sigma = _load(dirpath, "sigma_values.npy")
    Q_mean = _load(dirpath, "Q_mean.npy")
    Q_std = _load(dirpath, "Q_std.npy")
    Q_min = _load(dirpath, "Q_min.npy")
    Q_max = _load(dirpath, "Q_max.npy")

    fig, ax = plt.subplots(figsize=FIG_LINE)
    c = cm.get_cmap(CMAP)(0.3)
    ax.plot(sigma, Q_mean, "o-", color=c, markersize=5, linewidth=1.5, label="Mean Q")
    ax.fill_between(sigma, Q_min, Q_max, color=c, alpha=0.15, label="Min–Max")
    ax.fill_between(sigma, Q_mean - Q_std, Q_mean + Q_std, color=c, alpha=0.3, label="±1σ")
    ax.set_xlabel("Oxide roughness σ (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


def plot_random_oxide_2d(dirpath, dirname):
    """Multi-sigma Q mean ± std vs oxide thickness."""
    t_ox = _load(dirpath, "t_ox_nm.npy")
    sigma_list = _load(dirpath, "sigma_list.npy")
    colors = _colors(len(sigma_list))

    fig, ax = plt.subplots(figsize=FIG_LINE)
    for sig, c in zip(sigma_list, colors):
        Q_mean = _load(dirpath, f"Q_mean_s{sig:.1f}.npy")
        Q_std = _load(dirpath, f"Q_std_s{sig:.1f}.npy")
        ax.plot(t_ox, Q_mean, "o-", color=c, markersize=3, linewidth=1.5,
                label=f"σ = {sig:.1f} nm")
        ax.fill_between(t_ox, Q_mean - Q_std, Q_mean + Q_std, color=c, alpha=0.15)
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.set_title(_title_from_dir(dirname), fontsize=13)
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    _savefig(fig, dirpath)


# ── dispatch ─────────────────────────────────────────────────────────

SWEEP_HANDLERS = {
    "L3_opt_3hole": plot_optimization,
    "L3_opt_extended": plot_optimization,
    "taper_angle": plot_taper_single,
    "3h_taper_angle": plot_taper_single,
    "ext_taper_angle": plot_taper_single,
    "radius_taper": plot_radius_taper,
    "piecewise_taper_heatmap": plot_piecewise_heatmap,
    "3h_piecewise_taper_heatmap": plot_piecewise_heatmap,
    "ext_piecewise_taper_heatmap": plot_piecewise_heatmap,
    "oxide_thickness": plot_oxide_thickness,
    "3h_oxide_thickness": plot_oxide_thickness,
    "ext_oxide_thickness": plot_oxide_thickness,
    "consume_ratio_oxide": plot_consume_ratio_oxide,
    "3h_consume_ratio_oxide": plot_consume_ratio_oxide,
    "ext_consume_ratio_oxide": plot_consume_ratio_oxide,
    "3h_radius_oxide": plot_radius_oxide,
    "ext_radius_oxide": plot_radius_oxide,
    "dx_shift_oxide": plot_dx_shift_oxide,
    "dx_shift_oxide_smallShift": plot_dx_shift_oxide,
    "ellipticity": plot_ellipticity,
    "3h_ellipticity": plot_ellipticity,
    "ext_ellipticity": plot_ellipticity,
    "ellipticity_rotation": plot_ellipticity_rotation,
    "3h_ellipticity_rotation": plot_ellipticity_rotation,
    "ext_ellipticity_rotation": plot_ellipticity_rotation,
    "wg_consume_ratio_oxide": plot_wg_consume_ratio,
    "wg_consume_ratio_hole_only": plot_wg_consume_ratio,
    "lattice_constant": plot_lattice_constant,
    "ext_lattice_constant": plot_lattice_constant,
    "conical_oxide_sweep": plot_conical_oxide_sweep,
    "random_oxide_sigma": plot_random_oxide_sigma,
    "random_oxide_2d": plot_random_oxide_2d,
}


def main():
    dirs = sorted(d for d in os.listdir(DATA_DIR)
                  if os.path.isdir(os.path.join(DATA_DIR, d)) and d != "figures")

    success, fail, skip = 0, 0, 0
    for dirname in dirs:
        dirpath = os.path.join(DATA_DIR, dirname)
        sweep = _get_sweep_type(dirpath)
        if sweep is None:
            print(f"SKIP {dirname}: no info.txt")
            skip += 1
            continue
        handler = SWEEP_HANDLERS.get(sweep)
        if handler is None:
            print(f"SKIP {dirname}: unknown sweep type '{sweep}'")
            skip += 1
            continue
        print(f"Plotting {dirname} (sweep={sweep})")
        try:
            handler(dirpath, dirname)
            success += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            fail += 1

    print(f"\nDone: {success} plotted, {fail} failed, {skip} skipped")


if __name__ == "__main__":
    main()
