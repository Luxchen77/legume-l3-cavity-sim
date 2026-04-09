# Instructions: Generate a LaTeX/PDF Report of GaAs L3 Photonic Crystal Cavity Simulation Results

## Purpose

Create a professional LaTeX document (compiled to PDF) that summarizes **all** simulation results for GaAs L3 photonic crystal cavities. The report should be self-contained: a reader unfamiliar with the project should understand the physical system, the design choices, and the motivation behind each simulation sweep. The target audience is a physicist or engineer working in nanophotonics.

---

## System Under Study

The system is a **GaAs air-bridge L3 photonic crystal cavity** — three missing holes in a row within a triangular lattice of air holes etched through a GaAs slab.

Baseline parameters (use throughout unless a sweep explicitly varies them):

| Parameter | Symbol | Value |
|---|---|---|
| Lattice constant | $a$ | 250 nm |
| Hole radius | $r$ | 75 nm (i.e. $r/a = 0.3$) |
| Slab thickness | $d$ | 170 nm |
| Refractive index (GaAs) | $n$ | 3.3737 |
| Resonance wavelength (approx.) | $\lambda_0$ | ~970 nm |

---

## Cavity Designs

Three optimization levels exist. **Explain each clearly in the report**, including a schematic or diagram of the L3 cavity with the shifted holes highlighted.

### 1. 1-Hole Optimized (S1 only)

- Only the end-hole pair (nearest neighbors along the cavity axis) is shifted outward.
- Shift: $\mathrm{dx}_1 = 0.17964\,a$ (≈ 44.9 nm)
- Theoretical Q: **~200,000**
- This is a simple, well-known optimization originally proposed by Akahane et al. (2003).

### 2. 3-Hole Optimized (S1, S2, S3)

- The three nearest end-hole pairs along the cavity axis are shifted.
- Shifts: $\mathrm{dx}_1 = 0.27239\,a$, $\mathrm{dx}_2 = 0.21982\,a$, $\mathrm{dx}_3 = 0.00000\,a$
- Theoretical Q: **~1.44 × 10⁶**
- Found via global optimization (genetic algorithm / particle swarm), following Minkov & Savona (2014). The key insight is that exhaustive global search finds configurations far from the local optima found by sequential single-parameter sweeps.

### 3. Extended Areal Optimization

- Shifts applied to a larger neighborhood: row-0 neighbors plus rows 1–2 (both dx and dy shifts, and possibly dr for some holes).
- Theoretical Q: **~43.7 × 10⁶**
- This figure is **unrealistic experimentally** due to fabrication disorder limits (literature consistently shows $Q_{\mathrm{exp}} \lesssim 5 \times 10^6$ even for the best Si cavities). The extended design is retained as a **sensitivity canary** — its extreme sensitivity to geometric perturbations makes it a powerful probe for detecting small fabrication imperfections.

**In the report:** Include a table comparing the three designs side-by-side (shifts, Q, number of degrees of freedom). Explain why higher Q designs are more sensitive to fabrication errors, referencing the disorder analysis formula:

$$\frac{1}{Q_{\mathrm{exp}}} = \frac{1}{Q_{\mathrm{design}}} + \frac{1}{Q_{\mathrm{disorder}}} + \frac{1}{Q_{\mathrm{absorption}}}$$

When $Q_{\mathrm{design}} \gg Q_{\mathrm{disorder}}$, the measured Q is dominated by disorder and becomes design-independent. The different optimization levels thus probe different regimes.

---

## Simulation Sweeps to Include

The simulation results PDF (`Plots_L3_SimulationResults_pdf.pdf`) contains plots for several parameter sweeps. **Extract and present ALL data from this PDF.** The plots are images — describe the trends quantitatively, and recreate the key data in tables and/or pgfplots figures within LaTeX.

### Sweep 1: Q vs. Hole Radius (varying r)

- **Parameters varied:** $r = 72$–$78$ nm in 1 nm steps (or as available), at fixed $a = 250$ nm
- **Designs:** 1-hole optimized and 3-hole optimized
- **What to show:** Q factor and resonance wavelength $\lambda_0$ as functions of $r$
- **What to explain:**
  - The Q(r) curve has a sharp peak at the optimal radius. The peak position and width differ between designs.
  - The 3-hole optimized design has a much sharper peak — Q drops to ~1/3 for $\pm 2$ nm deviation from optimum. This sharpness is the price of high optimization.
  - The wavelength shifts approximately linearly with radius (~several nm per nm of $\Delta r$), providing an independent handle on the actual fabricated radius.
  - **Physics:** Changing $r$ shifts the photonic bandgap and alters the mode profile. The optimized hole shifts were computed for a specific $r$; deviating from it breaks the delicate far-field cancellation.

