import subprocess
import os
import re
import shutil

LIBS_DIR = os.path.expanduser("~/kicad-libs")
TEMP_DIR = os.path.expanduser("~/kicad-libs-temp")

CATEGORIES = {
    "1": "ics",
    "2": "regulators",
    "3": "connectors",
    "4": "microcontrollers",
    "5": "passives",
    "6": "transistors",
}

def merge_sym(target, source):
    with open(target, 'r') as f:
        existing = f.read()
    with open(source, 'r') as f:
        new = f.read()
    existing_names = re.findall(r'\(symbol "([^"]+)"', existing)
    new_symbols = re.findall(r'\(symbol "[^"]+".+?^\)', new, re.DOTALL | re.MULTILINE)
    for sym in new_symbols:
        name = re.search(r'\(symbol "([^"]+)"', sym).group(1)
        if name not in existing_names:
            existing = existing.rstrip().rstrip(')')
            existing += '\n  ' + sym + '\n)\n'
            print(f"  ✓ Dodano symbol: {name}")
        else:
            print(f"  ~ Pominięto (już istnieje): {name}")
    with open(target, 'w') as f:
        f.write(existing)

def main():
    print("=== Dodawanie komponentu z LCSC ===\n")
    lcsc = input("Podaj numer LCSC (np. C427537): ").strip()
    print("\nKategoria:")
    for k, v in CATEGORIES.items():
        print(f"  {k}. {v}")
    cat_num = input("Wybierz kategorię (1-6): ").strip()
    category = CATEGORIES.get(cat_num, "ics")
    print(f"\nPobieram {lcsc}...")
    temp = os.path.join(TEMP_DIR, lcsc)
    subprocess.run(["JLC2KiCadLib", lcsc, "-dir", temp], check=True)
    sym_src = os.path.join(temp, "symbol")
    sym_dst = os.path.join(LIBS_DIR, "symbols", f"{category}.kicad_sym")
    sym_files = [f for f in os.listdir(sym_src) if f.endswith(".kicad_sym")]
    if sym_files:
        src_path = os.path.join(sym_src, sym_files[0])
        if os.path.exists(sym_dst):
            merge_sym(sym_dst, src_path)
        else:
            shutil.copy(src_path, sym_dst)
            print(f"  ✓ Utworzono nową bibliotekę: {category}.kicad_sym")
    fp_src = os.path.join(temp, "footprint")
    fp_dst = os.path.join(LIBS_DIR, "footprints", f"{category}.pretty")
    for f in os.listdir(fp_src):
        if f.endswith(".kicad_mod"):
            shutil.copy(os.path.join(fp_src, f), fp_dst)
            print(f"  ✓ Footprint: {f}")
    models_src = os.path.join(fp_src, "packages3d")
    models_dst = os.path.join(LIBS_DIR, "3dmodels", category)
    if os.path.exists(models_src):
        for f in os.listdir(models_src):
            if f.endswith(".step"):
                shutil.copy(os.path.join(models_src, f), models_dst)
                print(f"  ✓ Model 3D: {f}")
    shutil.rmtree(TEMP_DIR)
    print(f"\nGotowe! Komponent {lcsc} dodany do kategorii '{category}'.")

if __name__ == "__main__":
    main()
