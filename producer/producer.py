from json import dumps
from kafka import KafkaProducer
import csv
import asyncio
import aiohttp
from aiohttp import ClientConnectorError, ClientResponseError
from typing import Generator


async def get_html(session: aiohttp.client.ClientSession, url: str, producer: KafkaProducer) -> None:
    #TODO: change prints to logs
    try:
        async with session.get(url) as resp:
            resp.raise_for_status()
            producer.send('html-topic', value={'resp': await resp.text(), 'url': url})
    except ClientConnectorError as e:
        print(f"url:{url} is not correct or website doesn't exist ({e}). Ignore and go to the next one")
    except ClientResponseError as e:
        print(f"Unexpected status code ({e}). Ignore and go to the next one")
    except Exception as e:
        print(f"Unknown exception: {e}")


def get_urls(file_name: str) -> Generator[str, None, None]:
    with open(file_name, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            yield row


async def main(producer: KafkaProducer) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for row in get_urls('input.csv'):
            tasks.append(get_html(session, row[0], producer))
            # TODO: number of tasks should be in config
            if len(tasks) < 3:
                continue
            await asyncio.gather(*tasks)
            tasks = list()
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    producer = KafkaProducer(
        # TODO: kafka url should be in config
        bootstrap_servers=['kafka-1:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(producer))
