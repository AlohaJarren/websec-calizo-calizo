import requests, time, multiprocessing
import asyncio, httpx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

async def agetUrlTitle(client, url):
    """
    This asynchronous function returns the <title> of an HTML document given its URL
    :param url: URL to retrieve
    :type client: HTTPX AsyncClient
    :type url: str
    :return: Title of URL
    :rtype: str
    """
    resp = await client.get(url, follow_redirects=True)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('title'):
        return soup.find('title').text
    else:
        return ''
    
async def async_main(urls):
    """
    Orchestrates asynchronous retrieval of titles for a list of URLs using an httpx AsyncClient.
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :return: list of page titles
    :rtype: list of str
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        titles = [agetUrlTitle(client, u) for u in urls]
        results = await asyncio.gather(*titles)
    return results

def time_decorator(func):
    """
    Takes a function and returns a version of it that prints out the elapsed time for executing it
    :param func: Function to decorate
    :return: Function which outputs execution time
    :rtype: Function
    """
    def inner(*args, **kwargs):
        s = time.perf_counter()
        return_vals = func(*args, **kwargs)
        elapsed = time.perf_counter() - s
        print(f'Function returned: {return_vals}')
        return elapsed
    return inner

def getUrlTitle(url):
  """
    This function returns the <title> of an HTML document given its URL
    :param url: URL to retrieve
    :type url: str
    :return: Title of URL
    :rtype: str
  """
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text,'html.parser')
  if soup.find('title'):
    return(soup.find('title').text)
  else:
    return ('')

@time_decorator
def getSequential(urls):
    """
    Given a list of URLs, retrieve the title for each one using a single synchronous process
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :return: list of titles for each URL
    :rtype: list of str
    """
    titles = []
    for u in urls:
        titles.append(getUrlTitle(u))
    return(titles)

@time_decorator
def getMulti(urls, num_processes):
    """
    Given a list of URLs, retrieve the title for each one using multiple processes in parallel.
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :param num_processes: Number of processes to use
    :type num_processes: int
    :return: list of titles
    :rtype: list of str
    """
    p = multiprocessing.Pool(num_processes)
    titles = p.map(getUrlTitle, urls)
    p.close()
    return titles

@time_decorator
def getAsync(urls):
    """
    Given a list of URLs, retrieve the title for each one using a single asynchronous event loop.
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :return: list of str
    """
    return asyncio.run(async_main(urls))


if __name__ == '__main__':
    # Download the large list of URLs
    resp = requests.get('https://thefengs.com/wuchang/courses/cs495/urls.txt')
    urls = resp.text.strip().split('\n')

    # Concurrency levels to test
    concurrencies = [25, 20, 15, 10, 5, 2, 1]
    elapsed = []

    print("\n== Batched Async Timing ==")
    for concurrency in concurrencies:
        total_time = 0
        for i in range(0, len(urls), concurrency):
            fetch_time = getAsync(urls[i:i + concurrency])
            total_time += fetch_time
        elapsed.append(total_time)
        print(f'Async version {concurrency}: {total_time:0.2f}')

    # Pair concurrency levels and elapsed times
    print(list(zip(concurrencies, elapsed)))

    plt.scatter(concurrencies, elapsed)
    plt.title("Async Batching Speedup (OdinID: calizo)")
    plt.xlabel("Number of Concurrent Requests")
    plt.ylabel("Retrieval Time (seconds)")
    plt.show()
