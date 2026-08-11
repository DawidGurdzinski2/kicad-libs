# KiCad Personal Library

Personal KiCad component library with JLCPCB design rules, project templates, and automation scripts.

---

## Step 1 — Install KiCad 10

Open a terminal (`Ctrl+Alt+T`) and run these commands one by one:

```bash
sudo add-apt-repository ppa:kicad/kicad-10.0-releases
sudo apt update
sudo apt install kicad
```

When prompted with `[y/n]` press `y` and Enter. Installation may take a few minutes.

After installation, open KiCad from your app menu or by typing `kicad` in the terminal.

---

## Step 2 — Install required tools

In the terminal run:

```bash
pip install JLC2KiCadLib --break-system-packages
```

This installs the tool that downloads component symbols, footprints and 3D models from LCSC automatically.

---

## Step 3 — Install KiCad plugins

Open KiCad (the main window, not the schematic or PCB editor).

1. Click **Tools → Plugin and Content Manager (PCM)**
2. Click **Refresh** to load the plugin list
3. Search for and install each of these:

| Plugin | What it does |
|--------|-------------|
| **Fabrication Toolkit** | One-click export of Gerber, BOM, CPL files ready for JLCPCB upload |
| **InteractiveHtmlBom** | Generates an interactive HTML BOM useful for manual soldering |

To install: click the plugin name → click **Install** → click **Apply Pending Changes**.

---

## Step 4 — Clone this repository

In the terminal run:

```bash
git clone https://github.com/DawidGurdzinski2/kicad-libs.git ~/kicad-libs
```

This creates a folder `~/kicad-libs` with all the library files. If you don't have git installed:

```bash
sudo apt install git
```

---

## Step 5 — Configure KiCad paths

This tells KiCad where your library folder is. You only do this once per computer.

1. Open KiCad main window
2. Click **Preferences → Configure Paths**
3. Click the **+** button to add a new entry
4. Fill in:
   - **Name:** `MY_LIBS`
   - **Path:** `/home/YOUR_USERNAME/kicad-libs`
5. Click **+** again and add:
   - **Name:** `KICAD_USER_TEMPLATE_DIR`
   - **Path:** `/home/YOUR_USERNAME/kicad-libs/templates`
6. Click **OK**

> To find your username, run `whoami` in the terminal. For example if it prints `dawid`, your path is `/home/dawid/kicad-libs`.

---

## Step 6 — Add Symbol Libraries

This tells KiCad where your schematic symbols are.

1. Open KiCad main window
2. Click **Preferences → Manage Symbol Libraries**
3. Click the **Global** tab
4. Click **+** at the bottom to add a new row
5. Fill in the **Nickname** and **Library Path** columns, set **Plugin Type** to `KiCad`
6. Repeat for each row in the table below:

| Nickname | Library Path | Plugin Type |
|----------|-------------|-------------|
| `MyLib_ICs` | `${MY_LIBS}/symbols/ics.kicad_sym` | KiCad |
| `MyLib_Regulators` | `${MY_LIBS}/symbols/regulators.kicad_sym` | KiCad |
| `MyLib_Connectors` | `${MY_LIBS}/symbols/connectors.kicad_sym` | KiCad |
| `MyLib_MCU` | `${MY_LIBS}/symbols/microcontrollers.kicad_sym` | KiCad |
| `MyLib_Passives` | `${MY_LIBS}/symbols/passives.kicad_sym` | KiCad |
| `MyLib_Transistors` | `${MY_LIBS}/symbols/transistors.kicad_sym` | KiCad |

7. Click **OK**

---

## Step 7 — Add Footprint Libraries

This tells KiCad where your PCB footprints are. This is done in the Footprint Editor, not the main window.

1. From KiCad main window, click **Footprint Editor** (or open any PCB project and go to **Preferences → Manage Footprint Libraries**)
2. Click **Preferences → Manage Footprint Libraries**
3. Click the **Global** tab
4. Click **+** and add each row below, setting **Plugin Type** to `KiCad`:

