# generar_mapa_grande.py
# Genera un archivo "mapa_grande.txt" rectangular.
# Uso básico (sin args): python generar_mapa_grande.py  -> 1100x1100, densidad 0.10
# Opciones:
#   --rows/-r N       filas (default 1100)
#   --cols/-c N       columnas (default 1100)
#   --density/-d P    probabilidad de 'X' por celda [0..1] (default 0.10)
#   --seed S          semilla de aleatoriedad (default 42)
#   --tile-from PATH  hace "tiling" de un mapa base en vez de aleatorio
#   --tile-x TX       repeticiones horizontales al tilar (default 1)
#   --tile-y TY       repeticiones verticales al tilar (default 1)
#   --force           crea aunque exceda MAX_* (útil si recompilaste el C con -D)

import argparse, os, random, sys

def generar_aleatorio(rows, cols, density, seed, out_path):
    rng = random.Random(seed)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        for _ in range(rows):
            fila = "".join("X" if rng.random() < density else "." for _ in range(cols))
            f.write(fila + "\n")

def tilar_desde(path_in, tile_x, tile_y, out_path):
    with open(path_in, "r", encoding="utf-8") as f:
        base = [line.rstrip("\n") for line in f if line.rstrip("\n") != ""]
    if not base:
        raise SystemExit("El mapa base está vacío.")
    ancho = len(base[0])
    if any(len(l) != ancho for l in base):
        raise SystemExit("Todas las líneas del mapa base deben tener la misma longitud (rectangularidad).")
    with open(out_path, "w", encoding="utf-8", newline="\n") as out:
        for _ in range(tile_y):
            for linea in base:
                out.write(linea * tile_x + "\n")
    return len(base) * tile_y, ancho * tile_x

def main():
    p = argparse.ArgumentParser(description="Genera mapa_grande.txt para pruebas de rendimiento.")
    p.add_argument("--rows", "-r", type=int, default=1100)
    p.add_argument("--cols", "-c", type=int, default=1100)
    p.add_argument("--density", "-d", type=float, default=0.10)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--tile-from", type=str, default=None)
    p.add_argument("--tile-x", type=int, default=1)
    p.add_argument("--tile-y", type=int, default=1)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    out_path = "mapa_grande.txt"

    # Límites por defecto según tu programa C (puedes sobrescribirlos compilando con -D)
    max_filas = int(os.environ.get("MAX_FILAS", "1100"))
    max_cols  = int(os.environ.get("MAX_COLUMNAS", "1100"))

    if args.tile_from:
        filas = None
        cols = None
        # Calcular tamaño resultante del tiling
        with open(args.tile_from, "r", encoding="utf-8") as f:
            base = [line.rstrip("\n") for line in f if line.rstrip("\n") != ""]
        if not base:
            raise SystemExit("El mapa base está vacío.")
        ancho = len(base[0])
        if any(len(l) != ancho for l in base):
            raise SystemExit("Todas las líneas del mapa base deben tener la misma longitud.")
        filas = len(base) * args.tile_y
        cols  = ancho * args.tile_x
        if not args.force and (filas > max_filas or cols > max_cols):
            raise SystemExit(
                f"Tamaño {filas}x{cols} excede MAX_FILAS={max_filas}, MAX_COLUMNAS={max_cols}. "
                f"Recompila el C con -DMAX_FILAS y -DMAX_COLUMNAS o usa --force."
            )
        real_rows, real_cols = tilar_desde(args.tile_from, args.tile_x, args.tile_y, out_path)
        print(f"OK: {out_path} creado por tiling ({real_rows}x{real_cols}).")
    else:
        if not args.force and (args.rows > max_filas or args.cols > max_cols):
            raise SystemExit(
                f"Tamaño {args.rows}x{args.cols} excede MAX_FILAS={max_filas}, MAX_COLUMNAS={max_cols}. "
                f"Recompila el C con -DMAX_FILAS y -DMAX_COLUMNAS o usa --force."
            )
        if not (0.0 <= args.density <= 1.0):
            raise SystemExit("La densidad debe estar en [0, 1].")
        generar_aleatorio(args.rows, args.cols, args.density, args.seed, out_path)
        print(f"OK: {out_path} creado aleatoriamente ({args.rows}x{args.cols}), densidad X={args.density:.0%}, seed={args.seed}.")

if __name__ == "__main__":
    main()
