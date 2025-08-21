#!/bin/bash

gcc serial.c -o serial -fopenmp
gcc parallel.c -o parallel -fopenmp

# Ejecutar serial
serial_output=$(./serial | grep "Tiempo de ejecucion")
serial_time=$(echo $serial_output | awk '{print $4}')

# Ejecutar paralelo
parallel_output=$(./parallel | grep "Tiempo de ejecucion")
parallel_time=$(echo $parallel_output | awk '{print $4}')
cores=$(./parallel | grep "Cores utilizados" | awk '{print $3}')

# Calcular speedup y eficiencia
speedup=$(echo "$serial_time / $parallel_time" | bc -l)
eficiencia=$(echo "$serial_time / ($cores * $parallel_time)" | bc -l)

echo "============= RESULTADOS ============="
echo "Tiempo Serial   = $serial_time"
echo "Tiempo Paralelo = $parallel_time"
echo "Cores           = $cores"
echo "Speedup         = $speedup"
echo "Eficiencia      = $eficiencia"
