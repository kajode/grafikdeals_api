from proxybroker import Broker
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import asyncio
from proxybroker import Broker

proxy_list = []

async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        ip = str(proxy.host)
        port = str(proxy.port)
        proxy_list.append(ip+':'+port)

def getproxies():

    proxies = asyncio.Queue()
    broker = Broker(proxies)

    tasks = asyncio.gather(broker.find(types=['HTTPS'], limit=10), show(proxies))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    return proxy_list