| Nickname | Library Path | Plugin Type |
|----------|-------------|-------------|
| `MyLib_ICs` | `${MY_LIBS}/footprints/ics.pretty` | KiCad |
| `MyLib_Regulators` | `${MY_LIBS}/footprints/regulators.pretty` | KiCad |
| `MyLib_Connectors` | `${MY_LIBS}/footprints/connectors.pretty` | KiCad |
| `MyLib_MCU` | `${MY_LIBS}/footprints/microcontrollers.pretty` | KiCad |
| `MyLib_Passives` | `${MY_LIBS}/footprints/passives.pretty` | KiCad |
| `MyLib_Transistors` | `${MY_LIBS}/footprints/transistors.pretty` | KiCad |

5. Click **OK**

---

## Step 8 — Start a new project with JLCPCB template

Every time you start a new PCB project, use this template so JLCPCB design rules are loaded automatically.

1. Open KiCad main window
2. Click **File → New Project from Template**
3. Click the **User Templates** tab
4. Select **JLCPCB**
5. Click **OK**, choose a folder and name for your project

Your project now has JLCPCB constraints built in. To check your design against these rules at any time, open the PCB Editor and go to **Inspect → Design Rules Checker → Run DRC**.

---

## Adding a new component from LCSC

### 1. Find the LCSC number

1. Go to [lcsc.com](https://lcsc.com)
2. Search for your component (e.g. `AMS1117 3.3`)
3. Open the component page
4. Copy the **LCSC number** — it starts with `C` followed by digits, e.g. `C6187`

### 2. Run the add script

In the terminal:

```bash
python3 ~/kicad-libs/add_component.py
```

The script will ask:
1. **LCSC number** — paste the number you copied (e.g. `C6187`)
2. **Category** — pick the right one from the list (see category table below)

It will automatically download the symbol, footprint and 3D model, and add them to the library without overwriting existing components.

### 3. Restart KiCad

Close and reopen KiCad so it picks up the new component.

### 4. Push to GitHub

```bash
cd ~/kicad-libs && git add . && git commit -m "add: component name" && git push
```

### On a new computer — get latest library

```bash
cd ~/kicad-libs && git pull
```

Then restart KiCad.

---

## Category reference

| Component type | Category to pick |
|---------------|----------|
| ICs, sensors, drivers, current sensors | `1. ics` |
| Voltage regulators, LDOs | `2. regulators` |
| Connectors, headers, USB, JST | `3. connectors` |
| MCUs, microcontrollers (STM32, ESP32 etc.) | `4. microcontrollers` |
| Resistors, capacitors, inductors | `5. passives` |
| MOSFETs, BJTs, transistors | `6. transistors` |

---

## Using a component in Schematic Editor

1. Open Schematic Editor
2. Press **A** — the Add Symbol window opens
3. Type the component name in the search box (e.g. `ACS758`)
4. Find it under `MyLib_ICs` (or whichever category you added it to)
5. Click **OK** and click on the schematic to place it

> **Important:** After placing the component, double-click it and check the **Footprint** field. It should start with `MyLib_ICs:` (or the correct category). If it says `footprint:` instead, change it manually to the correct library nickname.

---

## Useful keyboard shortcuts — Schematic Editor

| Key | Action |
|-----|--------|
| `A` | Add symbol |
| `W` | Draw wire |
| `P` | Add power symbol (GND, VCC etc.) |
| `L` | Add net label |
| `E` | Edit properties |
| `R` | Rotate |
| `G` | Drag (keeps connections) |
| `M` | Move |
| `Del` | Delete |
| `Ctrl+Z` | Undo |
| `Ctrl+S` | Save |

---

## JLCPCB Design Rules — 2-layer, 1oz copper

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

Run DRC: open PCB Editor → **Inspect → Design Rules Checker → Run DRC**
