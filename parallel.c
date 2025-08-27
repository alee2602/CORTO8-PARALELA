#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#ifndef MAX_FILAS
#define MAX_FILAS 1100
#endif
#ifndef MAX_COLUMNAS
#define MAX_COLUMNAS 1100
#endif

static char mapa[MAX_FILAS][MAX_COLUMNAS];
static int ancho_fila[MAX_FILAS];

int main() {
    int filas = 0;
    int i, j;
    int contador_total = 0;
    int num_hilos = 0;
    double inicio, fin;

    FILE *archivo = fopen("mapa_grande.txt", "r");
    if (!archivo) { printf("Error: no se pudo abrir mapa_grande.txt\n"); return 1; }

    char linea[MAX_COLUMNAS + 2];
    while (filas < MAX_FILAS && fgets(linea, sizeof(linea), archivo)) {
        linea[strcspn(linea, "\n")] = '\0';
        int columnas_leidas = (int)strlen(linea);
        if (columnas_leidas > MAX_COLUMNAS) columnas_leidas = MAX_COLUMNAS; // <-- tope

        for (j = 0; j < columnas_leidas; j++) {
            mapa[filas][j] = linea[j];
        }
        for (j = columnas_leidas; j < MAX_COLUMNAS; j++) {
            mapa[filas][j] = 0;
        }

        ancho_fila[filas] = columnas_leidas; 
        filas++;
    }
    fclose(archivo);

    inicio = omp_get_wtime();

    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        int contador_local = 0;

        #pragma omp single
        num_hilos = omp_get_num_threads();

        #pragma omp for
        for (i = 0; i < filas; i++) {
            int cols = ancho_fila[i]; // <-- usa el ancho correcto de esa fila
            for (j = 0; j < cols; j++) {
                if (mapa[i][j] == 'X') contador_local++;
            }
        }

        #pragma omp atomic
        contador_total += contador_local;

        #pragma omp critical
        printf("Hilo %d encontró %d tesoros en su sección.\n", tid, contador_local);
    }

    fin = omp_get_wtime();

    printf("\nParalelo: Total de tesoros = %d\n", contador_total);
    printf("Cores utilizados: %d\n", num_hilos);
    printf("Tiempo de ejecucion: %f segundos\n", fin - inicio);
    return 0;
}

