#!/usr/bin/env python
import os
import webbrowser

from goodreads import client


def get_client():
    gc = client.GoodreadsClient(
        os.getenv('GOODREADS_CLIENT_ID'),
        os.getenv('GOODREADS_CLIENT_SECRET'),
    )
    # gc.authenticate()
    return gc


def main():
    gc = get_client()
    with open('books', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                print('{} failed'.format(line))
            matches = gc.search_books(q=line, search_field='title')
            if not matches:
                print('{} failed'.format(line))
            webbrowser.open('https://goodreads.com/book/show/{}'.format(matches[0].gid))


if __name__ == '__main__':
    main()
