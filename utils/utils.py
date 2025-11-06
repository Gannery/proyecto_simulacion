"Utilidades para los métodos de prueba de aleatoriedad"
import pandas as pd
import os
from tabulate import tabulate
from typing import List, Union, Tuple

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def table_up_down(resultados: dict):
    """Muestra las tablas detalladas de resultados"""
    print("\n" + "="*80)
    print("Tabla de números aleatorios usados:")
    print("="*80)
    print(resultados['tabla_numeros'].to_string(index=False))
    
    print("\n" + "="*80)
    print("Tabla de símbolos y corridas:")
    print("="*80)
    print(resultados['tabla_simbolos'].to_string(index=False))
    
    print("\n" + "="*80)
    print("Resumen:")
    print("="*80)
    print(f"Total de símbolos: {len(resultados['simbolos'])}")
    print(f"Corridas observadas: {resultados['Co']}")
    print(f"Corridas esperadas: {resultados['mu_Co']:.2f}")
    print(f"Desviación: {abs(resultados['Co'] - resultados['mu_Co']):.2f}")

def get_valid_seed() -> int:
    """
    Solicita al usuario una semilla válida (solo dígitos, cantidad par de dígitos).
    
    Returns:
        int: Semilla validada
    """
    while True:
        entrada_usuario = input("Ingresa el número semilla: ")
        
        if entrada_usuario.isdigit() and len(entrada_usuario) % 2 == 0:
            return int(entrada_usuario)
        else:
            print("Error: Debes ingresar solo números y que la cantidad de dígitos sea par.")

def get_alpha() -> float:
    "Devuelve el nivel de significancia ingresado por el usuario."
    significancia = {
        90: 0.10,
        95: 0.05,
        99: 0.01
    }
    while True:
        try:
            alpha = int(input("Ingrese el nivel de significancia (90%, 95%, 99%): "))
            if alpha in significancia:
                return significancia[alpha]
            else:
                print("Error: El nivel de significancia debe ser alguno de: 90%, 95%, 99%.")
        except ValueError:
            print("Error: Entrada inválida. Por favor ingrese un número entero entre válido.")

def get_n_kolgomorov() -> int:
    "Devuelve la cantidad de números aleatorios a generar, máximo 20 números."
    while True:
        try:
            n = int(input("Ingrese la cantidad de números aleatorios a generar (máximo 20): "))
            if n > 0 and n <= 20:
                return n
            else:
                print("Error: La cantidad de números debe ser mayor a 1 y menor o igual a 20.")
        except ValueError:
            print("Error: Entrada inválida. Por favor ingrese un número entero válido.")

def get_n() -> int:
    """Devuelve la cantidad de números aleatorios a generar"""
    while True:
        try:
            n = int(input("Ingrese la cantidad de números aleatorios a generar: "))
            if 1 < n:
                return n
            else:
                print("Error: La cantidad debe ser mayor a 1.")
        except ValueError:
            print("Error: Entrada inválida. Por favor ingrese un número entero válido.")

def show_generator_table(
        numeros: List[float], 
        metodo: str, 
        semilla: Union[int, str, Tuple[int, int]], 
        parametros: dict):
    """
    Muestra los resultados de un generador en formato tabla
    
    Args:
        numeros: Lista de números generados
        metodo: Nombre del método usado
        semilla: Semilla(s) utilizada(s)
        parametros: Diccionario con parámetros adicionales
    """
    print("\n" + "=" * 80)
    print(f"Resultados - {metodo.upper()}")
    print("=" * 80)
    
    info = [
        ["Método", metodo],
        ["Semilla(s)", semilla],
    ]
    for key, value in parametros.items():
        info.append([key, value])
    
    print(tabulate(info, tablefmt="fancy_grid"))
    
    print("\nNúmeros generados:")
    df = pd.DataFrame({
        'i': range(1, len(numeros) + 1),
        'Número (ri)': [f"{num:.6f}" for num in numeros]
    })
    print(tabulate(df.to_dict('records'), headers='keys', tablefmt='fancy_grid', showindex=False))
    
    print("\nEstadísticas:")
    stats = [
        ["Media", f"{sum(numeros)/len(numeros):.6f}"],
        ["Mínimo", f"{min(numeros):.6f}"],
        ["Máximo", f"{max(numeros):.6f}"],
        ["Cantidad", len(numeros)]
    ]
    print(tabulate(stats, tablefmt="fancy_grid"))
    print("=" * 80)

