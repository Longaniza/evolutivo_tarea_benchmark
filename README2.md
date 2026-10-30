# Ejercicios con algoritmos genéticos

Soluciones a los tres ejercicios del PDF. Cada ejercicio está en su propio archivo y trae su propio algoritmo genético basado en el algoritmo génetico ya utilizado en clase, adaptado al problema.

| Archivo                        | Ejercicio                                |
|--------------------------------|------------------------------------------|
| `ejercicio1_rio.py`            | 1. Viaje más barato por río              |
| `ejercicio2_mensaje.py`        | 2. Decodificar un mensaje secreto        |
| `ejercicio3_cuadro_magico.py`  | 3. Cuadro mágico de N x N                |

## Ejercicio 1. Viaje más barato por río

```bash
python ejercicio1_rio.py
```

No pide datos. Usa la matriz de precios del PDF, donde -1 indica que dos ciudades no están conectadas, y busca la ruta más barata de la ciudad 0 a la ciudad 5.

Muestra el progreso cada 10 generaciones y al final la mejor ruta:

```
Generación   0 | precio =    70.00 | ruta = 0 -> 2 -> 5
...
Ruta: 0 -> 2 -> 5
Precio total: 70 €
```

Para probar otro río, cambia `MATRIZ_PRECIOS` dentro del archivo. Si no existe ninguna ruta entre el origen y el destino, el programa se detiene con un error que lo indica.

## Ejercicio 2. Decodificar un mensaje secreto

```bash
python ejercicio2_mensaje.py
```
Muestra el mejor mensaje cada 10 generaciones y se detiene en cuanto el costo llega a 0:
```
Generación   0 | costo =  166 | mensaje = hniibdaiedambdarudnyrdlo cerui
Generación  10 | costo =   23 | mensaje = enooy aod aly arb nur chmidrbo
Generación  20 | costo =    6 | mensaje = bnooy aod amy are nur childreo
Generación  22 | costo =    0 | mensaje = bonny and amy are our children
```

Para probar otro mensaje, cambia `MENSAJE_ORIGINAL` dentro del archivo. Solo puede tener letras minúsculas y espacios.

## Ejercicio 3. Cuadro mágico

```bash
python ejercicio3_cuadro_magico.py
```

Resuelve un cuadro de 4 x 4.

Para resolver un cuadro de otro tamaño, cambia el valor de la constante `N` dentro del archivo.

```python
N = 4
```

El valor debe ser un número entero de 3 en adelante, porque no existe un cuadro mágico de 2 x 2. Si pones un valor menor que 3, el programa se detiene con un error que lo indica.

Muestra el costo del mejor cuadro cada 50 generaciones y se detiene en cuanto el costo llega a 0. Al final imprime el cuadro con la suma de cada fila, columna y diagonal:

```
 10 12  5  7   | 34
 13  1  4 16   | 34
  3 15 14  2   | 34
  8  6 11  9   | 34
---------------
 34 34 34 34
Diagonal principal:  34
Diagonal secundaria: 34

Es un cuadro mágico: todo suma 34.
```

| N | Resultado esperado                                              |
|---|-----------------------------------------------------------------|
| 3 | Lo resuelve en pocas generaciones.                              |
| 4 | Con la semilla del archivo lo resuelve en la generación 220. Con otras semillas lo resuelve más o menos la mitad de las veces; si no, se queda en un cuadro casi mágico con costo 2 a 4. |
| 5 | En las pruebas no llegó a un cuadro mágico; se quedó con costo de 1 a 3. |
