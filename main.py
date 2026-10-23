from ga import simple_ga, graficar_fitness_function
import contextlib
import csv
import io
import numpy as np

# ==============================================================
# CONSTANTES DEL ALGORITMO GENÉTICO
# ==============================================================

TAM_POBLACION = 50
NUM_GENERACIONES = 500

PROB_CRUCE = 0.90
PROB_MUTACION = 0.20

NUM_VARIABLES = 2

# ==============================================================
# CONSTANTES DE LA TAREA DE PROMEDIOS
# ==============================================================

NUM_CORRIDAS = 30
ARCHIVO_RESULTADOS = "resultados.csv"


# ==============================================================
# FUNCIONES OBJETIVO
# ==============================================================

RASTRIGIN_LIMITE_INFERIOR = -5.12
RASTRIGIN_LIMITE_SUPERIOR = 5.12

GRIEWANK_LIMITE_INFERIOR = -600
GRIEWANK_LIMITE_SUPERIOR = 600

ZAKHAROV_LIMITE_INFERIOR = -5
ZAKHAROV_LIMITE_SUPERIOR = 10

ALPINE1_LIMITE_INFERIOR = -10
ALPINE1_LIMITE_SUPERIOR = 10


def rastrigin(individuo):

    x = np.asarray(individuo)
    n = len(x)

    return 10*n + np.sum(x**2 - 10*np.cos(2*np.pi*x))


def griewank(individuo):

    x = np.asarray(individuo)
    i = np.arange(1, len(x) + 1)

    return (
        1
        + np.sum(x**2) / 4000
        - np.prod(np.cos(x / np.sqrt(i)))
    )


def zakharov(individuo):

    x = np.asarray(individuo)
    i = np.arange(1, len(x) + 1)

    suma1 = np.sum(x**2)
    suma2 = np.sum(0.5*i*x)

    return suma1 + suma2**2 + suma2**4


def alpine1(individuo):

    x = np.asarray(individuo)

    return np.sum(np.abs(x*np.sin(x) + 0.1*x))

FUNCIONES_OBJETIVO = {
    "1": ("Rastrigin", rastrigin, RASTRIGIN_LIMITE_INFERIOR, RASTRIGIN_LIMITE_SUPERIOR, "f(0, ..., 0) = 0"),
    "2": ("Griewank", griewank, GRIEWANK_LIMITE_INFERIOR, GRIEWANK_LIMITE_SUPERIOR, "f(0, ..., 0) = 0"),
    "3": ("Zakharov", zakharov, ZAKHAROV_LIMITE_INFERIOR, ZAKHAROV_LIMITE_SUPERIOR, "f(0, ..., 0) = 0"),
    "4": ("Alpine N.1", alpine1, ALPINE1_LIMITE_INFERIOR, ALPINE1_LIMITE_SUPERIOR, "f(0, ..., 0) = 0"),
}


# ==============================================================
# MENÚ PRINCIPAL
# ==============================================================

while True:

    print("\n===================================")
    print("MENÚ")
    print("===================================")
    print("0. Tarea promedios")
    print("1.- Graficar función")
    print("2.- Ejecutar benchmark manualmente")
    print("3.- Salir")

    opcion = input("Elige una opción: ").strip()

    if opcion == "0":

        with open(ARCHIVO_RESULTADOS, "w", newline="") as archivo:

            escritor = csv.writer(archivo)

            for nombre, fitness_function, limite_inferior, limite_superior, minimo_global in (
                FUNCIONES_OBJETIVO.values()
            ):

                for num_variables in [2, 4, 6]:

                    print(
                        f"Ejecutando {nombre} [mínimo global: {minimo_global}] con {num_variables} variables "
                        f"({NUM_CORRIDAS} corridas)..."
                    )

                    mejores_fitness = []

                    for corrida in range(NUM_CORRIDAS):

                        # Se silencia lo que simple_ga imprime por generación
                        with contextlib.redirect_stdout(io.StringIO()):
                            mejores_fitness.append(simple_ga(
                                tam_poblacion=TAM_POBLACION,
                                num_generaciones=NUM_GENERACIONES,
                                prob_cruce=PROB_CRUCE,
                                prob_mutacion=PROB_MUTACION,
                                limite_inferior=limite_inferior,
                                limite_superior=limite_superior,
                                num_variables=num_variables,
                                fitness_function=fitness_function
                            ))

                    # Una tabla por función y número de variables
                    escritor.writerow(["Función", nombre])
                    escritor.writerow(["Variables", num_variables])
                    escritor.writerow(["Peor fitness", "Mejor fitness", "Promedio fitness"])
                    escritor.writerow([
                        np.max(mejores_fitness),
                        np.min(mejores_fitness),
                        np.mean(mejores_fitness)
                    ])
                    escritor.writerow([])

        print(f"Resultados guardados en {ARCHIVO_RESULTADOS}")

    elif opcion == "1":

        print("\nFunciones objetivo disponibles:")

        for clave, (nombre, _, _, _, minimo_global) in FUNCIONES_OBJETIVO.items():
            print(f"{clave}.- {nombre} [mínimo global: {minimo_global}]")

        opcion_funcion = input("Elige una función: ").strip()

        if opcion_funcion not in FUNCIONES_OBJETIVO:
            print("Función no válida")
            continue

        nombre, fitness_function, limite_inferior, limite_superior, minimo_global = (
            FUNCIONES_OBJETIVO[opcion_funcion]
        )

        graficar_fitness_function(
            limite_inferior=limite_inferior,
            limite_superior=limite_superior,
            fitness_function=fitness_function
        )

    elif opcion == "2":

        print("\nFunciones objetivo disponibles:")

        for clave, (nombre, _, _, _, minimo_global) in FUNCIONES_OBJETIVO.items():
            print(f"{clave}.- {nombre} [mínimo global: {minimo_global}]")

        opcion_funcion = input("Elige una función: ").strip()

        if opcion_funcion not in FUNCIONES_OBJETIVO:
            print("Función no válida")
            continue

        nombre, fitness_function, limite_inferior, limite_superior, minimo_global = (
            FUNCIONES_OBJETIVO[opcion_funcion]
        )

        try:
            num_variables = int(input("Número de variables: ").strip())
        except ValueError:
            print("El número de variables debe ser un entero")
            continue

        # simple_ga imprime x1 y x2, así que se necesitan al menos 2
        if num_variables < 2:
            print("El número de variables debe ser al menos 2")
            continue

        print("\nParámetros fijos usados en la ejecución:")
        print(f"Tamaño de población:      {TAM_POBLACION}")
        print(f"Número de generaciones:   {NUM_GENERACIONES}")
        print(f"Probabilidad de cruce:    {PROB_CRUCE}")
        print(f"Probabilidad de mutación: {PROB_MUTACION}")
        print(f"Límite inferior:          {limite_inferior}")
        print(f"Límite superior:          {limite_superior}")
        print()

        simple_ga(
            tam_poblacion=TAM_POBLACION,
            num_generaciones=NUM_GENERACIONES,
            prob_cruce=PROB_CRUCE,
            prob_mutacion=PROB_MUTACION,
            limite_inferior=limite_inferior,
            limite_superior=limite_superior,
            num_variables=num_variables,
            fitness_function=fitness_function
        )

    elif opcion == "3":
        break

    else:
        print("Opción no válida")
