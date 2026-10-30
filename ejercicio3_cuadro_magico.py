import numpy as np

# Para reproducir los mismos resultados (antes la fijaba ga.py al importarse)
np.random.seed(42)

def ga_cuadro_magico(
    n,
    tam_poblacion,
    num_generaciones,
    prob_cruce,
    prob_mutacion
):

    num_casillas = n * n
    numero_magico = (n**3 + n) // 2


    # ==========================================================
    # FUNCIÓN DE COSTO
    # ==========================================================

    def costo(individuo):

        cuadro = individuo.reshape(n, n)

        filas = np.abs(cuadro.sum(axis=1) - numero_magico).sum()
        columnas = np.abs(cuadro.sum(axis=0) - numero_magico).sum()

        # np.trace suma la diagonal principal. Volteando el cuadro de
        # izquierda a derecha, la otra diagonal pasa a ser la principal.
        diagonal = abs(np.trace(cuadro) - numero_magico)
        antidiagonal = abs(np.trace(np.fliplr(cuadro)) - numero_magico)

        return int(filas + columnas + diagonal + antidiagonal)


    # ==========================================================
    # CREAR POBLACIÓN INICIAL
    # ==========================================================

    def crear_poblacion():

        # Cada individuo es una permutación aleatoria de 1 a N²
        return [
            np.random.permutation(num_casillas) + 1
            for _ in range(tam_poblacion)
        ]


    # ==========================================================
    # EVALUAR POBLACIÓN
    # ==========================================================

    def evaluar_poblacion(poblacion):

        return np.array([costo(individuo) for individuo in poblacion])


    # ==========================================================
    # SELECCIÓN POR TORNEO
    # ==========================================================

    def seleccion_torneo(poblacion, fitness, k=3):

        # Elegimos k cuadros aleatoriamente
        indices = np.random.choice(
            len(poblacion),
            min(k, len(poblacion)),
            replace=False
        )

        # Gana el de menor costo
        mejor = indices[np.argmin(fitness[indices])]

        return poblacion[mejor].copy()

    def pmx(padre1, padre2, a, b):

        hijo = padre2.copy()
        hijo[a:b] = padre1[a:b]

        tramo = set(padre1[a:b])
        mapeo = {padre1[i]: padre2[i] for i in range(a, b)}

        for i in list(range(a)) + list(range(b, num_casillas)):

            valor = padre2[i]

            while valor in tramo:
                valor = mapeo[valor]

            hijo[i] = valor

        return hijo


    def cruce(padre1, padre2):

        if np.random.rand() < prob_cruce:

            # Tramo aleatorio [a, b) con al menos una casilla
            a, b = np.sort(np.random.choice(num_casillas + 1, 2, replace=False))

            hijo1 = pmx(padre1, padre2, a, b)
            hijo2 = pmx(padre2, padre1, a, b)

        else:

            hijo1 = padre1.copy()
            hijo2 = padre2.copy()

        return hijo1, hijo2


    # ==========================================================
    # OPERADOR DE MUTACIÓN
    # ==========================================================

    def mutacion(individuo):

        if np.random.rand() < prob_mutacion:

            # Se intercambian los números de dos casillas al azar
            i, j = np.random.choice(num_casillas, 2, replace=False)
            individuo[i], individuo[j] = individuo[j], individuo[i]

        return individuo


    poblacion = crear_poblacion()

    for generacion in range(num_generaciones):

        # Evaluar población
        fitness = evaluar_poblacion(poblacion)

        # Encontrar el mejor cuadro
        indice_mejor = np.argmin(fitness)

        mejor_individuo = poblacion[indice_mejor].copy()
        mejor_fitness = fitness[indice_mejor]

        # Mostrar información cada 50 generaciones y al resolverlo
        if generacion % 50 == 0 or mejor_fitness == 0:

            print(
                f"Generación {generacion:4d} | "
                f"costo = {mejor_fitness:4d}"
            )

        # Costo 0: ya es un cuadro mágico, no se puede mejorar
        if mejor_fitness == 0:
            break

        # ----------------------------------------------------------
        # ELITISMO
        # ----------------------------------------------------------

        nueva_poblacion = [mejor_individuo]

        # ----------------------------------------------------------
        # CREAR NUEVA GENERACIÓN
        # ----------------------------------------------------------

        while len(nueva_poblacion) < tam_poblacion:

            # Selección
            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)

            # Cruce
            hijo1, hijo2 = cruce(padre1, padre2)

            # Mutación
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)

            nueva_poblacion.append(hijo1)

            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion


    fitness = evaluar_poblacion(poblacion)

    indice_mejor = np.argmin(fitness)

    mejor_cuadro = poblacion[indice_mejor].reshape(n, n)
    costo_mejor = int(fitness[indice_mejor])
    return mejor_cuadro, costo_mejor, generacion

