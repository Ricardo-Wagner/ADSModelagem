import random
import time
import subprocess
import csv

class Estado:
    def __init__(self, nome, taxa, run, transicoes):
        self.nome = nome
        self.taxa = taxa # Adicionado para facilitar o registro no CSV
        self.run = run
        self.transicoes = transicoes
        self.visitas = 0

    def prox_estado(self):
        estados = list(self.transicoes.keys())
        probabilidades = list(self.transicoes.values())
        return random.choices(estados, probabilidades)[0]


def gerar_trafego(bitrate):
    cmd = [
        "sudo", "himage", "pc1", "iperf",
        "-c", "10.0.0.20", "-u",
        "-b", bitrate, "-l", "1400", "-t", "5", "-y", "C"
    ]

    # capture_output=True permite ler o que o iperf imprimiu
    result = subprocess.run(cmd, capture_output=True, text=True) 
    
    try:
        # O iperf -y C retorna uma string separada por vírgulas.
        # Pegamos a última linha da saída e dividimos por vírgula.
        linhas = result.stdout.strip().split('\n')
        dados = linhas[-1].split(',')
        
        # O 8º elemento (índice 7) costuma ser o total de Bytes Transmitidos
        bytes_transmitidos = int(dados[7])
        return bytes_transmitidos
    except Exception as e:
        print(f"Erro ao analisar saída do iperf: {e}")
        return 0


# Tratadores dos estados (agora eles retornam a quantidade de bytes)
def tratador_Ocioso():
    time.sleep(5)
    # Retorna 0 bytes diretamente, sem precisar simular a string do iperf
    return 0

def tratador_TrafMed():
    return gerar_trafego("10M")

def tratador_TrafAlt():
    return gerar_trafego("50M")


# Definição dos Estados (Nome, Taxa em Mbps, Função, Transições)
ocioso = Estado("0", 0, tratador_Ocioso, {})
trafMed = Estado("1", 10, tratador_TrafMed, {})
trafAlt = Estado("2", 50, tratador_TrafAlt, {})

ocioso.transicoes = {ocioso: 0.6, trafMed: 0.3, trafAlt: 0.1}
trafMed.transicoes = {ocioso: 0.2, trafMed: 0.6, trafAlt: 0.2}
trafAlt.transicoes = {ocioso: 0.1, trafMed: 0.3, trafAlt: 0.6}

# ATENÇÃO: O roteiro pede 50 épocas para o experimento real (250 segundos).
# A simulação teórica (seu 2º script) é que pedia 500. Ajustei para 50 aqui.
epocas = 50 
estado = ocioso

# Inicia o iperf servidor
cmd_server = [
    "sudo", "himage", "pc2", "iperf", "-s", "-u", "-D"
]
subprocess.run(cmd_server)

print("Iniciando o experimento. Os dados serão salvos em 'dados_coletados.csv'...")

# Configurando e abrindo o CSV para escrita
with open('dados_coletados.csv', mode='w', newline='') as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    # Escreve o cabeçalho exigido pelo roteiro
    escritor.writerow(["Passo", "Estado", "Taxa Configurada (Mbps)", "Bytes Transmitidos"])

    for passo in range(1, epocas + 1):
        estado.visitas += 1
        print(f"Passo {passo}/{epocas} | Estado: {estado.nome} ({estado.taxa} Mbps)")
        
        # Executa a ação do estado e captura os bytes
        bytes_tx = estado.run()
        
        # Grava a linha no CSV
        escritor.writerow([passo, estado.nome, estado.taxa, bytes_tx])
        
        # Opcional: flush para garantir que os dados sejam salvos no disco em tempo real
        arquivo_csv.flush() 
        
        time.sleep(0.3)
        estado = estado.prox_estado()

print("Experimento concluído! Verifique o arquivo 'dados_coletados.csv'.")