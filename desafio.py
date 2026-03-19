import time
from multiprocessing import Pool

def ler_arquivo(caminho):
    """Lê os números do ficheiro e retorna uma lista de inteiros."""
    try:
        with open(caminho, 'r') as f:
            # Lê cada linha, converte para inteiro e ignora linhas vazias
            return [int(linha.strip()) for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho} não foi encontrado.")
        return []

def soma_parcial(sublista):
    """Função auxiliar para somar uma parte da lista."""
    return sum(sublista)

def executar_paralelo(dados, num_processos):
    """Divide os dados e executa a soma em paralelo."""
    if not dados: return 0, 0
    
    # Cálculo para dividir a lista em partes iguais para os processos
    tamanho_lista = len(dados)
    tamanho_parte = (tamanho_lista + num_processos - 1) // num_processos
    partes = [dados[i:i + tamanho_parte] for i in range(0, tamanho_lista, tamanho_parte)]
    
    inicio = time.time()
    # Usamos Pool para processos (Multiprocessing)
    with Pool(processes=num_processos) as pool:
        resultados = pool.map(soma_parcial, partes)
        soma_total = sum(resultados)
    fim = time.time()
    
    return soma_total, fim - inicio

if __name__ == '__main__':
    arquivo = 'numero2.txt'
    
    print(f"Lendo dados do arquivo {arquivo}...")
    dados = ler_arquivo(arquivo)
    
    if dados:
        print(f"Total de elementos: {len(dados)}\n")

        # --- 1. Solução Serial ---
        print("Executando Soma Serial...")
        inicio_serial = time.time()
        soma_s = sum(dados)
        fim_serial = time.time()
        tempo_serial = fim_serial - inicio_serial
        print(f"Resultado Serial: {soma_s} | Tempo: {tempo_serial:.6f}s\n")

        # --- 2. Solução Paralela (Experimentos) ---
        # Cabeçalho da tabela no terminal
        print(f"{'Processos':<10} | {'Soma':<12} | {'Tempo (s)':<12} | {'Speedup':<10} | {'Eficiência':<10}")
        print("-" * 75)
        
        # O caso de 1 processo (Serial) para referência na tabela
        print(f"{1:<10} | {soma_s:<12} | {tempo_serial:.6f}     | {1.0000:<10} | {1.0000:<10}")

        processos_para_testar = [2, 4, 8, 12]
        
        for n in processos_para_testar:
            res, tempo = executar_paralelo(dados, n)
            
            # Cálculos de Performance
            speedup = tempo_serial / tempo
            eficiencia = speedup / n
            
            # Exibe os resultados formatados
            print(f"{n:<10} | {res:<12} | {tempo:.6f}     | {speedup:.4f}     | {eficiencia:.4f}")

        print("\n" + "="*45)
        print("Testes concluídos!")
        print("Use os valores acima para criar seus gráficos no Excel.")
        print("="*45)