# Tamaño del cuadro (N x N). Para resolver otro tamaño, cambia este
# valor. Debe ser al menos 3, porque no existe cuadro mágico de 2 x 2.
N = 4

# Cuadro de ejemplo del PDF, para comprobar la función de costo
EJEMPLO_PDF = np.array([
    [ 9, 12,  7,  6],
    [ 1,  4, 15, 14],
    [16,  5, 10,  3],
    [ 8, 13,  2, 11],
])

def numero_magico(n):
    """Suma que deben tener cada fila, columna y diagonal."""

    return (n**3 + n) // 2


def costo_cuadro(cuadro):
    """
    Distancia del cuadro para ser mágico, igual que en ga_cuadro_magico.
    """

    magico = numero_magico(len(cuadro))

    filas = np.abs(cuadro.sum(axis=1) - magico).sum()
    columnas = np.abs(cuadro.sum(axis=0) - magico).sum()
    diagonal = abs(np.trace(cuadro) - magico)
    antidiagonal = abs(np.trace(np.fliplr(cuadro)) - magico)

    return int(filas + columnas + diagonal + antidiagonal)


def imprimir_cuadro(cuadro):
    """Muestra el cuadro con la suma de cada fila, columna y diagonal."""

    # El ancho debe alcanzar para las sumas de las columnas, que son
    # más largas que los números del cuadro
    ancho = len(str(cuadro.sum(axis=0).max())) + 1

    for fila in cuadro:
        numeros = "".join(f"{numero:>{ancho}}" for numero in fila)
        print(f"{numeros}   | {fila.sum()}")

    print("-" * (ancho * len(cuadro) + 3))
    print("".join(f"{suma:>{ancho}}" for suma in cuadro.sum(axis=0)))
    print(f"Diagonal principal:  {np.trace(cuadro)}")
    print(f"Diagonal secundaria: {np.trace(np.fliplr(cuadro))}")

if N < 3:
    raise ValueError("N debe ser al menos 3 (no existe cuadro mágico de 2 x 2).")

print("===================================")
print("CUADRO MÁGICO")
print("===================================")
print(f"Tamaño: {N} x {N} (números del 1 al {N * N})")
print(f"Número mágico: ({N}³ + {N}) / 2 = {numero_magico(N)}")
print(f"Costo del cuadro 4 x 4 de ejemplo del PDF: {costo_cuadro(EJEMPLO_PDF)}")
print()

# La probabilidad de mutación se aplica a cada cuadro completo:
# con 0.3, a 3 de cada 10 hijos se les intercambian dos casillas.
cuadro, costo, generacion = ga_cuadro_magico(
    n=N,
    tam_poblacion=500,
    num_generaciones=1000,
    prob_cruce=0.9,
    prob_mutacion=0.3
)

print("\n===================================")
print("MEJOR CUADRO ENCONTRADO")
print("===================================")
imprimir_cuadro(cuadro)
print()

if costo == 0 and costo_cuadro(cuadro) == 0:
    print(f"Es un cuadro mágico: todo suma {numero_magico(N)}.")
    print(f"Se encontró en la generación {generacion}.")
else:
    print(
        f"No se encontró un cuadro mágico. El mejor tiene costo {costo}; "
        "la población se quedó atorada en un cuadro casi mágico. "
        "Prueba con otra semilla, más generaciones o más población."
    )