### Sweep 2: Q vs. Sidewall Taper Angle

- **Parameters varied:** Taper angle $\theta = 0°$–$5°$ (or as available), at several radii
- **Designs:** 1-hole optimized (shown for multiple radii)
- **What to show:** Q factor and resonance wavelength vs. taper angle
- **What to explain:**
  - Even a 2° taper drops Q by more than half. At 5°, Q is reduced to ~10–15% of the ideal value regardless of radius.
  - The wavelength **redshifts** with increasing taper (~4 nm/degree) — this is because the tapered holes have less air, increasing the effective index.
  - All radius curves converge at large taper angles, meaning taper becomes the dominant loss mechanism.
  - **Physics:** Taper breaks the vertical mirror symmetry of the slab, coupling the TE-like cavity mode to TM-like radiation modes. This is an out-of-plane loss channel. Include the formula for how the conical hole shape is parameterized (top radius vs. bottom radius as a function of $\theta$ and slab thickness).

### Sweep 3: Q vs. Oxide Thickness (fixed consumption ratio)

- **Parameters varied:** Oxide thickness 0–10 nm, at consumption ratio $c_r = 0.5$
- **Designs:** 3-hole optimized, at multiple radii ($r = 73$–$77$ nm)
- **What to show:** Q factor and resonance wavelength vs. oxide thickness
- **What to explain:**
  - At $c_r = 0.5$, the oxide grows both inward (consuming GaAs) and outward. The net effect depends on the starting radius relative to the optimum.
  - For $r = 73$ nm (near the 3-hole optimum): Q stays high (~1.4M) up to ~3–4 nm oxide, then drops.
  - For $r = 77$ nm: Q starts lower (~750k) and collapses to near zero by 8 nm oxide.
  - Wavelength blueshifts linearly at ~3–4 nm per nm of oxide (at $c_r = 0.5$).
  - **Physics:** The oxide layer does three things simultaneously: (1) if it consumes GaAs ($c_r > 0$), the effective hole radius increases, shifting the cavity away from its optimum; (2) the slab thins; (3) a low-index dielectric layer ($n_{\mathrm{oxide}} \approx 1.6$–$1.8$) replaces either GaAs (inward) or air (outward), modifying the effective index.

  Define the consumption ratio clearly:
  $$c_r = \frac{t_{\mathrm{consumed\;GaAs}}}{t_{\mathrm{total\;oxide}}}$$
  where $c_r = 0$ means pure outward growth (no GaAs removed), $c_r = 1$ means pure inward growth (all oxide replaces GaAs).

### Sweep 4: Q vs. Oxide Thickness (varying consumption ratio)

- **Parameters varied:** Oxide thickness 0–10 nm, at multiple $c_r = 0.0, 0.2, 0.4, 0.6, 0.8, 1.0$
- **Designs:** 3-hole optimized, at $r = 75$ nm (or as available)
- **What to show:** Q factor and resonance wavelength vs. oxide thickness, parametrized by $c_r$
- **What to explain:**
  - At $c_r = 0$ (pure outward growth): Q **increases slightly** — the gradual index transition acts as an anti-reflection coating on each hole, smoothing the Fourier components of the mode and reducing leaky components. This is the "index smoothing" effect.
  - At $c_r = 1$ (pure consumption): Q drops catastrophically because the carefully optimized hole geometry is destroyed.
  - Intermediate $c_r$ values interpolate smoothly between these extremes.
  - The wavelength shift rate increases with $c_r$ because more GaAs is replaced by lower-index oxide.
  - **This is the key diagnostic plot for the characterization chip**: by comparing measured Q and $\lambda_0$ changes after oxidation against these simulation curves, the consumption ratio can be extracted.

### Sweep 5: Q vs. Number of PhC Rows (d)

- **Parameters varied:** $d = 7$–$12$ rows (number of periodic lattice rows surrounding the cavity)
- **Designs:** 1-hole and/or 3-hole optimized
- **What to show:** Q factor vs. number of rows
- **What to explain:**
  - Q increases with $d$ and saturates. The saturation level gives the out-of-plane (vertical) Q, $Q_\perp$. The increase at small $d$ is due to in-plane leakage through the finite photonic crystal.
  - The total Q is: $\frac{1}{Q_{\mathrm{total}}} = \frac{1}{Q_\perp} + \frac{1}{Q_\parallel(d)}$
  - where $Q_\parallel(d)$ increases exponentially with $d$ (evanescent decay through the PhC mirror).
  - This sweep lets you decouple in-plane vs. out-of-plane losses experimentally. On the characterization chip, the row sweep is crucial because sidewall taper primarily affects $Q_\perp$ while disorder affects both, so comparing the $d$-dependence against simulation reveals which loss channel dominates.

### (Optional) Sweep 6: Lattice Constant Sweep

