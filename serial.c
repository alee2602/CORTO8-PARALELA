#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>

#define MAX_FILAS 10000
#define MAX_COLUMNAS 10000


int main() {
    char mapa[MAX_FILAS][MAX_COLUMNAS];
    int filas = 0, columnas = 0;
    int i, j;
    int contador_serial = 0;
    double inicio, fin;

    FILE *archivo = fopen("mapa.txt", "r");
    if (!archivo) {
        printf("Error: no se pudo abrir mapa.txt\n");
        return 1;
    }

    char linea[MAX_COLUMNAS + 2]; // +2 para '\n' y '\0'
    while (fgets(linea, sizeof(linea), archivo) && filas < MAX_FILAS) {
        linea[strcspn(linea, "\n")] = '\0';  // quitar '\n'
        columnas = (int)strlen(linea);
        if (columnas > MAX_COLUMNAS) columnas = MAX_COLUMNAS;
        for (j = 0; j < columnas; j++) {
            mapa[filas][j] = linea[j];
        }
        filas++;
    }
    fclose(archivo);

    // Iniciar medición del conteo
    inicio = omp_get_wtime();

    for (i = 0; i < filas; i++) {
        for (j = 0; j < columnas; j++) {
            if (mapa[i][j] == 'X') {
                contador_serial++;
                printf("Encontro tesoro no.: %d en posicion [%d,%d]\n",
                       contador_serial, i, j);
            }
        }
    }

    fin = omp_get_wtime();

    double tiempo = fin - inicio;
    double speedup = 1.0;              // base serial
    double eficiencia = speedup / 1;   // 1 núcleo

    printf("\nSerial: Total de tesoros = %d\n", contador_serial);
    printf("Cores utilizados: %d\n", 1);
    printf("Tiempo de ejecucion: %f segundos\n", tiempo);
    printf("Eficiencia: %.2f\n", eficiencia);

    return 0;
}
