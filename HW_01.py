import pathlib
import os
import random
import time
import functools
from collections import OrderedDict
import requests
import sys
from time import sleep


def foo():
    return foo


def profile(f):
    def internal():
        start = time.time()
        f()
        finish = time.time()
        print(f'Elapsed time: {finish - start}s')
    return internal


def profile(f):
    def internal():
        start = time.time()
        f()
        print(f'Elapsed time ({f.__name__}): {time.time() - start}s')
    return internal

foo_profiled = profile(foo)
foo_profiled()


def fetch_url():
    res = requests.get('https://google.com')
    print('Content: \t', res.content[:100])

fetch_url_profiled = profile(fetch_url)
fetch_url_profiled()


def fetch_url(url):
    res = requests.get(url)
    print(f'\nContent for "{url}":\t ', res.content[:100])

def profile(f):
    def internal(url):
        start = time.time()
        f(url)
        print(f'Elapsed time ({f.__name__}): {time.time() - start}s')
    return internal

fetch_url_profiled = profile(fetch_url)
fetch_url_profiled('https://google.com')
fetch_url_profiled('https://ithillel.ua')
fetch_url_profiled('https://lms.ithillel.ua')


def profile(f):
    def internal(*args):
        start = time.time()
        f(*args)
        print(f'Elapsed time ({f.__name__}): {time.time() - start}s')
    return internal

fetch_url = profile(fetch_url)
fetch_url('https://ithillel.ua')


def fetch_url(url, first_n=None):
    res = requests.get(url)
    print(f'\nContent for "{url}":\t ', res.content[:first_n] if first_n else res.content)

def profile(f):
    def internal(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        print(f'Elapsed time ({f.__name__}): {time.time() - start}s')
    return internal

fetch_url = profile(fetch_url)
fetch_url('https://ithillel.ua', first_n=42)
fetch_url('https://ithillel.ua', first_n=100)
fetch_url('https://ithillel.ua', first_n=1024)


def fetch_url(url, first_n=100):
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

fetch_url = profile(fetch_url)


def profile(f):
    def internal(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f'Elapsed time for function {f.__name__} with params {args}, {kwargs}: {time.time() - start}ms')
        return result
    return internal

fetch_url = profile(fetch_url)


@profile
def fetch_url(url, first_n=100):
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

print(fetch_url('https://ithillel.ua', first_n=42))
print(fetch_url('https://google.com'))


def profile(f):
    def internal(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f'Elapsed time for function {f.__name__} with params {args}, {kwargs}: {time.time() - start}ms')
        return result
    return internal

@profile
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

help(fetch_url)


def profile(f):
    @functools.wraps(f)
    def internal(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f'Elapsed time for function {f.__name__} with params {args}, {kwargs}: {time.time() - start}ms')
        return result
    return internal


@profile
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

help(fetch_url)


def profile(msg='Elapsed time'):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            print(msg, f'({f.__name__}): {time.time() - start}s')
            return result
        return deco
    return internal


@profile(msg='Прошло времени')
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://google.com')


@profile(msg='Elapsed time')
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

fetch_url('https://google.com')


@profile('Elapsed time')
def foo():
    """Help for foo"""
    return 42

help(foo)
print("RESULT: ", foo())


def repeate(max_repeat=10):
    def internal(f):
        @functools.wraps(f)
        def repeater(*args, **kwargs):
            while repeater._num_repeats <= max_repeat:
                try:
                    return f(*args, **kwargs)
                except Exception as ex:
                    if repeater._num_repeats == max_repeat:
                        raise
                    else:
                        print(
                            f'Failed after {repeater._num_repeats + 1} times, trying again after {2 ** repeater._num_repeats} sec...')
                        sleep(2 ** repeater._num_repeats)
                        repeater._num_repeats += 1

        repeater._num_repeats = 0
        return repeater

    return internal


@repeate(max_repeat=4)
def connect_to_server(*args):
    print('Trying to connect: ', *args)
    if sum(random.choices([0, 1], [0.8, 0.2])) == 0:
        raise RuntimeError('Failed to connect')
    print('SUCCESS!')


connect_to_server('google.com')


def cache(f):
    @functools.wraps(f)
    def deco(*args):
        if args in deco._cache:
            return deco._cache[args]

        result = f(*args)
        deco._cache[args] = result
        return result

    deco._cache = {}
    return deco

def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args):
            def add_content_in_cache(*args):
                if len(deco._cache_entries) == max_limit:
                    delete_content_from_cache()

                heap_node = [1, args, f(*args)]
                heapq.heappush(deco._heap, heap_node)
                deco._cache_entries[args] = heap_node

            def delete_content_from_cache():
                while deco._heap:
                    count, args, content = heapq.heappop(deco._heap)
                    del deco._cache_entries[args]
                    return

            def update_frequency_in_cache(*args):
                heap_node = deco._cache_entries[args]
                heap_node[0] = heap_node[0] + 1
                heapq.heappush(deco._heap, heap_node)
                deco._cache_entries[args] = heap_node

            if args in deco._cache_entries:
                print(*args, "in cache")
                update_frequency_in_cache(args)
            else:
                print(*args, "not in cache")
                add_content_in_cache(args)

            return deco._cache_entries[args][2]
        deco._cache_entries = {}
        deco._heap = []
        return deco
    return internal


@profile(msg='Elapsed time')
@cache
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://youtube.com')
fetch_url('https://reddit.com')