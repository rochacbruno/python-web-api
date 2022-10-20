import time
import concurrent.futures


def consulta_dados():
    print("Consultando dados...")
    time.sleep(2)
    return "dados"


def processa_dados(dados):
    print("Processando dados...")
    time.sleep(2)


def grava_log():
    print("Gravando log...")
    time.sleep(2)


def main():
    start = time.perf_counter()
    print("Inicio")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.submit(consulta_dados)
        dados = future.result()
        executor.submit(processa_dados, dados)
        executor.submit(grava_log)

        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)

    finish = time.perf_counter()
    print("fim")
    print(f"Finished in {round(finish-start, 2)} second(s)")


main()
