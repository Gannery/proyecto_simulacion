""" Módulo que contiene diferentes métodos para generar números pseudoaleatorios. """
from typing import List

class RandomGenerators():
    
    def __init__(self) -> None:
        pass

    def linear_algorithm(self, semilla: int, a: int, c: int, m: int, cantidad_numeros: int) -> List:
        """
        Genera una lista de números pseudoaleatorios usando el método de algoritmo lineal.

        Args:
            semilla (int): Semilla inicial
            a (int): Multiplicador
            c (int): Incremento
            m (int): Módulo
            cantidad_numeros (int): Cantidad de números a generar

        returns: 
            list: Lista de números pseudoaleatorios entre 0 y 1
        """
        secuencia_aleatoria = []

        for _ in range(cantidad_numeros):
            nueva_semilla = (a * semilla + c) % m
            numero_normalizado = nueva_semilla / m
            secuencia_aleatoria.append(numero_normalizado)

            semilla = nueva_semilla
        return secuencia_aleatoria
    
    def mean_squares(self, semilla_inicial: int, cantidad_numeros: int) -> List:
        """
        Genera una lista de números pseudoaleatorios usando el método de cuadrados medios.
        
        Args:
            semilla_inicial (int): Semilla inicial con cantidad par de dígitos
            cantidad_numeros (int): Cantidad de números a generar
        
        Returns:
            list: Lista de números pseudoaleatorios entre 0 y 1
        """
        secuencia_aleatoria = []
        valor_actual = semilla_inicial
        longitud_digitos = len(str(semilla_inicial))
        
        for i in range(cantidad_numeros):
            cuadrado = valor_actual ** 2
            cuadrado_str = str(cuadrado).zfill(2 * longitud_digitos)
            
            # Extraer los dígitos del medio
            punto_medio = len(cuadrado_str) // 2
            inicio = punto_medio - longitud_digitos // 2
            fin = punto_medio + longitud_digitos // 2
            digitos_medios = cuadrado_str[inicio:fin]
            
            # Actualizar valor actual y normalizar
            valor_actual = int(digitos_medios)
            numero_normalizado = valor_actual / (10 ** longitud_digitos)
            secuencia_aleatoria.append(numero_normalizado)
        
        return secuencia_aleatoria
    
    def constant_multiplier(self, semilla_1: int, semilla_2: int, cantidad_numeros: int) -> List:
        """
        Genera una lista de números pseudoaleatorios usando el método de multiplicador constante.
        
        Args:
            semilla_1 (int): Primera semilla con cantidad par de dígitos
            semilla_2 (int): Segunda semilla con cantidad par de dígitos
            cantidad_numeros (int): Cantidad de números a generar
        
        Returns:
            list: Lista de números pseudoaleatorios entre 0 y 1
        """
        secuencia_aleatoria = []
        longitud_digitos = len(str(semilla_1))
        
        for i in range(cantidad_numeros):
            producto = semilla_1 * semilla_2
            e = str(producto).zfill(2 * longitud_digitos)
            
            # Extraer los dígitos del medio
            inicio = (len(e) // 2) - (longitud_digitos // 2)
            fin = inicio + longitud_digitos
            digitos_medios = e[inicio:fin]

            nueva_semilla = int(digitos_medios)
            numero_normalizado = nueva_semilla / (10 ** longitud_digitos)
            secuencia_aleatoria.append(numero_normalizado)
            
            # Actualizar valores de las semillas
            semilla_2 = nueva_semilla
        
        return secuencia_aleatoria
    
    def middle_product(self, semilla_1: int, semilla_2: int, cantidad_numeros: int) -> List:
        """
        Genera una lista de números pseudoaleatorios usando el método de productos medios.
        
        Args:
            semilla_1 (int): Primera semilla con cantidad par de dígitos
            semilla_2 (int): Segunda semilla con cantidad par de dígitos
            cantidad_numeros (int): Cantidad de números a generar
        
        Returns:
            list: Lista de números pseudoaleatorios entre 0 y 1
        """
        secuencia_aleatoria = []
        longitud_digitos = len(str(semilla_1))
        
        for i in range(cantidad_numeros):
            producto = semilla_1 * semilla_2
            e = str(producto).zfill(2 * longitud_digitos)
            
            # Extraer los dígitos del medio
            inicio = (len(e) // 2) - (longitud_digitos // 2)
            fin = inicio + longitud_digitos
            digitos_medios = e[inicio:fin]

            nueva_semilla = int(digitos_medios)
            numero_normalizado = nueva_semilla / (10 ** longitud_digitos)
            secuencia_aleatoria.append(numero_normalizado)
            
            # Actualizar valores de las semillas
            semilla_1, semilla_2 = semilla_2, nueva_semilla
        
        return secuencia_aleatoria