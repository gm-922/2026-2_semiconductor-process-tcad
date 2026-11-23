# SIM-000 — 2 nm reference grid for as-implanted B profiles
# Selected using 20 / 80 / 170 keV output convergence comparison on 2026-11-23.
# This is a reusable GRID FRAGMENT, not a complete runnable Sentaurus deck.
# Si 0~0.80 um: 2 nm; progressively coarser thereafter.
# RTA diffusion convergence has NOT been validated.

line x location=0.00<um> spacing=2<nm> tag=SiTop
line x location=0.05<um> spacing=2<nm>
line x location=0.25<um> spacing=2<nm>
line x location=0.45<um> spacing=2<nm>
line x location=0.80<um> spacing=2<nm>
line x location=1.20<um> spacing=10<nm>
line x location=2.00<um> spacing=20<nm> tag=SiBottom
region Silicon xlo=SiTop xhi=SiBottom
