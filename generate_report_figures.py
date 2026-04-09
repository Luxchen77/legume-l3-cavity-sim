"""
Generate combined figures for the simulation report.
Saves PNGs to paper/figures/.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FuncFormatter

DATA = os.path.join(os.path.dirname(__file__), "data")
OUT  = os.path.join(os.path.dirname(__file__), "paper", "figures")
os.makedirs(OUT, exist_ok=True)

DPI = 200
CMAP = "plasma"

def _colors(n, cmap=CMAP):
    return [cm.get_cmap(cmap)(i / max(n - 1, 1)) for i in range(n)]

def _load(subdir, name):
    return np.load(os.path.join(DATA, subdir, name))

def _freq_to_lam(freq, a=250):
    return a / freq

def _thousands_formatter(x, pos):
    """Format y-axis as e.g. '200k', '1.4M'."""
    if x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.0f}k"
    else:
        return f"{x:.0f}"

def _millions_formatter(x, pos):
    if x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.0f}k"
    else:
        return f"{x:.0f}"

fmt_Q = FuncFormatter(_thousands_formatter)


# ═══════════════════════════════════════════════════════════════════
# Figure 1: Q vs Hole Radius (1-hole + 3-hole, dual panel)
# ═══════════════════════════════════════════════════════════════════
def fig_Q_vs_radius():
    # 1-hole from radius_taper at taper=0
    rt = "2026-03-17_223032_radius_taper"
    radii = [73, 74, 75, 76, 77]
    Q_1h = [_load(rt, f"Qs_r{r}.npy")[0] for r in radii]
    f_1h = [_load(rt, f"freqs_r{r}.npy")[0] for r in radii]
    lam_1h = [_freq_to_lam(f) for f in f_1h]

    # 3-hole from 3h_radius_oxide at t_ox=0
    ro = "2026-03-20_171522_3h_radius_oxide"
    Q_3h = [_load(ro, f"Qs_r{r}.npy")[0] for r in radii]
    f_3h = [_load(ro, f"freqs_r{r}.npy")[0] for r in radii]
    lam_3h = [_freq_to_lam(f) for f in f_3h]

    c1, c2 = cm.get_cmap(CMAP)(0.15), cm.get_cmap(CMAP)(0.65)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Q panel
    ax1.plot(radii, Q_1h, "o-", color=c1, markersize=6, linewidth=2, label="1-hole")
    ax1.plot(radii, Q_3h, "s-", color=c2, markersize=6, linewidth=2, label="3-hole")
    ax1.set_xlabel("Hole radius r (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=11)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title("(a) Quality factor", fontsize=12)

    # Wavelength panel
    ax2.plot(radii, lam_1h, "o-", color=c1, markersize=6, linewidth=2, label="1-hole")
    ax2.plot(radii, lam_3h, "s-", color=c2, markersize=6, linewidth=2, label="3-hole")
    ax2.set_xlabel("Hole radius r (nm)", fontsize=12)
    ax2.set_ylabel("Resonance wavelength λ₀ (nm)", fontsize=12)
    ax2.legend(fontsize=11)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_title("(b) Resonance wavelength", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_Q_vs_radius.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_Q_vs_radius.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: Q vs Taper Angle — all 3 designs combined
# ═══════════════════════════════════════════════════════════════════
def fig_Q_vs_taper_combined():
    d1h = "2026-03-17_150847_taper_angle"
    d3h = "2026-04-01_114658_3h_taper_angle"
    dex = "2026-04-01_135028_ext_taper_angle"

    a1 = _load(d1h, "taper_angles.npy"); Q1 = _load(d1h, "Qs.npy"); f1 = _load(d1h, "freqs.npy")
    a3 = _load(d3h, "taper_angles.npy"); Q3 = _load(d3h, "Qs.npy"); f3 = _load(d3h, "freqs.npy")
    ae = _load(dex, "taper_angles.npy"); Qe = _load(dex, "Qs.npy"); fe = _load(dex, "freqs.npy")

    c1, c2, c3 = cm.get_cmap(CMAP)(0.1), cm.get_cmap(CMAP)(0.5), cm.get_cmap(CMAP)(0.85)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.5))

    # Absolute Q panel
    ax1.plot(a1, Q1, "o-", color=c1, markersize=3, linewidth=2, label="1-hole")
    ax1.plot(a3, Q3, "s-", color=c2, markersize=3, linewidth=2, label="3-hole")
    ax1.plot(ae, Qe, "^-", color=c3, markersize=3, linewidth=2, label="Extended")
    ax1.set_xlabel("Taper angle θ (°)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=10)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title("(a) Absolute Q", fontsize=12)

    # Normalized Q/Q0 panel
    ax2.plot(a1, Q1 / Q1[0], "o-", color=c1, markersize=3, linewidth=2, label="1-hole")
    ax2.plot(a3, Q3 / Q3[0], "s-", color=c2, markersize=3, linewidth=2, label="3-hole")
    ax2.plot(ae, Qe / Qe[0], "^-", color=c3, markersize=3, linewidth=2, label="Extended")
    ax2.set_xlabel("Taper angle θ (°)", fontsize=12)
    ax2.set_ylabel("Normalized $Q / Q_0$", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    ax2.set_title("(b) Fraction of ideal Q retained", fontsize=12)

    # Wavelength panel
    ax3.plot(a1, _freq_to_lam(f1), "o-", color=c1, markersize=3, linewidth=2, label="1-hole")
    ax3.plot(a3, _freq_to_lam(f3), "s-", color=c2, markersize=3, linewidth=2, label="3-hole")
    ax3.plot(ae, _freq_to_lam(fe), "^-", color=c3, markersize=3, linewidth=2, label="Extended")
    ax3.set_xlabel("Taper angle θ (°)", fontsize=12)
    ax3.set_ylabel("Resonance wavelength λ₀ (nm)", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.tick_params(labelsize=10)
    ax3.grid(alpha=0.3)
    ax3.set_title("(c) Resonance wavelength", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_Q_vs_taper_combined.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_Q_vs_taper_combined.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: Q vs Taper — 1-hole multi-radius
# ═══════════════════════════════════════════════════════════════════
def fig_Q_vs_taper_multiradius():
    rt = "2026-03-17_223032_radius_taper"
    angles = _load(rt, "taper_angles.npy")
    radii = [73, 74, 75, 76, 77]
    colors = _colors(len(radii))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for r, c in zip(radii, colors):
        Qs = _load(rt, f"Qs_r{r}.npy")
        ax.plot(angles, Qs, "o-", color=c, markersize=4, linewidth=1.8, label=f"r = {r} nm")
    ax.set_xlabel("Taper angle θ (°)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.yaxis.set_major_formatter(fmt_Q)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_Q_vs_taper_multiradius.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_Q_vs_taper_multiradius.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: Q vs Oxide Thickness, cr=0.5, 3-hole multi-radius
# ═══════════════════════════════════════════════════════════════════
def fig_oxide_fixed_cr():
    ro = "2026-03-20_171522_3h_radius_oxide"
    t_ox = _load(ro, "t_ox_nm.npy")
    radii = [73, 74, 75, 76, 77]
    colors = _colors(len(radii))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    for r, c in zip(radii, colors):
        Qs = _load(ro, f"Qs_r{r}.npy")
        freqs = _load(ro, f"freqs_r{r}.npy")
        ax1.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.8, label=f"r = {r} nm")
        ax2.plot(t_ox, _freq_to_lam(freqs), "o-", color=c, markersize=3, linewidth=1.8, label=f"r = {r} nm")

    ax1.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=10)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title("(a) Quality factor", fontsize=12)

    ax2.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax2.set_ylabel("Resonance wavelength λ₀ (nm)", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_title("(b) Resonance wavelength", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_oxide_fixed_cr.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_oxide_fixed_cr.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 5: Q vs Oxide Thickness, varying cr — 3-hole
# ═══════════════════════════════════════════════════════════════════
def fig_oxide_varying_cr():
    cr_dir = "2026-03-20_174404_3h_consume_ratio_oxide"
    t_ox = _load(cr_dir, "t_ox_nm.npy")
    cr_vals = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    colors = _colors(len(cr_vals))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    for cr, c in zip(cr_vals, colors):
        Qs = _load(cr_dir, f"Qs_cr{cr:.2f}.npy")
        freqs = _load(cr_dir, f"freqs_cr{cr:.2f}.npy")
        ax1.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.8, label=f"$c_r$ = {cr:.1f}")
        ax2.plot(t_ox, _freq_to_lam(freqs), "o-", color=c, markersize=3, linewidth=1.8, label=f"$c_r$ = {cr:.1f}")

    ax1.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=10)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title("(a) Quality factor", fontsize=12)

    ax2.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax2.set_ylabel("Resonance wavelength λ₀ (nm)", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_title("(b) Resonance wavelength", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_oxide_varying_cr.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_oxide_varying_cr.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 6: Oxide comparison across all 3 designs at cr=0.5, r=75nm
# ═══════════════════════════════════════════════════════════════════
def fig_oxide_all_designs():
    # 1-hole: only 4 points
    d1h = "2026-03-12_130411_oxide_thickness"
    t1 = _load(d1h, "t_ox_nm.npy")
    Q1 = _load(d1h, "Qs.npy")

    # 3-hole: from radius_oxide at r=75
    d3h = "2026-03-20_171522_3h_radius_oxide"
    t3 = _load(d3h, "t_ox_nm.npy")
    Q3 = _load(d3h, "Qs_r75.npy")

    # Extended: newest
    dex = "2026-03-24_191423_ext_oxide_thickness"
    te = _load(dex, "t_ox_nm.npy")
    Qe = _load(dex, "Qs.npy")

    c1, c2, c3 = cm.get_cmap(CMAP)(0.1), cm.get_cmap(CMAP)(0.5), cm.get_cmap(CMAP)(0.85)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Absolute Q
    ax1.plot(t1, Q1, "o-", color=c1, markersize=5, linewidth=2, label="1-hole")
    ax1.plot(t3, Q3, "s-", color=c2, markersize=4, linewidth=2, label="3-hole")
    ax1.plot(te, Qe, "^-", color=c3, markersize=4, linewidth=2, label="Extended")
    ax1.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=10)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title("(a) Absolute Q", fontsize=12)

    # Normalized Q/Q0
    ax2.plot(t1, Q1 / Q1[0], "o-", color=c1, markersize=5, linewidth=2, label="1-hole")
    ax2.plot(t3, Q3 / Q3[0], "s-", color=c2, markersize=4, linewidth=2, label="3-hole")
    ax2.plot(te, Qe / Qe[0], "^-", color=c3, markersize=4, linewidth=2, label="Extended")
    ax2.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax2.set_ylabel("Normalized $Q / Q_0$", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    ax2.set_title("(b) Fraction of ideal Q retained", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_oxide_all_designs.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_oxide_all_designs.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 7: Piecewise taper heatmaps — 1h, 3h, ext side by side
# ═══════════════════════════════════════════════════════════════════
def fig_piecewise_heatmaps():
    dirs = [
        ("2026-03-26_181204_piecewise_taper_heatmap", "1-hole"),
        ("2026-04-01_121843_3h_piecewise_taper_heatmap", "3-hole"),
        ("2026-04-01_142012_ext_piecewise_taper_heatmap", "Extended"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, (d, label) in zip(axes, dirs):
        Q_mat = _load(d, "Q_matrix.npy")
        angles = _load(d, "angles.npy")
        im = ax.imshow(Q_mat, origin="lower", cmap=CMAP, aspect="auto",
                       extent=[angles[0], angles[-1], angles[0], angles[-1]])
        ax.set_xlabel("Bottom angle (°)", fontsize=11)
        ax.set_ylabel("Top angle (°)", fontsize=11)
        ax.set_title(label, fontsize=12)
        ax.tick_params(labelsize=9)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cb.ax.tick_params(labelsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_piecewise_heatmaps.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_piecewise_heatmaps.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 8: Conical taper + oxide combined sweep
# ═══════════════════════════════════════════════════════════════════
def fig_conical_oxide():
    d = "2026-03-24_150737_conical_oxide_sweep"
    angles = _load(d, "taper_angles.npy")
    tox_vals = [0, 2, 4, 6, 8]
    colors = _colors(len(tox_vals))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for tox, c in zip(tox_vals, colors):
        Qs = _load(d, f"Qs_tox{tox}.npy")
        ax.plot(angles, Qs, "o-", color=c, markersize=4, linewidth=1.8, label=f"$t_{{ox}}$ = {tox} nm")
    ax.set_xlabel("Taper angle θ (°)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.yaxis.set_major_formatter(fmt_Q)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_conical_oxide.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_conical_oxide.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 9: Ellipticity — all 3 designs combined
# ═══════════════════════════════════════════════════════════════════
def fig_ellipticity_combined():
    d1 = "2026-04-01_100348_ellipticity"
    d3 = "2026-04-01_122409_3h_ellipticity"
    de = "2026-04-01_153033_ext_ellipticity"

    c1, c2, c3 = cm.get_cmap(CMAP)(0.1), cm.get_cmap(CMAP)(0.5), cm.get_cmap(CMAP)(0.85)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    datasets = [(d1, c1, "1-hole", "o"), (d3, c2, "3-hole", "s"), (de, c3, "Extended", "^")]

    # Absolute Q
    for d, c, label, marker in datasets:
        e = _load(d, "ellipticities.npy")
        Qs = _load(d, "Qs.npy")
        ax1.plot(e, Qs, f"{marker}-", color=c, markersize=4, linewidth=1.8, label=label)
    ax1.set_xlabel("Ellipticity e", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=10)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.axvline(x=1.0, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    ax1.set_title("(a) Absolute Q", fontsize=12)

    # Normalized Q/Q(e=1)
    for d, c, label, marker in datasets:
        e = _load(d, "ellipticities.npy")
        Qs = _load(d, "Qs.npy")
        # Find Q at e=1.0 for normalization
        idx_1 = np.argmin(np.abs(e - 1.0))
        Q0 = Qs[idx_1]
        ax2.plot(e, Qs / Q0, f"{marker}-", color=c, markersize=4, linewidth=1.8, label=label)
    ax2.set_xlabel("Ellipticity e", fontsize=12)
    ax2.set_ylabel("Normalized $Q / Q(e{=}1)$", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.axvline(x=1.0, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    ax2.axhline(y=1.0, color="gray", linestyle=":", alpha=0.4, linewidth=1)
    ax2.set_title("(b) Fraction of circular-hole Q", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_ellipticity_combined.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_ellipticity_combined.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 10: Ellipticity+rotation heatmaps side by side
# ═══════════════════════════════════════════════════════════════════
def fig_ellipticity_rotation_heatmaps():
    dirs = [
        ("2026-04-01_103009_ellipticity_rotation", "1-hole"),
        ("2026-04-01_124108_3h_ellipticity_rotation", "3-hole"),
        ("2026-04-01_154537_ext_ellipticity_rotation", "Extended"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, (d, label) in zip(axes, dirs):
        Q_map = _load(d, "Q_map.npy")
        ells = _load(d, "ellipticities.npy")
        phis = _load(d, "phi_degs.npy")
        im = ax.imshow(Q_map, origin="lower", cmap=CMAP, aspect="auto",
                       extent=[phis[0], phis[-1], ells[0], ells[-1]])
        ax.set_xlabel("Rotation angle (°)", fontsize=11)
        ax.set_ylabel("Ellipticity", fontsize=11)
        ax.set_title(label, fontsize=12)
        ax.tick_params(labelsize=9)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cb.ax.tick_params(labelsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_ellipticity_rotation.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_ellipticity_rotation.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 11: Random oxide variation
# ═══════════════════════════════════════════════════════════════════
def fig_random_oxide():
    # sigma sweep
    ds = "2026-03-26_161619_random_oxide_sigma"
    sigma = _load(ds, "sigma_values.npy")
    Q_mean = _load(ds, "Q_mean.npy")
    Q_std = _load(ds, "Q_std.npy")
    Q_min = _load(ds, "Q_min.npy")
    Q_max = _load(ds, "Q_max.npy")

    # 2D
    d2 = "2026-03-27_003413_random_oxide_2d"
    t_ox = _load(d2, "t_ox_nm.npy")
    sigma_list = _load(d2, "sigma_list.npy")

    c_main = cm.get_cmap(CMAP)(0.3)
    colors2 = _colors(len(sigma_list))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Panel a: Q vs sigma
    ax1.plot(sigma, Q_mean, "o-", color=c_main, markersize=5, linewidth=2, label="Mean Q", zorder=3)
    ax1.fill_between(sigma, Q_min, Q_max, color=c_main, alpha=0.12, label="Min–Max")
    ax1.fill_between(sigma, Q_mean - Q_std, Q_mean + Q_std, color=c_main, alpha=0.25, label="±1σ")
    ax1.set_xlabel("Oxide roughness σ (nm)", fontsize=12)
    ax1.set_ylabel("Quality factor Q", fontsize=12)
    ax1.yaxis.set_major_formatter(fmt_Q)
    ax1.legend(fontsize=10)
    ax1.tick_params(labelsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title("(a) Q vs. oxide roughness", fontsize=12)

    # Panel b: Q vs t_ox at different sigmas
    for sig, c in zip(sigma_list, colors2):
        Qm = _load(d2, f"Q_mean_s{sig:.1f}.npy")
        Qs = _load(d2, f"Q_std_s{sig:.1f}.npy")
        ax2.plot(t_ox, Qm, "o-", color=c, markersize=3, linewidth=1.8, label=f"σ = {sig:.1f} nm")
        ax2.fill_between(t_ox, Qm - Qs, Qm + Qs, color=c, alpha=0.12)
    ax2.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax2.set_ylabel("Quality factor Q", fontsize=12)
    ax2.yaxis.set_major_formatter(fmt_Q)
    ax2.legend(fontsize=10)
    ax2.tick_params(labelsize=10)
    ax2.grid(alpha=0.3)
    ax2.set_title("(b) Q vs. oxide thickness", fontsize=12)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_random_oxide.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_random_oxide.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 12: dx shift + oxide
# ═══════════════════════════════════════════════════════════════════
def fig_dx_shift_oxide():
    d = "2026-03-17_171739_dx_shift_oxide_smallShift"
    t_ox = _load(d, "t_ox_nm.npy")
    dx_list = _load(d, "dx_list.npy")
    colors = _colors(len(dx_list))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for dx, c in zip(dx_list, colors):
        Qs = _load(d, f"Qs_dx{dx:.4f}.npy")
        ax.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.8, label=f"dx₁ = {dx:.4f}a")
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.yaxis.set_major_formatter(fmt_Q)
    ax.legend(fontsize=9, ncol=2)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_dx_shift_oxide.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_dx_shift_oxide.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 13: Extended radius+oxide
# ═══════════════════════════════════════════════════════════════════
def fig_ext_radius_oxide():
    d = "2026-03-24_193928_ext_radius_oxide"
    t_ox = _load(d, "t_ox_nm.npy")
    radii = [73, 74, 75, 76, 77]
    colors = _colors(len(radii))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for r, c in zip(radii, colors):
        Qs = _load(d, f"Qs_r{r}.npy")
        ax.plot(t_ox, Qs, "o-", color=c, markersize=3, linewidth=1.8, label=f"r = {r} nm")
    ax.set_xlabel("Oxide thickness (nm)", fontsize=12)
    ax.set_ylabel("Quality factor Q", fontsize=12)
    ax.yaxis.set_major_formatter(fmt_Q)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_ext_radius_oxide.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  fig_ext_radius_oxide.png")


# ═══════════════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating report figures...")
    fig_Q_vs_radius()
    fig_Q_vs_taper_combined()
    fig_Q_vs_taper_multiradius()
    fig_oxide_fixed_cr()
    fig_oxide_varying_cr()
    fig_oxide_all_designs()
    fig_piecewise_heatmaps()
    fig_conical_oxide()
    fig_ellipticity_combined()
    fig_ellipticity_rotation_heatmaps()
    fig_random_oxide()
    fig_dx_shift_oxide()
    fig_ext_radius_oxide()
    print("Done.")