def show_test_results(resultados: dict, nombre_prueba: str):
    """
    Muestra los resultados de una prueba estadística
    
    Args:
        resultados: Diccionario con resultados de la prueba
        nombre_prueba: Nombre de la prueba realizada
    """
    print("\n" + "=" * 80)
    print(f"Resultados - Prueba de {nombre_prueba.upper()}")
    print("=" * 80)
    
    print(f"\nInformación General:")
    info_general = [
        ["Cantidad de números (n)", resultados.get('n', 'N/A')],
        ["Nivel de significancia (α)", resultados.get('alpha', 'N/A')],
    ]
    print(tabulate(info_general, tablefmt="fancy_grid"))
    
    # Resultados específicos según el tipo de prueba
    if nombre_prueba == "Chi-Cuadrada":
        mostrar_chi_cuadrada(resultados)
    elif nombre_prueba == "Kolmogorov-Smirnov":
        mostrar_kolmogorov(resultados)
    elif "Corridas" in nombre_prueba:
        mostrar_corridas(resultados)
    elif nombre_prueba == "Huecos":
        mostrar_huecos(resultados)
    
    print("\n" + "=" * 80)
    print("Conclusión:")
    print("=" * 80)
    
    aceptado = resultados.get('aceptado', False)
    conclusion = resultados.get('conclusion', 'No disponible')
    
    if aceptado:
        print(f"{conclusion}")
    else:
        print(f"{conclusion}")
    
    print("=" * 80)

def mostrar_chi_cuadrada(resultados: dict):
    """Muestra resultados específicos de Chi-Cuadrada"""
    print(f"\nEstadísticos:")
    stats = [
        ["Chi-cuadrado calculado (x²)", f"{resultados.get('chi_cuadrado', 0):.6f}"],
        ["Chi-cuadrado crítico", f"{resultados.get('chi_critico', 0):.6f}"],
        ["Grados de libertad", resultados.get('grados_libertad', 'N/A')],
    ]
    print(tabulate(stats, tablefmt="fancy_grid"))
    
    if 'tabla_frecuencias' in resultados:
        print("\nTabla de Frecuencias:")
        print(tabulate(resultados['tabla_frecuencias'], headers='keys', tablefmt='fancy_grid', showindex=False))

def mostrar_kolmogorov(resultados: dict):
    """Muestra resultados específicos de Kolmogorov-Smirnov"""
    print(f"\nEstadísticos:")
    stats = [
        ["D+ (máxima diferencia positiva)", f"{resultados.get('D_plus', 0):.6f}"],
        ["D- (máxima diferencia negativa)", f"{resultados.get('D_minus', 0):.6f}"],
        ["D (estadístico de prueba)", f"{resultados.get('D', 0):.6f}"],
        ["D crítico", f"{resultados.get('D_critico', 0):.6f}"],
    ]
    print(tabulate(stats, tablefmt="fancy_grid"))
    
    if 'tabla_completa' in resultados:
        print("\nTabla Detallada:")
        print(tabulate(resultados['tabla_completa'], headers='keys', tablefmt='fancy_grid', showindex=False))

def mostrar_corridas(resultados: dict):
    """Muestra resultados específicos de pruebas de corridas"""
    print(f"\nEstadísticos:")
    stats = [
        ["Corridas observadas (Co)", resultados.get('Co', 'N/A')],
        ["Corridas esperadas", f"{resultados.get('mu_Co', 0):.4f}"],
        ["Desviación estándar", f"{resultados.get('sigma_Co', 0):.4f}"],
        ["Estadístico Z₀", f"{resultados.get('Z0', 0):.4f}"],
        ["Valor crítico Z", f"{resultados.get('Z_critico', 0):.4f}"],
    ]
    
    if 'n0' in resultados:  # Para corridas de la media
        stats.insert(1, ["Números debajo (n₀)", resultados['n0']])
        stats.insert(2, ["Números arriba (n₁)", resultados['n1']])
    
    print(tabulate(stats, tablefmt="fancy_grid"))
    
    if 'tabla' in resultados:
        print("\nTabla Detallada:")
        print(tabulate(resultados['tabla'], headers='keys', tablefmt='fancy_grid', showindex=False))
    elif 'tabla_simbolos' in resultados:
        print("\nTabla de Símbolos:")
        print(tabulate(resultados['tabla_simbolos'], headers='keys', tablefmt='fancy_grid', showindex=False))

def mostrar_huecos(resultados: dict):
    """Muestra resultados específicos de prueba de huecos"""
    print(f"\nEstadísticos:")
    stats = [
        ["Chi-cuadrado calculado (x²)", f"{resultados.get('chi_cuadrado', 0):.6f}"],
        ["Chi-cuadrado crítico", f"{resultados.get('chi_critico', 0):.6f}"],
        ["Grados de libertad", resultados.get('grados_libertad', 'N/A')],
        ["Total de huecos", resultados.get('total_huecos', 'N/A')],
    ]
    print(tabulate(stats, tablefmt="fancy_grid"))
    
    if 'tabla_huecos' in resultados:
        print("\nDistribución de Huecos:")
        print(tabulate(resultados['tabla_huecos'], headers='keys', tablefmt='fancy_grid', showindex=False))
