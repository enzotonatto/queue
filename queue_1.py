import queue
import random

# Parâmetros do LCG
a = 1664525
c = 1013904223
M = 2**32
seed = 42

# Parâmetros da simulação
chegada_min = 2
chegada_max = 5
atendimento_min = 3
atendimento_max = 5
total_randoms = 100000

# Inicialização da semente do gerador
last_random_number = seed

def NextRandom():
    global last_random_number
    last_random_number = (a * last_random_number + c) % M
    return last_random_number / M

# Função para gerar tempo de chegada ou atendimento
def gera_tempo(tempo_min, tempo_max):
    return tempo_min + (tempo_max - tempo_min) * NextRandom()

# Função para simular uma fila G/G/1/5 ou G/G/2/5
def simular_fila(num_servidores, capacidade_fila):
    fila = queue.Queue(maxsize=capacidade_fila)
    servidores = [0] * num_servidores  # Inicialmente todos os servidores estão livres
    tempo_total = 0
    tempo_estado = [0] * (capacidade_fila + 1)
    count = total_randoms
    perda_clientes = 0
    tempo_atual = 0
    clientes_na_fila = 0
    
    while count > 0:
        # Tempo até a próxima chegada e próximo atendimento
        tempo_chegada = gera_tempo(chegada_min, chegada_max)
        tempo_atendimento = gera_tempo(atendimento_min, atendimento_max)
        
        if tempo_chegada < tempo_atendimento:
            tempo_atual += tempo_chegada
            if fila.full():
                perda_clientes += 1
            else:
                fila.put(tempo_atual)
                clientes_na_fila += 1
                tempo_estado[clientes_na_fila] += tempo_chegada
        else:
            tempo_atual += tempo_atendimento
            for i in range(num_servidores):
                if servidores[i] <= tempo_atual and not fila.empty():
                    servidores[i] = tempo_atual + tempo_atendimento
                    fila.get()
                    clientes_na_fila -= 1
                    tempo_estado[clientes_na_fila] += tempo_atendimento

        tempo_total += max(tempo_chegada, tempo_atendimento)
        count -= 1

    # Calcular e exibir os resultados
    print(f"\nSimulação G/G/{num_servidores}/{capacidade_fila}")
    for i in range(capacidade_fila + 1):
        probabilidade = tempo_estado[i] / tempo_total
        print(f"Estado {i} clientes: Tempo acumulado = {tempo_estado[i]}, Probabilidade = {probabilidade:.4f}")
    
    print(f"Clientes perdidos: {perda_clientes}")
    print(f"Tempo global da simulação: {tempo_total:.2f}\n")

if __name__ == "__main__":
    # Simular fila G/G/1/5
    simular_fila(1, 5)
    
    # Simular fila G/G/2/5
    simular_fila(2, 5)
