"""
Proyecto: Generador y Pruebas de Números Aleatorios
Menú principal para interactuar con generadores y métodos de prueba
"""
from random_number_generators import RandomGenerators
from tests import TestMethods
from utils import (
    get_valid_seed, get_alpha, show_generator_table, 
    clear_screen, show_test_results, get_n, get_n_kolgomorov
)
from tabulate import tabulate
import sys

from utils.utils import get_n_kolgomorov

class MenuPrincipal:
    def __init__(self):
        self.generadores = RandomGenerators()
        self.pruebas = TestMethods()
        self.numeros_generados = None
        self.metodo_usado = None
        self.semilla_actual = None
        
    def show_main_menu(self):
        """Muestra el menú principal del programa"""
        clear_screen()
        print("=" * 60)
        print("### Bienvenido al Generador de Números Aleatorios ###")
        print("=" * 60)
        print("Escoge una opción:")
        print("1. Método de cuadrados medios")
        print("2. Productos medios")
        print("3. Multiplicador constante")
        print("4. Algoritmo lineal")
        print("5. Probar los métodos (Submenú)")
        print("6. Salir")
        print("=" * 60)
        
    def execute_mean_squares(self):
        """Ejecuta el método de cuadrados medios"""
        print("\n--- Método de Cuadrados Medios ---")
        semilla = get_valid_seed()
        cantidad = get_n()
        
        self.numeros_generados = self.generadores.mean_squares(semilla, cantidad)
        self.metodo_usado = "Cuadrados Medios"
        self.semilla_actual = semilla
        
        show_generator_table(
            numeros=self.numeros_generados,
            metodo="Cuadrados Medios",
            semilla=semilla,
            parametros={"Cantidad": cantidad}
        )
        
    def execute_middle_product(self):
        """Ejecuta el método de productos medios"""
        print("\n--- Método de Productos Medios ---")
        print("Se necesitan dos semillas con la misma cantidad de dígitos")
        semilla_1 = get_valid_seed()
        semilla_2 = get_valid_seed()
        cantidad = get_n()
        
        self.numeros_generados = self.generadores.middle_product(semilla_1, semilla_2, cantidad)
        self.metodo_usado = "Productos Medios"
        self.semilla_actual = (semilla_1, semilla_2)
        
        show_generator_table(
            numeros=self.numeros_generados,
            metodo="Productos Medios",
            semilla=f"{semilla_1}, {semilla_2}",
            parametros={"Cantidad": cantidad}
        )
        
    def execute_constant_multiplier(self):
        """Ejecuta el método de multiplicador constante"""
        print("\n--- Método de Multiplicador Constante ---")
        print("Se necesitan dos semillas con la misma cantidad de dígitos")
        semilla_1 = get_valid_seed()
        semilla_2 = get_valid_seed()
        cantidad = get_n()
        
        self.numeros_generados = self.generadores.constant_multiplier(semilla_1, semilla_2, cantidad)
        self.metodo_usado = "Multiplicador Constante"
        self.semilla_actual = (semilla_1, semilla_2)
        
        show_generator_table(
            numeros=self.numeros_generados,
            metodo="Multiplicador Constante",
            semilla= f"{semilla_1}, {semilla_2}",
            parametros={"Cantidad": cantidad}
        )
        
    def execute_linear_algorithm(self):
        """Ejecuta el algoritmo lineal congruencial"""
        print("\n--- Algoritmo Lineal Congruencial ---")
        semilla = int(input("Ingresa la semilla (X0): "))
        a = int(input("Ingresa el multiplicador (a): "))
        c = int(input("Ingresa el incremento (c): "))
        m = int(input("Ingresa el módulo (m): "))
        cantidad = get_n()
        
        self.numeros_generados = self.generadores.linear_algorithm(semilla, a, c, m, cantidad)
        self.metodo_usado = "Algoritmo Lineal"
        self.semilla_actual = semilla
        
        show_generator_table(
            numeros=self.numeros_generados,
            metodo="Algoritmo Lineal Congruencial",
            semilla=semilla,
            parametros={"a": a, "c": c, "m": m, "Cantidad": cantidad}
        )
        
    def show_test_submenu(self):
        """Muestra el submenú de pruebas"""
        while True:
            clear_screen()
            print("=" * 60)
            print("### Menú de pruebas estadísticas ###")
            print("=" * 60)
            
            if self.numeros_generados:
                print(f"Números generados disponibles: {len(self.numeros_generados)}")
                print(f"Método usado: {self.metodo_usado}")
            else:
                print("No hay números generados. Se usarán números aleatorios.")
            
            print("\n-- UNIFORMIDAD --")
            print("1. Prueba Chi-Cuadrada (x²)")
            print("2. Prueba Kolmogorov-Smirnov (KS)")
            print("\n-- ALEATORIEDAD --")
            print("3. Prueba de corridas arriba y abajo")
            print("4. Prueba de corridas arriba y abajo de la media")
            print("\n-- INDEPENDENCIA --")
            print("5. Prueba de huecos")
            print("\n6. Volver al menú principal")
            print("=" * 60)
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.execute_chi_square()
            elif opcion == "2":
                self.execute_kolmogorov()
            elif opcion == "3":
                self.execute_up_down()
            elif opcion == "4":
                self.execute_up_down_average()
            elif opcion == "5":
                self.execute_gaps()
            elif opcion == "6":
                break
            else:
                print("Opción inválida")
                input("Presiona Enter para continuar...")
                
    def execute_chi_square(self):
        """Ejecuta la prueba Chi-Cuadrada"""
        print("\n--- Prueba Chi-Cuadrada (x²) ---")
        alpha = get_alpha()
        
        if self.numeros_generados:
            usar_generados = input("¿Usar números ya generados? (s/n): ").lower()
            numeros = self.numeros_generados if usar_generados == 's' else None
        else:
            numeros = None
            
        n = len(numeros) if numeros else get_n()
        
        resultados = self.pruebas.chi_squared_test(numeros=numeros, n=n, alpha=alpha)
        show_test_results(resultados, "Chi-Cuadrada")
        input("\nPresiona Enter para continuar...")
        
    def execute_kolmogorov(self):
        """Ejecuta la prueba Kolmogorov-Smirnov"""
        print("\n--- Prueba Kolmogorov-Smirnov ---")
        alpha = get_alpha()
        
        if self.numeros_generados and len(self.numeros_generados) > 20:
            print("ERROR: El método Kolmogorov-Smirnov solo soporta máximo 20 números.")
            print("Por favor, genera una nueva secuencia con 20 o menos números.")
            input("Presiona Enter para continuar...")
            return
            
        if self.numeros_generados:
            usar_generados = input("¿Usar números ya generados? (s/n): ").lower()
            numeros = self.numeros_generados if usar_generados == 's' else None
        else:
            numeros = None
            
        n = len(numeros) if numeros else get_n_kolgomorov()
        
        if n > 20:
            print("ERROR: Solo se permiten máximo 20 números. Usando 20 por defecto.")
            n = 20
            
        resultados = self.pruebas.kolgomorov_method(numeros=numeros, alpha=alpha, n=n)
        show_test_results(resultados, "Kolmogorov-Smirnov")
        input("\nPresiona Enter para continuar...")
        
    def execute_up_down(self):
        """Ejecuta la prueba de corridas arriba y abajo"""
        print("\n--- Prueba de Corridas Arriba y Abajo ---")
        alpha = get_alpha()
        
        if self.numeros_generados:
            usar_generados = input("¿Usar números ya generados? (s/n): ").lower()
            numeros = self.numeros_generados if usar_generados == 's' else None
        else:
            numeros = None
            
        n = len(numeros) if numeros else get_n()
        
        resultados = self.pruebas.up_down_method(numeros=numeros, n=n, alpha=alpha)
        show_test_results(resultados, "Corridas Arriba y Abajo")
        input("\nPresiona Enter para continuar...")
        
    def execute_up_down_average(self):
        """Ejecuta la prueba de corridas arriba y abajo de la media"""
        print("\n--- Prueba de Corridas Arriba y Abajo de la Media ---")
        alpha = get_alpha()
        
        if self.numeros_generados:
            usar_generados = input("¿Usar números ya generados? (s/n): ").lower()
            numeros = self.numeros_generados if usar_generados == 's' else None
        else:
            numeros = None
            
        n = len(numeros) if numeros else get_n()
        
        resultados = self.pruebas.up_down_average(numeros=numeros, n=n, alpha=alpha)
        show_test_results(resultados, "Corridas Arriba y Abajo de la Media")
        input("\nPresiona Enter para continuar...")
        
    def execute_gaps(self):
        """Ejecuta la prueba de huecos"""
        print("\n--- Prueba de Huecos ---")
        alpha = get_alpha()
        
        if self.numeros_generados:
            usar_generados = input("¿Usar números ya generados? (s/n): ").lower()
            numeros = self.numeros_generados if usar_generados == 's' else None
        else:
            numeros = None
            
        n = len(numeros) if numeros else get_n()
        
        resultados = self.pruebas.gap_test(numeros=numeros, n=n, alpha=alpha)
        show_test_results(resultados, "Huecos")
        input("\nPresiona Enter para continuar...")
        
    def execute(self):
        """Ejecuta el programa principal"""
        while True:
            self.show_main_menu()
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.execute_mean_squares()
                input("\nPresiona Enter para continuar...")
            elif opcion == "2":
                self.execute_middle_product()
                input("\nPresiona Enter para continuar...")
            elif opcion == "3":
                self.execute_constant_multiplier()
                input("\nPresiona Enter para continuar...")
            elif opcion == "4":
                self.execute_linear_algorithm()
                input("\nPresiona Enter para continuar...")
            elif opcion == "5":
                self.show_test_submenu()
            elif opcion == "6":
                print("\nBye.")
                sys.exit(0)
            else:
                print("Opción inválida. Por favor intenta de nuevo.")
                input("Presiona Enter para continuar...")


def main():
    """Función principal del programa"""
    try:
        menu = MenuPrincipal()
        menu.execute()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        input("Presiona Enter para salir...")
        sys.exit(1)


if __name__ == "__main__":
    main()
