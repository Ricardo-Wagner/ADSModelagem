# ADSModelagem

## Exercício: Geração de Tráfego Baseada em Cadeia de Markov e Comparação de Resultados
### Objetivo
O objetivo deste exercício é implementar um gerador de tráfego de rede baseado em uma
cadeia de Markov discreta no tempo (DTMC) com 3 estados, utilizando o iperf para gerar
tráfego real. Em seguida, você deverá comparar os resultados práticos obtidos com os
resultados teóricos calculados no Octave, usando a função dtmc do pacote Queueing.
### Descrição do Problema
O gerador de tráfego será modelado por uma cadeia de Markov discreta no tempo
(DTMC) com 3 estados:

- Estado 0 (Ocioso): Sem geração de tráfego.
- Estado 1 (Tráfego Moderado): Geração de pacotes com taxa de 10 Mbps.
- Estado 2 (Tráfego Alto): Geração de pacotes com taxa de 50 Mbps.
  
A matriz de transição P deve ser fornecida como parâmetro para o gerador. Escolha uma
matriz P e faça as etapas que se seguem.

O sistema segue as seguintes etapas:

1. Implementação do Gerador de Tráfego Prático:
- Use o iperf para gerar tráfego de acordo com o estado atual da cadeia de
Markov. Capture a saída do iperf e extraia os bytes transmitidos.
- A execução deve ter como época 5s segundos, totalizando 50 passos (ou 250 segundos).
  
2. Coleta de Dados:
- Registre:
  
  ■ Tempo em cada estado.

  ■ Bytes transmitidos pelo iperf em cada transição.

3. Análise Teórica no Octave:
- Use a função dtmc do pacote Queueing no Octave (ou similar em python)
para calcular as probabilidades estacionárias dos estados.
- Estime a vazão média teórica considerando as taxas de tráfego de cada
estado.

4. Comparação e Discussão:
- Compare os resultados práticos e teóricos:
  
  ■ Proporção de tempo em cada estado.

  ■ Vazão média calculada (prática vs teórica).
