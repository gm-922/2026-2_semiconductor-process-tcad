# ==========================================
# S0 Grid Convergence Test
# ==========================================

# 1. Grid Definition

line x location=0.00<um> spacing=@grid_nm@<nm> tag=SiTop

line x location=0.05<um> spacing=@grid_nm@<nm>

line x location=0.25<um> spacing=@grid_nm@<nm>

line x location=0.45<um> spacing=@grid_nm@<nm>

line x location=0.80<um> spacing=@grid_nm@<nm>

line x location=1.20<um> spacing=10<nm>

line x location=2.00<um> spacing=20<nm> tag=SiBottom

# 2. Silicon Region

region Silicon xlo=SiTop xhi=SiBottom


# 3. Silicon Substrate Initialization

init concentration=1.0e15<cm-3> field=Phosphorus wafer.orient=100

# 4. Boron Ion Implantation

implant Boron \
    dose=1.0e12<cm-2> \
    energy=80<keV> \
    tilt=7<degree> \
    rotation=22<degree>

# ==========================================
# 5. Save Simulation Results
# ==========================================

# Boron Concentration Profile
SetPlxList {BTotal}

WritePlx n@node@_S0_asimpl.plx Silicon

# Save Structure and Mesh
struct tdr=n@node@_S0_asimpl

exit
