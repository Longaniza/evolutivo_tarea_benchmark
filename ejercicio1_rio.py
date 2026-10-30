import numpy as np

# Para reproducir los mismos resultados (antes la fijaba ga.py al importarse)
np.random.seed(42)


def ga_rutas(
    matriz_precios,
    tam_poblacion,
    num_generaciones,
    prob_cruce,
    prob_mutacion,
    origen=0,
    destino=None,
    sin_conexion=-1
):

    matriz = np.asarray(matriz_precios)
    num_ciudades = len(matriz)

    if destino is None:
        destino = num_ciudades - 1


    # ==========================================================
    # FUNCIONES AUXILIARES DE RUTAS
    # ==========================================================

    def vecinos(ciudad):

        # Ciudades conectadas
        return [
            otra for otra in range(num_ciudades)
            if otra != ciudad and matriz[ciudad][otra] != sin_conexion
        ]


    def camino_aleatorio(desde, prohibidas):
        visitadas = set(prohibidas) | {desde}
        camino = [desde]
        opciones = [list(np.random.permutation(vecinos(desde)))]

        while camino:

            if camino[-1] == destino:
                return [int(ciudad) for ciudad in camino]

            # Siguiente vecino pendiente que no se haya visitado
            pendientes = opciones[-1]
            while pendientes and pendientes[0] in visitadas:
                pendientes.pop(0)

            if pendientes:
                siguiente = pendientes.pop(0)
                visitadas.add(siguiente)
                camino.append(siguiente)
                opciones.append(list(np.random.permutation(vecinos(siguiente))))
            else:
                # Callejón sin salida: se regresa una ciudad
                camino.pop()
                opciones.pop()

        return None


    def quitar_ciclos(ruta):

        # Si una ciudad aparece dos veces, se elimina el tramo entre
        # sus dos apariciones. Con precios positivos, quitar un ciclo
        # siempre abarata la ruta.
        resultado = []

        for ciudad in ruta:
            if ciudad in resultado:
                resultado = resultado[:resultado.index(ciudad)]
            resultado.append(ciudad)

        return resultado


    def precio(ruta):

        # Suma de los precios de cada trayecto de la ruta
        return float(sum(matriz[a][b] for a, b in zip(ruta, ruta[1:])))


    # ==========================================================
    # CREAR POBLACIÓN INICIAL
    # ==========================================================

    def crear_poblacion():

        poblacion = []

        for _ in range(tam_poblacion):

            ruta = camino_aleatorio(origen, prohibidas=[])

            if ruta is None:
                raise ValueError(
                    f"No existe ninguna ruta de la ciudad {origen} "
                    f"a la ciudad {destino}"
                )

            poblacion.append(ruta)

        return poblacion


    # ==========================================================
    # EVALUAR POBLACIÓN
    # ==========================================================

    def evaluar_poblacion(poblacion):

        return np.array([precio(ruta) for ruta in poblacion])


    # ==========================================================
    # SELECCIÓN POR TORNEO
    # ==========================================================

    def seleccion_torneo(poblacion, fitness, k=3):

        # Elegimos k rutas aleatoriamente
        indices = np.random.choice(
            len(poblacion),
            min(k, len(poblacion)),
            replace=False
        )
        mejor = indices[np.argmin(fitness[indices])]

        return list(poblacion[mejor])


    # ==========================================================
    # OPERADOR DE CRUCE
    # ==========================================================

    def cruce(padre1, padre2):

        # Se busca una ciudad intermedia que este en los dos padres.
        # Cada hijo toma el inicio de un padre hasta esa ciudad y el
        # final del otro padre desde esa ciudad. Ambos tramos usan
        # trayectos que existen, asi que los hijos son rutas validas.
        comunes = list(set(padre1[1:-1]) & set(padre2[1:-1]))

        if np.random.rand() < prob_cruce and comunes:

            ciudad = comunes[np.random.randint(len(comunes))]

            i = padre1.index(ciudad)
            j = padre2.index(ciudad)

            hijo1 = quitar_ciclos(padre1[:i] + padre2[j:])
            hijo2 = quitar_ciclos(padre2[:j] + padre1[i:])

        else:

            hijo1 = list(padre1)
            hijo2 = list(padre2)

        return hijo1, hijo2


    # ==========================================================
    # OPERADOR DE MUTACIÓN
    # ==========================================================

    def mutacion(ruta):

        if np.random.rand() < prob_mutacion:

            # Se corta la ruta en una ciudad al azar y se completa con un camino aleatorio nuevo
            # hasta el destino, sin repetir las ciudades ya usadas.
            corte = np.random.randint(len(ruta) - 1)
            inicio = ruta[:corte + 1]

            final = camino_aleatorio(ruta[corte], prohibidas=ruta[:corte])

            # Siempre existe al menos el final original, pero se
            # revisa por seguridad
            if final is not None:
                ruta = inicio[:-1] + final

        return ruta


    poblacion = crear_poblacion()

    for generacion in range(num_generaciones):

        # Evaluar población
        fitness = evaluar_poblacion(poblacion)

        # Encontrar la mejor ruta
        indice_mejor = np.argmin(fitness)

        mejor_ruta = list(poblacion[indice_mejor])
        mejor_fitness = fitness[indice_mejor]

        # Mostrar información cada 10 generaciones
        if generacion % 10 == 0:

            print(
                f"Generación {generacion:3d} | "
                f"precio = {mejor_fitness:8.2f} | "
                f"ruta = {' -> '.join(map(str, mejor_ruta))}"
            )

        # ----------------------------------------------------------
        # ELITISMO
        # ----------------------------------------------------------

        nueva_poblacion = [mejor_ruta]

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

    mejor_ruta = poblacion[indice_mejor]
    precio_mejor = fitness[indice_mejor]
    return mejor_ruta, precio_mejor



MATRIZ_PRECIOS = np.array([
    [-1, 16, 20, 57, -1, -1],
    [16, -1, -1, -1, 80, -1],
    [20, -1, -1, -1, -1, 50],
    [57, -1, -1, -1, 44, -1],
    [-1, 80, -1, 44, -1, 14],
    [-1, -1, 50, -1, 14, -1],
])

NUM_CIUDADES = len(MATRIZ_PRECIOS)
CIUDAD_ORIGEN = 0
CIUDAD_DESTINO = NUM_CIUDADES - 1



print("VIAJE MÁS BARATO")
print("-------------------------------------")
print(f"Ciudades: {NUM_CIUDADES} (origen {CIUDAD_ORIGEN}, destino {CIUDAD_DESTINO})")

mejor_ruta, mejor_precio = ga_rutas(
    matriz_precios=MATRIZ_PRECIOS,
    tam_poblacion=50,
    num_generaciones=50,
    prob_cruce=0.9,
    prob_mutacion=0.20,
    origen=CIUDAD_ORIGEN,
    destino=CIUDAD_DESTINO
)

print("Ruta:", " -> ".join(str(ciudad) for ciudad in mejor_ruta))

print(f"Precio total: {mejor_precio:g} €")
