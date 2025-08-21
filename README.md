# Corto 7 - Paralela
* **Jose Joaquín Campos** 22155
* **Derek Fabian Arreaga** 22537

Este corto consistió en programar una simulación de manera serial y paralela para luego comparar los tiempos, calcular el `speed up` y la `eficiencia` al paralelizar.

## Descripción del problema: Mapa del Tesoro

Se tiene un enorme mapa pirata donde cada **`X`** marca un tesoro, se tiene como **meta** contar cuántos tesoros hay en el mapa.
El programa tendrá como entrada un archivo [mapa.txt](mapa.txt) como el siguiente:

```txt
.....X...
..X.....X
X...X....
...X..X..
```
---
## **Variables**
* **`shared`**: 
    - `mapa`, `filas`, `columnas`
    - `contador_total`
    - `num_hilos`
    - `inicio`, `fin`
* **`private`**:
    - `i`, `j`
    - `contador_local`

---
## **Versiones de la simulación**
### Versión Serial:
Se recorren todas las `"celdas"` y se contará cada **`X`** encontrada, una por una.

### Versión Paralela:
Se divide el mapa en **partes** y se contará en paralelo, al finalizar se harán los conteos parciales.

#### Explicación detallada:
Para la paralelización utilizamos ``OpenMP`` y se aplicaron las siguientes directivas para distribuir y sincronizar el trabajo entre los hilos:

1. **`#pragma omp parallel`**

   * Inicia una región paralela.
   * Todos los hilos creados ejecutan el bloque de código que encierra.
   * Dentro de esta región, cada hilo tiene su propia copia de las variables declaradas como `private`.

2. **`#pragma omp for`**

   * Divide automáticamente las iteraciones de un bucle `for` entre los hilos.
   * En este caso, cada hilo recibe un subconjunto de filas del mapa.
   * Esto permite un conteo paralelo sin necesidad de programar la división manual del trabajo.

3. **`#pragma omp atomic`**

   * Se usa para acumular el conteo de cada hilo en la variable global `contador_total` de forma segura y eficiente.

4. **`#pragma omp critical`**

   * Define una **sección crítica**, donde solo un hilo a la vez puede ejecutar el bloque de código.
   * Se utilizó únicamente para **imprimir resultados parciales** (`printf` de cada hilo).
   * Esto evita que las salidas de varios hilos se mezclen en la consola.

5. **`#pragma omp single`**

   * Especifica que **solo un hilo** debe ejecutar la sección de código.
   * En este caso, se usó para obtener el número de hilos (`num_hilos = omp_get_num_threads();`) sin que todos lo hagan.

6. **`omp_get_wtime()`**

   * Función de OpenMP que devuelve el tiempo de pared (wall-clock time) en segundos.
   * Se utilizó para medir el tiempo de ejecución paralelo con mayor precisión que las funciones estándar de C.