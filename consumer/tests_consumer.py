from consumer import get_urls, add_to_file

def test_get_urls():
    test_html = "<html><a href='https://test.com'></a><a></a></html>"
    urls=[url for url in get_urls(test_html)]
    assert urls == ['https://test.com']


def tests_add_to_file():
    file_name = 'test_file.txt'
    text = 'add_line\n'
    open(file_name, 'w').close()
    add_to_file(file_name, text)

    with open(file_name) as f:
        content = f.read()
        assert text.strip() == content.strip()

