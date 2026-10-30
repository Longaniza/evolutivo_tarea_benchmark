import numpy as np

# Para reproducir los mismos resultados (antes la fijaba ga.py al importarse)
np.random.seed(42)


def ga_mensaje(
    mensaje_cifrado,
    mensaje_original,
    tam_poblacion,
    num_generaciones,
    prob_cruce,
    prob_mutacion,
    alfabeto=" abcdefghijklmnopqrstuvwxyz"
):

    # Los S símbolos distintos de cada mensaje, en orden alfabético
    simbolos_cifrados = sorted(set(mensaje_cifrado), key=alfabeto.index)
    simbolos_originales = sorted(set(mensaje_original), key=alfabeto.index)
    num_simbolos = len(simbolos_cifrados)

    posiciones = np.array([simbolos_cifrados.index(s) for s in mensaje_cifrado])
    valores_simbolos = np.array([alfabeto.index(s) for s in simbolos_originales])
    valores_originales = np.array([alfabeto.index(s) for s in mensaje_original])


    def descifrar(individuo):

        # Traduce cada letra del mensaje cifrado con el código
        return "".join(simbolos_originales[individuo[p]] for p in posiciones)


    def costo(individuo):

        # suma |mensaje(n) - adivinado(n)|
        valores_adivinados = valores_simbolos[individuo[posiciones]]

        return int(np.sum(np.abs(valores_originales - valores_adivinados)))


    # ==========================================================
    # CREAR POBLACIÓN INICIAL
    # ==========================================================

    def crear_poblacion():

        # Cada individuo es una permutación aleatoria de 0 a S-1
        return [np.random.permutation(num_simbolos) for _ in range(tam_poblacion)]


    # ==========================================================
    # EVALUAR POBLACIÓN
    # ==========================================================

    def evaluar_poblacion(poblacion):

        return np.array([costo(individuo) for individuo in poblacion])


    # ==========================================================
    # SELECCIÓN POR TORNEO
    # ==========================================================

    def seleccion_torneo(poblacion, fitness, k=3):

        # Elegimos k códigos aleatoriamente
        indices = np.random.choice(
            len(poblacion),
            min(k, len(poblacion)),
            replace=False
        )

        mejor = indices[np.argmin(fitness[indices])]

        return poblacion[mejor].copy()

    def pmx(padre1, padre2, a, b):
        hijo = padre2.copy()
        hijo[a:b] = padre1[a:b]

        tramo = set(padre1[a:b])
        mapeo = {padre1[i]: padre2[i] for i in range(a, b)}

        for i in list(range(a)) + list(range(b, num_simbolos)):

            valor = padre2[i]

            while valor in tramo:
                valor = mapeo[valor]

            hijo[i] = valor

        return hijo


    def cruce(padre1, padre2):

        if np.random.rand() < prob_cruce:

            # Tramo aleatorio [a, b) con al menos un símbolo
            a, b = np.sort(np.random.choice(num_simbolos + 1, 2, replace=False))

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

            # Se intercambian las traducciones de dos símbolos cifrados
            i, j = np.random.choice(num_simbolos, 2, replace=False)
            individuo[i], individuo[j] = individuo[j], individuo[i]

        return individuo


    poblacion = crear_poblacion()

    for generacion in range(num_generaciones):

        # Evaluar población
        fitness = evaluar_poblacion(poblacion)

        # Encontrar el mejor código
        indice_mejor = np.argmin(fitness)

        mejor_individuo = poblacion[indice_mejor].copy()
        mejor_fitness = fitness[indice_mejor]

        # Mostrar información cada 10 generaciones y al descifrarlo
        if generacion % 10 == 0 or mejor_fitness == 0:

            print(
                f"Generación {generacion:3d} | "
                f"costo = {mejor_fitness:4d} | "
                f"mensaje = {descifrar(mejor_individuo)}"
            )

        # Costo 0: el mensaje ya está descifrado, no se puede mejorar
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

    mejor_individuo = poblacion[indice_mejor]
    costo_mejor = int(fitness[indice_mejor])

    codigo = {
        simbolos_cifrados[i]: simbolos_originales[mejor_individuo[i]]
        for i in range(num_simbolos)
    }

    return descifrar(mejor_individuo), costo_mejor, codigo


# Los 27 símbolos posibles. La posición de cada uno es su valor
# numérico para el costo: espacio = 0, a = 1, ..., z = 26.
ALFABETO = " abcdefghijklmnopqrstuvwxyz"

# Mensaje del ejemplo
MENSAJE_ORIGINAL = "bonny and amy are our children"

# Semilla del código secreto. Se usa un generador propio para no
# alterar la semilla global que se fija al inicio de este archivo.
SEMILLA_CODIGO = 7


# ==============================================================
# CIFRADO DEL MENSAJE
# ==============================================================

def crear_codigo_secreto(semilla=SEMILLA_CODIGO):
    """Código de sustitución aleatorio: cada símbolo va a otro distinto."""

    rng = np.random.default_rng(semilla)
    permutacion = rng.permutation(len(ALFABETO))

    return {
        ALFABETO[i]: ALFABETO[permutacion[i]]
        for i in range(len(ALFABETO))
    }


def cifrar(mensaje, codigo):
    """Sustituye cada símbolo del mensaje según el código."""

    return "".join(codigo[simbolo] for simbolo in mensaje)


mensaje_cifrado = cifrar(MENSAJE_ORIGINAL, crear_codigo_secreto())
num_simbolos = len(set(mensaje_cifrado))

print(f"Mensaje cifrado: '{mensaje_cifrado}'")
print(f"Símbolos usados: S = {num_simbolos} ({num_simbolos}! códigos posibles)")
print()

mensaje, costo, codigo = ga_mensaje(
    mensaje_cifrado=mensaje_cifrado,
    mensaje_original=MENSAJE_ORIGINAL,
    tam_poblacion=50,
    num_generaciones=100,
    prob_cruce=0.9,
    prob_mutacion=0.3,
    alfabeto=ALFABETO
)

print(f"Mensaje original:   '{MENSAJE_ORIGINAL}'")
print(f"Mensaje descifrado: '{mensaje}'")
print(f"Costo final: {costo}")

