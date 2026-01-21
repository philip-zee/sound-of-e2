import json
import aiofiles

def process(contract):
    pass

def read_contracts(path):
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


for contract in read_contracts("contracts.jsonl"):
    process(contract)


def read_contracts(path):
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                process(json.loads(line))




async def read_contracts(path):
    async with aiofiles.open(path, "r") as f:
        async for line in f:
            if line.strip():
                yield json.loads(line)

async def async_process(contract):
    pass


async for contract in read_contracts("contracts.jsonl"):
    await async_process(contract)




import asyncio

async def worker(contract, sem):
    async with sem:
        await process(contract)

async def main():
    sem = asyncio.Semaphore(10)  # max 10 concurrent tasks
    tasks = []

    async for contract in read_contracts("contracts.jsonl"):
        task = asyncio.create_task(worker(contract, sem))
        tasks.append(task)

    await asyncio.gather(*tasks)
