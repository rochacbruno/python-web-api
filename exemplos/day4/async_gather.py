import time
import asyncio


async def consulta_dados():  # I/O bound
    print("Consultando dados...")
    await asyncio.sleep(2)  # fazendo select no BD
    return "dados"


async def processa_dados(dados):  # CPU bound
    print("Processando dados...")
    print(await dados)
    await asyncio.sleep(2)  # calculando alguma coisa com os dados

async def grava_log():  # I/O Bound
    print("Gravando log...")
    await asyncio.sleep(2)


async def main():
    dados = asyncio.create_task(consulta_dados()) # esperando DB
    t1 = asyncio.create_task(processa_dados(dados))
    t2 = asyncio.create_task(grava_log())
    await asyncio.gather(t1, t2)


start = time.perf_counter()
print("Inicio")

asyncio.run(main())  # eventloop
print("Fim")
finish = time.perf_counter()
print(f"Finished in {round(finish-start, 2)} seconds")
