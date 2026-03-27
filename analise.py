import pandas as pd
import numpy as np

# 1. CÁLCULOS TEÓRICOS
# Matriz de transição P
P = np.array([
    [0.6, 0.3, 0.1],
    [0.2, 0.6, 0.2],
    [0.1, 0.3, 0.6]
])

# Para encontrar o vetor estacionário (pi), resolvemos pi * P = pi e sum(pi) = 1
# Transformando em sistema linear: pi * (P - I) = 0
A = np.transpose(P) - np.identity(3)
A = np.vstack([A, np.ones(3)]) # Adiciona a restrição de que a soma das probabilidades é 1
b = np.array([0, 0, 0, 1])

# Resolve o sistema linear usando mínimos quadrados
pi_teorico = np.linalg.lstsq(A, b, rcond=None)[0]

# Taxas em Mbps
taxas_mbps = np.array([0, 10, 50])
vazao_teorica_mbps = np.sum(pi_teorico * taxas_mbps)

# 2. CÁLCULOS EXPERIMENTAIS (Lendo o CSV)
try:
    df = pd.read_csv('dados_coletados.csv')
    
    passos_totais = len(df)
    epoca_segundos = 5
    tempo_total = passos_totais * epoca_segundos
    
    # Garante que os estados sejam tratados como inteiros
    df['Estado'] = df['Estado'].astype(int)
    
    # Proporção de tempo em cada estado (Frequência)
    contagem_estados = df['Estado'].value_counts(normalize=True)
    pi_experimental = np.array([contagem_estados.get(i, 0) for i in range(3)])
    
    # Tempo total em cada estado
    tempo_por_estado = pi_experimental * tempo_total
    
    # Cálculo da Vazão Média Observada
    total_bytes = df['Bytes Transmitidos'].sum()
    
    # Conversão: Bytes para Megabits (Bytes * 8 bits / 1.000.000)
    total_megabits = (total_bytes * 8) / 1_000_000
    vazao_experimental_mbps = total_megabits / tempo_total
    
    # 3. IMPRESSÃO DOS RESULTADOS COMPARATIVOS
    print("="*50)
    print(" COMPARAÇÃO: TEÓRICO VS EXPERIMENTAL")
    print("="*50)
    
    print("\n1. Vetor Estacionário (Proporção de Tempo nos Estados):")
    print(f"Estado 0 (Ocioso):   Teórico = {pi_teorico[0]:.4f} | Experimental = {pi_experimental[0]:.4f} ({tempo_por_estado[0]:.0f}s)")
    print(f"Estado 1 (TrafMed):  Teórico = {pi_teorico[1]:.4f} | Experimental = {pi_experimental[1]:.4f} ({tempo_por_estado[1]:.0f}s)")
    print(f"Estado 2 (TrafAlt):  Teórico = {pi_teorico[2]:.4f} | Experimental = {pi_experimental[2]:.4f} ({tempo_por_estado[2]:.0f}s)")
    
    print("\n2. Vazão Média:")
    print(f"Teórica:      {vazao_teorica_mbps:.2f} Mbps")
    print(f"Experimental: {vazao_experimental_mbps:.2f} Mbps")
    print("="*50)

except FileNotFoundError:
    print("Erro: O arquivo 'dados_coletados.csv' não foi encontrado. Execute o gerador primeiro.")