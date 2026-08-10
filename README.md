# KiCad Personal Library

Personal KiCad component library with JLCPCB design rules and project templates.

## Library Structure

```
kicad-libs/
├── symbols/              # Schematic symbols (.kicad_sym)
├── footprints/           # PCB footprints (.pretty folders)
│   ├── regulators.pretty
│   ├── connectors.pretty
│   ├── microcontrollers.pretty
│   ├── passives.pretty
│   ├── transistors.pretty
│   └── ics.pretty
├── 3dmodels/             # 3D models (.step files)
│   ├── regulators/
│   ├── connectors/
│   ├── microcontrollers/
│   ├── passives/
│   ├── transistors/
│   └── ics/
├── rules/                # DRC rules for manufacturers
│   └── jlcpcb.kicad_dru
└── templates/            # KiCad project templates
    └── JLCPCB/           # JLCPCB 2-layer template
```

## Requirements

- KiCad 10.x
- Python 3 + pip (for adding components via JLC2KiCadLib)
- Git

---

## Setup on a New Computer

### 1. Install KiCad 10

```bash
sudo add-apt-repository ppa:kicad/kicad-10.0-releases
sudo apt update
sudo apt install kicad
```

### 2. Clone this repository

```bash
git clone https://github.com/DawidGurdzinski2/kicad-libs.git ~/kicad-libs
```

### 3. Install JLC2KiCadLib (for adding new components)

```bash
pip install JLC2KiCadLib --break-system-packages
```

### 4. Configure KiCad paths

Open KiCad → **Preferences → Configure Paths** → click **+** and add:

| Name | Path |
|------|------|
| `MY_LIBS` | `/home/YOUR_USERNAME/kicad-libs` |
| `KICAD_USER_TEMPLATE_DIR` | `/home/YOUR_USERNAME/kicad-libs/templates` |

> Replace `YOUR_USERNAME` with your Linux username (`whoami` to check).

### 5. Add Symbol Libraries

Open KiCad → **Preferences → Manage Symbol Libraries** → **Global** tab → click **+** for each:

| Nickname | Path | Plugin Type |
|----------|------|-------------|
| `MyLib_Regulators` | `${MY_LIBS}/symbols/regulators.kicad_sym` | KiCad |
| `MyLib_Connectors` | `${MY_LIBS}/symbols/connectors.kicad_sym` | KiCad |
| `MyLib_MCU` | `${MY_LIBS}/symbols/microcontrollers.kicad_sym` | KiCad |
| `MyLib_Passives` | `${MY_LIBS}/symbols/passives.kicad_sym` | KiCad |
| `MyLib_Transistors` | `${MY_LIBS}/symbols/transistors.kicad_sym` | KiCad |
| `MyLib_ICs` | `${MY_LIBS}/symbols/ics.kicad_sym` | KiCad |

### 6. Add Footprint Libraries

Open **Footprint Editor** → **Preferences → Manage Footprint Libraries** → **Global** tab → click **+** for each:

| Nickname | Path | Plugin Type |
|----------|------|-------------|
| `MyLib_Regulators` | `${MY_LIBS}/footprints/regulators.pretty` | KiCad |
| `MyLib_Connectors` | `${MY_LIBS}/footprints/connectors.pretty` | KiCad |
| `MyLib_MCU` | `${MY_LIBS}/footprints/microcontrollers.pretty` | KiCad |
| `MyLib_Passives` | `${MY_LIBS}/footprints/passives.pretty` | KiCad |
| `MyLib_Transistors` | `${MY_LIBS}/footprints/transistors.pretty` | KiCad |
| `MyLib_ICs` | `${MY_LIBS}/footprints/ics.pretty` | KiCad |

---

## Starting a New Project with JLCPCB Template

1. Open KiCad → **File → New Project from Template**
2. Select **User Templates** tab
3. Choose **JLCPCB** → enter project name → OK

The project will have JLCPCB design rules pre-loaded.

---

## Adding a New Component from JLCPCB/LCSC

1. Find the component on [lcsc.com](https://lcsc.com) and copy the **LCSC number** (e.g. `C6187`)

2. Download symbol + footprint + 3D model:
```bash
JLC2KiCadLib C6187 -dir ~/kicad-libs-temp
```

3. Check what was downloaded:
```bash
find ~/kicad-libs-temp -type f
```

4. Copy files to the correct category (example for a regulator):
```bash
cp ~/kicad-libs-temp/symbol/*.kicad_sym ~/kicad-libs/symbols/regulators.kicad_sym
cp ~/kicad-libs-temp/footprint/*.kicad_mod ~/kicad-libs/footprints/regulators.pretty/
cp ~/kicad-libs-temp/footprint/packages3d/*.step ~/kicad-libs/3dmodels/regulators/
```

5. Clean up temp folder:
```bash
rm -rf ~/kicad-libs-temp
```

6. Push to GitHub:
```bash
cd ~/kicad-libs
git add .
git commit -m "add: component name"
git push
```

### Category mapping

| Component type | Symbol file | Footprint folder |
|---------------|-------------|-----------------|
| Voltage regulators, LDOs | `symbols/regulators.kicad_sym` | `footprints/regulators.pretty` |
| Connectors, headers, USB | `symbols/connectors.kicad_sym` | `footprints/connectors.pretty` |
| MCUs, microcontrollers | `symbols/microcontrollers.kicad_sym` | `footprints/microcontrollers.pretty` |
| Resistors, capacitors, inductors | `symbols/passives.kicad_sym` | `footprints/passives.pretty` |
| MOSFETs, BJTs | `symbols/transistors.kicad_sym` | `footprints/transistors.pretty` |
| ICs, sensors, drivers | `symbols/ics.kicad_sym` | `footprints/ics.pretty` |

---

## Using a Component in Schematic

1. Open **Schematic Editor** → press **A** (Add Symbol)
2. Search for the component name (e.g. `ACS758`)
3. Select it from `MyLib_ICs` → place on schematic

> **Important:** After placing, double-click the symbol and check the **Footprint** field.
> It should read `MyLib_ICs:footprint-name`, not `footprint:footprint-name`.
> Fix it manually if needed before updating the PCB.

---

## JLCPCB Design Rules (2-layer, 1oz copper)

| Parameter | Value |
|-----------|-------|
| Min track width | 0.127mm |
| Min clearance | 0.127mm |
| Min via hole | 0.3mm |
| Min via diameter | 0.56mm |
| Min drill hole | 0.3mm |
| Hole to hole clearance | 0.5mm |
| Copper to edge clearance | 0.3mm |
| Min silkscreen text height | 1.0mm |
| Min silkscreen line width | 0.15mm |

Run DRC: **Inspect → Design Rules Checker → Run DRC**
