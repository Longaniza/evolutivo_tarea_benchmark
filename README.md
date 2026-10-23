# Algoritmo genético para funciones de benchmark

Algoritmo genético simple para minimizar cuatro funciones de prueba clásicas:

| Función    | Dominio usado     | Mínimo global     |
|------------|-------------------|-------------------|
| Rastrigin  | [-5.12, 5.12]     | f(0, ..., 0) = 0  |
| Griewank   | [-600, 600]       | f(0, ..., 0) = 0  |
| Zakharov   | [-5, 10]          | f(0, ..., 0) = 0  |
| Alpine N.1 | [-10, 10]         | f(0, ..., 0) = 0  |

## Archivos

- `ga.py`: el algoritmo genético (`simple_ga`) y la gráfica 3D de una función (`graficar_fitness_function`).
- `main.py`: las funciones objetivo, los parámetros del algoritmo y el menú de terminal. Es el archivo que se ejecuta.
- `resultados.csv`: se genera con la opción 0 del menú.

## Requisitos

- Python 3
- `numpy`
- `matplotlib`

## Cómo correr el programa
Desde la carpeta del proyecto:

```bash
python3 main.py
```

## Uso del menú

Al ejecutar `main.py` aparece este menú:

```
===================================
MENÚ
===================================
0. Tarea promedios
1.- Graficar función
2.- Ejecutar benchmark manualmente
3.- Salir
Elige una opción:
```

Escribe el número de la opción y presiona Enter. Después de cada opción el menú vuelve a aparecer, hasta que elijas salir.

### 0. Tarea promedios

Corre el algoritmo genético 30 veces para cada función con 2, 4 y 6 variables (12 combinaciones). Para cada combinación calcula, sobre el mejor fitness de cada corrida:

- el peor fitness (máximo),
- el mejor fitness (mínimo),
- el promedio.

Los resultados se guardan en `resultados.csv`, una tabla por combinación:

```
Función,Rastrigin
Variables,2
Peor fitness,Mejor fitness,Promedio fitness
8.21e-05,1.42e-14,4.68e-06
```


### 1. Graficar función

1. Muestra la lista de funciones con su mínimo global:
   ```
   1.- Rastrigin [mínimo global: f(0, ..., 0) = 0]
   2.- Griewank [mínimo global: f(0, ..., 0) = 0]
   3.- Zakharov [mínimo global: f(0, ..., 0) = 0]
   4.- Alpine N.1 [mínimo global: f(0, ..., 0) = 0]
   ```
2. Escribe el número de la función.
3. Se abre una ventana con la superficie 3D de la función en 2 variables, dentro de su dominio. Cierra la ventana para volver al menú.

### 2. Ejecutar benchmark manualmente

1. Elige la función de la misma lista.
2. Escribe el número de variables (entero, mínimo 2).
3. Se muestran los parámetros que no se piden por terminal (tamaño de población, generaciones, probabilidades de cruce y mutación, y el dominio de la función elegida).
4. El algoritmo imprime el mejor individuo cada 10 generaciones y, al final, la mejor solución encontrada y su fitness.

### 3. Salir

Termina el programa.

