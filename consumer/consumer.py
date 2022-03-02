from kafka import KafkaConsumer
from json import loads
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin
from typing import Generator, List


def get_urls(html: str) -> Generator[str, None, None]:
    for link in BeautifulSoup(html, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            yield link['href']


def add_to_file(file_name: str, urls: List[str]) -> None:
    with open(file_name, "a") as file_object:
        file_object.write("\n".join(urls) + '\n')


def main():

    consumer = KafkaConsumer(
        'html-topic',
        bootstrap_servers=['kafka-1:9092'],
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for message in consumer:
        html = message.value['resp']
        base_url = message.value['url']
        parsed_urls = [urljoin(base_url, url) for url in get_urls(html)]
        add_to_file('output.txt', parsed_urls)


if __name__ == "__main__":
    main()

