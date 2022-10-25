import time
import concurrent.futures


def consulta_dados():
    time.sleep(2)
    print("Consultando dados...")
    return "dados"


def processa_dados(dados):
    time.sleep(2)
    print("Processando dados...")


def grava_log():
    print("Gravando log...")
    time.sleep(2)


def main():
    start = time.perf_counter()
    print("Inicio")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(consulta_dados)
        dados = future.result()
        executor.submit(processa_dados, dados)
        executor.submit(grava_log)
    finish = time.perf_counter()
    print("fim")
    print(f"Finished in {round(finish-start, 2)} second(s)")


main()
