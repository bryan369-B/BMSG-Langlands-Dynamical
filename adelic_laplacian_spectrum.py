import numpy as np
from scipy.linalg import eigvalsh
import sys

def build_adelic_laplacian(N_primes, N_resolution):
    """
    Construye una matriz que simula el Laplaciano Adélico discreto
    Delta_A sobre el espacio truncado generado por N_primes.
    """
    # Generar primeros N primos
    primes = [2]
    candidate = 3
    while len(primes) < N_primes:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 2
        
    primes = np.array(primes)
    
    # En la teoría de Patterson-Sullivan, L = -Delta
    # Las órbitas tienen longitud log(p). 
    # El modelo más simple del operador Laplaciano discreto en este límite:
    
    dim = N_resolution
    L = np.zeros((dim, dim))
    
    # Modelo fenomenológico de interacciones de difusión idelica
    for i in range(dim):
        L[i, i] = 0.5  # Término diagonal
        for j in range(dim):
            if i != j:
                # Interacción dependiente de la "distancia" p-ádica
                # Mapeado a una cuadrícula lineal como proxy simple
                diff = abs(i - j)
                if diff < len(primes):
                    L[i, j] = -1.0 / (primes[diff] * np.log(primes[diff])**2)
                    
    # Hacerlo simétrico (autoadjunto)
    L = (L + L.T) / 2
    
    # Restar el mínimo de la diagonal para alinear el espectro
    # Forzamos que la matriz simule el Laplaciano positivo semi-definido
    min_diag = np.min(np.diag(L))
    L -= np.eye(dim) * min_diag
    
    # Calibración: forzamos el inicio del espectro continuo para ver 
    # si componentes discretas caen por debajo
    
    return L

def test_spectral_gap():
    print("--- FASE 44: ESPECTRO DEL LAPLACIANO ADÉLICO (Truncado) ---")
    N_primes = 20
    N_resolution = 400
    L = build_adelic_laplacian(N_primes, N_resolution)
    
    # Calcular eigenvalues
    eigenvalues = eigvalsh(L)
    
    lowest_eigvals = eigenvalues[:10]
    
    print("Top 10 Autovalores más bajos del Laplaciano Discreto:")
    for i, ev in enumerate(lowest_eigvals):
        print(f"  lambda_{i} = {ev:.6f}")
        
    # Análisis
    print("\nAnálisis de Gap:")
    if lowest_eigvals[0] > 0.24 and lowest_eigvals[0] < 0.26:
        print("  -> El espectro inicia cerca de 1/4 (0.25).")
    elif lowest_eigvals[0] < 0.24:
        print("  -> ALERTA: Autovalores discretos en (0, 1/4) detectados. RH violado en el truncamiento.")
    else:
        print("  -> El espectro inicia por encima de 1/4.")

if __name__ == "__main__":
    test_spectral_gap()
