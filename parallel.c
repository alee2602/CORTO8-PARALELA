#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define MAX_FILAS 1100
#define MAX_COLUMNAS 1100

int main() {
    char mapa[MAX_FILAS][MAX_COLUMNAS];
    int filas = 0, columnas = 0;
    int i, j;
    int contador_total = 0;
    int num_hilos = 0;
    double inicio, fin;

    FILE *archivo = fopen("mapa.txt", "r");
    if (!archivo) {
        printf("Error: no se pudo abrir mapa.txt\n");
        return 1;
    }

    char linea[MAX_COLUMNAS + 2];
    while (fgets(linea, sizeof(linea), archivo)) {
        linea[strcspn(linea, "\n")] = '\0';
        columnas = strlen(linea);
        for (j = 0; j < columnas; j++) {
            mapa[filas][j] = linea[j];
        }
        filas++;
    }
    fclose(archivo);

    inicio = omp_get_wtime();

    #pragma omp parallel private(j)
    {
        int tid = omp_get_thread_num();
        int contador_local = 0;

        #pragma omp single
        num_hilos = omp_get_num_threads();

        #pragma omp for
        for (i = 0; i < filas; i++) {
            for (j = 0; j < columnas; j++) {
                if (mapa[i][j] == 'X') {
                    contador_local++;
                }
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
