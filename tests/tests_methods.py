"""Módulo de pruebas estadísticas para números aleatorios."""
import numpy as np
import pandas as pd
from typing import Optional
from scipy import stats
from collections import Counter

class TestMethods():
    
    def up_down_method(self, numeros=None, n=20, alpha=0.05, seed=None) -> dict:
        """
        Prueba de Corridas Arriba y Abajo
        
        Compara cada número con el anterior para determinar si sube o baja.
        Cuenta las corridas (secuencias de subidas o bajadas consecutivas).
        
        Args:
            numeros: Lista de números a probar (opcional)
            n: int - Cantidad de números a generar si numeros es None
            alpha: float - Nivel de significancia (default: 0.05)
            seed: int - Semilla para reproducibilidad (opcional)
        
        Returns:
            dict: con todos los resultados de la prueba
        """
        
        if numeros is None:
            if seed is not None:
                np.random.seed(seed)
            numeros = np.random.uniform(0, 1, n)
        else:
            numeros = np.array(numeros)
            n = len(numeros)
        
        simbolos = []
        for i in range(1, n):
            if numeros[i] > numeros[i-1]:
                simbolos.append('+')  # Sube
            else:
                simbolos.append('-')  # Baja
        
        # Contar corridas
        Co = 1  
        for i in range(1, len(simbolos)):
            if simbolos[i] != simbolos[i-1]:
                Co += 1
        
        mu_Co = (2 * n - 1) / 3
        varianza_Co = (16 * n - 29) / 90
        sigma_Co = np.sqrt(varianza_Co)
        
        Z0 = abs(Co - mu_Co) / sigma_Co
        
        Z_critico = stats.norm.ppf(1 - alpha/2)
        
        if abs(Z0) < Z_critico:
            resultado = "Se acepta hipótesis"
            conclusion = "Los números son aleatorios"
            aceptado = True
        else:
            resultado = "Se rechaza la hipótesis"
            conclusion = "Los números no son aleatorios"
            aceptado = False
        
        df_numeros = pd.DataFrame({
            'i': range(1, n+1),
            'Número (ri)': [f"{num:.6f}" for num in numeros]
        })
        
        comparaciones = []
        for i in range(1, n):
            if numeros[i] > numeros[i-1]:
                comparaciones.append(f"{numeros[i]:.4f} > {numeros[i-1]:.4f}")
            else:
                comparaciones.append(f"{numeros[i]:.4f} ≤ {numeros[i-1]:.4f}")
        
        df_simbolos = pd.DataFrame({
            'i': range(2, n+1),
            'Comparación': comparaciones,
            'Símbolo': simbolos
        })
        
        corridas = ['Corrida 1']
        corrida_actual = 1
        for i in range(1, len(simbolos)):
            if simbolos[i] != simbolos[i-1]:
                corrida_actual += 1
            corridas.append(f'Corrida {corrida_actual}')
        df_simbolos['Corrida'] = corridas
        
        return {
            'numeros': numeros,
            'n': n,
            'simbolos': simbolos,
            'Co': Co,
            'mu_Co': mu_Co,
            'varianza_Co': varianza_Co,
            'sigma_Co': sigma_Co,
            'Z0': Z0,
            'Z_critico': Z_critico,
            'alpha': alpha,
            'aceptado': aceptado,
            'conclusion': conclusion,
            'resultado': resultado,
            'tabla_numeros': df_numeros,
            'tabla_simbolos': df_simbolos
        }
    
    def up_down_average(self, numeros=None, n=20, alpha=0.05, seed=None) -> dict:
        """
        Prueba de Corridas Arriba y Abajo de la Media
        
        Args:
            numeros: Lista de números a probar (opcional)
            n: int - Cantidad de números a generar si numeros es None
            alpha: float - Nivel de significancia (default: 0.05)
            seed: int - Semilla para reproducibilidad (opcional)
        
        Returns:
            dict: con todos los resultados de la prueba
        """
        
        if numeros is None:
            if seed is not None:
                np.random.seed(seed)
            numeros = np.random.uniform(0, 1, n)
        else:
            numeros = np.array(numeros)
            n = len(numeros)
        
        media = np.mean(numeros)        
        S = (numeros >= media).astype(int)
        
        n0 = np.sum(S == 0)  # Números debajo de la media
        n1 = np.sum(S == 1)  # Números arriba de la media
        
        Co = 1  # Primera corrida
        for i in range(1, n):
            if S[i] != S[i-1]:
                Co += 1
                
        mu_Co = (2 * n0 * n1) / n + 0.5
        varianza_Co = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n**2 * (n - 1))
        sigma_Co = np.sqrt(varianza_Co)
        
        Z0 = abs(Co - mu_Co) / sigma_Co
        
        Z_critico = stats.norm.ppf(1 - alpha/2)
        
        if abs(Z0) < Z_critico:
            resultado = "Se acepta hipótesis"
            conclusion = "Los números son aleatorios"
            aceptado = True
        else:
            resultado = "Se rechaza la hipótesis"
            conclusion = "Los números no son aleatorios"
            aceptado = False
        
        df = pd.DataFrame({
            'i': range(1, n+1),
            'Número (ri)': [f"{num:.6f}" for num in numeros],
            'S': S,
            'Posición': ['Debajo' if s == 0 else 'Arriba' for s in S]
        })
        
        corridas = ['Corrida 1']
        corrida_actual = 1
        for i in range(1, n):
            if S[i] != S[i-1]:
                corrida_actual += 1
            corridas.append(f'Corrida {corrida_actual}')
        df['Corrida'] = corridas
        
        return {
            'numeros': numeros,
            'n': n,
            'media': media,
            'S': S,
            'n0': n0,
            'n1': n1,
            'Co': Co,
            'mu_Co': mu_Co,
            'varianza_Co': varianza_Co,
            'sigma_Co': sigma_Co,
            'Z0': Z0,
            'Z_critico': Z_critico,
            'alpha': alpha,
            'aceptado': aceptado,
            'conclusion': conclusion,
            'resultado': resultado,
            'tabla': df
        }
    
    def kolgomorov_method(self, numeros=None, alpha=0.05, n=20) -> dict:
        """
        Realiza la prueba de Kolmogorov-Smirnov para uniformidad en [0,1].

        Args:
            numeros: Lista de números a probar (opcional)
            alpha: float - Nivel de significancia
            n: int - Cantidad de números a generar si numeros es None
            
        Returns:
            dict: con todos los resultados de la prueba
        """
        
        if numeros is None:
            numeros = np.random.uniform(0, 1, n)
        else:
            numeros = np.array(numeros)
            n = len(numeros)
            
        num_ordenados = np.sort(numeros)

        i_n = np.arange(1, n + 1) / n
        i_n_1 = np.arange(0, n) / n
        
        D_plus = np.max(i_n - num_ordenados)
        D_minus = np.max(num_ordenados - i_n_1)  
        D = max(D_plus, D_minus) 

        valores_criticos = {
            0.10: 1.22 / np.sqrt(n),
            0.05: 1.36 / np.sqrt(n),
            0.01: 1.63 / np.sqrt(n)
        }
        D_critico = valores_criticos[alpha]
        
        aceptado = D < D_critico
        conclusion = "Los números son uniformes" if aceptado else "Los números no son uniformes"
        
        tabla = pd.DataFrame({
            'i': range(1, n + 1),
            'ri': [f"{num:.6f}" for num in numeros],
            'ri ordenado': [f"{num:.6f}" for num in num_ordenados],
            'i/n': [f"{val:.6f}" for val in i_n],
            '(i-1)/n': [f"{val:.6f}" for val in i_n_1]
        })

        return {
            "numeros_generados": numeros,
            "numeros_ordenados": num_ordenados,
            "i_n": i_n,
            "i_n_1": i_n_1,
            "D_plus": D_plus,
            "D_minus": D_minus,
            "D": D,
            "D_critico": D_critico,
            "alpha": alpha,
            "n": n,
            "aceptado": aceptado,
            "conclusion": conclusion,
            "tabla_completa": tabla
        }
    
    def chi_squared_test(self, numeros=None, n=20, alpha=0.05, intervalos=5) -> dict:
        """
        Prueba Chi-Cuadrada para uniformidad
        
        Args:
            numeros: Lista de números a probar (opcional)
            n: int - Cantidad de números a generar si numeros es None
            alpha: float - Nivel de significancia
            intervalos: int - Número de intervalos (default: 5)
            
        Returns:
            dict: con todos los resultados de la prueba
        """
        
        if numeros is None:
            numeros = np.random.uniform(0, 1, n)
        else:
            numeros = np.array(numeros)
            n = len(numeros)
        
        fe = n / intervalos
        
        bins = np.linspace(0, 1, intervalos + 1)
        fo, _ = np.histogram(numeros, bins=bins)
        
        chi_cuadrado = np.sum(((fo - fe) ** 2) / fe)
        
        grados_libertad = intervalos - 1
        
        chi_critico = stats.chi2.ppf(1 - alpha, grados_libertad)
        
        aceptado = chi_cuadrado < chi_critico
        conclusion = "Los números son uniformes" if aceptado else "Los números no son uniformes"
        
        tabla_freq = pd.DataFrame({
            'Intervalo': [f"[{bins[i]:.2f}, {bins[i+1]:.2f})" for i in range(intervalos)],
            'FO (Observada)': fo,
            'FE (Esperada)': [fe] * intervalos,
            '(FO-FE)²/FE': [((o - fe) ** 2) / fe for o in fo]
        })
        
        return {
            'numeros': numeros,
            'n': n,
            'intervalos': intervalos,
            'chi_cuadrado': chi_cuadrado,
            'chi_critico': chi_critico,
            'grados_libertad': grados_libertad,
            'alpha': alpha,
            'aceptado': aceptado,
            'conclusion': conclusion,
            'tabla_frecuencias': tabla_freq,
            'fo': fo,
            'fe': fe
        }
    
    def gap_test(self, numeros=None, n=20, alpha=0.05, a=0.3, b=0.7) -> dict:
        """
        Prueba de Huecos (Gap Test)
        
        Mide la longitud de huecos entre números que caen en un intervalo [a, b]
        
        Args:
            numeros: Lista de números a probar (opcional)
            n: int - Cantidad de números a generar si numeros es None
            alpha: float - Nivel de significancia
            a: float - Límite inferior del intervalo (default: 0.3)
            b: float - Límite superior del intervalo (default: 0.7)
            
        Returns:
            dict: con todos los resultados de la prueba
        """
        
        if numeros is None:
            numeros = np.random.uniform(0, 1, n)
        else:
            numeros = np.array(numeros)
            n = len(numeros)
        
        # Probabilidad de estar en el intervalo
        p = b - a
        
        huecos = []
        hueco_actual = 0
        
        for num in numeros:
            if a <= num < b:
                huecos.append(hueco_actual)
                hueco_actual = 0
            else:
                hueco_actual += 1
        
        if len(huecos) == 0:
            return {
                'numeros': numeros,
                'n': n,
                'alpha': alpha,
                'aceptado': False,
                'conclusion': "No se encontraron suficientes huecos para la prueba",
                'a': a,
                'b': b,
                'p': p,
                'total_huecos': 0
            }
        
        contador_huecos = Counter(huecos)
        max_hueco = max(contador_huecos.keys()) if contador_huecos else 0
        
        # Agrupar huecos grandes en una categoría "≥4"
        categorias_num = list(range(min(4, max_hueco + 1)))
        if max_hueco >= 4:
            categorias_num.append(4)  # Usamos 4 para los cálculos de ≥4
        
        # Lista de etiquetas para mostrar
        categorias_str = [str(i) for i in categorias_num]
        if max_hueco >= 4:
            categorias_str[-1] = "≥4"
        
        fo = []
        fe = []
        for i, (cat_num, cat_str) in enumerate(zip(categorias_num, categorias_str)):
            if cat_str == "≥4":
                fo_val = sum(count for gap, count in contador_huecos.items() if gap >= 4)
                fe_val = len(huecos) * ((1 - p) ** 4)
            else:
                fo_val = contador_huecos.get(cat_num, 0)
                fe_val = len(huecos) * p * ((1 - p) ** cat_num)
            
            fo.append(fo_val)
            fe.append(fe_val)
        
        chi_cuadrado = sum(((o - e) ** 2) / e if e > 0 else 0 for o, e in zip(fo, fe))
        grados_libertad = len(categorias_num) - 1
        chi_critico = stats.chi2.ppf(1 - alpha, grados_libertad)
        
        aceptado = chi_cuadrado < chi_critico
        conclusion = "Los números son independientes" if aceptado else "Los números no son independientes"
        
        tabla = pd.DataFrame({
            'Longitud Hueco': categorias_str,
            'FO (Observada)': fo,
            'FE (Esperada)': [f"{e:.4f}" for e in fe],
            '(FO-FE)²/FE': [f"{((o - e) ** 2) / e if e > 0 else 0:.4f}" for o, e in zip(fo, fe)]
        })
        
        return {
            'numeros': numeros,
            'n': n,
            'alpha': alpha,
            'a': a,
            'b': b,
            'p': p,
            'huecos': huecos,
            'total_huecos': len(huecos),
            'chi_cuadrado': chi_cuadrado,
            'chi_critico': chi_critico,
            'grados_libertad': grados_libertad,
            'aceptado': aceptado,
            'conclusion': conclusion,
            'tabla_huecos': tabla
        }
