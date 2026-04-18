import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import log, ceil

def simulate_selberg_violation(s0_assumed, max_k=20, p=2):
    """
    Simula la rotura de la cota de unitaridad de Jacquet-Shalika 
    bajo el levantamiento de potencia simétrica Sym^k de Langlands.
    """
    theta = s0_assumed - 0.5
    
    print(f"\n{'='*60}")
    print(f"ANALISIS DE ESTADO EXCEPCIONAL: s0 = {s0_assumed} (theta = {theta:.5f})")
    lam = s0_assumed * (1 - s0_assumed)
    print(f"Autovalor de Laplace asociado: lambda = {lam:.5f}")
    print(f"{'='*60}")

    if theta <= 0:
        print("[+] RESULTADO: Autovalor temperado/válido (lambda >= 1/4). No hay violación.")
        return None

    data = []
    k_break = None

    for k in range(1, max_k + 1):
        # El exponente del parámetro de Satake modificado es k * theta
        satake_exponent = k * theta
        
        # El límite absoluto de unitaridad local (Jacquet-Shalika en GL(N)) es p^(1/2)
        # Esto significa que el exponente máximo permitido es 0.5
        unitarity_bound_exponent = 0.5
        
        is_violated = satake_exponent > unitarity_bound_exponent
        
        data.append({
            "k (Sym^k)": k,
            "Grupo": f"GL({k+1})",
            "Parámetro Exponente (k*θ)": round(satake_exponent, 5),
            "Límite Unitaridad (0.5)": unitarity_bound_exponent,
            "Violación Jacquet-Shalika": "SÍ (COLAPSO)" if is_violated else "No"
        })
        
        if is_violated and k_break is None:
            k_break = k

    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    
    if k_break:
        print(f"\n[!] DICTAMEN MATEMÁTICO: La forma automorfa excepcional colapsa en k = {k_break}.")
        print(f"    Si Langlands Functoriality (Sym^{k_break}) es cierta, s0 = {s0_assumed} ES IMPOSIBLE.")
        print(f"    Esto demuestra computacionalmente por qué θ debe ser 0 bajo el levantamiento a GL(N).")
        
    return df, k_break

def plot_violations():
    # 1. Caso de la barrera de Selberg original (3/16), s0 = 0.75 -> theta = 0.25
    df1, kb1 = simulate_selberg_violation(s0_assumed=0.75)

    # 2. Caso de la cota de Kim-Sarnak (975/4096), s0 = 0.615 -> theta = 0.115
    df2, kb2 = simulate_selberg_violation(s0_assumed=0.615)

    # Gráfico del crecimiento
    k_vals = np.arange(1, 21)
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, k_vals * 0.25, 'b-o', label=r'$s_0=0.75$ (θ=0.25, Barrera Selberg)')
    plt.plot(k_vals, k_vals * 0.115, 'g-s', label=r'$s_0=0.615$ (θ=0.115, Cota Kim-Sarnak)')
    
    plt.axhline(y=0.5, color='r', linestyle='--', linewidth=2, label='Frontera de Unitaridad (Jacquet-Shalika)')
    plt.fill_between(k_vals, 0.5, max(k_vals * 0.25) + 0.1, color='red', alpha=0.1, label='Región Físicamente Prohibida')
    
    plt.xlabel('Potencia Simétrica k')
    plt.ylabel('Exponente de Satake Máximo $k \cdot \\theta$')
    plt.title('Violación de la Unitaridad Local en GL(k+1) bajo Langlands Sym$^k$')
    plt.legend()
    plt.grid(True)
    plt.xticks(k_vals)
    plt.savefig('symmetric_power_violation.png', dpi=300)
    print("\n[+] Gráfico guardado en 'symmetric_power_violation.png'.")

if __name__ == "__main__":
    plot_violations()
