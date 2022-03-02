from unittest.mock import patch
from producer import get_html, get_urls
from aioresponses import aioresponses
import aiohttp
import pytest


@patch('kafka.KafkaProducer')
@pytest.mark.asyncio
async def tests_get_html(KafkaProducerMock):
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get('http://test.com', body='<html>content</html>')
            await get_html(session, 'http://test.com', KafkaProducerMock)

    KafkaProducerMock.send.assert_called()
    data = KafkaProducerMock.send.call_args[1]['value']
    assert data['resp'] == '<html>content</html>'


@patch('kafka.KafkaProducer')
@pytest.mark.asyncio
async def tests_client_connector_error_get_html(KafkaProducerMock):
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get('test.com', exception=aiohttp.ClientConnectorError)
            await get_html(session, 'test.com', KafkaProducerMock)
    assert not KafkaProducerMock.send.called

#TODO: tests for incorrect status codes

def tests_get_urls():
    reader = get_urls('test_file.csv')
    assert [row[0] for row in reader] == ['url1', 'url2', 'url3', 'url4']

