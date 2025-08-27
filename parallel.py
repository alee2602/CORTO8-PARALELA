
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import ceil
import os
import time
import sys

FILENAME = "mapa_grande.txt"
MAX_FILAS = 1100
MAX_COLUMNAS = 1100

def leer_mapa(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lineas = []
            for idx, raw in enumerate(f):
                if idx >= MAX_FILAS:
                    break
                linea = raw.rstrip("\n")
                # recortar si supera MAX_COLUMNAS
                if len(linea) > MAX_COLUMNAS:
                    linea = linea[:MAX_COLUMNAS]
                lineas.append(linea)
            return lineas
    except FileNotFoundError:
        print("Error: no se pudo abrir", path)
        sys.exit(1)

def contar_en_bloque(bloque, worker_id):
    # Cuenta 'X' en un bloque de filas. Retorna (id, conteo_local)
    contador_local = 0
    for fila in bloque:
        contador_local += fila.count('X')
    msg = f"Hilo {worker_id} encontró {contador_local} tesoros en su sección."
    return worker_id, contador_local, msg

def dividir_en_bloques(filas, num_workers):
    n = len(filas)
    if n == 0:
        return []
    tam = ceil(n / num_workers)
    bloques = []
    start = 0
    worker_id = 0
    while start < n:
        bloques.append((filas[start:start+tam], worker_id))
        start += tam
        worker_id += 1
    return bloques

def main():
    mapa = leer_mapa(FILENAME)
    filas = len(mapa)
    columnas = max((len(s) for s in mapa), default=0)

    # Número de procesos (como "num_hilos" en OpenMP).
    num_workers = os.cpu_count() or 1

    inicio = time.perf_counter()

    # Partimos el trabajo por bloques de filas
    bloques = dividir_en_bloques(mapa, num_workers)

    contador_total = 0
    mensajes = []
    # Ejecutamos en paralelo
    with ProcessPoolExecutor(max_workers=num_workers) as ex:
        futuros = [ex.submit(contar_en_bloque, bloque, wid) for (bloque, wid) in bloques]
        for fut in as_completed(futuros):
            wid, local_count, msg = fut.result()
            contador_total += local_count
            mensajes.append((wid, msg))

    fin = time.perf_counter()

    for _, msg in sorted(mensajes, key=lambda x: x[0]):
        print(msg)

    print(f"\nParalelo: Total de tesoros = {contador_total}")
    print(f"Cores utilizados: {num_workers}")
    print(f"Tiempo de ejecucion: {fin - inicio:.6f} segundos")
    print(f"Filas leídas: {filas}, Columnas (máx por fila): {columnas}")

if __name__ == "__main__":
    main()
