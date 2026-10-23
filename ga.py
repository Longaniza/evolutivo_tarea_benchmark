# ==============================================================
# ALGORITMO GENÉTICO PARA MINIMIZAR LA FUNCIÓN RASTRIGIN
# Ejemplo didáctico para alumnos de posgrado en ciencias de la computacion
# Dr. Fevrier Adolfo Valdez Acosta
# 7 de enero de 2024

# ==============================================================

import numpy as np
import matplotlib.pyplot as plt

# Para reproducir los mismos resultados
np.random.seed(42)

# ==============================================================
# ALGORITMO GENÉTICO
# ==============================================================

def simple_ga(
    tam_poblacion,
    num_generaciones,
    prob_cruce,
    prob_mutacion,
    limite_inferior,
    limite_superior,
    num_variables,
    fitness_function
):

    # ==========================================================
    # CREAR POBLACIÓN INICIAL
    # ==========================================================

    def crear_poblacion():

        poblacion = np.random.uniform(
            limite_inferior,
            limite_superior,
            size=(tam_poblacion, num_variables)
        )

        return poblacion


    # ==========================================================
    # EVALUAR POBLACIÓN
    # ==========================================================

    def evaluar_poblacion(poblacion):

        valores = []

        for individuo in poblacion:
            valor = fitness_function(individuo)
            valores.append(valor)

        return np.array(valores)


    # ==========================================================
    # SELECCIÓN POR TORNEO
    # ==========================================================

    def seleccion_torneo(poblacion, fitness, k=3):

        # Elegimos k individuos aleatoriamente
        indices = np.random.choice(
            len(poblacion),
            k,
            replace=False
        )

        # Encontramos el mejor del torneo
        mejor = indices[np.argmin(fitness[indices])]

        return poblacion[mejor].copy()


    # ==========================================================
    # OPERADOR DE CRUCE
    # ==========================================================

    def cruce(padre1, padre2):

        if np.random.rand() < prob_cruce:

            # alpha controla la combinación
            alpha = np.random.rand()

            hijo1 = alpha*padre1 + (1-alpha)*padre2
            hijo2 = alpha*padre2 + (1-alpha)*padre1

        else:

            hijo1 = padre1.copy()
            hijo2 = padre2.copy()

        return hijo1, hijo2


    # ==========================================================
    # OPERADOR DE MUTACIÓN
    # ==========================================================

    def mutacion(individuo):

        for i in range(num_variables):

            if np.random.rand() < prob_mutacion:

                # Ruido gaussiano
                individuo[i] += np.random.normal(
                    loc=0,
                    scale=0.5
                )

        # Evitar que las variables salgan del dominio permitido
        individuo = np.clip(
            individuo,
            limite_inferior,
            limite_superior
        )

        return individuo


    poblacion = crear_poblacion()

    for generacion in range(num_generaciones):

        # Evaluar población
        fitness = evaluar_poblacion(poblacion)

        # Encontrar mejor individuo
        indice_mejor = np.argmin(fitness)

        mejor_individuo = poblacion[indice_mejor].copy()
        mejor_fitness = fitness[indice_mejor]

        # Mostrar información cada 10 generaciones
        if generacion % 10 == 0:

            print(
                f"Generación {generacion:3d} | "
                f"x1 = {mejor_individuo[0]:8.5f} | "
                f"x2 = {mejor_individuo[1]:8.5f} | "
                f"f(x) = {mejor_fitness:10.6f}"
            )

        # ----------------------------------------------------------
        # ELITISMO
        # ----------------------------------------------------------

        nueva_poblacion = [mejor_individuo]

        # ----------------------------------------------------------
        # CREAR NUEVA GENERACIÓN
        # ----------------------------------------------------------

        while len(nueva_poblacion) < tam_poblacion:

            # Selección
            padre1 = seleccion_torneo(
                poblacion,
                fitness
            )

            padre2 = seleccion_torneo(
                poblacion,
                fitness
            )

            # Cruce
            hijo1, hijo2 = cruce(
                padre1,
                padre2
            )

            # Mutación
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)

            nueva_poblacion.append(hijo1)

            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(hijo2)

        poblacion = np.array(nueva_poblacion)

    
    fitness = evaluar_poblacion(poblacion)

    indice_mejor = np.argmin(fitness)

    mejor = poblacion[indice_mejor]
    fitness_mejor = fitness_function(mejor)
    
    print("\n===================================")
    print("MEJOR SOLUCIÓN ENCONTRADA")
    print("===================================")

    print("x1 =", mejor[0])
    print("x2 =", mejor[1])
    print("f(x1,x2) =", fitness_mejor)    
    return fitness_mejor


# ==============================================================
# GRÁFICA DE LA FUNCIÓN OBJETIVO
# ==============================================================

def graficar_fitness_function(
    limite_inferior,
    limite_superior,
    fitness_function
):

    # Crear valores para x1 y x2
    x1 = np.linspace(limite_inferior, limite_superior, 200)
    x2 = np.linspace(limite_inferior, limite_superior, 200)

    # Crear una malla
    X1, X2 = np.meshgrid(x1, x2)

    # Evaluar la función objetivo en cada punto (2 variables)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):

            individuo = [X1[i, j], X2[i, j]]

            Z[i, j] = fitness_function(individuo)

    # Crear figura
    fig = plt.figure(figsize=(12, 8))

    # Crear gráfico 3D
    ax = fig.add_subplot(111, projection='3d')

    # Graficar superficie
    superficie = ax.plot_surface(
        X1,
        X2,
        Z,
        cmap='viridis',
        edgecolor='none',
        alpha=0.9
    )

    # Etiquetas
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x1, x2)')

    ax.set_title(
        f'Función {fitness_function.__name__} - Paisaje de búsqueda'
    )

    # Barra de colores
    fig.colorbar(
        superficie,
        ax=ax,
        shrink=0.6,
        label='f(x1, x2)'
    )

    plt.show()