- If data exists for varying $a$ while keeping $r/a$ constant, include it.
- Explain that Q should be invariant under spatial rescaling (all lengths scale together), so any Q variation with $a$ at fixed $r/a$ indicates feature-size-dependent fabrication effects.

---

## Report Structure

Use the following structure for the LaTeX document:

1. **Title page** — "Simulation Results: GaAs L3 Photonic Crystal Cavity Design and Characterization" with author name and date
2. **Abstract** — 1 paragraph summarizing the project scope, key results, and purpose (designing a characterization chip)
3. **Introduction** — Brief background on PhC cavities, Q factor optimization, and the L3 cavity. Cite the key references: Akahane et al. (2003), Minkov & Savona (2014), Vasco & Gerace (encapsulated Si optimization), Asano/Takahashi/Noda (fabrication and characterization). Explain the GaAs platform and why it differs from Si.
4. **Cavity Design** — Describe the three optimization levels with schematics, tables of hole shifts, and the baseline parameters.
5. **Simulation Results** — One subsection per sweep (radius, taper, oxide at fixed $c_r$, oxide at varying $c_r$, row number). Each subsection should have:
   - A brief statement of what was varied and why
   - The key figure(s) — either reproduced from the simulation data or described in detail
   - A table of representative numerical values
   - A discussion of the physical interpretation
6. **Implications for Chip Design** — Summarize how the simulation results inform the characterization chip layout:
   - Radius sweep ($r = 72$–$78$ nm) maps the Q(r) curve and serves as an "oxidation ruler"
   - Row number sweep ($d = 7$–$12$) decouples in-plane vs. out-of-plane losses
   - Pairing 1-hole and 3-hole designs at each point creates a differential probe (the ratio $Q_{\mathrm{3-hole}}/Q_{\mathrm{1-hole}}$ distinguishes taper from consumption from disorder)
   - Extended design at $r = 74, 75, 76$ nm as a sensitivity canary
   - Two identical chips from same wafer: one passivated, one unpassivated (tracks native oxide growth over time)
7. **Conclusion**
8. **References**

---

## Formatting Requirements

- Use `article` document class, 11pt, A4 paper
- Use `siunitx` for all quantities with units
- Use `booktabs` for tables
- Use `pgfplots` or included graphics for figures
- Use `amsmath` for equations
- Number all equations, figures, and tables
- Cross-reference everything
- Keep the tone technical but accessible — a new group member should be able to understand the document

---

## Data Extraction Instructions

The simulation data lives in the project knowledge as:

1. **`Plots_L3_SimulationResults_pdf.pdf`** — Contains the actual simulation plots (5 pages of figures). These are images of matplotlib-style plots. Read them carefully and extract:
   - Axis labels, ranges, and scales
   - All curve labels (which radius, which design, which $c_r$)
   - Approximate numerical values at key points (peak Q, Q at boundary radii, wavelength values)
   - Any trends or features (crossings, plateaus, collapses)

2. **Project knowledge papers** — The three reference papers provide context on optimization methods and experimental validation:
   - Minkov & Savona (2014) — "Automated optimization of photonic crystal slab cavities"
   - Vasco & Gerace — "Global optimization of an encapsulated Si L3 cavity"
   - Asano, Takahashi, Noda (2021) — "Fabrication and characterization of an L3 nanocavity"

3. **Conversation history / memory** — Contains the specific design parameters (hole shifts, Q values, chip design strategy). Key facts:
   - 1-hole optimized: $\mathrm{dx}_1 = 0.17964a$, Q ~ 200k
   - 3-hole optimized: $\mathrm{dx}_1 = 0.27239a$, $\mathrm{dx}_2 = 0.21982a$, $\mathrm{dx}_3 = 0.00000a$, Q ~ 1.44M
   - Extended: Q ~ 43.7M (theoretical only, unrealistic experimentally)
   - Chip strategy: radius sweep r = 72–78 nm, row sweep d = 7–12, two chips (passivated + unpassivated), extended design only at r = 74, 75, 76 nm

---

## What NOT to Do

- Do not invent data. If a specific numerical value cannot be read from the plots, say "approximately" and give the range.
- Do not omit any sweep that has data in the PDF — include all of them.
- Do not write a generic photonic crystal review. The report should be focused specifically on **our** GaAs L3 simulations and their implications for **our** characterization chip.
- Do not forget to explain the physical motivation for each sweep — the "why" matters as much as the "what."
- Do not use the word "we" inconsistently — use "we" throughout (it's a research report, not a textbook).

---

## Compile Instructions

Compile with `pdflatex` (two passes for cross-references). If `pgfplots` figures are generated, ensure they compile correctly. If images from the simulation PDF need to be included directly, extract them as PNGs and use `\includegraphics`.
