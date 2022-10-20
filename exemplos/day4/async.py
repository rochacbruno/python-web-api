import asyncio
import time


async def consulta_dados():
    print("Consultando dados...")
    await asyncio.sleep(2)
    return "dados"


async def processa_dados(dados):
    print(f"Processando dados {dados}...")
    await asyncio.sleep(2)


async def grava_log():
    print("Gravando log...")
    await asyncio.sleep(2)


async def main():
    start = time.perf_counter()
    print("Inicio")

    dados = asyncio.create_task(consulta_dados())
    asyncio.create_task(processa_dados(await dados))
    await grava_log()

    finish = time.perf_counter()
    print("fim")
    print(f"Finished in {round(finish-start, 2)} second(s)")


asyncio.run(main())
