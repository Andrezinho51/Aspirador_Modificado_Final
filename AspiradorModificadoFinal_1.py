import random

def criar_ambiente(num_salas, num_sujas):
    ambiente = ["LIMPO"] * num_salas
    salas_sujas = random.sample(range(num_salas), num_sujas)
    for sala_suja in salas_sujas:
        ambiente[sala_suja] = "SUJA"
    return ambiente

def mostrar_ambiente(ambiente, posicao_aspirador):
    for i in range(len(ambiente)):
        if i == posicao_aspirador:
            print("A", end=" ")
        elif ambiente[i] == "SUJA":
            print("S", end=" ")
        else:
            print("L", end=" ")
    print()

def mostrar_ambiente_visivel(ambiente, posicao_aspirador, controlador_atual):
    if controlador_atual == "BASE":     # Mostrar só a sala do aspirador
        visibilidade = ["ESCONDIDA"] * len(ambiente)
        visibilidade[posicao_aspirador] = ambiente[posicao_aspirador]
    else:
        visibilidade = ambiente     # Mostrar todas

    for i in range(len(ambiente)):
        if visibilidade[i] == "ESCONDIDA":
            print("?", end=" ")
        else:
            print(visibilidade[i], end=" ")
    print()

# Controlador Manual
def controlador_manual(ambiente, posicao_aspirador):
    controlador_atual = "BASE"

    while True:
        mostrar_ambiente_visivel(ambiente, posicao_aspirador, controlador_atual)
        acao = input("Digite 'M' para mover o aspirador, 'S' para aspirar, 'B' para Base, 'O' para Onisciente, ou 'Q' para sair: ").upper()
        
        if acao == "M":
            direcao = input("Digite 'D' para mover para a direita ou 'E' para mover para a esquerda: ").upper()
            if direcao == "D":
                posicao_aspirador = (posicao_aspirador + 1) % len(ambiente)
            elif direcao == "E":
                posicao_aspirador = (posicao_aspirador - 1) % len(ambiente)
        elif acao == "S":
            ambiente[posicao_aspirador] = "LIMPO"
        elif acao == "B":
            controlador_atual = "BASE"
        elif acao == "O":
            controlador_atual = "ONISCIENTE"
        elif acao == "Q":
            return "SAIR"

# Controlador Base (Algoritmo Guloso)
def controlador_base(ambiente, posicao_aspirador):
    movimentos = 0
    direcao = +1

    while "SUJA" in ambiente:
        movimentos += 1
        #ambiente[posicao_aspirador] = "A"
        if random.random() < 0.2:
            sala_aleatoria = random.randint(0, len(ambiente) - 1)
            ambiente[sala_aleatoria] = "SUJA"
            print(f"A sala {sala_aleatoria} foi sujada aleatoriamente!")
        if ambiente[posicao_aspirador] == "SUJA":
            if random.random() < 0.2:
                print("O robô decidiu não limpar esta sala.")
        else:
            if ambiente[posicao_aspirador] == "SUJA":
                ambiente[posicao_aspirador] = "LIMPO"
                print(f"A sala {posicao_aspirador} foi limpa!")
                
        posicao_anterior = posicao_aspirador
        posicao_aspirador += direcao
        
        if posicao_aspirador >= len(ambiente) or posicao_aspirador < 0:
            direcao = -direcao
            posicao_aspirador += direcao

        # Sistema de identificação da sala que o aspirador acabou de passar para verificar se criou uma sujeira ou ele não limpou ali
        if ambiente[posicao_anterior] == "SUJA":
            ambiente[posicao_anterior] = "LIMPO"
            print(f"A sala {posicao_anterior} foi limpa!")

        print(f"Movimento {movimentos} - Ambiente: {ambiente}")

    return "LIMPEZA CONCLUÍDA"

    
# Controlador Onisciente (Algoritmo Guloso com Conhecimento Global)
def controlador_onisciente(ambiente, posicao_aspirador):
    movimentos = 0

    while "SUJA" in ambiente:
        movimentos += 1
        sala_mais_proxima = None
        distancia_mais_proxima = float('inf')

        for i, status in enumerate(ambiente):
            if status == "SUJA":
                distancia = abs(i - posicao_aspirador)
                if distancia < distancia_mais_proxima:
                    sala_mais_proxima = i
                    distancia_mais_proxima = distancia

        posicao_aspirador = sala_mais_proxima
        ambiente[sala_mais_proxima] = "LIMPO"
        ambiente[posicao_aspirador] = "A"
        print(f"Movimento {movimentos} - Ambiente: {ambiente}")

    return "LIMPEZA CONCLUÍDA"
    
def main():
    num_salas = int(input("Digite o número de salas (até 10): "))
    num_sujas = int(input("Digite o número de salas sujas: "))

    if num_salas <= 0 or num_salas > 10 or num_sujas < 0 or num_sujas > num_salas:
        print("Entrada inválida. Certifique-se de que o número de salas e sujas está correto.")
        return

    ambiente = criar_ambiente(num_salas, num_sujas)
    posicao_aspirador = random.randint(0, num_salas - 1)

    while True:
        mostrar_ambiente(ambiente, posicao_aspirador)
        print("Escolha um controlador:")
        print("1 - Manual")
        print("2 - Base (Algoritmo Guloso)")
        print("3 - Onisciente (Algoritmo Guloso com Conhecimento Global)")
        escolha = input("Digite o número do controlador ou 'Q' para sair: ")

        if escolha == '1':
            acao = controlador_manual(ambiente, posicao_aspirador)
        elif escolha == '2':
            acao = controlador_base(ambiente, posicao_aspirador)
        elif escolha == '3':
            acao = controlador_onisciente(ambiente, posicao_aspirador)
        elif escolha == 'Q':
            break
        else:
            print("Escolha inválida. Por favor, escolha um controlador válido.")
            
        if acao == "Q":
            break

main()